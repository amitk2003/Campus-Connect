"""
CampusConnect - Multi-Modal Matching Engine Architecture Diagram Generator
Generates a high-resolution presentation graphic (PNG) using Pillow.
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Create 1600x1050 high-res image
WIDTH = 1600
HEIGHT = 1050
BG_COLOR = (15, 23, 42)  # Dark slate background #0F172A

img = Image.new("RGBA", (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

# Try loading standard system fonts or default
try:
    font_title = ImageFont.truetype("arialbd.ttf", 36)
    font_subtitle = ImageFont.truetype("arial.ttf", 20)
    font_card_title = ImageFont.truetype("arialbd.ttf", 22)
    font_card_sub = ImageFont.truetype("arialbd.ttf", 16)
    font_body = ImageFont.truetype("arial.ttf", 15)
    font_badge = ImageFont.truetype("arialbd.ttf", 14)
    font_decision = ImageFont.truetype("arialbd.ttf", 18)
except Exception:
    font_title = ImageFont.load_default()
    font_subtitle = ImageFont.load_default()
    font_card_title = ImageFont.load_default()
    font_card_sub = ImageFont.load_default()
    font_body = ImageFont.load_default()
    font_badge = ImageFont.load_default()
    font_decision = ImageFont.load_default()


def draw_rounded_card(xy, bg_color, border_color, radius=12, border_width=2):
    draw.rounded_rectangle(xy, radius=radius, fill=bg_color, outline=border_color, width=border_width)


def draw_arrow(start, end, color=(148, 163, 184), width=3, arrow_size=10):
    # Draw line
    draw.line([start, end], fill=color, width=width)
    x1, y1 = start
    x2, y2 = end
    
    # Downward arrow
    if y2 > y1 and x1 == x2:
        draw.polygon([(x2 - arrow_size, y2 - arrow_size), (x2 + arrow_size, y2 - arrow_size), (x2, y2)], fill=color)
    elif y2 > y1 and x2 < x1: # Diagonal down-left
        draw.polygon([(x2, y2 - arrow_size*1.5), (x2 + arrow_size*1.5, y2), (x2, y2)], fill=color)
    elif y2 > y1 and x2 > x1: # Diagonal down-right
        draw.polygon([(x2, y2 - arrow_size*1.5), (x2 - arrow_size*1.5, y2), (x2, y2)], fill=color)
    elif x2 > x1: # Right arrow
        draw.polygon([(x2 - arrow_size, y2 - arrow_size), (x2 - arrow_size, y2 + arrow_size), (x2, y2)], fill=color)


# ─── 1. HEADER SECTION ────────────────────────────────────────────────────────
draw.text((WIDTH//2, 45), "CampusConnect: Multi-Modal Smart Matching Engine", fill=(255, 255, 255), font=font_title, anchor="mm")
draw.text((WIDTH//2, 85), "Tri-Signal Intelligent Linking of Lost & Found Items (NLP + Computer Vision + Heuristics)", fill=(148, 163, 184), font=font_subtitle, anchor="mm")

# ─── 2. INPUT CARD (TOP CENTER) ───────────────────────────────────────────────
input_w = 460
input_h = 130
input_x1 = (WIDTH - input_w) // 2
input_y1 = 130
input_x2 = input_x1 + input_w
input_y2 = input_y1 + input_h

draw_rounded_card((input_x1, input_y1, input_x2, input_y2), (30, 41, 59), (59, 130, 246), radius=14, border_width=2)
# Badge
draw.rounded_rectangle((input_x1 + 20, input_y1 + 15, input_x1 + 170, input_y1 + 42), radius=6, fill=(37, 99, 235))
draw.text((input_x1 + 95, input_y1 + 28), "NEW LOST REPORT", fill=(255, 255, 255), font=font_badge, anchor="mm")
# Content
draw.text((input_x1 + 25, input_y1 + 55), "• Title & Description Text", fill=(226, 232, 240), font=font_body)
draw.text((input_x1 + 25, input_y1 + 78), "• Uploaded Photo (Image URL)", fill=(226, 232, 240), font=font_body)
draw.text((input_x1 + 25, input_y1 + 101), "• Category (Electronics, Books, Personal...)", fill=(226, 232, 240), font=font_body)

# Connection lines from Input to 3 signals
center_bottom_input = (WIDTH // 2, input_y2)
split_y = 310

draw.line([center_bottom_input, (WIDTH // 2, split_y)], fill=(96, 165, 250), width=3)
draw.line([(275, split_y), (1325, split_y)], fill=(96, 165, 250), width=3)

draw_arrow((275, split_y), (275, 360), color=(96, 165, 250))
draw_arrow((WIDTH // 2, split_y), (WIDTH // 2, 360), color=(96, 165, 250))
draw_arrow((1325, split_y), (1325, 360), color=(96, 165, 250))

# ─── 3. THREE SIGNAL PILLARS (MIDDLE ROW) ─────────────────────────────────────
card_w = 420
card_h = 240
card_y1 = 360
card_y2 = card_y1 + card_h

# ── Card 1: TF-IDF Text Similarity (Left) ──
c1_x1 = 65
c1_x2 = c1_x1 + card_w
draw_rounded_card((c1_x1, card_y1, c1_x2, card_y2), (30, 41, 59), (99, 102, 241), radius=14, border_width=2)

draw.rounded_rectangle((c1_x1 + 20, card_y1 + 15, c1_x1 + 250, card_y1 + 45), radius=6, fill=(79, 70, 229))
draw.text((c1_x1 + 135, card_y1 + 30), "TF-IDF TEXT SIMILARITY", fill=(255, 255, 255), font=font_badge, anchor="mm")

draw.rounded_rectangle((c1_x2 - 120, card_y1 + 15, c1_x2 - 20, card_y1 + 45), radius=6, fill=(49, 46, 129))
draw.text((c1_x2 - 70, card_y1 + 30), "Weight: 40%", fill=(165, 180, 252), font=font_card_sub, anchor="mm")

draw.text((c1_x1 + 25, card_y1 + 65), "1. Tokenize & Stop-Word Filtering", fill=(226, 232, 240), font=font_body)
draw.text((c1_x1 + 40, card_y1 + 88), "Strips noise: 'lost', 'found', 'near', 'at'", fill=(148, 163, 184), font=font_body)
draw.text((c1_x1 + 25, card_y1 + 115), "2. Normalized Term Frequency (TF)", fill=(226, 232, 240), font=font_body)
draw.text((c1_x1 + 40, card_y1 + 138), "TF(t, d) = count(t, d) / total_words", fill=(148, 163, 184), font=font_body)
draw.text((c1_x1 + 25, card_y1 + 165), "3. Smooth IDF & Cosine Angle", fill=(226, 232, 240), font=font_body)
draw.text((c1_x1 + 40, card_y1 + 188), "IDF = ln((1+N)/(1+df)) + 1.0", fill=(148, 163, 184), font=font_body)
draw.text((c1_x1 + 40, card_y1 + 210), "Cosine = (V1 · V2) / (||V1|| × ||V2||)", fill=(129, 140, 248), font=font_body)


# ── Card 2: OpenCV 3-Way Image Similarity (Center) ──
c2_x1 = (WIDTH - card_w) // 2
c2_x2 = c2_x1 + card_w
draw_rounded_card((c2_x1, card_y1, c2_x2, card_y2), (30, 41, 59), (168, 85, 247), radius=14, border_width=2)

draw.rounded_rectangle((c2_x1 + 20, card_y1 + 15, c2_x1 + 250, card_y1 + 45), radius=6, fill=(147, 51, 234))
draw.text((c2_x1 + 135, card_y1 + 30), "OPENCV 3-WAY VISION", fill=(255, 255, 255), font=font_badge, anchor="mm")

draw.rounded_rectangle((c2_x2 - 120, card_y1 + 15, c2_x2 - 20, card_y1 + 45), radius=6, fill=(88, 28, 135))
draw.text((c2_x2 - 70, card_y1 + 30), "Weight: 35%", fill=(216, 180, 254), font=font_card_sub, anchor="mm")

draw.text((c2_x1 + 25, card_y1 + 65), "1. HSV Color Histogram (40%)", fill=(226, 232, 240), font=font_body)
draw.text((c2_x1 + 40, card_y1 + 88), "Color distribution (lighting invariant)", fill=(148, 163, 184), font=font_body)
draw.text((c2_x1 + 25, card_y1 + 115), "2. ORB Feature Matching (35%)", fill=(226, 232, 240), font=font_body)
draw.text((c2_x1 + 40, card_y1 + 138), "500 keypoints + Lowe's Ratio Test", fill=(148, 163, 184), font=font_body)
draw.text((c2_x1 + 25, card_y1 + 165), "3. Structural SSIM Difference (25%)", fill=(226, 232, 240), font=font_body)
draw.text((c2_x1 + 40, card_y1 + 188), "128x128 grayscale pixel difference", fill=(148, 163, 184), font=font_body)
draw.text((c2_x1 + 40, card_y1 + 210), "Rotation & angle invariant matching", fill=(192, 132, 252), font=font_body)


# ── Card 3: Heuristic Bonuses (Right) ──
c3_x1 = WIDTH - card_w - 65
c3_x2 = c3_x1 + card_w
draw_rounded_card((c3_x1, card_y1, c3_x2, card_y2), (30, 41, 59), (16, 185, 129), radius=14, border_width=2)

draw.rounded_rectangle((c3_x1 + 20, card_y1 + 15, c3_x1 + 250, card_y1 + 45), radius=6, fill=(5, 150, 105))
draw.text((c3_x1 + 135, card_y1 + 30), "HEURISTIC BONUSES", fill=(255, 255, 255), font=font_badge, anchor="mm")

draw.rounded_rectangle((c3_x2 - 120, card_y1 + 15, c3_x2 - 20, card_y1 + 45), radius=6, fill=(6, 78, 59))
draw.text((c3_x2 - 70, card_y1 + 30), "Weight: 25%", fill=(110, 231, 183), font=font_card_sub, anchor="mm")

draw.text((c3_x1 + 25, card_y1 + 65), "1. Category Match Bonus (+0.15)", fill=(226, 232, 240), font=font_body)
draw.text((c3_x1 + 40, card_y1 + 88), "Awarded if category dropdowns match", fill=(148, 163, 184), font=font_body)
draw.text((c3_x1 + 25, card_y1 + 115), "2. Name Substring Bonus (+0.20)", fill=(226, 232, 240), font=font_body)
draw.text((c3_x1 + 40, card_y1 + 138), "Checks if title is contained in found title", fill=(148, 163, 184), font=font_body)
draw.text((c3_x1 + 25, card_y1 + 165), "3. Short Query Rescue", fill=(226, 232, 240), font=font_body)
draw.text((c3_x1 + 40, card_y1 + 188), "Prevents 2-word reports from failing", fill=(148, 163, 184), font=font_body)
draw.text((c3_x1 + 40, card_y1 + 210), "Normalized: (Cat + Name)/0.35 × 0.25", fill=(52, 211, 153), font=font_body)


# ─── 4. FUSION & COMBINED SCORE CARD (BOTTOM CENTER) ──────────────────────────
merge_y = 650
draw.line([(275, card_y2), (275, merge_y)], fill=(148, 163, 184), width=3)
draw.line([(WIDTH // 2, card_y2), (WIDTH // 2, merge_y)], fill=(148, 163, 184), width=3)
draw.line([(1325, card_y2), (1325, merge_y)], fill=(148, 163, 184), width=3)

draw.line([(275, merge_y), (1325, merge_y)], fill=(148, 163, 184), width=3)
draw_arrow((WIDTH // 2, merge_y), (WIDTH // 2, 700), color=(148, 163, 184))

comb_w = 600
comb_h = 100
comb_x1 = (WIDTH - comb_w) // 2
comb_y1 = 700
comb_x2 = comb_x1 + comb_w
comb_y2 = comb_y1 + comb_h

draw_rounded_card((comb_x1, comb_y1, comb_x2, comb_y2), (30, 41, 59), (245, 158, 11), radius=14, border_width=2)
draw.text((WIDTH // 2, comb_y1 + 30), "COMBINED MATCH SCORE: [0.0 - 1.0]", fill=(251, 191, 36), font=font_card_title, anchor="mm")
draw.text((WIDTH // 2, comb_y1 + 65), "Score = (Text × 0.40) + (Image × 0.35) + (Bonuses × 0.25)", fill=(226, 232, 240), font=font_body, anchor="mm")


# ─── 5. DECISION GATE & FINAL OUTCOMES (BOTTOM) ───────────────────────────────
draw_arrow((WIDTH // 2, comb_y2), (WIDTH // 2, 850), color=(245, 158, 11), width=3)

# Decision Diamond / Box
dec_w = 340
dec_h = 55
dec_x1 = (WIDTH - dec_w) // 2
dec_y1 = 850
dec_x2 = dec_x1 + dec_w
dec_y2 = dec_y1 + dec_h

draw_rounded_card((dec_x1, dec_y1, dec_x2, dec_y2), (69, 26, 3), (217, 119, 6), radius=10, border_width=2)
draw.text((WIDTH // 2, dec_y1 + 27), "Is Score > 0.25 Threshold?", fill=(254, 215, 170), font=font_decision, anchor="mm")

# Left Arrow -> YES
draw.line([(dec_x1, dec_y1 + dec_h//2), (dec_x1 - 100, dec_y1 + dec_h//2)], fill=(16, 185, 129), width=3)
draw_arrow((dec_x1 - 100, dec_y1 + dec_h//2), (dec_x1 - 100, 950), color=(16, 185, 129))

# Right Arrow -> NO
draw.line([(dec_x2, dec_y1 + dec_h//2), (dec_x2 + 100, dec_y1 + dec_h//2)], fill=(239, 68, 68), width=3)
draw_arrow((dec_x2 + 100, dec_y1 + dec_h//2), (dec_x2 + 100, 950), color=(239, 68, 68))

# Outcome 1: MATCH (Green)
out1_w = 400
out1_h = 65
out1_x1 = dec_x1 - 100 - out1_w//2
out1_y1 = 950
out1_x2 = out1_x1 + out1_w
out1_y2 = out1_y1 + out1_h

draw_rounded_card((out1_x1, out1_y1, out1_x2, out1_y2), (6, 78, 59), (16, 185, 129), radius=10, border_width=2)
draw.text((out1_x1 + out1_w//2, out1_y1 + 22), "YES -> AUTO-LINK & RECOMMEND", fill=(255, 255, 255), font=font_card_sub, anchor="mm")
draw.text((out1_x1 + out1_w//2, out1_y1 + 45), "Surfaces item to owner | +30% Accuracy Gain", fill=(167, 243, 208), font=font_body, anchor="mm")

# Outcome 2: DISCARD (Red)
out2_w = 400
out2_h = 65
out2_x1 = dec_x2 + 100 - out2_w//2
out2_y1 = 950
out2_x2 = out2_x1 + out2_w
out2_y2 = out2_y1 + out2_h

draw_rounded_card((out2_x1, out2_y1, out2_x2, out2_y2), (69, 10, 10), (239, 68, 68), radius=10, border_width=2)
draw.text((out2_x1 + out2_w//2, out2_y1 + 22), "NO -> DISCARD / NO MATCH", fill=(255, 255, 255), font=font_card_sub, anchor="mm")
draw.text((out2_x1 + out2_w//2, out2_y1 + 45), "Prevents false positives & irrelevant spam", fill=(254, 202, 202), font=font_body, anchor="mm")

# Save file
OUTPUT_IMAGE = "matching_engine_architecture.png"
img.save(OUTPUT_IMAGE, "PNG", quality=95)
print(f"[SUCCESS] Saved high-resolution architecture diagram: {OUTPUT_IMAGE}")
