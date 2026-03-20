# CampusConnect: Smart Campus Lost & Found + Marketplace System

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![React](https://img.shields.io/badge/Frontend-React.js-61DAFB?logo=react&logoColor=black)
![Flask](https://img.shields.io/badge/Backend-Flask-000000?logo=flask&logoColor=white)
![MongoDB](https://img.shields.io/badge/Database-MongoDB_Atlas-47A248?logo=mongodb&logoColor=white)

CampusConnect is an intelligent, unified campus platform designed exclusively for university students and alumni. It solves two critical campus problems through advanced technology:
1. **Lost & Found:** An AI-powered matching system to seamlessly report and recover lost items securely using TF-IDF text similarity and OpenCV image analysis.
2. **Campus Marketplace:** A trusted, peer-to-peer ecosystem where graduating seniors or alumni can sell pre-owned academic materials, electronics, and hostel essentials to juniors.

By leveraging cutting-edge web technologies and a secure internal payment system, CampusConnect fosters a circular campus economy while maintaining trust through university-verified accounts.

---

## 🚀 Key Features

### Module 1: AI-Powered Lost & Found
*Traditional lost & found systems rely on manual logs. CampusConnect automates this via intelligent matching.*
- **Detailed Reporting:** Submit lost or found reports containing the item's Name, Category, Location, Date, Description, and Image.
- **Smart Matching (TF-IDF & OpenCV):** The system passively compares lost and found databases using Natural Language Processing (NLP) on descriptions along with visual similarity checks.
- **Instant Notifications:** High-confidence matches automatically trigger alerts to the original owner.
- **Secure Verification:** Claims are passed through an Admin to verify ownership via private details.
- **Convenient Retrieval:** Items are returned securely at the campus reception, supported by a minimal platform fee.

### Module 2: Peer-to-Peer Campus Marketplace
*A secure alternative to generic public marketplaces, restricted strictly to campus members.*
- **Customized Listings:** Seniors/Alumni can list items securely indicating the price, category, and pickup instructions.
- **Intelligent Browsing:** Students can filter listings specifically tailored for campus living (e.g., specific semester textbooks or dorm furniture).
- **Integrated Payments:** Direct, secure payment integration via Razorpay/Stripe, featuring an automatic platform fee deduction.
- **Safe Handoff:** Coordinated on-campus meeting setups completely localized to the university.

### Advanced Capabilities (AI & Analytics)
- **Semantic Text Matching:** Using TF-IDF logic to match phrases contextually (e.g., "Lost Black Water Bottle" intelligently maps to "Found Dark Flask").
- **Image Similarity Rating:** OpenCV checks color histograms and contours of items uploaded.
- **Trust System:** Integrated seller ratings and peer reviews.
- **Admin Dashboard:** Centralized monitoring for recovered items count, transaction volumes, and revenue tracking.

---

## 🛠️ Tech Stack & Architecture

### Frontend (React Ecosystem)
- **Framework:** React.js
- **Styling:** Tailwind CSS for a modern, responsive user interface.
- **State Management:** Modern hooks and context layers.

### Backend (Python/Flask API)
- **Framework:** Flask (Python)
- **Authentication:** JSON Web Tokens (JWT) for stateless, secure API communication.
- **Payment Processing:** Razorpay or Stripe integration.
- **AI/ML Modules:** Scikit-Learn (for TF-IDF similarity) and OpenCV (for visual item comparison).

### Database (MongoDB)
- **Platform:** MongoDB Atlas (Cloud)
- **Core Collections:** `Users`, `Items`, `LostReports`, `Transactions`, `Reviews`, `Payments`.

---

## 📁 Project Structure

```text
campus-connecting/
├── backend/                    # Python Flask Server & AI Modules
│   ├── app.py                  # Main entry point for Flask
│   ├── config.py               # Application configurations
│   ├── db.py                   # MongoDB connection logic
│   ├── requirements.txt        # Python dependencies
│   └── routes/                 # API endpoint handlers
├── frontend/                   # React.js Client
│   ├── src/
│   │   ├── App.jsx             # Main React entry point
│   │   ├── components/         # Reusable UI components
│   │   ├── pages/              # Application views
│   │   └── index.css           # Global Tailwind entries
│   ├── vite.config.js          # Vite configuration
│   └── package.json            # Node.js dependencies
└── README.md                   # Project documentation
```

---

## 👥 User Roles & Workflows

1. **Student:** Report lost/found items, browse marketplace, contact sellers, process purchases, and claim verified items.
2. **Alumni / Seniors:** Post pre-owned items for sale and coordinate secure hand-offs.
3. **Admin (Campus Security/Reception):** Oversee system integrity, verify lost item claims, resolve marketplace disputes, and manage platform metrics.

---

## 💻 Getting Started

### Prerequisites
- Node.js (v18+)
- Python (v3.10+)
- MongoDB Atlas Account / Local Instance

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/campus-connecting.git
cd campus-connecting
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
# Activate virtual environment (Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
```
*Note: Ensure you have your `.env` variables mapped (e.g., `MONGO_URI`, `JWT_SECRET`).*
```bash
# Start Flask API
python app.py
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 🛡️ License
This project is restricted for campus-wide use. Educational or open-source licenses apply depending on university scope.

**Built to modernize campus living.**