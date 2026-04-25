from flask import Blueprint, request, jsonify, current_app
from db import db
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import datetime
import os
import stripe
from werkzeug.utils import secure_filename
from bson import ObjectId
import math
from collections import Counter

lostandfound_bp = Blueprint('lostandfound', __name__)

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "sk_test_mock")
stripe.api_key = STRIPE_SECRET_KEY

def calculate_finder_reward(reward_amount):
    """Platform takes 0% — 100% of the reward goes to the finder."""
    return max(0.0, float(reward_amount))

reports_collection = db['Reports']
claims_collection = db['Claims']

# --- Text Similarity (TF-IDF Cosine) ---

def compute_text_similarity(str1, str2):
    """Compute cosine similarity between two strings using word frequency vectors (TF-IDF style)."""
    words1 = str1.lower().split()
    words2 = str2.lower().split()
    vec1 = Counter(words1)
    vec2 = Counter(words2)
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1.get(x, 0) * vec2.get(x, 0) for x in intersection])
    sum1 = sum([val**2 for val in vec1.values()])
    sum2 = sum([val**2 for val in vec2.values()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    if not denominator:
        return 0.0
    return float(numerator) / denominator


# --- Image Similarity (OpenCV) ---

def compute_image_similarity_safe(url1, url2):
    """
    Safely attempt OpenCV image comparison.
    Returns similarity dict or None if OpenCV is unavailable.
    """
    try:
        from utils.image_similarity import compute_image_similarity
        return compute_image_similarity(url1, url2)
    except ImportError:
        print("[Warning] OpenCV not installed. Skipping image similarity.")
        return None
    except Exception as e:
        print(f"[Warning] Image similarity failed: {e}")
        return None


# --- Combined Smart Matching ---

def smart_match(new_report, found_report):
    """
    Combine text similarity + image similarity + category/name matching
    to produce a comprehensive match score.
    
    Returns:
        dict: { text_score, image_score, combined_score, is_match }
    """
    # 1. Text similarity (TF-IDF)
    desc1 = str(new_report.get('description', '')) + " " + str(new_report.get('item_name', ''))
    desc2 = str(found_report.get('description', '')) + " " + str(found_report.get('item_name', ''))
    text_score = compute_text_similarity(desc1, desc2)
    
    # 2. Category match bonus
    category_bonus = 0.15 if new_report.get('category') == found_report.get('category') else 0.0
    
    # 3. Name substring match bonus
    lost_name = str(new_report.get('item_name', '')).lower()
    found_name = str(found_report.get('item_name', '')).lower()
    name_bonus = 0.2 if (lost_name in found_name or found_name in lost_name) else 0.0
    
    # 4. Image similarity (OpenCV) — only if both have images
    image_score = 0.0
    image_details = None
    lost_img = new_report.get('image_url', '')
    found_img = found_report.get('image_url', '')
    
    if lost_img and found_img:
        img_result = compute_image_similarity_safe(lost_img, found_img)
        if img_result:
            image_score = img_result.get('combined_score', 0.0)
            image_details = img_result
    
    # 5. Combined score:
    #    - If both have images: Text 40% + Image 35% + Bonuses 25%
    #    - If no images:        Text 70% + Bonuses 30%
    if lost_img and found_img and image_details:
        combined = (text_score * 0.40) + (image_score * 0.35) + (category_bonus + name_bonus) * 0.25 / 0.35
    else:
        combined = (text_score * 0.70) + (category_bonus + name_bonus) * 0.30 / 0.35

    # Clamp to [0, 1]
    combined = max(0.0, min(1.0, combined))
    
    MATCH_THRESHOLD = 0.25
    
    return {
        "text_score": round(text_score, 4),
        "image_score": round(image_score, 4),
        "image_details": image_details,
        "category_match": new_report.get('category') == found_report.get('category'),
        "combined_score": round(combined, 4),
        "is_match": combined > MATCH_THRESHOLD or (category_bonus > 0 and name_bonus > 0)
    }


@lostandfound_bp.route('/report', methods=['POST'])
@jwt_required()
def create_report():
    claims = get_jwt()
    if claims.get('role', '').lower() == 'admin':
        return jsonify({"message": "Admin cannot report lost/found items"}), 403

    data = request.form if request.form else request.get_json()
    user_id = get_jwt_identity()
    user = db['Users'].find_one({"_id": ObjectId(user_id)})
    anon_name = user.get('anon_name', 'Anonymous') if user else 'Anonymous'

    if not data or not data.get('item_name') or not data.get('type'):
        return jsonify({"message": "Missing item_name or type (lost/found)"}), 400

    report_type = data.get('type')  # 'lost' or 'found'
    
    image_url = data.get('image_url', '')
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            filename = f"{datetime.datetime.utcnow().timestamp()}_{filename}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_url = f"http://localhost:5000/uploads/{filename}"

    new_report = {
        "user_id": user_id,
        "user_anon_name": anon_name,
        "type": report_type,
        "item_name": data.get('item_name'),
        "category": data.get('category', 'General'),
        "location": data.get('location', ''),
        "date": data.get('date', datetime.datetime.utcnow().isoformat()),
        "description": data.get('description', ''),
        "image_url": image_url,
        "status": "Open",  # 'Open', 'Claimed', 'Resolved'
        "created_at": datetime.datetime.utcnow()
    }
    
    result = reports_collection.insert_one(new_report)
    
    # Smart matching trigger
    matches = []
    if report_type == 'lost':
        # Find all open 'found' items and run smart matching
        found_reports = list(reports_collection.find({"type": "found", "status": "Open"}))
        for found in found_reports:
            match_result = smart_match(new_report, found)
            if match_result['is_match']:
                matches.append({
                    "match_id": str(found['_id']),
                    "item_name": found.get('item_name', ''),
                    "text_similarity": match_result['text_score'],
                    "image_similarity": match_result['image_score'],
                    "combined_score": match_result['combined_score'],
                    "category_match": match_result['category_match'],
                    "match_method": "text+image" if match_result['image_score'] > 0 else "text_only"
                })
        
        # Sort matches by combined score (best first)
        matches.sort(key=lambda x: x['combined_score'], reverse=True)
                
    return jsonify({
        "message": "Report posted successfully",
        "report_id": str(result.inserted_id),
        "matches": matches,
        "match_count": len(matches)
    }), 201


@lostandfound_bp.route('/reports', methods=['GET'])
def get_reports():
    rtype = request.args.get('type')  # 'lost' or 'found'
    query = {"status": "Open"}
    if rtype:
        query['type'] = rtype
        
    reports = list(reports_collection.find(query).sort("created_at", -1))
    return jsonify(reports), 200


@lostandfound_bp.route('/match/<report_id>', methods=['GET'])
@jwt_required()
def find_matches(report_id):
    """Manually trigger matching for an existing report."""
    claims = get_jwt()
    if claims.get('role', '').lower() == 'admin':
        return jsonify({"message": "Admin cannot trigger participant matches"}), 403
    try:
        report = reports_collection.find_one({"_id": ObjectId(report_id)})
        if not report:
            return jsonify({"message": "Report not found"}), 404
        
        opposite_type = "found" if report.get("type") == "lost" else "lost"
        candidates = list(reports_collection.find({"type": opposite_type, "status": "Open"}))
        
        matches = []
        for candidate in candidates:
            match_result = smart_match(report, candidate)
            if match_result['is_match']:
                matches.append({
                    "match_id": str(candidate['_id']),
                    "item_name": candidate.get('item_name', ''),
                    "text_similarity": match_result['text_score'],
                    "image_similarity": match_result['image_score'],
                    "combined_score": match_result['combined_score'],
                    "category_match": match_result['category_match'],
                    "match_method": "text+image" if match_result['image_score'] > 0 else "text_only"
                })
        
        matches.sort(key=lambda x: x['combined_score'], reverse=True)
        
        return jsonify({
            "report_id": report_id,
            "matches": matches,
            "match_count": len(matches)
        }), 200
    except Exception as e:
        return jsonify({"message": "Error finding matches", "error": str(e)}), 400


@lostandfound_bp.route('/claim', methods=['POST'])
@jwt_required()
def submit_claim():
    jwt_claims = get_jwt()
    if jwt_claims.get('role', '').lower() == 'admin':
        return jsonify({"message": "Admin cannot submit claims"}), 403

    data = request.get_json() if request.is_json else request.form
    if not data:
        data = {}

    claimer_id = get_jwt_identity()
    report_id = data.get('report_id')  # The found report they are claiming

    if not report_id:
        return jsonify({"message": "report_id is required"}), 400

    report = reports_collection.find_one({"_id": ObjectId(report_id)})
    if not report or report.get('type') != 'found':
        return jsonify({"message": "Invalid found report"}), 404

    # Prevent claimer from claiming their own report
    if str(report.get('user_id')) == str(claimer_id):
        return jsonify({"message": "You cannot claim an item you reported yourself"}), 400

    verification_details = data.get('verification_details', '')

    # --- Reward Model: Owner rewards the Finder (platform takes 0%) ---
    reward_amount = calculate_finder_reward(data.get('reward_amount', 0))
    finder_id = report.get('user_id')  # The person who found & reported the item

    new_claim = {
        "found_report_id": report_id,
        "claimer_id": claimer_id,
        "finder_id": finder_id,
        "verification_details": verification_details,
        "reward_amount": reward_amount,  # Amount owner is rewarding the finder
        "reward_paid": False,
        "status": "Pending",
        "created_at": datetime.datetime.utcnow()
    }

    claims_collection.insert_one(new_claim)
    return jsonify({
        "message": "Claim submitted successfully. Admin will verify your ownership.",
        "reward_amount": reward_amount,
        "note": f"₹{reward_amount} will be rewarded to the finder upon admin approval." if reward_amount > 0 else "No reward offered."
    }), 201


@lostandfound_bp.route('/claims', methods=['GET'])
@jwt_required()
def get_claims():
    claims = get_jwt()
    if claims.get('role', '').lower() == 'admin':
        return jsonify({"message": "Use /api/admin/claims instead"}), 403
    claims = list(claims_collection.find().sort("created_at", -1))
    return jsonify(claims), 200


@lostandfound_bp.route('/claim/verify/<claim_id>', methods=['POST'])
@jwt_required()
def verify_claim(claim_id):
    data = request.get_json()
    action = data.get('action')  # 'approve' or 'reject'
    
    if action not in ['approve', 'reject']:
        return jsonify({"message": "Action must be approve or reject"}), 400
        
    claim = claims_collection.find_one({"_id": ObjectId(claim_id)})
    if not claim:
        return jsonify({"message": "Claim not found"}), 404
        
    if action == 'approve':
        claims_collection.update_one({"_id": ObjectId(claim_id)}, {"$set": {"status": "Approved"}})
        reports_collection.update_one({"_id": ObjectId(claim['found_report_id'])}, {"$set": {"status": "Resolved"}})
        return jsonify({"message": "Claim approved, item handed over"}), 200
    else:
        claims_collection.update_one({"_id": ObjectId(claim_id)}, {"$set": {"status": "Rejected"}})
        return jsonify({"message": "Claim rejected"}), 200
