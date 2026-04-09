from flask import Blueprint, request, jsonify, current_app
from db import db
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import datetime
import os
import stripe
from werkzeug.utils import secure_filename
from bson import ObjectId

marketplace_bp = Blueprint('marketplace', __name__)
marketplace_collection = db['MarketplaceItems']
transactions_collection = db['Transactions']
payments_collection = db['Payments']

PLATFORM_FEE_PERCENT = 5  # 5% platform fee

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "sk_test_mock")
stripe.api_key = STRIPE_SECRET_KEY


@marketplace_bp.route('/items', methods=['POST'])
@jwt_required()
def post_item():
    claims = get_jwt()
    if claims.get('role', '').lower() == 'admin':
        return jsonify({"message": "Admin cannot post items"}), 403

    # Support multipart/form-data for file uploads
    data = request.form if request.form else request.get_json()
    seller_id = get_jwt_identity()
    user = db['Users'].find_one({"_id": ObjectId(seller_id)})
    anon_name = user.get('anon_name', 'Anonymous') if user else 'Anonymous'

    if not data or not data.get('title') or not data.get('price'):
        return jsonify({"message": "Missing required fields (title, price)"}), 400

    image_url = data.get('image_url', '')
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            filename = f"{datetime.datetime.utcnow().timestamp()}_{filename}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_url = f"http://localhost:5000/uploads/{filename}"

    new_item = {
        "title": data.get('title'),
        "description": data.get('description', ''),
        "price": float(data.get('price')),
        "category": data.get('category', 'General'),
        "seller_id": seller_id,
        "seller_anon_name": anon_name,  # Store the anonymous name
        "status": "Available",
        "image_url": image_url,
        "pickup_location": data.get('location', ''),
        "created_at": datetime.datetime.utcnow()
    }

    result = marketplace_collection.insert_one(new_item)
    return jsonify({"message": "Item posted successfully", "item_id": str(result.inserted_id), "seller_anon_name": anon_name}), 201

