"""
Logo generator for VocabLoury application
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_logo(size=(120, 120), save_path="static/images/logo.png"):
    """Create a professional logo for VocabLoury"""
    
    # Create image with transparent background
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Colors
    primary_color = (59, 130, 246)  # Blue
    secondary_color = (30, 64, 175)  # Darker blue
    white = (255, 255, 255, 255)
    
    # Draw background circle with gradient effect
    center_x, center_y = size[0] // 2, size[1] // 2
    radius = 50
    
    # Draw circle background
    draw.ellipse([center_x - radius, center_y - radius, 
                  center_x + radius, center_y + radius], 
                 fill=primary_color, outline=white, width=2)
    
    # Draw book icon
    book_x = center_x - 15
    book_y = center_y - 10
    
    # Book pages (stacked effect)
    for i in range(3):
        offset = i * 3
        draw.rectangle([book_x + offset, book_y + offset, 
                       book_x + 30 + offset, book_y + 20 + offset], 
                      fill=white, outline=primary_color, width=1)
    
    # Draw lines on book pages
    for i in range(4):
        y_pos = book_y + 5 + (i * 3)
        draw.line([book_x + 5, y_pos, book_x + 25, y_pos], 
                 fill=primary_color, width=1)
    
    # Draw "V" letter
    try:
        # Try to use a system font
        font_size = 24
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
    
    # Draw "V" text
    text = "V"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    text_x = center_x - text_width // 2
    text_y = center_y + 15
    
    draw.text((text_x, text_y), text, fill=white, font=font)
    
    # Save the image
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    img.save(save_path, "PNG")
    
    return save_path

def create_favicon(size=(32, 32), save_path="static/favicon.png"):
    """Create a favicon for the web interface"""
    
    # Create image with transparent background
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Colors
    primary_color = (59, 130, 246)  # Blue
    white = (255, 255, 255, 255)
    
    # Draw background circle
    center_x, center_y = size[0] // 2, size[1] // 2
    radius = 14
    
    draw.ellipse([center_x - radius, center_y - radius, 
                  center_x + radius, center_y + radius], 
                 fill=primary_color)
    
    # Draw simple "V" letter
    try:
        font_size = 16
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
    
    text = "V"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    text_x = center_x - text_width // 2
    text_y = center_y - text_height // 2
    
    draw.text((text_x, text_y), text, fill=white, font=font)
    
    # Save the image
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    img.save(save_path, "PNG")
    
    return save_path

if __name__ == "__main__":
    # Generate logos
    logo_path = create_logo()
    favicon_path = create_favicon()
    
    print(f"Logo created: {logo_path}")
    print(f"Favicon created: {favicon_path}")
