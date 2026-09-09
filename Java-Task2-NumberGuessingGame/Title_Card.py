from PIL import Image, ImageDraw, ImageFont

# 1. Canvas Dimensions (Standard Full HD 1080p)
WIDTH, HEIGHT = 1920, 1080

# 2. Colors (Dark Modern Theme)
BG_COLOR = (18, 22, 34)       # Deep slate navy
CARD_BG = (28, 33, 50)        # Slightly lighter slate
ACCENT_BLUE = (59, 130, 246)  # Electric blue
TEXT_WHITE = (248, 250, 252)  # Crisp white
TEXT_MUTED = (148, 163, 184)  # Muted silver/gray
BORDER_COLOR = (45, 55, 72)

# Create canvas
img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

# 3. Load Fonts
# Uses default fallback if specific OS fonts aren't found
try:
    font_badge = ImageFont.truetype("arialbd.ttf", 26)
    font_title = ImageFont.truetype("arialbd.ttf", 52)
    font_label = ImageFont.truetype("arial.ttf", 34)
    font_value = ImageFont.truetype("arialbd.ttf", 36)
    font_footer = ImageFont.truetype("arial.ttf", 24)
except IOError:
    font_badge = font_title = font_label = font_value = font_footer = ImageFont.load_default()

# 4. Draw Center Container Card
card_x1, card_y1 = 260, 160
card_x2, card_y2 = WIDTH - 260, HEIGHT - 160

draw.rounded_rectangle(
    [(card_x1, card_y1), (card_x2, card_y2)],
    radius=24,
    fill=CARD_BG,
    outline=BORDER_COLOR,
    width=2
)

# 5. Header Section
badge_text = "OASIS INFOBYTE INTERNSHIP PROGRAM (OIBSIP)"
badge_bbox = draw.textbbox((0, 0), badge_text, font=font_badge)
badge_w = badge_bbox[2] - badge_bbox[0]
draw.text(((WIDTH - badge_w) // 2, 230), badge_text, fill=ACCENT_BLUE, font=font_badge)

header_title = "PROJECT DEMONSTRATION"
header_bbox = draw.textbbox((0, 0), header_title, font=font_title)
header_w = header_bbox[2] - header_bbox[0]
draw.text(((WIDTH - header_w) // 2, 280), header_title, fill=TEXT_WHITE, font=font_title)

# Decorative Divider Line
draw.line([(340, 370), (WIDTH - 340, 370)], fill=BORDER_COLOR, width=2)

# 6. Metadata Field Rows
fields = [
    ("Candidate Name :", "Achilles Gautham J B"),
    ("Domain Track   :", "Java Development Track"),
    ("Task Number    :", "Task 2"),
    ("Project Title  :", "Number Guessing Game (Swing GUI)")
]

start_y = 440
line_gap = 85
label_x = 420
value_x = 760

for label, val in fields:
    draw.text((label_x, start_y), label, fill=TEXT_MUTED, font=font_label)
    draw.text((value_x, start_y), val, fill=TEXT_WHITE, font=font_value)
    start_y += line_gap

# 7. Subtle Footer Note
footer_text = "Submission Verification • GitHub: achillespersonal2007-spec/OIBSIP"
footer_bbox = draw.textbbox((0, 0), footer_text, font=font_footer)
footer_w = footer_bbox[2] - footer_bbox[0]
draw.text(((WIDTH - footer_w) // 2, 840), footer_text, fill=TEXT_MUTED, font=font_footer)

# 8. Save Image
output_filename = "task2_title_card.png"
img.save(output_filename, "PNG")
print(f"Title card generated successfully: {output_filename}")