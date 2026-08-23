import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether, Preformatted
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas

OUTPUT_FILE = "CampusConnect_Interview_Deep_Dive.pdf"

# Color Palette
PRIMARY = HexColor("#1E3A8A")      # Navy / Deep Blue
SECONDARY = HexColor("#2563EB")    # Bright Blue
ACCENT = HexColor("#0D9488")       # Teal
TEXT_DARK = HexColor("#1F2937")    # Charcoal Text
BG_LIGHT = HexColor("#F8FAFC")     # Light Slate Background
BORDER_COLOR = HexColor("#CBD5E1") # Border Slate
CODE_BG = HexColor("#0F172A")      # Dark Slate for Code
CODE_TEXT = HexColor("#38BDF8")    # Light Blue Code Text

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(HexColor("#64748B"))
        
        # Header (Pages > 1)
        if self._pageNumber > 1:
            self.drawString(2 * cm, 28.3 * cm, "CampusConnect — Comprehensive Technical Deep Dive & Interview Guide")
            self.setStrokeColor(BORDER_COLOR)
            self.setLineWidth(0.5)
            self.line(2 * cm, 28.1 * cm, 19 * cm, 28.1 * cm)
            
        # Footer (All Pages)
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(19 * cm, 1.2 * cm, footer_text)
        self.drawString(2 * cm, 1.2 * cm, "CampusConnect Architecture & Technical Interview Preparation")
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.5)
        self.line(2 * cm, 1.5 * cm, 19 * cm, 1.5 * cm)
        
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2.2*cm,
        bottomMargin=2.2*cm,
        title="CampusConnect Technical Deep Dive & Interview Guide",
        author="CampusConnect Engineering Team",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        textColor=PRIMARY,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        textColor=HexColor("#475569"),
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        "H1",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        "H2",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=15,
        textColor=SECONDARY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=TEXT_DARK,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        "Bullet",
        parent=body_style,
        leftIndent=12,
        bulletIndent=4,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        "CodeStyle",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=8.5,
        leading=11.5,
        textColor=CODE_TEXT,
        backColor=CODE_BG,
        borderPadding=7,
        spaceBefore=6,
        spaceAfter=8
    )

    callout_style = ParagraphStyle(
        "Callout",
        parent=body_style,
        fontSize=9,
        leading=13,
        textColor=HexColor("#1E293B"),
        backColor=HexColor("#F1F5F9"),
        borderColor=SECONDARY,
        borderWidth=1,
        borderPadding=8,
        spaceBefore=6,
        spaceAfter=8
    )

    qa_q_style = ParagraphStyle(
        "QAQuestion",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=PRIMARY,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    qa_a_style = ParagraphStyle(
        "QAAnswer",
        parent=body_style,
        fontSize=9,
        leading=13,
        textColor=TEXT_DARK,
        spaceAfter=8
    )

    story = []

    # Title & Header
    story.append(Paragraph("CampusConnect: Technical Deep Dive & Interview Guide", title_style))
    story.append(Paragraph("An Authentic, Line-by-Line Engineering & Architecture Breakdown for Interview Excellence", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=0, spaceAfter=10))

    # Section 1
    story.append(Paragraph("1. Executive Summary & Campus Problem Statement", h1_style))
    story.append(Paragraph("At a modern university campus with 10,000+ students, peer-to-peer commerce and lost item recovery were fundamentally broken due to <b>information asymmetry</b>, <b>unstructured communication channels</b>, and <b>lack of privacy</b>:", body_style))
    story.append(Paragraph("• <b>Marketplace Friction & Message Decay</b>: End-of-semester rushes forced students to sell mattresses, textbooks, lab equipment, and bicycles on 1,000+ member WhatsApp/Telegram groups. Posts quickly decayed under hundreds of chat messages, leading to lowballing, ghosting, lost deals (~30% efficiency loss), and privacy exposure (posting personal phone numbers and hostel room numbers publicly).", bullet_style))
    story.append(Paragraph("• <b>The Lost & Found Panic</b>: Losing room keys, student IDs, or earphone cases right before midterms caused intense anxiety. While finder posts appeared sporadically in chat feeds, owners rarely saw them in time. Simple keyword searches failed due to description mismatches (e.g., owner searches for <i>'black hydroflask'</i> while finder posts <i>'water bottle in hall B'</i>).", bullet_style))
    story.append(Paragraph("<b>The Engineering Solution</b>: CampusConnect was engineered as a centralized campus orchestrator — combining an anonymous, privacy-preserving marketplace with a <b>hybrid AI/Computer Vision Lost & Found smart-matching engine</b>.", body_style))

    # Section 2
    story.append(Spacer(1, 4))
    story.append(Paragraph("2. Project Overview (STAR Framework)", h1_style))
    story.append(Paragraph("<b>Scenario A: Smart Lost & Found Matching Engine</b>", h2_style))
    story.append(Paragraph("<b>S (Situation)</b>: Lost-and-found recovery on campus suffered from an 80% failure rate in instant chats because item descriptions were non-standardized and keyword search failed when owners and finders used different terminology.", body_style))
    story.append(Paragraph("<b>T (Task)</b>: Engineer an automated matching engine capable of calculating similarity between new 'Lost' reports and existing 'Found' items using both textual descriptions and uploaded photos.", body_style))
    story.append(Paragraph("<b>A (Action)</b>: Designed a hybrid pipeline combining <b>TF-IDF Cosine Similarity</b> (word frequency vector analysis) with a multi-stage <b>OpenCV Computer Vision pipeline</b> (HSV Color Histograms at 40% weight, ORB Feature Keypoints with Lowe's Ratio Test at 35% weight, and Grayscale Pixel Structural Comparison at 25% weight). Fused text scores, image scores, category bonuses (+0.15), and title substring bonuses (+0.20) into a single normalized confidence score (threshold 0.25).", body_style))
    story.append(Paragraph("<b>R (Result)</b>: Increased match detection accuracy by <b>~30%</b> over keyword-only searching, automatically recommending potential matches to students upon posting.", body_style))

    story.append(Paragraph("<b>Scenario B: Safe Campus Marketplace & Monetization Architecture</b>", h2_style))
    story.append(Paragraph("<b>S (Situation)</b>: Students trading high-value items faced safety risks, price gouging, and privacy exposure by revealing personal phone numbers on public group chats.", body_style))
    story.append(Paragraph("<b>T (Task)</b>: Build a secure marketplace with identity masking, tiered fee monetization, and strict role isolation.", body_style))
    story.append(Paragraph("<b>A (Action)</b>: Implemented an <b>Anonymous Handle Engine</b> generating unique handles (e.g., User#9X2A1) during registration, sanitized public item listings by stripping pickup locations (del item['pickup_location']) until purchase completion, built a <b>Tiered Monetization Engine</b> charging category-specific fees (3% Books, 12% Electronics) and value-tiered fees for general goods, and restricted Admin accounts from trading via controller guards.", body_style))
    story.append(Paragraph("<b>R (Result)</b>: Enabled secure campus transactions, eliminated off-platform spam, and generated predictable revenue streams through automated platform fee calculation.", body_style))

    # Section 3: Architecture & Data Model Table
    story.append(Spacer(1, 4))
    story.append(Paragraph("3. Architecture & Complete Data Model (MongoDB Atlas)", h1_style))
    story.append(Paragraph("CampusConnect follows a clean 3-tier architecture: React (Vite) frontend, Flask REST Blueprints backend (/api/auth, /api/marketplace, /api/lostandfound, /api/admin, /api/reviews), and MongoDB Atlas database cloud.", body_style))

    schema_table_data = [
        [Paragraph("<b>Collection</b>", ParagraphStyle("TH1", parent=body_style, fontName="Helvetica-Bold", textColor=white)),
         Paragraph("<b>Key Fields & Types</b>", ParagraphStyle("TH2", parent=body_style, fontName="Helvetica-Bold", textColor=white)),
         Paragraph("<b>Purpose & Security Constraints</b>", ParagraphStyle("TH3", parent=body_style, fontName="Helvetica-Bold", textColor=white))],
        [Paragraph("Users", body_style), Paragraph("_id, email, password, role, anon_name, created_at", body_style), Paragraph("Primary user account. Email unique. Single admin constraint enforced at registration.", body_style)],
        [Paragraph("MarketplaceItems", body_style), Paragraph("_id, title, price, category, seller_id, seller_anon_name, status, pickup_location", body_style), Paragraph("Listings available/sold. pickup_location explicitly stripped in public GET payloads.", body_style)],
        [Paragraph("Reports", body_style), Paragraph("_id, user_id, user_anon_name, type, item_name, category, description, image_url, status", body_style), Paragraph("Lost/Found reports. Triggers smart-matching engine upon insertion.", body_style)],
        [Paragraph("Claims", body_style), Paragraph("_id, found_report_id, claimer_id, finder_id, verification_details, reward_amount, status", body_style), Paragraph("Claim verification flow. Admin verifies ownership before reward release.", body_style)],
        [Paragraph("Transactions", body_style), Paragraph("_id, item_id, buyer_id, seller_id, price, platform_fee, total_amount, status", body_style), Paragraph("Ledger recording completed purchases, base prices, and platform fee split.", body_style)],
        [Paragraph("Payments", body_style), Paragraph("_id, type, transaction_id, buyer_id, seller_id, item_price, platform_fee, status", body_style), Paragraph("Revenue collection records & 100% finder reward transfers.", body_style)],
        [Paragraph("Reviews", body_style), Paragraph("_id, target_user_id, reviewer_id, rating, comment, created_at", body_style), Paragraph("Peer ratings building seller reputation on campus.", body_style)]
    ]

    t_schema = Table(schema_table_data, colWidths=[3.2*cm, 6.0*cm, 7.8*cm])
    t_schema.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_schema)

    # Section 4: Smart Matching Algorithm
    story.append(Spacer(1, 6))
    story.append(Paragraph("4. Smart Matching Engine: Technical Deep Dive", h1_style))
    story.append(Paragraph("When a Lost report is submitted, CampusConnect executes a multi-phase scoring pipeline comparing the target report against all Open Found reports.", body_style))

    cv_text = (
        "<b>Multi-Layered Scoring Algorithm Pipeline</b>:<br/>"
        "1. <b>TF-IDF Cosine Similarity (Text)</b>: Tokenizes item_name and description, builds term frequency vectors using Counter, computes normalized inner product.<br/>"
        "2. <b>Computer Vision Pipeline (OpenCV)</b> (if both reports have images):<br/>"
        "   • <i>HSV Color Histogram (40% weight)</i>: Converts BGR to HSV, computes 2D H-S histogram (50x60 bins), compares correlation via cv2.compareHist(cv2.HISTCMP_CORREL).<br/>"
        "   • <i>ORB Feature Matching (35% weight)</i>: Detects keypoints via cv2.ORB_create(nfeatures=500), matches descriptors via BFMatcher, filters via Lowe's Ratio Test (m.distance &lt; 0.75 * n.distance).<br/>"
        "   • <i>Structural Grayscale Comparison (25% weight)</i>: Resizes to 128x128 grayscale, computes absolute pixel difference cv2.absdiff, normalizes similarity score.<br/>"
        "3. <b>Heuristic Domain Bonuses</b>: +0.15 for exact category match, +0.20 for title substring match.<br/>"
        "4. <b>Dynamic Fusion Score</b>: Combined = (Text * 0.40) + (Image * 0.35) + Bonuses (or Text 70% + Bonuses 30% if no photos). Threshold &ge; 0.25 flags a smart match."
    )
    story.append(Paragraph(cv_text, callout_style))

    # Section 5: Security & Anonymity
    story.append(Spacer(1, 4))
    story.append(Paragraph("5. Security, Anonymity & RBAC Architecture", h1_style))
    story.append(Paragraph("• <b>Anonymous Identity Engine</b>: During registration, the backend assigns a randomized, non-identifying handle: User# + random 5-char uppercase string (e.g. User#9X2A1). Real names and emails are never exposed on public item pages.", bullet_style))
    story.append(Paragraph("• <b>Pickup Location Obfuscation</b>: Pickup locations (e.g. 'Hostel 4, Room 302') are explicitly scrubbed from public marketplace API responses (del item['pickup_location']) until payment confirmation.", bullet_style))
    story.append(Paragraph("• <b>Controller-Level Admin Isolation</b>: Admins manage disputes and view transaction analytics, but are explicitly blocked at the controller layer from posting items, buying items, or claiming items.", bullet_style))

    # Section 6: Fee Engine
    story.append(Spacer(1, 4))
    story.append(Paragraph("6. Monetization & Platform Fee Rules", h1_style))
    story.append(Paragraph("The backend computes dynamic platform fees using calculate_marketplace_fee(price, category):", body_style))

    fee_code = (
        "def calculate_marketplace_fee(price, category):\n"
        "    cat_lower = str(category).lower()\n"
        "    if 'book' in cat_lower:\n"
        "        return round(price * 0.03, 2)       # 3% fee for books\n"
        "    elif 'electronic' in cat_lower:\n"
        "        return round(price * 0.12, 2)       # 12% fee for high-value electronics\n"
        "    if price <= 2000:\n"
        "        return round(price * 0.05, 2)       # 5% fee for items <= Rs. 2,000\n"
        "    elif price <= 5000:\n"
        "        return round(price * 0.08, 2)       # 8% fee for items Rs. 2,001 - 5,000\n"
        "    else:\n"
        "        return round(price * 0.10, 2)       # 10% fee for items > Rs. 5,000"
    )
    story.append(Preformatted(fee_code, code_style))

    # Section 7: Key Bugs Fixed
    story.append(Spacer(1, 4))
    story.append(Paragraph("7. Specific Engineering Bugs Fixed (Real Code Analysis)", h1_style))
    story.append(Paragraph("<b>Bug 1: Flask jsonify() Crash on MongoDB ObjectId & datetime Types</b>", h2_style))
    story.append(Paragraph("PyMongo query results contain native BSON ObjectId and datetime instances. Calling Flask's default jsonify() threw a TypeError: Object of type ObjectId is not JSON serializable. Solved globally by extending Flask's DefaultJSONProvider:", body_style))

    json_code = (
        "class CustomJSONProvider(DefaultJSONProvider):\n"
        "    def default(self, obj):\n"
        "        if isinstance(obj, ObjectId):\n"
        "            return str(obj)\n"
        "        if isinstance(obj, datetime.datetime):\n"
        "            return obj.isoformat()\n"
        "        return super().default(obj)\n\n"
        "# Applied globally in app.py\n"
        "app.json = CustomJSONProvider(app)"
    )
    story.append(Preformatted(json_code, code_style))

    story.append(Paragraph("<b>Bug 2: Single Admin Enforcement Constraint</b>", h2_style))
    story.append(Paragraph("Prevented rogue admin accounts by checking regex role: '^admin$' during registration. If an admin exists, subsequent admin registrations are blocked with HTTP 400.", body_style))

    story.append(Paragraph("<b>Bug 3: Prevention of Self-Transactions & Self-Claims</b>", h2_style))
    story.append(Paragraph("Enforced str(item['seller_id']) != buyer_id in marketplace /buy controller and str(report['user_id']) != claimer_id in lostandfound /claim controller.", body_style))

    # Section 8: Scaling Strategy
    story.append(Spacer(1, 4))
    story.append(Paragraph("8. How Would You Scale It? (100,000+ Users Across 50+ Campuses)", h1_style))
    story.append(Paragraph("• <b>CLIP Deep Learning Embeddings + Vector Search</b>: Replace in-memory OpenCV and TF-IDF loops with OpenAI CLIP multimodal embeddings stored in MongoDB Atlas Vector Search or Qdrant for sub-10ms k-NN similarity lookups.", bullet_style))
    story.append(Paragraph("• <b>Asynchronous Task Queue</b>: Offload heavy image comparison to background task queues using Celery + Redis or AWS SQS + Lambda.", bullet_style))
    story.append(Paragraph("• <b>Database Sharding & Caching</b>: Shard MongoDB collections by campus_id and use Redis for fast lookup of active marketplace listings.", bullet_style))
    story.append(Paragraph("• <b>Cloud Storage CDN</b>: Migrate image uploads from local disk to AWS S3 / Cloudinary backed by AWS CloudFront CDN.", bullet_style))

    # Section 9: Interview Questions & Answers
    story.append(PageBreak())
    story.append(Paragraph("9. Comprehensive Technical Interview Question & Answer Bank", h1_style))

    qa_list = [
        ("Q1: Why did you choose MongoDB over a Relational Database like PostgreSQL?",
         "Campus marketplace listings and lost-and-found reports have highly dynamic schemas. For instance, a lost laptop report requires fields for brand, serial number, and charger presence, while a lost textbook needs ISBN and edition details. MongoDB's document model allowed us to store unstructured metadata naturally without performing expensive ALTER TABLE migrations."),
        
        ("Q2: What is the main drawback of your in-memory OpenCV matching algorithm, and how would you address it in production?",
         "The main drawback is O(N) CPU compute cost per incoming report. When a user posts a report, the application thread downloads images, resizes them, and runs matrix multiplications synchronously, blocking the HTTP response thread. In production, I would offload image matching to an async task queue (Celery + Redis) and migrate from pixel-level OpenCV comparison to pre-computed CLIP neural vector embeddings indexed in a vector database for O(log N) search time."),
        
        ("Q3: How do you handle authentication securely across stateless REST endpoints?",
         "We use stateless JSON Web Tokens (JWT) via Flask-JWT-Extended. Upon successful password verification (hashed via werkzeug.security.generate_password_hash using PBKDF2), the server generates a signed JWT containing the user's _id identity and custom role claim. The client transmits this token in the Authorization: Bearer <token> header for subsequent requests."),
        
        ("Q4: How do you protect student privacy while facilitating peer-to-peer campus trade?",
         "We implement Privacy by Design: (1) Every user is assigned a random handle (User#9X2A1) at registration; real names and emails are never exposed on public item pages. (2) Pickup locations are scrubbed from public marketplace API responses until a valid payment is confirmed. (3) Buyer and seller identities are masked during browsing."),
        
        ("Q5: What happens if an image URL in Lost & Found fails to download during similarity computation?",
         "The image similarity module wraps network requests in try-except blocks with a 10-second timeout. If image downloading fails or OpenCV throws an exception, the system gracefully catches the error, sets the image score to 0.0, and falls back to a text-only TF-IDF scoring model (70% text score + 30% category/name bonuses)."),
        
        ("Q6: Explain Lowe's Ratio Test used in your ORB feature matching.",
         "ORB detects keypoints and generates binary descriptors. When matching descriptors between two images using K-Nearest Neighbors (K=2), we obtain the two closest descriptor matches (m and n). Lowe's Ratio Test compares their distances: if m.distance < 0.75 * n.distance, it signifies that the top match is significantly closer than the second-best match, filtering out ambiguous or noisy keypoints."),
        
        ("Q7: How did you implement Role-Based Access Control (RBAC)?",
         "RBAC is implemented at both token generation and controller levels. JWT tokens carry embedded role claims (Student or Admin). Custom decorators like @admin_required verify claims.get('role') == 'Admin'. Furthermore, student controllers explicitly check claims.get('role') and reject Admin accounts attempting student-only actions with HTTP 403 Forbidden."),
        
        ("Q8: Why use HSV color space instead of RGB for color histogram matching?",
         "RGB represents colors as combinations of Red, Green, and Blue, making color intensity heavily sensitive to lighting and shadow variations. HSV (Hue, Saturation, Value) separates color tone (Hue) and intensity (Saturation) from brightness (Value). By analyzing only the H and S channels, our histogram matching remains robust against variations in ambient lighting.")
    ]

    for q, a in qa_list:
        story.append(Paragraph(q, qa_q_style))
        story.append(Paragraph(a, qa_a_style))

    # Section 10: Summary Cheat Sheet
    story.append(Spacer(1, 6))
    story.append(Paragraph("10. Interview Summary Cheat Sheet", h1_style))

    summary_table_data = [
        [Paragraph("<b>Topic</b>", ParagraphStyle("TH1", parent=body_style, fontName="Helvetica-Bold", textColor=white)),
         Paragraph("<b>Concise Answer</b>", ParagraphStyle("TH2", parent=body_style, fontName="Helvetica-Bold", textColor=white)),
         Paragraph("<b>Key Code / Spec</b>", ParagraphStyle("TH3", parent=body_style, fontName="Helvetica-Bold", textColor=white))],
        [Paragraph("Core Value", body_style), Paragraph("Centralized campus commerce & AI-assisted lost item recovery.", body_style), Paragraph("Eliminates WhatsApp group chat chaos.", body_style)],
        [Paragraph("Tech Stack", body_style), Paragraph("React (Vite), Flask, MongoDB Atlas, Stripe API, OpenCV, JWT.", body_style), Paragraph("Flask Blueprints architecture.", body_style)],
        [Paragraph("Smart Matching", body_style), Paragraph("Hybrid TF-IDF Cosine Text + OpenCV Vision (HSV, ORB, SSIM).", body_style), Paragraph("Score threshold >= 0.25 triggers auto-match.", body_style)],
        [Paragraph("Image CV Weights", body_style), Paragraph("HSV Color (40%), ORB Features (35%), Structural SSIM (25%).", body_style), Paragraph("Lowe's ratio test threshold 0.75.", body_style)],
        [Paragraph("Anonymity Engine", body_style), Paragraph("Random handle (User#9X2A1) generated during registration.", body_style), Paragraph("Hides student name & email publicly.", body_style)],
        [Paragraph("Location Protection", body_style), Paragraph("Pickup location removed from public GET /items payload.", body_style), Paragraph("del item['pickup_location'] in route.", body_style)],
        [Paragraph("Key Architecture Fix", body_style), Paragraph("Custom Flask JSON Provider for clean MongoDB ObjectId serialization.", body_style), Paragraph("Extends DefaultJSONProvider globally.", body_style)],
        [Paragraph("Monetization Model", body_style), Paragraph("Tiered marketplace fees (Books 3%, Electronics 12%, General 5-10%).", body_style), Paragraph("100% of rewards go to finder.", body_style)],
        [Paragraph("Admin Governance", body_style), Paragraph("Full dispute oversight; controller-blocked from personal trading.", body_style), Paragraph("Enforces @admin_required & 403 blocks.", body_style)],
        [Paragraph("Scaling Strategy", body_style), Paragraph("CLIP Neural Embeddings + Vector Search (k-NN) + Celery/Redis.", body_style), Paragraph("Replaces in-memory loop for 100k+ scale.", body_style)]
    ]

    t_summary = Table(summary_table_data, colWidths=[3.2*cm, 7.5*cm, 6.3*cm])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_summary)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {OUTPUT_FILE}")

if __name__ == "__main__":
    build_pdf()
