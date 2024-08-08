def crop_to_9_16(image):
    width, height = image.size
    target_aspect_ratio = 9 / 16
    target_height = height
    target_width = int(target_height * target_aspect_ratio)
    
    if target_width > width:
        target_width = width
        target_height = int(target_width / target_aspect_ratio)

    left = (width - target_width) // 2
    top = (height - target_height) // 2
    right = (width + target_width) // 2
    bottom = (height + target_height) // 2

    return image.crop((left, top, right, bottom))
