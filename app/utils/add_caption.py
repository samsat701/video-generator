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
        if draw.textsize(line + word, font=font)[0] < width - 20:  # 20 for padding
            line += word + " "
        else:
            lines.append(line)
            line = word + " "
    lines.append(line)

    # Adjust box height based on the number of lines
    box_height = (len(lines) * draw.textsize(lines[0], font=font)[1]) + 20  # 20 for padding
    box = [(0, height - box_height), (width, height)]

    # Draw the black box
    draw.rectangle(box, fill="black")

    # Draw the text on the black box
    text_y = height - box_height + 10  # 10 for padding
    for line in lines:
        text_size = draw.textsize(line, font=font)
        text_x = (width - text_size[0]) // 2
        draw.text((text_x, text_y), line, font=font, fill="white")
        text_y += draw.textsize(line, font=font)[1]

    return image
