from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from bson import ObjectId
from flask.json.provider import DefaultJSONProvider
import datetime

class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)

import os
from flask import send_from_directory

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ✅ Use new JSON provider
app.json = CustomJSONProvider(app)

CORS(
    app,
    resources={r"/api/*": {"origins": "http://localhost:5173"}},
    allow_headers=["Content-Type", "Authorization"],
    supports_credentials=True
)
jwt = JWTManager(app)

# Register Blueprints
from routes.auth_routes import auth_bp
from routes.marketplace_routes import marketplace_bp
from routes.lostandfound_routes import lostandfound_bp
from routes.admin_routes import admin_bp
from routes.reviews_routes import reviews_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(marketplace_bp, url_prefix='/api/marketplace')
app.register_blueprint(lostandfound_bp, url_prefix='/api/lostandfound')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(reviews_bp, url_prefix='/api/reviews')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "Healthy", "message": "CampusConnect API is running."}), 200

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)