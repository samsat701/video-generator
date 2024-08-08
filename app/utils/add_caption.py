from PIL import ImageDraw, ImageFont

def add_caption_to_image(image, text):
    width, height = image.size
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("LiberationSerif-Regular.ttf", 45)  # Adjust font size here for 9:16
    
    # Calculate the size and position of the black box
    lines = []
    words = text.split()
    line = ""
    for word in words:
        line_with_word = line + word + " "
        bbox = draw.textbbox((0, 0), line_with_word, font=font)
        if bbox[2] < width - 20:  # 20 for padding
            line = line_with_word
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)

    # Adjust box height based on the number of lines
    box_height = (len(lines) * draw.textbbox((0, 0), lines[0], font=font)[3]) + 20  # 20 for padding
    box = [(0, height - box_height), (width, height)]

    # Draw the black box
    draw.rectangle(box, fill="black")

    # Draw the text on the black box
    text_y = height - box_height + 10  # 10 for padding
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_x = (width - bbox[2]) // 2
        draw.text((text_x, text_y), line, font=font, fill="white")
        text_y += bbox[3]

    return image
