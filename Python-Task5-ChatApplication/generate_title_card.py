from PIL import Image, ImageDraw, ImageFont

# Create high-res 1920x1080 canvas
width, height = 1920, 1080
image = Image.new("RGB", (width, height), "#06090f")
draw = ImageDraw.Draw(image)

# Draw decorative borders
draw.rectangle([(60, 60), (width - 60, height - 60)], outline="#00e5ff", width=4)
draw.rectangle([(80, 80), (width - 80, height - 80)], outline="#112240", width=2)

try:
    font_title = ImageFont.truetype("consolab.ttf", 72)
    font_sub = ImageFont.truetype("consola.ttf", 38)
    font_meta = ImageFont.truetype("consolab.ttf", 44)
except Exception:
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_meta = ImageFont.load_default()

# Text details
draw.text((width // 2, 260), "OASIS INFOBYTE INTERNSHIP", font=font_title, fill="#00e5ff", anchor="mm")
draw.text((width // 2, 350), "Python Programming Track", font=font_sub, fill="#ffd600", anchor="mm")

draw.line([(width // 2 - 300, 420), (width // 2 + 300, 420)], fill="#00ffa3", width=3)

draw.text((width // 2, 540), "TASK 5: MULTI-ROOM CHAT APPLICATION", font=font_meta, fill="#ffffff", anchor="mm")
draw.text((width // 2, 630), "Tech: Raw Sockets | Multithreading | Tkinter | SQLite", font=font_sub, fill="#8892b0", anchor="mm")

draw.text((width // 2, 780), "DEVELOPER: Achilles Gautham J B", font=font_meta, fill="#00ffa3", anchor="mm")
draw.text((width // 2, 850), "OIBSIP Batch Verification", font=font_sub, fill="#8892b0", anchor="mm")

image.save("Task5_TitleCard.png")
print("[+] Title card saved as Task5_TitleCard.png")