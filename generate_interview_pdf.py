"""
CampusConnect — Interview Preparation PDF Generator
Run: pip install reportlab && python generate_interview_pdf.py
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
import datetime

# ─── Color Palette ────────────────────────────────────────────────────────────
BLUE        = HexColor("#2563EB")
BLUE_LIGHT  = HexColor("#DBEAFE")
INDIGO      = HexColor("#4F46E5")
PURPLE      = HexColor("#7C3AED")
EMERALD     = HexColor("#059669")
EMERALD_LT  = HexColor("#D1FAE5")
AMBER       = HexColor("#D97706")
AMBER_LT    = HexColor("#FEF3C7")
RED         = HexColor("#DC2626")
RED_LT      = HexColor("#FEE2E2")
SLATE_900   = HexColor("#0F172A")
SLATE_700   = HexColor("#334155")
SLATE_500   = HexColor("#64748B")
SLATE_200   = HexColor("#E2E8F0")
SLATE_100   = HexColor("#F1F5F9")
SLATE_50    = HexColor("#F8FAFC")

OUTPUT_FILE = "CampusConnect_Interview_Guide.pdf"

doc = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=A4,
    rightMargin=2*cm,
    leftMargin=2*cm,
    topMargin=2*cm,
    bottomMargin=2*cm,
    title="CampusConnect — Interview Guide",
    author="CampusConnect",
)

styles = getSampleStyleSheet()

# ─── Custom Styles ─────────────────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

style_cover_title = S("CoverTitle",
    fontSize=34, fontName="Helvetica-Bold",
    textColor=white, alignment=TA_CENTER, spaceAfter=6)

style_cover_sub = S("CoverSub",
    fontSize=14, fontName="Helvetica",
    textColor=HexColor("#BFDBFE"), alignment=TA_CENTER, spaceAfter=4)

style_cover_date = S("CoverDate",
    fontSize=10, fontName="Helvetica",
    textColor=HexColor("#93C5FD"), alignment=TA_CENTER)

style_h1 = S("H1",
    fontSize=20, fontName="Helvetica-Bold",
    textColor=BLUE, spaceBefore=18, spaceAfter=6)

style_h2 = S("H2",
    fontSize=14, fontName="Helvetica-Bold",
    textColor=INDIGO, spaceBefore=14, spaceAfter=4)

style_h3 = S("H3",
    fontSize=11, fontName="Helvetica-Bold",
    textColor=SLATE_700, spaceBefore=8, spaceAfter=3)

style_body = S("Body",
    fontSize=10, fontName="Helvetica",
    textColor=SLATE_700, leading=16, spaceAfter=4, alignment=TA_JUSTIFY)

style_bullet = S("Bullet",
    fontSize=10, fontName="Helvetica",
    textColor=SLATE_700, leading=15, leftIndent=16,
    spaceAfter=2, bulletText="•")

style_code = S("Code",
    fontSize=9, fontName="Courier",
    textColor=HexColor("#1E293B"), leading=14,
    backColor=SLATE_100, leftIndent=12, rightIndent=12,
    spaceAfter=6, spaceBefore=4,
    borderPadding=(6, 8, 6, 8))

style_q = S("Question",
    fontSize=11, fontName="Helvetica-Bold",
    textColor=white, leading=15,
    spaceAfter=4, spaceBefore=4)

style_a = S("Answer",
    fontSize=10, fontName="Helvetica",
    textColor=SLATE_700, leading=16,
    spaceAfter=2, leftIndent=8, alignment=TA_JUSTIFY)

style_highlight = S("Highlight",
    fontSize=10, fontName="Helvetica-Bold",
    textColor=EMERALD, leading=15, spaceAfter=2)

style_label = S("Label",
    fontSize=8, fontName="Helvetica-Bold",
    textColor=SLATE_500, spaceAfter=1)

style_toc = S("TOC",
    fontSize=11, fontName="Helvetica",
    textColor=BLUE, leading=18, leftIndent=8)

story = []

# ══════════════════════════════════════════════════════════════════════════════
# COVER PAGE
# ══════════════════════════════════════════════════════════════════════════════
cover_data = [[
    Paragraph("CampusConnect", style_cover_title),
], [
    Paragraph("Complete Interview Preparation Guide", style_cover_sub),
], [
    Paragraph("End-to-End Project Explanation + 25 Follow-Up Q&amp;A", style_cover_sub),
], [
    Spacer(1, 0.5*cm),
], [
    Paragraph(f"Generated on {datetime.datetime.now().strftime('%d %B %Y, %I:%M %p')}", style_cover_date),
]]

cover_table = Table([[row[0]] for row in cover_data], colWidths=[17*cm])
cover_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), BLUE),
    ("TOPPADDING", (0,0), (-1,-1), 18),
    ("BOTTOMPADDING", (0,0), (-1,-1), 18),
    ("LEFTPADDING", (0,0), (-1,-1), 24),
    ("RIGHTPADDING", (0,0), (-1,-1), 24),
    ("ROUNDEDCORNERS", (0,0), (-1,-1), 12),
]))
story.append(cover_table)
story.append(Spacer(1, 0.8*cm))

# Badges row
badge_data = [["🎓 Full-Stack Project", "🐍 Python Flask", "⚛️ React", "🍃 MongoDB", "🧠 AI/ML"]]
badge_table = Table(badge_data, colWidths=[3.4*cm]*5)
badge_table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), BLUE_LIGHT),
    ("FONTNAME", (0,0), (-1,-1), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("TEXTCOLOR", (0,0), (-1,-1), BLUE),
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,0), (-1,-1), 8),
    ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ("ROUNDEDCORNERS", (0,0), (-1,-1), 6),
    ("GRID", (0,0), (-1,-1), 0.5, SLATE_200),
]))
story.append(badge_table)
story.append(Spacer(1, 1.2*cm))

# ══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def section_header(title, emoji=""):
    tbl = Table([[Paragraph(f"{emoji}  {title}" if emoji else title, S("SH",
        fontSize=13, fontName="Helvetica-Bold", textColor=white))]], colWidths=[17*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), INDIGO),
        ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LEFTPADDING", (0,0), (-1,-1), 14),
    ]))
    return tbl

def info_box(text, color=BLUE_LIGHT, text_color=BLUE):
    tbl = Table([[Paragraph(text, S("IB", fontSize=10, fontName="Helvetica",
        textColor=text_color, leading=15))]], colWidths=[17*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), color),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING", (0,0), (-1,-1), 12),
        ("RIGHTPADDING", (0,0), (-1,-1), 12),
    ]))
    return tbl

def qa_block(q_num, question, answer_lines):
    """Render a styled Q&A block."""
    q_row = Table([[Paragraph(f"Q{q_num}.  {question}", style_q)]], colWidths=[17*cm])
    q_row.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), INDIGO),
        ("TOPPADDING", (0,0), (-1,-1), 9),
        ("BOTTOMPADDING", (0,0), (-1,-1), 9),
        ("LEFTPADDING", (0,0), (-1,-1), 12),
    ]))
    ans_content = [q_row]
    ans_content.append(Spacer(1, 0.15*cm))
    for line in answer_lines:
        if line.startswith("•"):
            ans_content.append(Paragraph(line[1:].strip(), style_bullet))
        elif line.startswith(">>"):
            ans_content.append(info_box(line[2:].strip()))
        else:
            ans_content.append(Paragraph(line, style_a))
    ans_content.append(Spacer(1, 0.4*cm))
    return KeepTogether(ans_content)

def two_col_table(rows, headers=None, w1=6*cm, w2=11*cm):
    data = []
    if headers:
        data.append(headers)
    data.extend(rows)
    t = Table(data, colWidths=[w1, w2])
    style_list = [
        ("FONTNAME", (0,0), (-1,-1), "Helvetica"),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("TEXTCOLOR", (0,0), (-1,-1), SLATE_700),
        ("GRID", (0,0), (-1,-1), 0.4, SLATE_200),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [SLATE_50, white]),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]
    if headers:
        style_list += [
            ("BACKGROUND", (0,0), (-1,0), INDIGO),
            ("TEXTCOLOR", (0,0), (-1,0), white),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ]
    t.setStyle(TableStyle(style_list))
    return t

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — PROJECT OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
story.append(section_header("1. Project Overview", "📋"))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    "CampusConnect is a full-stack web platform built to solve two real, painful problems "
    "that every college campus faces daily. It serves students and alumni throughout their "
    "entire campus lifecycle — from their first day buying used textbooks to their last day "
    "selling belongings and returning found items on the way out.",
    style_body))
story.append(Spacer(1, 0.3*cm))

overview_data = [
    ["Module", "Problem Solved", "Key Feature"],
    ["Lost & Found", "Lost items never get returned — WhatsApp messages get buried", "AI Smart Matching (TF-IDF + OpenCV)"],
    ["Marketplace", "No trusted channel connecting Alumni (sellers) to Students (buyers)", "Stripe Payments + Tiered Fee Model + Finder Rewards"],
]
t = Table(overview_data, colWidths=[3.5*cm, 7*cm, 6.5*cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), BLUE),
    ("TEXTCOLOR", (0,0), (-1,0), white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("TEXTCOLOR", (0,1), (-1,-1), SLATE_700),
    ("GRID", (0,0), (-1,-1), 0.4, SLATE_200),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [SLATE_50, white]),
    ("TOPPADDING", (0,0), (-1,-1), 7),
    ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ("LEFTPADDING", (0,0), (-1,-1), 8),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
]))
story.append(t)
story.append(Spacer(1, 0.5*cm))

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — TECH STACK
# ══════════════════════════════════════════════════════════════════════════════
story.append(section_header("2. Tech Stack", "🛠️"))
story.append(Spacer(1, 0.3*cm))

stack_data = [
    ["Layer", "Technology", "Why Chosen"],
    ["Frontend", "React + Vite + Tailwind CSS", "Component-based UI, fast dev server, utility-first styling"],
    ["Routing", "React Router v6", "SPA navigation without full page reloads"],
    ["Backend", "Python Flask + Blueprints", "Lightweight REST API, easy to modularize by feature"],
    ["Authentication", "Flask-JWT-Extended + Google OAuth 2.0", "Stateless JWT tokens embedded with role claims"],
    ["Database", "MongoDB Atlas (NoSQL)", "Flexible schema — item listings have varying attributes"],
    ["Payments", "Stripe Checkout", "Hosted payment page, PCI compliant, no raw card data"],
    ["AI — Text", "TF-IDF Cosine Similarity (custom)", "Match lost/found reports by description similarity"],
    ["AI — Image", "OpenCV (ORB + Histogram + SSIM)", "Match items visually via uploaded photo comparison"],
    ["File Storage", "Local /uploads/ (backend)", "Served via Flask static route /uploads/<filename>"],
    ["Deployment", "Gunicorn (WSGI server)", "Production-grade multi-worker Flask server"],
]
t = Table(stack_data, colWidths=[3.2*cm, 5.8*cm, 8*cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), BLUE),
    ("TEXTCOLOR", (0,0), (-1,0), white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
    ("FONTSIZE", (0,0), (-1,-1), 8.5),
    ("TEXTCOLOR", (0,1), (-1,-1), SLATE_700),
    ("GRID", (0,0), (-1,-1), 0.4, SLATE_200),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [SLATE_50, white]),
    ("TOPPADDING", (0,0), (-1,-1), 6),
    ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ("LEFTPADDING", (0,0), (-1,-1), 8),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
]))
story.append(t)
story.append(Spacer(1, 0.5*cm))

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — ARCHITECTURE
# ══════════════════════════════════════════════════════════════════════════════
story.append(section_header("3. System Architecture", "🏗️"))
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    "The application follows a three-tier architecture: React frontend communicates "
    "with a Flask REST API backend, which reads/writes to MongoDB Atlas cloud database.",
    style_body))
story.append(Spacer(1, 0.2*cm))

arch_data = [["React Frontend\n(Port 5173)", "⟺  REST API  ⟺", "Flask Backend\n(Port 5000)", "⟺  PyMongo  ⟺", "MongoDB Atlas\n(Cloud)"]]
t = Table(arch_data, colWidths=[3.2*cm, 2.5*cm, 3.2*cm, 2.5*cm, 3.6*cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (0,0), BLUE_LIGHT),
    ("BACKGROUND", (2,0), (2,0), EMERALD_LT),
    ("BACKGROUND", (4,0), (4,0), AMBER_LT),
    ("BACKGROUND", (1,0), (1,0), SLATE_100),
    ("BACKGROUND", (3,0), (3,0), SLATE_100),
    ("FONTNAME", (0,0), (-1,-1), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("TOPPADDING", (0,0), (-1,-1), 14),
    ("BOTTOMPADDING", (0,0), (-1,-1), 14),
    ("GRID", (0,0), (-1,-1), 0.5, SLATE_200),
    ("TEXTCOLOR", (0,0), (0,0), BLUE),
    ("TEXTCOLOR", (2,0), (2,0), EMERALD),
    ("TEXTCOLOR", (4,0), (4,0), AMBER),
]))
story.append(t)
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("<b>Flask Blueprint Structure (5 Modules):</b>", style_h3))
bp_data = [
    ["Blueprint", "URL Prefix", "Responsibility"],
    ["auth_bp", "/api/auth", "Register, Login, Google OAuth, Password Reset"],
    ["marketplace_bp", "/api/marketplace", "Post/Browse/Buy/Edit/Delete items + Stripe"],
    ["lostandfound_bp", "/api/lostandfound", "Report/Claim items + AI Smart Matching"],
    ["admin_bp", "/api/admin", "Dashboard stats, moderation, claim verification"],
    ["reviews_bp", "/api/reviews", "Item reviews and ratings"],
]
story.append(two_col_table(bp_data[1:], headers=bp_data[0], w1=3.5*cm, w2=13.5*cm))
story.append(Spacer(1, 0.5*cm))

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — AUTHENTICATION
# ══════════════════════════════════════════════════════════════════════════════
story.append(section_header("4. Authentication Flow", "🔐"))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("<b>Three User Roles:</b>", style_h3))
role_data = [
    ["Role", "Capabilities", "Restriction"],
    ["Student", "Post/Buy items, Report Lost/Found, Claim items", "Cannot access Admin dashboard"],
    ["Alumni", "Same as Student — account persists after graduation", "Cannot access Admin dashboard"],
    ["Admin", "View stats, moderate listings, verify claims", "Cannot post, buy, report or claim items"],
]
t = Table(role_data, colWidths=[2.5*cm, 8*cm, 6.5*cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), PURPLE),
    ("TEXTCOLOR", (0,0), (-1,0), white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("TEXTCOLOR", (0,1), (-1,-1), SLATE_700),
    ("GRID", (0,0), (-1,-1), 0.4, SLATE_200),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [SLATE_50, white]),
    ("TOPPADDING", (0,0), (-1,-1), 7),
    ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ("LEFTPADDING", (0,0), (-1,-1), 8),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
]))
story.append(t)
story.append(Spacer(1, 0.3*cm))

auth_steps = [
    "1. User registers with email + password + role → password hashed (werkzeug) → MongoDB Users collection",
    "2. A random anon_name like User#AB3K7 is auto-generated and stored — used as public display name",
    "3. On login → JWT token created (Flask-JWT-Extended) with user_id + role embedded as claims",
    "4. Token stored in browser localStorage → sent as Authorization: Bearer <token> on every API call",
    "5. Google OAuth: /api/auth/google-login creates/finds user by email → issues JWT identically",
    "6. Password Reset: secure token stored in DB with 1-hour expiry → /reset-password?token=... page",
    "7. Admin routes use a custom @admin_required decorator that validates JWT role claim → 403 if not Admin",
]
for step in auth_steps:
    story.append(Paragraph(step, style_bullet))
story.append(Spacer(1, 0.5*cm))

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5 — MARKETPLACE
# ══════════════════════════════════════════════════════════════════════════════
story.append(section_header("5. Marketplace Flow", "🛒"))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("<b>Tiered Platform Fee Structure:</b>", style_h3))
fee_data = [
    ["Category / Price Range", "Platform Fee", "Rationale"],
    ["Books", "3%", "Encourage affordable textbook exchange"],
    ["Electronics", "12%", "High-value items justify higher fee"],
    ["Other — Price ≤ ₹2,000", "5%", "Low-value items, keep fee minimal"],
    ["Other — ₹2,001 to ₹5,000", "8%", "Mid-range fee"],
    ["Other — Price > ₹5,000", "10%", "High-value warrants higher cut"],
]
t = Table(fee_data, colWidths=[6*cm, 3*cm, 8*cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), EMERALD),
    ("TEXTCOLOR", (0,0), (-1,0), white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("TEXTCOLOR", (0,1), (-1,-1), SLATE_700),
    ("GRID", (0,0), (-1,-1), 0.4, SLATE_200),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [EMERALD_LT, white]),
    ("TOPPADDING", (0,0), (-1,-1), 7),
    ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ("LEFTPADDING", (0,0), (-1,-1), 8),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
]))
story.append(t)
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("<b>Buy Flow (Step by Step):</b>", style_h3))
buy_steps = [
    "1. Buyer clicks 'Buy' → POST /api/marketplace/buy/<item_id> (JWT required)",
    "2. Backend checks: role ≠ Admin, item status = Available, buyer ≠ seller",
    "3. calculate_marketplace_fee(price, category) → platform fee computed",
    "4. Stripe Checkout Session created → URL returned to frontend",
    "5. User completes payment on Stripe → redirected back to /marketplace?success=true&session_id=...",
    "6. Frontend calls backend again with session_id → backend verifies with Stripe API",
    "7. Transaction saved to MongoDB Transactions collection → item status updated to 'Sold'",
    "8. Payment record saved to Payments collection (for admin revenue tracking)",
]
for step in buy_steps:
    story.append(Paragraph(step, style_bullet))
story.append(Spacer(1, 0.5*cm))

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6 — LOST & FOUND + AI
# ══════════════════════════════════════════════════════════════════════════════
story.append(PageBreak())
story.append(section_header("6. Lost & Found + AI Smart Matching", "🔍"))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("<b>The Smart Matching Algorithm:</b>", style_h3))
story.append(Paragraph(
    "When a 'lost' report is submitted, the backend immediately scans every open 'found' report "
    "and scores each one using a multi-signal algorithm:",
    style_body))
story.append(Spacer(1, 0.2*cm))

ai_data = [
    ["Signal", "Method", "Weight (with images)", "Weight (text only)"],
    ["Text Similarity", "TF-IDF Cosine Similarity", "40%", "70%"],
    ["Image Similarity", "OpenCV (Histogram + ORB + SSIM)", "35%", "0% (skipped)"],
    ["Category Bonus", "+0.15 if same category", "Part of 25%", "Part of 30%"],
    ["Name Bonus", "+0.20 if name substring matches", "Part of 25%", "Part of 30%"],
    ["Match Threshold", "Combined score > 0.25 = shown as match", "0.25", "0.25"],
]
t = Table(ai_data, colWidths=[3.5*cm, 5.5*cm, 4*cm, 4*cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), PURPLE),
    ("TEXTCOLOR", (0,0), (-1,0), white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
    ("FONTSIZE", (0,0), (-1,-1), 8.5),
    ("TEXTCOLOR", (0,1), (-1,-1), SLATE_700),
    ("GRID", (0,0), (-1,-1), 0.4, SLATE_200),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [SLATE_50, white]),
    ("TOPPADDING", (0,0), (-1,-1), 7),
    ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ("LEFTPADDING", (0,0), (-1,-1), 8),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
]))
story.append(t)
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("<b>What TF-IDF Cosine Similarity Does (Plain English):</b>", style_h3))
tfidf_points = [
    "Splits both descriptions into individual words and counts their frequencies",
    "Builds a mathematical 'vector' (arrow in space) for each report",
    "Measures the angle between the two vectors — small angle = similar items",
    "Score range: 0.0 (nothing in common) to 1.0 (identical descriptions)",
    "Example: 'blue leather wallet near library' vs 'found blue wallet near library cafe' → Score ~0.72",
]
for pt in tfidf_points:
    story.append(Paragraph(pt, style_bullet))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph("<b>What OpenCV Image Similarity Does:</b>", style_h3))
img_data = [
    ["Method", "How It Works", "Weight"],
    ["Color Histogram", "Compares color distribution across the image (HSV color space)", "40%"],
    ["ORB Feature Matching", "Detects edges & corners, compares keypoint 'fingerprints' across photos", "35%"],
    ["Structural Similarity", "Resizes both to 128×128, compares pixel-by-pixel difference", "25%"],
]
t = Table(img_data, colWidths=[4*cm, 9*cm, 4*cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), INDIGO),
    ("TEXTCOLOR", (0,0), (-1,0), white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
    ("FONTSIZE", (0,0), (-1,-1), 9),
    ("TEXTCOLOR", (0,1), (-1,-1), SLATE_700),
    ("GRID", (0,0), (-1,-1), 0.4, SLATE_200),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [SLATE_50, white]),
    ("TOPPADDING", (0,0), (-1,-1), 7),
    ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ("LEFTPADDING", (0,0), (-1,-1), 8),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
]))
story.append(t)
story.append(Spacer(1, 0.5*cm))

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 7 — FINDER REWARD SYSTEM
# ══════════════════════════════════════════════════════════════════════════════
story.append(section_header("7. Finder Reward System", "🎁"))
story.append(Spacer(1, 0.3*cm))
story.append(info_box(
    "KEY DESIGN DECISION: The platform charges ZERO fees on Lost & Found. "
    "Instead, the item owner voluntarily offers a 'Thank You Reward' to the finder. "
    "100% of the reward goes to the finder. Platform takes nothing.",
    color=EMERALD_LT, text_color=EMERALD))
story.append(Spacer(1, 0.3*cm))

reward_steps = [
    "1. Finder reports 'Found: Blue Wallet at Library' → stored in Reports collection as type='found'",
    "2. Owner sees the AI-matched report → clicks 'Claim This Item'",
    "3. Claim modal shows green reward banner: 'Platform charges zero fees'",
    "4. Owner fills: proof of ownership (description) + optional reward amount (e.g. ₹50)",
    "5. Claim saved: { claimer_id, finder_id, reward_amount: 50, status: 'Pending' }",
    "6. Admin reviews verification details → clicks Approve",
    "7. Backend records: { type: 'finder_reward', from: owner, to: finder, amount: 50, platform_fee: 0 }",
    "8. Report status → 'Resolved' | Claim status → 'Approved' | reward_paid → true",
]
for step in reward_steps:
    story.append(Paragraph(step, style_bullet))
story.append(Spacer(1, 0.5*cm))

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 8 — ADMIN DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
story.append(section_header("8. Admin Dashboard", "🛡️"))
story.append(Spacer(1, 0.3*cm))

admin_data = [
    ["Admin Capability", "Endpoint", "Action"],
    ["View platform stats", "GET /api/admin/dashboard", "Users, revenue, items, claims aggregate"],
    ["View all transactions", "GET /api/admin/transactions", "Enriched with buyer/seller real names"],
    ["View marketplace items", "GET /api/admin/marketplace", "All listings with seller info"],
    ["Delete marketplace item", "DELETE /api/admin/marketplace/<id>", "Remove inappropriate listing"],
    ["View L&F reports", "GET /api/admin/lost-and-found", "All reports with reporter info"],
    ["Delete L&F report", "DELETE /api/admin/lost-and-found/<id>", "Remove spam reports"],
    ["View all claims", "GET /api/admin/claims", "With finder + claimer + reward info"],
    ["Approve/Reject claim", "POST /api/admin/claims/<id>/verify", "Triggers reward recording on approve"],
]
t = Table(admin_data, colWidths=[4.5*cm, 5.5*cm, 7*cm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), AMBER),
    ("TEXTCOLOR", (0,0), (-1,0), white),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTNAME", (0,1), (-1,-1), "Helvetica"),
    ("FONTSIZE", (0,0), (-1,-1), 8.5),
    ("TEXTCOLOR", (0,1), (-1,-1), SLATE_700),
    ("GRID", (0,0), (-1,-1), 0.4, SLATE_200),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [AMBER_LT, white]),
    ("TOPPADDING", (0,0), (-1,-1), 6),
    ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ("LEFTPADDING", (0,0), (-1,-1), 8),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
]))
story.append(t)
story.append(Spacer(1, 0.5*cm))

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 9 — MONGODB COLLECTIONS
# ══════════════════════════════════════════════════════════════════════════════
story.append(section_header("9. MongoDB Collections (Schema)", "🍃"))
story.append(Spacer(1, 0.3*cm))

db_data = [
    ["Collection", "Key Fields"],
    ["Users", "name, email, hashed_password, role, anon_name, google_id, reset_token, reset_token_expiry"],
    ["MarketplaceItems", "title, price, category, seller_id, seller_anon_name, image_url, pickup_location, status (Available/Sold)"],
    ["Transactions", "item_id, buyer_id, seller_id, price, platform_fee, total_amount, status"],
    ["Payments", "type (marketplace_fee / finder_reward), from_user_id, to_user_id, amount, platform_fee, status"],
    ["Reports", "type (lost/found), item_name, category, description, image_url, location, user_id, user_anon_name, status (Open/Resolved)"],
    ["Claims", "found_report_id, claimer_id, finder_id, verification_details, reward_amount, reward_paid, status (Pending/Approved/Rejected)"],
]
story.append(two_col_table(db_data[1:], headers=db_data[0], w1=4.5*cm, w2=12.5*cm))
story.append(Spacer(1, 0.5*cm))

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 10 — KEY DESIGN DECISIONS
# ══════════════════════════════════════════════════════════════════════════════
story.append(section_header("10. Key Design Decisions", "💡"))
story.append(Spacer(1, 0.3*cm))

decisions = [
    ("Full Anonymity by Default",
     "Every user gets User#AB3K7 style anon_name. Real names never shown publicly. "
     "Admin can see real identities for moderation. Prevents social pressure and harassment."),
    ("One Admin Rule",
     "Only one Admin account allowed across the entire platform. Enforced at registration "
     "and Google OAuth. Prevents multiple admins causing conflicting moderation decisions."),
    ("Zero Fee on Lost & Found",
     "Platform earns nothing from Lost & Found. Revenue comes only from Marketplace. "
     "This maximizes participation — if there's a fee, people go back to WhatsApp."),
    ("Finder Reward (not Platform Fee)",
     "The reward for honest finders goes 100% to the finder, not the platform. "
     "This creates the right incentive — honesty is financially rewarded by the community."),
    ("MongoDB over SQL",
     "Items have flexible structures (books vs electronics have different attributes). "
     "MongoDB's schema-less documents fit this better than a rigid SQL schema."),
    ("OpenCV Graceful Fallback",
     "If OpenCV is not installed, image similarity is silently skipped. The system "
     "falls back to text-only matching without crashing. Zero-dependency failure."),
    ("Pickup Location Hidden from Listings",
     "The pickup_location field is deliberately removed from GET /api/marketplace/items response. "
     "This forces buyers to go through the platform rather than arranging off-platform deals."),
    ("Alumni Account Persistence",
     "Alumni keep their accounts after graduation. They can still sell items to juniors. "
     "This creates a network effect — more alumni = richer inventory for incoming students."),
]
for title, desc in decisions:
    story.append(info_box(f"<b>{title}:</b> {desc}", color=BLUE_LIGHT, text_color=SLATE_700))
    story.append(Spacer(1, 0.15*cm))

story.append(Spacer(1, 0.3*cm))

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 11 — 25 Q&A
# ══════════════════════════════════════════════════════════════════════════════
story.append(PageBreak())
story.append(section_header("11. Interview Q&A — 25 Questions with Model Answers", "❓"))
story.append(Spacer(1, 0.4*cm))

qa_list = [
    (
        "Tell me about your project in 30 seconds.",
        [
            "I built CampusConnect — a full-stack web platform that solves two interconnected campus problems.",
            "First: Lost items on campus never get returned efficiently — WhatsApp messages get buried. "
            "I solved this with an AI matching engine using TF-IDF text similarity and OpenCV image comparison.",
            "Second: There is no trusted marketplace connecting Alumni (who have textbooks, laptops, equipment) "
            "with Students who need them. I built a closed, payment-integrated campus marketplace using Stripe.",
            "Backend: Python Flask + MongoDB. Frontend: React. Auth: JWT + Google OAuth. "
            "And the platform charges zero fees on Lost & Found — reward goes directly to honest finders.",
        ]
    ),
    (
        "Why did you choose MongoDB over a SQL database like PostgreSQL?",
        [
            "Marketplace items have flexible, varying attributes. A book listing differs from an "
            "electronics listing. MongoDB's schema-less document model fits this much better than "
            "a rigid SQL table with fixed columns.",
            "Also, Lost & Found reports have optional fields (image, location, date) that vary per report. "
            "MongoDB handles sparse data naturally without NULLs everywhere.",
            ">> Bonus: If heavier relational queries were needed — like joins across users, transactions, "
            "and items — I would have considered PostgreSQL.",
        ]
    ),
    (
        "Why Flask and not Django or Node.js?",
        [
            "Flask is a microframework — I only get what I need, nothing more. Since I was building "
            "a REST API with specific feature modules, I didn't need Django's full ORM and built-in admin.",
            "Flask's Blueprint system let me cleanly separate auth, marketplace, lost-and-found, and admin "
            "into independent modules — making the codebase very maintainable.",
            "I chose Python specifically because TF-IDF and OpenCV are Python-native libraries. "
            "Doing AI matching in Node.js would have been significantly harder.",
        ]
    ),
    (
        "How does JWT authentication work in your project?",
        [
            "When a user logs in, credentials are validated against MongoDB's Users collection.",
            "Flask-JWT-Extended generates a JWT token with the user's _id and role embedded as claims.",
            "The token is stored in browser localStorage and sent as Authorization: Bearer <token> on every API call.",
            "The backend decodes and verifies the token, extracts the role, and decides what the user can do.",
            "Admin routes use a custom @admin_required decorator that checks the role claim and returns 403 if it's not Admin.",
        ]
    ),
    (
        "Explain the TF-IDF algorithm used in Lost & Found matching.",
        [
            "TF-IDF stands for Term Frequency-Inverse Document Frequency. In my project, I use a simplified version.",
            "Step 1: Split both lost + found descriptions into words and count their frequencies (word vectors).",
            "Step 2: Find the common words between the two descriptions.",
            "Step 3: Compute cosine similarity — the dot product of the two vectors divided by their magnitudes.",
            "This gives a score between 0.0 (nothing in common) and 1.0 (identical descriptions).",
            ">> Example: 'blue leather wallet near library' vs 'found blue wallet near library cafe' scores ~0.72",
            "Any combined score above 0.25 is shown as a potential match to the user.",
        ]
    ),
    (
        "Explain the OpenCV image similarity used in your project.",
        [
            "I use three complementary OpenCV techniques, each catching different aspects of similarity:",
            "• Color Histogram (40%): Compares the color distribution of both images in HSV color space. "
            "A blue wallet vs a red shoe will have completely different histograms.",
            "• ORB Feature Matching (35%): Detects corners and edges as keypoints, builds descriptors, "
            "and matches them between images. Works even if photos are taken from different angles.",
            "• Structural Similarity (25%): Resizes both images to 128x128 and compares pixel differences. "
            "Near-identical images have near-zero mean difference.",
            "Combined image score threshold is 0.35. The image score then feeds into the final smart match formula.",
        ]
    ),
    (
        "How does the full Smart Matching formula work?",
        [
            "For each found report, I compute text similarity, image similarity (if both have photos), "
            "category bonus (+0.15), and name substring bonus (+0.20).",
            "With images:    Final = Text×0.40 + Image×0.35 + Bonuses×0.25",
            "Without images: Final = Text×0.70 + Bonuses×0.30",
            "The score is clamped to [0.0, 1.0]. Anything above 0.25 is returned as a match.",
            "Matches are sorted by combined_score descending — best match shown first.",
        ]
    ),
    (
        "How does the Stripe payment integration work?",
        [
            "Step 1: Buyer clicks Buy — backend calculates item price + platform fee.",
            "Step 2: Backend creates a Stripe Checkout Session with line items and success/cancel URLs.",
            "Step 3: The session URL (hosted by Stripe) is returned to the frontend.",
            "Step 4: Frontend redirects the user to Stripe's hosted checkout page.",
            "Step 5: After payment, Stripe redirects to: /marketplace?success=true&session_id=...",
            "Step 6: Frontend calls backend again with session_id — backend verifies with stripe.checkout.Session.retrieve().",
            "Step 7: If payment_status == 'paid', transaction is recorded and item marked Sold.",
            ">> In dev mode with mock key, a fake order is returned without touching Stripe at all.",
        ]
    ),
    (
        "What is the platform's business model?",
        [
            "Revenue comes exclusively from the Marketplace module — not from Lost & Found.",
            "• Books: 3% — keeps textbook exchange affordable for students",
            "• Electronics: 12% — higher value items justify a higher platform cut",
            "• Other items: 5% (≤₹2000) / 8% (≤₹5000) / 10% (above ₹5000) — tiered by value",
            "Lost & Found is deliberately kept fee-free. The finder reward (if any) goes 100% to "
            "the finder — the platform earns nothing from it.",
            ">> Philosophy: Marketplace generates revenue. Lost & Found generates community trust.",
        ]
    ),
    (
        "How do you ensure user privacy in the platform?",
        [
            "Every user gets an auto-generated anon_name like User#AB3K7 on registration.",
            "This anon_name is stored in MongoDB and used as the public display name everywhere — "
            "listings, reports, claim information shown to other users.",
            "Real names and emails are stored in the database but never exposed to other regular users.",
            "Only the Admin can see real identities — for moderation, dispute resolution, and claim verification.",
            "This design means: no social pressure if you're selling something cheap, no harassment, "
            "and no one can identify who reported a found item before the claim is approved.",
        ]
    ),
    (
        "How does role-based access control work?",
        [
            "JWT tokens include the user's role as a custom claim when generated at login.",
            "The @admin_required decorator (in admin_routes.py) wraps every admin endpoint. "
            "It calls get_jwt() to extract the role and returns 403 Forbidden if it's not 'Admin'.",
            "On the frontend, App.jsx reads the role from localStorage and conditionally renders "
            "the Admin nav link and hides Buy/Report buttons for Admin users.",
            "Both layers are necessary — the frontend hides UI, but the backend enforces security. "
            "Malicious users bypassing the UI would still get 403 from the backend.",
        ]
    ),
    (
        "What was the most challenging technical problem you faced?",
        [
            "Three stood out:",
            "• MongoDB ObjectId serialization: Flask's default JSON encoder doesn't handle MongoDB's ObjectId "
            "type. I wrote a CustomJSONProvider class that extends DefaultJSONProvider and converts "
            "ObjectId to string and datetime to ISO format automatically.",
            "• OpenCV graceful fallback: OpenCV is a heavy dependency. I wrapped all image similarity "
            "calls in a compute_image_similarity_safe() function using try-except. If OpenCV isn't installed, "
            "the function returns None and the algorithm skips image scoring silently.",
            "• Dual-layer access control: Enforcing that Admin can't post/buy/claim at both the API level "
            "AND the UI level required careful coordination between backend JWT claims and frontend state.",
        ]
    ),
    (
        "Why does the Lost & Found module have zero platform fee?",
        [
            "Two reasons — ethical and strategic.",
            "Ethically: Someone losing their wallet is already distressed. Charging them a fee to reclaim "
            "it feels extractive and wrong. The platform shouldn't profit from misfortune.",
            "Strategically: Any friction in the Lost & Found flow sends users back to WhatsApp. "
            "Zero fee maximizes participation, which means a larger pool of found reports, "
            "which makes the AI matching engine more effective.",
            "Revenue comes from the Marketplace, not from people's losses.",
        ]
    ),
    (
        "Why does the reward go to the finder and not the platform?",
        [
            "It's an incentive alignment problem.",
            "If there's no reward, finders have no motivation to report honestly — they might keep the item.",
            "If the platform keeps the fee, it creates the wrong incentive — the platform profits from lost items.",
            "By routing the reward 100% to the finder, honest behavior is directly rewarded by the "
            "person who benefits from it — the owner who gets their item back.",
            ">> This is also a strong differentiator: 'We don't charge fees on community kindness.'",
        ]
    ),
    (
        "How is the Admin dashboard protected from regular users?",
        [
            "Backend protection: Every admin route uses the @admin_required decorator which extracts "
            "the JWT role claim. If role != 'Admin', it returns 403 Forbidden.",
            "Frontend protection: The Admin nav link only renders when user.role === 'Admin' in localStorage. "
            "The /admin route renders AdminDashboard component which internally checks role.",
            "Database-level protection: Only one Admin account can exist — enforced during registration "
            "with a MongoDB query: find_one({'role': {'$regex': '^admin$', '$options': 'i'}}).",
        ]
    ),
    (
        "What makes your marketplace different from OLX or Quikr?",
        [
            "• Closed ecosystem: Only verified campus members. No random strangers, no scammers.",
            "• Real payment integration: Stripe handles actual money transfer. OLX is cash on delivery.",
            "• Admin moderation: Disputes resolved internally. OLX has zero dispute mechanism.",
            "• Full anonymity: Seller shown as User#AB3K7, not their real name. OLX shows your phone number to everyone.",
            "• Alumni persistence: Alumni accounts survive graduation, maintaining supply for incoming students.",
            "• Lost & Found built-in: OLX has no concept of this. CampusConnect handles the full campus lifecycle.",
        ]
    ),
    (
        "What is the go-to-market strategy if you launched this for real?",
        [
            "Phase 1 — Seeding: Manually recruit 20-30 people (friends, seniors) to create early listings. "
            "An empty marketplace is dead.",
            "Phase 2 — Orientation Day: Pitch to freshers: 'Your seniors listed textbooks for ₹50-200 "
            "that cost ₹600 new. Register here.' Immediate value.",
            "Phase 3 — Farewell Season: Approach passing-out students: 'Don't dump your stuff. List on "
            "CampusConnect — your juniors need it.' Emotional + practical appeal.",
            "• LinkedIn for Alumni outreach — they've left WhatsApp groups",
            "• Campus notice boards with QR codes linking to the platform",
            "• College fest demos — show the AI matching live",
            ">> The network effect: More Alumni = richer inventory = more freshers join = more Alumni list next year.",
        ]
    ),
    (
        "How would you handle the objection that students prefer eBooks now?",
        [
            "I'd acknowledge it honestly: eBook adoption is real for standard textbooks.",
            "But books are one category out of many. Alumni also sell laptops, cycles, hostel furniture, "
            "scientific calculators, headphones, lab equipment — none of which has a digital equivalent.",
            "Interestingly, the shift to eBooks increases electronics transactions on the platform — "
            "students now sell tablets and Kindles to their juniors instead of books.",
            ">> The underlying problem — Alumni have things, juniors need them, no trusted closed channel "
            "exists — doesn't go away because of eBooks. It just shifts categories.",
        ]
    ),
    (
        "How would you scale this application for a real deployment?",
        [
            "• Image storage: Move from local /uploads/ to AWS S3 or Cloudinary for CDN delivery",
            "• Backend scaling: Run Flask behind Gunicorn with 4-8 workers behind an Nginx reverse proxy",
            "• Database: Add MongoDB indexes on status, seller_id, type, created_at for faster queries",
            "• Caching: Use Redis to cache frequently-accessed data like homepage listings (TTL: 60s)",
            "• Matching optimization: Pre-compute similarity scores in background Celery jobs "
            "instead of synchronously on every report submission",
            "• Real email service: Replace debug print() for password reset with SendGrid/AWS SES",
        ]
    ),
    (
        "Why did you not use a full ML library like scikit-learn for TF-IDF?",
        [
            "The campus dataset is small — a few hundred reports at most. A full scikit-learn "
            "TfidfVectorizer needs to refit every time a new document is added, adding complexity.",
            "My manual cosine similarity with word-frequency Counter gives adequate results for this "
            "scale with zero additional dependencies.",
            ">> If this scaled to a national multi-campus platform with millions of reports, I'd "
            "switch to scikit-learn's TfidfVectorizer with pre-fitted IDF weights stored in a cache.",
        ]
    ),
    (
        "What is the anon_name system and why is it important?",
        [
            "On registration, every user gets an auto-generated anon_name like User#AB3K7.",
            "This is stored in MongoDB alongside the real name and email.",
            "All public-facing APIs (marketplace items, L&F reports, claim info shown to users) use anon_name.",
            "The JWT login response returns anon_name as the display name — so even on the navbar, "
            "you see your anonymous identity, not your real name.",
            "This is important because: on a small campus, everyone knows each other. Anonymity "
            "prevents social dynamics from affecting who reports items, who claims them, or who buys "
            "from whom at what price.",
        ]
    ),
    (
        "How does CORS work in your application?",
        [
            "CORS (Cross-Origin Resource Sharing) is a browser security policy that blocks requests "
            "from one origin (localhost:5173) to another (localhost:5000) by default.",
            "I configured Flask-CORS to only allow requests from http://localhost:5173 (the React dev server).",
            "The CORS config also allows the Authorization and Content-Type headers to pass through, "
            "which are needed for JWT token sending and JSON body parsing.",
            "In production, localhost:5173 would be replaced with the actual deployed frontend domain.",
        ]
    ),
    (
        "What happens if a user tries to buy their own listing?",
        [
            "The backend explicitly checks this in the buy_item() route:",
            "It compares str(item.get('seller_id')) with str(buyer_id) — if they match, "
            "it returns 400: 'You cannot buy your own item'.",
            "This check happens before any Stripe session is created, so no payment is initiated.",
            "The frontend also hides the Buy button for items the current user posted (by comparing seller_id).",
        ]
    ),
    (
        "How do you handle file/image uploads?",
        [
            "Frontend: The report/listing forms use multipart/form-data with an <input type='file'> field.",
            "Backend: Flask reads the file from request.files['image'] using werkzeug's secure_filename().",
            "The filename is prefixed with a UTC timestamp to prevent collisions: "
            "1714000000.0_wallet.jpg",
            "Files are saved to backend/uploads/ directory, which is created on startup if it doesn't exist.",
            "Flask serves these files via a dedicated route: GET /uploads/<filename> using send_from_directory().",
            "Image URL stored in MongoDB: http://localhost:5000/uploads/1714000000.0_wallet.jpg",
        ]
    ),
    (
        "What features would you add next if you had more time?",
        [
            "• In-app anonymous chat between buyer and seller (using anon_name identities)",
            "• Item condition badge: New / Like New / Good / Fair / Poor on listings",
            "• Campus Zone filter: 'Show items near Hostel Block A' or 'Library Area'",
            "• Wishlist with price drop notifications: 'Notify me when Data Structures book < ₹200'",
            "• Seller reputation score: aggregate rating from completed transactions (reviews_routes.py already exists)",
            "• Bundle deals: 'Selling all 3rd year CSE books as a lot for ₹800'",
            "• Item Swap option: 'Open to Exchange' — no money, peer-to-peer swap",
            "• Real email notifications via SendGrid for claim approvals and match alerts",
        ]
    ),
]

for i, (q, a_lines) in enumerate(qa_list, 1):
    story.append(qa_block(i, q, a_lines))

# ══════════════════════════════════════════════════════════════════════════════
# QUICK REFERENCE CHEAT SHEET
# ══════════════════════════════════════════════════════════════════════════════
story.append(PageBreak())
story.append(section_header("Quick Reference Cheat Sheet", "⚡"))
story.append(Spacer(1, 0.3*cm))

cheat_data = [
    ["Key", "Value"],
    ["Modules", "Lost & Found (AI matching) + Marketplace (Stripe payments)"],
    ["Roles", "Student / Alumni → use platform | Admin → moderate only"],
    ["Backend", "Python Flask + 5 Blueprints + Flask-JWT-Extended + PyMongo"],
    ["Frontend", "React + Vite + Tailwind CSS + React Router + Lucide Icons"],
    ["Database", "MongoDB Atlas — 6 collections (Users, MarketplaceItems, Reports, Claims, Transactions, Payments)"],
    ["Auth", "JWT (role claim embedded) + Google OAuth 2.0 + Password Reset (1hr token)"],
    ["Payments", "Stripe Checkout — tiered fee: Books 3%, Electronics 12%, Others 5/8/10%"],
    ["AI — Text", "TF-IDF Cosine Similarity (manual implementation with Counter)"],
    ["AI — Image", "OpenCV: Color Histogram (40%) + ORB Features (35%) + Structural (25%)"],
    ["Match Threshold", "Combined score > 0.25 → shown as potential match"],
    ["L&F Fee", "ZERO — platform earns nothing from Lost & Found"],
    ["Finder Reward", "100% to finder — owner voluntarily sets amount, platform_fee = 0"],
    ["Privacy", "Public name = anon_name (User#AB3K7), real name only seen by Admin"],
    ["One Admin Rule", "Only one Admin account allowed — enforced at registration + Google OAuth"],
    ["CORS", "Allowed origin: http://localhost:5173 only"],
    ["File Uploads", "Saved to backend/uploads/, served via GET /uploads/<filename>"],
]
story.append(two_col_table(cheat_data[1:], headers=cheat_data[0], w1=4*cm, w2=13*cm))
story.append(Spacer(1, 0.5*cm))

# Practice pitch
pitch_tbl = Table([[
    Paragraph(
        "<b>🎤 Practice This Pitch Out Loud Tonight:</b><br/><br/>"
        '"CampusConnect is a full-stack campus platform solving two problems. '
        'First, the Lost &amp; Found module uses AI — TF-IDF cosine similarity for text and '
        'OpenCV image comparison — to automatically match lost items with found items. '
        'When you report a lost wallet, the system instantly scans all open found reports '
        'and ranks matches. The finder gets rewarded by the owner — platform charges zero. '
        'Second, the Marketplace connects Alumni who are leaving with Students who need '
        'affordable goods — a closed, trusted, Stripe-integrated campus exchange. '
        'Backend: Python Flask. Database: MongoDB Atlas. Frontend: React. '
        'Auth: JWT + Google OAuth. Together, these two modules serve a student '
        'from day one to graduation day."',
        S("P", fontSize=10, fontName="Helvetica", textColor=white, leading=16, alignment=TA_JUSTIFY))
]], colWidths=[17*cm])
pitch_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), SLATE_900),
    ("TOPPADDING", (0,0), (-1,-1), 16),
    ("BOTTOMPADDING", (0,0), (-1,-1), 16),
    ("LEFTPADDING", (0,0), (-1,-1), 16),
    ("RIGHTPADDING", (0,0), (-1,-1), 16),
    ("ROUNDEDCORNERS", (0,0), (-1,-1), 8),
]))
story.append(pitch_tbl)
story.append(Spacer(1, 0.5*cm))

footer_tbl = Table([[
    Paragraph("Good luck in your interview! You built this — own it. 🚀",
              S("F", fontSize=12, fontName="Helvetica-Bold", textColor=white, alignment=TA_CENTER))
]], colWidths=[17*cm])
footer_tbl.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,-1), BLUE),
    ("TOPPADDING", (0,0), (-1,-1), 14),
    ("BOTTOMPADDING", (0,0), (-1,-1), 14),
    ("ROUNDEDCORNERS", (0,0), (-1,-1), 8),
]))
story.append(footer_tbl)

# ─── Build ────────────────────────────────────────────────────────────────────
doc.build(story)
print(f"✅ PDF generated successfully: {OUTPUT_FILE}")
