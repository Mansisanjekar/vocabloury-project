"""
Logo generator for VocabLoury application
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_logo(size=(120, 120), save_path="app_icon.png"):
    """Create a modern logo for VocabLoury desktop application"""
    
    # Create image with transparent background
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Modern colors
    dark_bg = (31, 83, 141)  # Dark blue background
    light_accent = (59, 142, 208)  # Light blue accent
    white = (255, 255, 255, 255)
    gold = (255, 215, 0)  # Gold for highlights
    
    # Draw circular background
    margin = 8
    center_x, center_y = size[0] // 2, size[1] // 2
    radius = (size[0] - margin * 2) // 2
    
    # Draw main circle
    circle_coords = [margin, margin, size[0] - margin, size[1] - margin]
    draw.ellipse(circle_coords, fill=dark_bg, outline=light_accent, width=3)
    
    # Draw "V" letter in the center
    try:
        font_size = 48
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
    
    # Draw "V" letter
    letter_v = "V"
    bbox = draw.textbbox((0, 0), letter_v, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = center_x - text_width // 2
    text_y = center_y - text_height // 2
    
    draw.text((text_x, text_y), letter_v, fill=white, font=font)
    
    # Draw small accent dots
    dot_radius = 3
    # Top accent
    draw.ellipse([center_x - dot_radius, center_y - 35, center_x + dot_radius, center_y - 29], fill=gold)
    # Bottom accent
    draw.ellipse([center_x - dot_radius, center_y + 29, center_x + dot_radius, center_y + 35], fill=gold)
    
    # Save the image
    if os.path.dirname(save_path):
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
    img.save(save_path, "PNG")
    
    return save_path

def create_favicon(size=(32, 32), save_path="static/favicon.png"):
    """Create a favicon for the web interface based on Vocabulary Booster design"""
    
    # Create image with transparent background
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Colors based on the design
    cream_bg = (255, 248, 220)  # Light yellow/cream background
    dark_brown = (101, 67, 33)  # Dark brown for text and outlines
    orange_book = (255, 165, 0)  # Orange for book covers
    white = (255, 255, 255, 255)
    
    # Draw rounded rectangle background
    margin = 2
    rect_coords = [margin, margin, size[0] - margin, size[1] - margin]
    draw.rounded_rectangle(rect_coords, radius=4, fill=cream_bg, outline=dark_brown, width=1)
    
    # Calculate positions
    center_x, center_y = size[0] // 2, size[1] // 2
    
    # Draw "Aa" letters (smaller for favicon)
    try:
        font_size = 8
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
    
    # Draw "A" and "a" letters
    letter_a = "A"
    letter_a_lower = "a"
    
    # Position the letters
    letter_a_x = center_x - 6
    letter_a_y = center_y - 8
    
    letter_a_lower_x = center_x + 2
    letter_a_lower_y = center_y - 8
    
    # Draw "A"
    draw.text((letter_a_x, letter_a_y), letter_a, fill=dark_brown, font=font)
    # Draw "a"
    draw.text((letter_a_lower_x, letter_a_lower_y), letter_a_lower, fill=dark_brown, font=font)
    
    # Draw simple book below the letters
    book_x = center_x - 4
    book_y = center_y - 2
    
    # Simple book representation
    book_rect = [book_x, book_y, book_x + 8, book_y + 6]
    draw.rectangle(book_rect, fill=orange_book, outline=dark_brown, width=1)
    
    # Book pages
    page_rect = [book_x + 1, book_y + 1, book_x + 7, book_y + 5]
    draw.rectangle(page_rect, fill=white, outline=dark_brown, width=1)
    
    # Save the image
    if os.path.dirname(save_path):
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
    img.save(save_path, "PNG")
    
    return save_path

if __name__ == "__main__":
    # Generate logos
    logo_path = create_logo()
    favicon_path = create_favicon()
    
    print(f"Logo created: {logo_path}")
    print(f"Favicon created: {favicon_path}")
