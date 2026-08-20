"""
CampusConnect - MongoDB Schema Architecture Diagram Generator
Generates a high-resolution presentation graphic (PNG) using Pillow.
"""

from PIL import Image, ImageDraw, ImageFont
import os

WIDTH = 1650
HEIGHT = 1150
BG_COLOR = (15, 23, 42)  # Dark slate background #0F172A

img = Image.new("RGBA", (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

try:
    font_title = ImageFont.truetype("arialbd.ttf", 36)
    font_subtitle = ImageFont.truetype("arial.ttf", 20)
    font_card_title = ImageFont.truetype("arialbd.ttf", 20)
    font_card_sub = ImageFont.truetype("arialbd.ttf", 15)
    font_body = ImageFont.truetype("arial.ttf", 14)
    font_field = ImageFont.truetype("arialbd.ttf", 13)
    font_badge = ImageFont.truetype("arialbd.ttf", 13)
    font_annot = ImageFont.truetype("arial.ttf", 13)
except Exception:
    font_title = ImageFont.load_default()
    font_subtitle = ImageFont.load_default()
    font_card_title = ImageFont.load_default()
    font_card_sub = ImageFont.load_default()
    font_body = ImageFont.load_default()
    font_field = ImageFont.load_default()
    font_badge = ImageFont.load_default()
    font_annot = ImageFont.load_default()


def draw_rounded_card(xy, bg_color, border_color, radius=12, border_width=2):
    draw.rounded_rectangle(xy, radius=radius, fill=bg_color, outline=border_color, width=border_width)


def draw_arrow(start, end, color=(148, 163, 184), width=3, arrow_size=9):
    draw.line([start, end], fill=color, width=width)
    x1, y1 = start
    x2, y2 = end
    
    # Downward
    if y2 > y1 and x1 == x2:
        draw.polygon([(x2 - arrow_size, y2 - arrow_size*1.3), (x2 + arrow_size, y2 - arrow_size*1.3), (x2, y2)], fill=color)
    elif y2 > y1 and x2 < x1: # Diagonal down-left
        draw.polygon([(x2, y2 - arrow_size*1.4), (x2 + arrow_size*1.4, y2), (x2, y2)], fill=color)
    elif y2 > y1 and x2 > x1: # Diagonal down-right
        draw.polygon([(x2, y2 - arrow_size*1.4), (x2 - arrow_size*1.4, y2), (x2, y2)], fill=color)
    elif x2 > x1: # Right
        draw.polygon([(x2 - arrow_size*1.3, y2 - arrow_size), (x2 - arrow_size*1.3, y2 + arrow_size), (x2, y2)], fill=color)


# ─── 1. HEADER SECTION ────────────────────────────────────────────────────────
draw.text((WIDTH//2, 40), "CampusConnect: MongoDB Schema Architecture", fill=(255, 255, 255), font=font_title, anchor="mm")
draw.text((WIDTH//2, 78), "Hybrid Denormalized NoSQL Design (Privacy Isolation, O(1) Zero-Join Feeds, Immutable Ledgers)", fill=(148, 163, 184), font=font_subtitle, anchor="mm")


# ─── 2. TOP NODE: USERS COLLECTION ────────────────────────────────────────────
u_w = 460
u_h = 160
u_x1 = (WIDTH - u_w) // 2
u_y1 = 115
u_x2 = u_x1 + u_w
u_y2 = u_y1 + u_h

draw_rounded_card((u_x1, u_y1, u_x2, u_y2), (30, 41, 59), (59, 130, 246), radius=14, border_width=2)
# Badge
draw.rounded_rectangle((u_x1 + 18, u_y1 + 14, u_x1 + 190, u_y1 + 40), radius=6, fill=(37, 99, 235))
draw.text((u_x1 + 104, u_y1 + 27), "COLLECTION: Users", fill=(255, 255, 255), font=font_badge, anchor="mm")

draw.rounded_rectangle((u_x2 - 190, u_y1 + 14, u_x2 - 18, u_y1 + 40), radius=6, fill=(29, 78, 216))
draw.text((u_x2 - 104, u_y1 + 27), "Identity & RBAC Core", fill=(191, 219, 254), font=font_badge, anchor="mm")

# Fields
draw.text((u_x1 + 25, u_y1 + 52), "• _id (ObjectId, Primary Key)", fill=(226, 232, 240), font=font_body)
draw.text((u_x1 + 25, u_y1 + 74), "• name, email (Unique Index), password (Bcrypt)", fill=(226, 232, 240), font=font_body)
draw.text((u_x1 + 25, u_y1 + 96), "• role ('Student' | 'Admin')", fill=(226, 232, 240), font=font_body)
draw.text((u_x1 + 25, u_y1 + 118), "• anon_name (Auto-generated Privacy Alias, e.g. User#AB3K7)", fill=(96, 165, 250), font=font_field)
draw.text((u_x1 + 25, u_y1 + 138), "• created_at, reset_token, reset_token_expiry", fill=(148, 163, 184), font=font_body)


# ─── CONNECTIONS FROM USERS TO MIDDLE TIER ────────────────────────────────────
center_u_bottom = (WIDTH // 2, u_y2)
split_y1 = 310

draw.line([center_u_bottom, (WIDTH // 2, split_y1)], fill=(96, 165, 250), width=3)
draw.line([(280, split_y1), (1370, split_y1)], fill=(96, 165, 250), width=3)

draw_arrow((280, split_y1), (280, 350), color=(96, 165, 250))
draw_arrow((WIDTH // 2, split_y1), (WIDTH // 2, 350), color=(96, 165, 250))
draw_arrow((1370, split_y1), (1370, 350), color=(96, 165, 250))


# ─── 3. MIDDLE TIER (REPORTS, MARKETPLACE, REVIEWS) ───────────────────────────
card_w = 440
card_h = 220
m_y1 = 350
m_y2 = m_y1 + card_h

# ── Collection: Reports (Left) ──
r_x1 = 60
r_x2 = r_x1 + card_w
draw_rounded_card((r_x1, m_y1, r_x2, m_y2), (30, 41, 59), (168, 85, 247), radius=14, border_width=2)

draw.rounded_rectangle((r_x1 + 18, m_y1 + 14, r_x1 + 200, m_y1 + 40), radius=6, fill=(147, 51, 234))
draw.text((r_x1 + 109, m_y1 + 27), "COLLECTION: Reports", fill=(255, 255, 255), font=font_badge, anchor="mm")

draw.rounded_rectangle((r_x2 - 190, m_y1 + 14, r_x2 - 18, m_y1 + 40), radius=6, fill=(88, 28, 135))
draw.text((r_x2 - 104, m_y1 + 27), "Polymorphic Schema", fill=(216, 180, 254), font=font_badge, anchor="mm")

draw.text((r_x1 + 22, m_y1 + 52), "• _id (ObjectId)", fill=(226, 232, 240), font=font_body)
draw.text((r_x1 + 22, m_y1 + 74), "• type ('lost' | 'found') -> Discriminator", fill=(192, 132, 252), font=font_field)
draw.text((r_x1 + 22, m_y1 + 96), "• item_name, category, description", fill=(226, 232, 240), font=font_body)
draw.text((r_x1 + 22, m_y1 + 118), "• image_url, location, created_at", fill=(226, 232, 240), font=font_body)
draw.text((r_x1 + 22, m_y1 + 140), "• user_id (ObjectId Reference -> Users)", fill=(226, 232, 240), font=font_body)
draw.text((r_x1 + 22, m_y1 + 162), "• user_anon_name (Denormalized Alias)", fill=(168, 85, 247), font=font_field)
draw.text((r_x1 + 22, m_y1 + 184), "• status ('Open' | 'Resolved')", fill=(148, 163, 184), font=font_body)


# ── Collection: MarketplaceItems (Center) ──
mp_x1 = (WIDTH - card_w) // 2
mp_x2 = mp_x1 + card_w
draw_rounded_card((mp_x1, m_y1, mp_x2, m_y2), (30, 41, 59), (16, 185, 129), radius=14, border_width=2)

draw.rounded_rectangle((mp_x1 + 18, m_y1 + 14, mp_x1 + 260, m_y1 + 40), radius=6, fill=(5, 150, 105))
draw.text((mp_x1 + 139, m_y1 + 27), "COLLECTION: MarketplaceItems", fill=(255, 255, 255), font=font_badge, anchor="mm")

draw.rounded_rectangle((mp_x2 - 150, m_y1 + 14, mp_x2 - 18, m_y1 + 40), radius=6, fill=(6, 78, 59))
draw.text((mp_x2 - 84, m_y1 + 27), "Product Catalog", fill=(110, 231, 183), font=font_badge, anchor="mm")

draw.text((mp_x1 + 22, m_y1 + 52), "• _id (ObjectId)", fill=(226, 232, 240), font=font_body)
draw.text((mp_x1 + 22, m_y1 + 74), "• title, description, category", fill=(226, 232, 240), font=font_body)
draw.text((mp_x1 + 22, m_y1 + 96), "• price (Float, INR)", fill=(226, 232, 240), font=font_body)
draw.text((mp_x1 + 22, m_y1 + 118), "• image_url, pickup_location", fill=(226, 232, 240), font=font_body)
draw.text((mp_x1 + 22, m_y1 + 140), "• seller_id (ObjectId Reference -> Users)", fill=(226, 232, 240), font=font_body)
draw.text((mp_x1 + 22, m_y1 + 162), "• seller_anon_name (Denormalized Alias)", fill=(52, 211, 153), font=font_field)
draw.text((mp_x1 + 22, m_y1 + 184), "• status ('Available' | 'Sold')", fill=(148, 163, 184), font=font_body)


# ── Collection: Reviews (Right) ──
rv_x1 = WIDTH - card_w - 60
rv_x2 = rv_x1 + card_w
draw_rounded_card((rv_x1, m_y1, rv_x2, m_y2), (30, 41, 59), (245, 158, 11), radius=14, border_width=2)

draw.rounded_rectangle((rv_x1 + 18, m_y1 + 14, rv_x1 + 200, m_y1 + 40), radius=6, fill=(217, 119, 6))
draw.text((rv_x1 + 109, m_y1 + 27), "COLLECTION: Reviews", fill=(255, 255, 255), font=font_badge, anchor="mm")

draw.rounded_rectangle((rv_x2 - 160, m_y1 + 14, rv_x2 - 18, m_y1 + 40), radius=6, fill=(120, 53, 15))
draw.text((rv_x2 - 89, m_y1 + 27), "Campus Trust System", fill=(254, 215, 170), font=font_badge, anchor="mm")

draw.text((rv_x1 + 22, m_y1 + 52), "• _id (ObjectId)", fill=(226, 232, 240), font=font_body)
draw.text((rv_x1 + 22, m_y1 + 74), "• reviewer_id (ObjectId -> Users)", fill=(226, 232, 240), font=font_body)
draw.text((rv_x1 + 22, m_y1 + 96), "• reviewer_anon_name (Denormalized)", fill=(251, 191, 36), font=font_field)
draw.text((rv_x1 + 22, m_y1 + 118), "• target_user_id (Seller / Finder ID)", fill=(226, 232, 240), font=font_body)
draw.text((rv_x1 + 22, m_y1 + 140), "• rating (Integer 1 to 5 Stars)", fill=(226, 232, 240), font=font_body)
draw.text((rv_x1 + 22, m_y1 + 162), "• comment (Feedback text)", fill=(226, 232, 240), font=font_body)
draw.text((rv_x1 + 22, m_y1 + 184), "• created_at (Timestamp)", fill=(148, 163, 184), font=font_body)


# ─── CONNECTIONS FROM MIDDLE TO LOWER TIER ────────────────────────────────────
# Reports -> Claims
draw_arrow((280, m_y2), (280, 630), color=(168, 85, 247))

# Marketplace -> Transactions
draw_arrow((WIDTH // 2, m_y2), (WIDTH // 2, 630), color=(16, 185, 129))


# ─── 4. LOWER TIER (CLAIMS & TRANSACTIONS) ─────────────────────────────────────
l_y1 = 630
l_y2 = l_y1 + card_h

# ── Collection: Claims (Left) ──
draw_rounded_card((r_x1, l_y1, r_x2, l_y2), (30, 41, 59), (236, 72, 153), radius=14, border_width=2)

draw.rounded_rectangle((r_x1 + 18, l_y1 + 14, r_x1 + 190, l_y1 + 40), radius=6, fill=(219, 39, 119))
draw.text((r_x1 + 104, l_y1 + 27), "COLLECTION: Claims", fill=(255, 255, 255), font=font_badge, anchor="mm")

draw.rounded_rectangle((r_x2 - 180, l_y1 + 14, r_x2 - 18, l_y1 + 40), radius=6, fill=(131, 24, 67))
draw.text((r_x2 - 99, l_y1 + 27), "Verification State Machine", fill=(251, 207, 232), font=font_badge, anchor="mm")

draw.text((r_x1 + 22, l_y1 + 52), "• _id (ObjectId)", fill=(226, 232, 240), font=font_body)
draw.text((r_x1 + 22, l_y1 + 74), "• found_report_id (ObjectId -> Reports)", fill=(226, 232, 240), font=font_body)
draw.text((r_x1 + 22, l_y1 + 96), "• claimer_id, finder_id (ObjectIds -> Users)", fill=(226, 232, 240), font=font_body)
draw.text((r_x1 + 22, l_y1 + 118), "• verification_details (Proof of Ownership)", fill=(244, 114, 182), font=font_field)
draw.text((r_x1 + 22, l_y1 + 140), "• reward_amount (Optional Finder Reward, INR)", fill=(226, 232, 240), font=font_body)
draw.text((r_x1 + 22, l_y1 + 162), "• reward_paid (Boolean: True / False)", fill=(226, 232, 240), font=font_body)
draw.text((r_x1 + 22, l_y1 + 184), "• status ('Pending' -> 'Approved' | 'Rejected')", fill=(244, 114, 182), font=font_field)


# ── Collection: Transactions (Center) ──
draw_rounded_card((mp_x1, l_y1, mp_x2, l_y2), (30, 41, 59), (14, 165, 233), radius=14, border_width=2)

draw.rounded_rectangle((mp_x1 + 18, l_y1 + 14, mp_x1 + 240, l_y1 + 40), radius=6, fill=(2, 132, 199))
draw.text((mp_x1 + 129, l_y1 + 27), "COLLECTION: Transactions", fill=(255, 255, 255), font=font_badge, anchor="mm")

draw.rounded_rectangle((mp_x2 - 170, l_y1 + 14, mp_x2 - 18, l_y1 + 40), radius=6, fill=(12, 74, 110))
draw.text((mp_x2 - 94, l_y1 + 27), "Immutable Sales Ledger", fill=(186, 230, 253), font=font_badge, anchor="mm")

draw.text((mp_x1 + 22, l_y1 + 52), "• _id (ObjectId)", fill=(226, 232, 240), font=font_body)
draw.text((mp_x1 + 22, l_y1 + 74), "• item_id (ObjectId -> MarketplaceItems)", fill=(226, 232, 240), font=font_body)
draw.text((mp_x1 + 22, l_y1 + 96), "• buyer_id, seller_id (ObjectIds -> Users)", fill=(226, 232, 240), font=font_body)
draw.text((mp_x1 + 22, l_y1 + 118), "• price, platform_fee (Tiered 3% - 12%)", fill=(56, 189, 248), font=font_field)
draw.text((mp_x1 + 22, l_y1 + 140), "• total_amount = price + platform_fee", fill=(226, 232, 240), font=font_body)
draw.text((mp_x1 + 22, l_y1 + 162), "• stripe_session_id (Payment Gateway ref)", fill=(226, 232, 240), font=font_body)
draw.text((mp_x1 + 22, l_y1 + 184), "• status ('Completed' | 'Pending')", fill=(148, 163, 184), font=font_body)


# ── Annotation Box on Right Side ──
ann_w = card_w
ann_h = card_h
draw_rounded_card((rv_x1, l_y1, rv_x2, l_y2), (15, 23, 42), (71, 85, 105), radius=14, border_width=2)
draw.text((rv_x1 + 20, l_y1 + 25), "KEY ARCHITECTURAL HIGHLIGHTS:", fill=(255, 255, 255), font=font_card_sub)
draw.text((rv_x1 + 20, l_y1 + 55), "1. Zero-Join O(1) Reads:", fill=(96, 165, 250), font=font_field)
draw.text((rv_x1 + 35, l_y1 + 75), "Denormalizes 'anon_name' on items", fill=(148, 163, 184), font=font_annot)
draw.text((rv_x1 + 20, l_y1 + 100), "2. Privacy Isolation:", fill=(168, 85, 247), font=font_field)
draw.text((rv_x1 + 35, l_y1 + 120), "Student PII masked from public feeds", fill=(148, 163, 184), font=font_annot)
draw.text((rv_x1 + 20, l_y1 + 145), "3. Immutable Ledgers:", fill=(52, 211, 153), font=font_field)
draw.text((rv_x1 + 35, l_y1 + 165), "Preserves receipts if item is deleted", fill=(148, 163, 184), font=font_annot)


# ─── 5. BOTTOM TIER: PAYMENTS COLLECTION (CENTER) ─────────────────────────────
pay_y1 = 920
pay_y2 = pay_y1 + 150
pay_w = 620
pay_x1 = (WIDTH - pay_w) // 2
pay_x2 = pay_x1 + pay_w

# Lines from Claims and Transactions to Payments
split_pay_y = 880
draw.line([(280, l_y2), (280, split_pay_y)], fill=(148, 163, 184), width=3)
draw.line([(WIDTH // 2, l_y2), (WIDTH // 2, split_pay_y)], fill=(148, 163, 184), width=3)
draw.line([(280, split_pay_y), (WIDTH // 2, split_pay_y)], fill=(148, 163, 184), width=3)
draw_arrow((WIDTH // 2, split_pay_y), (WIDTH // 2, pay_y1), color=(148, 163, 184))

draw_rounded_card((pay_x1, pay_y1, pay_x2, pay_y2), (30, 41, 59), (234, 179, 8), radius=14, border_width=2)

draw.rounded_rectangle((pay_x1 + 18, pay_y1 + 14, pay_x1 + 240, pay_y1 + 40), radius=6, fill=(202, 138, 4))
draw.text((pay_x1 + 129, pay_y1 + 27), "COLLECTION: Payments", fill=(255, 255, 255), font=font_badge, anchor="mm")

draw.rounded_rectangle((pay_x2 - 250, pay_y1 + 14, pay_x2 - 18, pay_y1 + 40), radius=6, fill=(113, 63, 18))
draw.text((pay_x2 - 134, pay_y1 + 27), "Dual-Stream Financial Audit", fill=(254, 240, 138), font=font_badge, anchor="mm")

draw.text((pay_x1 + 25, pay_y1 + 52), "• _id (ObjectId, Primary Key)", fill=(226, 232, 240), font=font_body)
draw.text((pay_x1 + 25, pay_y1 + 74), "• type ('marketplace_fee' | 'finder_reward') -> Dual Platform Ledger", fill=(250, 204, 21), font=font_field)
draw.text((pay_x1 + 25, pay_y1 + 96), "• from_user_id, to_user_id (ObjectIds -> Users)", fill=(226, 232, 240), font=font_body)
draw.text((pay_x1 + 25, pay_y1 + 118), "• amount, platform_fee (0% on Finder Reward, 3-12% on Marketplace)", fill=(226, 232, 240), font=font_body)
draw.text((pay_x1 + 25, pay_y1 + 136), "• stripe_payment_id, status ('Success'), timestamp", fill=(148, 163, 184), font=font_body)

# Save
OUTPUT_IMAGE = "mongodb_schema_architecture.png"
img.save(OUTPUT_IMAGE, "PNG", quality=95)
print(f"[SUCCESS] Saved high-resolution schema diagram: {OUTPUT_IMAGE}")
