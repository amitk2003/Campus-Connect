# 🚀 CampusConnect: Project Report & Working Model

CampusConnect is a comprehensive digital ecosystem designed for university campuses. It facilitates secure peer-to-peer transactions and an AI-powered Lost & Found recovery system, specifically tailored to the needs of students and staff.

---

## 🏗️ System Architecture
The application follows a modern **MERN-like stack** (using Flask for the backend):

- **Frontend**: React.js with Tailwind CSS & Lucide Icons.
- **Backend**: Python (Flask) with JWT Authentication.
- **Database**: MongoDB Atlas (NoSQL) for flexible data storage.
- **Payment Gateway**: Stripe (Integrated for Marketplace sales and Claim fees).
- **AI Matching**: Custom TF-IDF similarity algorithm for Lost & Found item recovery.

---

## 🌟 Key Features

### 1. Secure Marketplace
- **Anonymous Trading**: Users are identified by unique anonymous handles (e.g., `User#ABC12`) to protect privacy during transactions.
- **Verified Payments**: Integrated with Stripe to handle secure transactions and platform fees (5%).
- **Item Management**: Students can list, edit, and track their items for sale.

### 2. AI-Powered Lost & Found
- **Smart Matching**: Automated system that matches "Lost" reports with "Found" items using text similarity and image matching.
- **Verified Claims**: Claimers must provide proof of ownership and pay a nominal fee (based on item value) to ensure legitimacy.
- **End-to-End Recovery**: Tracks items from report to handover.

### 3. Dedicated Admin Dashboard
- **Role Isolation**: Admin is restricted from participating as a regular user to maintain neutrality.
- **Platform Analytics**: Real-time stats on total users, marketplace volume, and recovered items.
- **Financial Oversight**: Tracking platform revenue from marketplace fees and claim fees.
- **Dispute Resolution**: Admins verify and approve/reject claims after verifying ownership proof.

---

## 🔒 Security & Roles
- **Student/Alumni**: Can buy/sell and report lost items. Identity is protected via `anon_name`.
- **Admin**: Has full visibility of all real names and emails to resolve disputes, but is **restricted from buying, selling, or claiming items** for personal use.

---

## 🛠️ Tech Stack Details
| Layer | Technology |
|---|---|
| **Frontend** | React, Vite, Axios, React Router, Tailwind CSS |
| **Backend** | Flask, Flask-JWT-Extended, Flask-CORS |
| **Database** | MongoDB Atlas (Cloud) |
| **Payments** | Stripe API |
| **Design** | Dark-mode enabled, Responsive Glassmorphic UI |

---

## 📄 Final Status
The application is **Production Ready**. Admin roles have been strictly isolated from the marketplace functionality as requested, and the platform is ready for demonstration.
