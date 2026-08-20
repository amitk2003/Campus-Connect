from flask import Blueprint, request, jsonify
from db import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
import datetime

reviews_bp = Blueprint('reviews', __name__)
reviews_collection = db['Reviews']
users_collection = db['Users']
transactions_collection = db['Transactions']


@reviews_bp.route('/add', methods=['POST'])
@jwt_required()
def add_review():
    """Add a review for a seller after a completed transaction."""
    data = request.get_json()
    reviewer_id = get_jwt_identity()

    transaction_id = data.get('transaction_id')
    rating = data.get('rating')
    comment = data.get('comment', '')

    if not transaction_id or not rating:
        return jsonify({"message": "transaction_id and rating are required"}), 400

    if not (1 <= int(rating) <= 5):
        return jsonify({"message": "Rating must be between 1 and 5"}), 400

    # Verify the transaction exists and buyer is the reviewer
    transaction = transactions_collection.find_one({"_id": ObjectId(transaction_id)})
    if not transaction:
        return jsonify({"message": "Transaction not found"}), 404

    if transaction.get("buyer_id") != reviewer_id:
        return jsonify({"message": "Only the buyer can review this transaction"}), 403

    # Check if already reviewed
    existing = reviews_collection.find_one({
        "transaction_id": transaction_id,
        "reviewer_id": reviewer_id
    })
    if existing:
        return jsonify({"message": "You have already reviewed this transaction"}), 400

    review = {
        "transaction_id": transaction_id,
        "seller_id": transaction.get("seller_id"),
        "reviewer_id": reviewer_id,
        "rating": int(rating),
        "comment": comment,
        "created_at": datetime.datetime.utcnow()
    }

    reviews_collection.insert_one(review)
    return jsonify({"message": "Review submitted successfully"}), 201


@reviews_bp.route('/seller/<seller_id>', methods=['GET'])
def get_seller_reviews(seller_id):
    """Get all reviews for a specific seller with average rating."""
    reviews = list(reviews_collection.find({"seller_id": seller_id}).sort("created_at", -1))

    # Calculate average
    if reviews:
        avg_rating = sum(r.get("rating", 0) for r in reviews) / len(reviews)
    else:
        avg_rating = 0

    # Enrich with reviewer name
    enriched = []
    for r in reviews:
        reviewer = users_collection.find_one({"_id": ObjectId(r.get("reviewer_id"))})
        enriched.append({
            "_id": str(r["_id"]),
            "rating": r.get("rating"),
            "comment": r.get("comment", ""),
            "reviewer_name": reviewer.get("name", "Anonymous") if reviewer else "Anonymous",
            "created_at": r.get("created_at")
        })

    return jsonify({
        "seller_id": seller_id,
        "average_rating": round(avg_rating, 1),
        "total_reviews": len(reviews),
        "reviews": enriched
    }), 200
