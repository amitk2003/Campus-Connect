from flask import Blueprint, request, jsonify
from db import db
from flask_jwt_extended import jwt_required, get_jwt
from bson import ObjectId
import datetime

admin_bp = Blueprint('admin', __name__)

reports_collection = db['Reports']
claims_collection = db['Claims']
transactions_collection = db['Transactions']
marketplace_collection = db['MarketplaceItems']
users_collection = db['Users']
payments_collection = db['Payments']


def admin_required(fn):
    """Decorator to restrict routes to Admin role only."""
    from functools import wraps
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get('role') != 'Admin':
            return jsonify({"message": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper


@admin_bp.route('/dashboard', methods=['GET'])
@admin_required
def dashboard_stats():
    """Get overall platform statistics for the admin dashboard."""
    total_users = users_collection.count_documents({})
    total_students = users_collection.count_documents({"role": "Buyer"})
    total_alumni = users_collection.count_documents({"role": "Seller"})

    total_lost = reports_collection.count_documents({"type": "lost"})
    total_found = reports_collection.count_documents({"type": "found"})
    resolved_reports = reports_collection.count_documents({"status": "Resolved"})

    total_marketplace_items = marketplace_collection.count_documents({})
    sold_items = marketplace_collection.count_documents({"status": "Sold"})
    available_items = marketplace_collection.count_documents({"status": "Available"})

    total_transactions = transactions_collection.count_documents({})

    # Calculate platform revenue from payments
    pipeline = [
        {"$group": {"_id": None, "total_revenue": {"$sum": "$platform_fee"}}}
    ]
    revenue_result = list(payments_collection.aggregate(pipeline))
    total_revenue = revenue_result[0]["total_revenue"] if revenue_result else 0

    # Claims stats
    pending_claims = claims_collection.count_documents({"status": "Pending"})
    approved_claims = claims_collection.count_documents({"status": "Approved"})
    rejected_claims = claims_collection.count_documents({"status": "Rejected"})

    return jsonify({
        "users": {
            "total": total_users,
            "students": total_students,
            "alumni": total_alumni
        },
        "lost_and_found": {
            "total_lost": total_lost,
            "total_found": total_found,
            "resolved": resolved_reports
        },
        "marketplace": {
            "total_items": total_marketplace_items,
            "available": available_items,
            "sold": sold_items
        },
        "transactions": total_transactions,
        "revenue": total_revenue,
        "claims": {
            "pending": pending_claims,
            "approved": approved_claims,
            "rejected": rejected_claims
        }
    }), 200


@admin_bp.route('/claims', methods=['GET'])
@admin_required
def get_all_claims():
    """Get all claims with report details for admin review."""
    claims = list(claims_collection.find().sort("created_at", -1))
    enriched_claims = []
    for claim in claims:
        report = reports_collection.find_one({"_id": ObjectId(claim.get("found_report_id"))})
        claimer = users_collection.find_one({"_id": ObjectId(claim.get("claimer_id"))})
        enriched_claims.append({
            "_id": str(claim["_id"]),
            "found_report_id": claim.get("found_report_id"),
            "item_name": report.get("item_name", "Unknown") if report else "Unknown",
            "item_category": report.get("category", "") if report else "",
            "item_description": report.get("description", "") if report else "",
            "claimer_name": claimer.get("name", "Unknown") if claimer else "Unknown",
            "claimer_email": claimer.get("email", "") if claimer else "",
            "verification_details": claim.get("verification_details", ""),
            "status": claim.get("status"),
            "created_at": claim.get("created_at")
        })
    return jsonify(enriched_claims), 200


@admin_bp.route('/claims/<claim_id>/verify', methods=['POST'])
@admin_required
def verify_claim(claim_id):
    """Approve or reject a claim and charge claim fee."""
    data = request.get_json()
    action = data.get('action')  # 'approve' or 'reject'

    if action not in ['approve', 'reject']:
        return jsonify({"message": "Action must be 'approve' or 'reject'"}), 400

    claim = claims_collection.find_one({"_id": ObjectId(claim_id)})
    if not claim:
        return jsonify({"message": "Claim not found"}), 404

    if claim.get("status") != "Pending":
        return jsonify({"message": "Claim already processed"}), 400

    if action == 'approve':
        claims_collection.update_one(
            {"_id": ObjectId(claim_id)},
            {"$set": {"status": "Approved", "resolved_at": datetime.datetime.utcnow()}}
        )
        reports_collection.update_one(
            {"_id": ObjectId(claim.get("found_report_id"))},
            {"$set": {"status": "Resolved"}}
        )
        # Record claim fee payment
        payment = {
            "type": "claim_fee",
            "claim_id": claim_id,
            "user_id": claim.get("claimer_id"),
            "amount": 20,
            "platform_fee": 20,
            "status": "Completed",
            "created_at": datetime.datetime.utcnow()
        }
        payments_collection.insert_one(payment)
        return jsonify({"message": "Claim approved. ₹20 fee charged. Item ready for pickup at reception."}), 200
    else:
        claims_collection.update_one(
            {"_id": ObjectId(claim_id)},
            {"$set": {"status": "Rejected", "resolved_at": datetime.datetime.utcnow()}}
        )
        return jsonify({"message": "Claim rejected"}), 200


@admin_bp.route('/transactions', methods=['GET'])
@admin_required
def get_all_transactions():
    """Get all marketplace transactions."""
    transactions = list(transactions_collection.find().sort("created_at", -1))
    enriched = []
    for tx in transactions:
        item = marketplace_collection.find_one({"_id": ObjectId(tx.get("item_id"))})
        buyer = users_collection.find_one({"_id": ObjectId(tx.get("buyer_id"))})
        seller = users_collection.find_one({"_id": ObjectId(tx.get("seller_id"))})
        enriched.append({
            "_id": str(tx["_id"]),
            "item_name": item.get("title", "Unknown") if item else "Unknown",
            "buyer_name": buyer.get("name", "Unknown") if buyer else "Unknown",
            "seller_name": seller.get("name", "Unknown") if seller else "Unknown",
            "price": tx.get("price", 0),
            "platform_fee": tx.get("platform_fee", 0),
            "status": tx.get("status"),
            "created_at": tx.get("created_at")
        })
    return jsonify(enriched), 200


@admin_bp.route('/payments', methods=['GET'])
@admin_required
def get_all_payments():
    """Get all payment records (claim fees + marketplace fees)."""
    payments = list(payments_collection.find().sort("created_at", -1))
    return jsonify(payments), 200