@marketplace_bp.route('/items', methods=['GET'])
def get_items():
    category = request.args.get('category')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    search = request.args.get('search')

    query = {"status": "Available"}

    if category:
        query["category"] = category

    if min_price or max_price:
        query["price"] = {}
        try:
            if min_price and min_price.strip() != "":
                query["price"]["$gte"] = float(min_price)

            if max_price and max_price.strip() != "":
                query["price"]["$lte"] = float(max_price)

        except ValueError:
            return jsonify({"message": "Invalid price value"}), 400

    if search:
        query["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]

    items_cursor = marketplace_collection.find(query).sort("created_at", -1)

    items = []
    for item in items_cursor:
        item['_id'] = str(item['_id'])
        if 'created_at' in item:
            item['created_at'] = item['created_at'].isoformat()
        
        # Hide location to prevent bypassing the platform
        if 'pickup_location' in item:
            del item['pickup_location']
            
        items.append(item)

    return jsonify(items), 200
@marketplace_bp.route('/items/<item_id>', methods=['GET'])
def get_item(item_id):
    try:
        item = marketplace_collection.find_one({"_id": ObjectId(item_id)})
        if not item:
            return jsonify({"message": "Item not found"}), 404
        return jsonify(item), 200
    except Exception as e:
        return jsonify({"message": "Invalid item ID", "error": str(e)}), 400


@marketplace_bp.route('/buy/<item_id>', methods=['POST'])
@jwt_required()
def buy_item(item_id):
    claims = get_jwt()
    if claims.get('role', '').lower() == 'admin':
        return jsonify({"message": "Admin cannot buy items"}), 403

    buyer_id = get_jwt_identity()

    try:
        data = request.get_json() if request.is_json else request.form
        if not data:
            data = {}
        
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_signature = data.get('razorpay_signature')
        
        item = marketplace_collection.find_one({"_id": ObjectId(item_id)})
        if not item:
            return jsonify({"message": "Item not found"}), 404

        if item.get("status") != "Available":
            return jsonify({"message": "Item is no longer available"}), 400

        if str(item.get("seller_id")) == str(buyer_id):
            return jsonify({"message": "You cannot buy your own item"}), 400

        item_price = float(item["price"])
        platform_fee = round(item_price * PLATFORM_FEE_PERCENT / 100, 2)
        total_amount = item_price + platform_fee
        order_amount_paise = int(total_amount * 100)

        # Step 1: Create Order if no payment details passed
        session_id = data.get('session_id')
        
        if not session_id:
            if STRIPE_SECRET_KEY == "sk_test_mock":
                order_id = "mock_order_id_" + str(item_id)
                return jsonify({
                    "message": "Order created successfully",
                    "order_id": order_id,
                    "price": item_price,
                    "platform_fee": platform_fee,
                    "total_charged": total_amount,
                    "key": "mock"
                }), 200
            else:
                try:
                    frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
                    session = stripe.checkout.Session.create(
                        payment_method_types=['card'],
                        line_items=[{
                            'price_data': {
                                'currency': 'inr',
                                'product_data': {
                                    'name': f"CampusConnect Purchase: {item.get('title')}",
                                },
                                'unit_amount': int(total_amount * 100),
                            },
                            'quantity': 1,
                        }],
                        mode='payment',
                        success_url=f"{frontend_url}/marketplace?success=true&session_id={{CHECKOUT_SESSION_ID}}&item_id={item_id}",
                        cancel_url=f"{frontend_url}/marketplace?canceled=true",
                        metadata={"item_id": item_id, "buyer_id": buyer_id}
                    )
                    return jsonify({
                        "message": "Stripe Session Created",
                        "url": session.url,
                        "session_id": session.id
                    }), 200
                except Exception as e:
                    return jsonify({"error": str(e)}), 400

        # Step 2: Verify Payment
        if STRIPE_SECRET_KEY != "sk_test_mock":
            try:
                session = stripe.checkout.Session.retrieve(session_id)
                if session.payment_status != 'paid':
                     return jsonify({"message": "Payment not finalized"}), 400
            except Exception as e:
                return jsonify({"message": "Invalid session", "error": str(e)}), 400

        # Step 3: Complete Transaction
        transaction = {
            "item_id": str(item["_id"]),
            "buyer_id": buyer_id,
            "seller_id": item["seller_id"],
            "price": item_price,
            "platform_fee": platform_fee,
            "total_amount": total_amount,
            "razorpay_payment_id": razorpay_payment_id,
            "razorpay_order_id": razorpay_order_id,
            "created_at": datetime.datetime.utcnow(),
            "status": "Completed"
        }
        transaction_result = transactions_collection.insert_one(transaction)

        payment = {
            "type": "marketplace_fee",
            "transaction_id": str(transaction_result.inserted_id),
            "buyer_id": buyer_id,
            "seller_id": item["seller_id"],
            "item_price": item_price,
            "platform_fee": platform_fee,
            "total_amount": total_amount,
            "status": "Completed",
            "created_at": datetime.datetime.utcnow()
        }
        payments_collection.insert_one(payment)

        marketplace_collection.update_one(
            {"_id": ObjectId(item_id)},
            {"$set": {"status": "Sold"}}
        )

        return jsonify({
            "message": "Item purchased successfully",
            "transaction_id": str(transaction_result.inserted_id),
            "price": item_price,
            "platform_fee": platform_fee,
            "total_charged": total_amount
        }), 200

    except Exception as e:
        return jsonify({"message": "Error processing purchase", "error": str(e)}), 400


@marketplace_bp.route('/my-items', methods=['GET'])
@jwt_required()
def get_my_items():
    """Get items listed by the currently logged-in user."""
    user_id = get_jwt_identity()
    items = list(marketplace_collection.find({"seller_id": user_id}).sort("created_at", -1))
    return jsonify(items), 200


@marketplace_bp.route('/items/<item_id>', methods=['DELETE'])
@jwt_required()
def delete_item(item_id):
    """Allow seller to delete their own listing."""
    user_id = get_jwt_identity()
    try:
        item = marketplace_collection.find_one({"_id": ObjectId(item_id)})
        if not item:
            return jsonify({"message": "Item not found"}), 404
        if item.get("seller_id") != user_id:
            return jsonify({"message": "You can only delete your own items"}), 403
        marketplace_collection.delete_one({"_id": ObjectId(item_id)})
        return jsonify({"message": "Item deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": "Error deleting item", "error": str(e)}), 400

@marketplace_bp.route('/items/<item_id>', methods=['PUT'])
@jwt_required()
def edit_item(item_id):
    """Allow seller to edit their own listing."""
    user_id = get_jwt_identity()
    try:
        data = request.form if request.form else request.get_json()
        item = marketplace_collection.find_one({"_id": ObjectId(item_id)})
        if not item:
            return jsonify({"message": "Item not found"}), 404
        if item.get("seller_id") != user_id:
            return jsonify({"message": "You can only edit your own items"}), 403

        update_fields = {}
        if data.get('title'): update_fields['title'] = data.get('title')
        if data.get('description'): update_fields['description'] = data.get('description')
        if data.get('price'): update_fields['price'] = float(data.get('price'))
        if data.get('category'): update_fields['category'] = data.get('category')
        if data.get('location'): update_fields['pickup_location'] = data.get('location')

        # Handle image upload for edit
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                filename = f"{datetime.datetime.utcnow().timestamp()}_{filename}"
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                update_fields['image_url'] = f"http://localhost:5000/uploads/{filename}"

        if not update_fields:
            return jsonify({"message": "No fields to update"}), 400

        marketplace_collection.update_one({"_id": ObjectId(item_id)}, {"$set": update_fields})
        return jsonify({"message": "Item updated successfully"}), 200
    except Exception as e:
        return jsonify({"message": "Error updating item", "error": str(e)}), 400
