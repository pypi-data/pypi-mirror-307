import re

def hex_to_hsl(hex_color):
    r = int(hex_color[1:3], 16) / 255
    g = int(hex_color[3:5], 16) / 255
    b = int(hex_color[5:7], 16) / 255

    max_val = max(r, g, b)
    min_val = min(r, g, b)
    l = (max_val + min_val) / 2

    if max_val == min_val:
        h = s = 0  # Achromatic
    else:
        d = max_val - min_val
        s = d / (2 - max_val - min_val) if l > 0.5 else d / (max_val + min_val)
        if max_val == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif max_val == g:
            h = (b - r) / d + 2
        else:
            h = (r - g) / d + 4
        h /= 6

    h = round(h * 360)
    s = round(s * 100)
    l = round(l * 100)

    return f"hsl({h}, {s}%, {l}%)"

# def hex_to_rgb(hex_color):
#     # Remove '#' if it's there
#     hex_color = hex_color.lstrip('#')
#     # Convert hex to RGB components
#     r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
#     return f"rgb({r}, {g}, {b})"

# Function to convert HEX to RGB format
def hex_to_rgb(hex_color):
    # Remove the '#' from the HEX code if it's present
    hex_color = hex_color.lstrip('#')
    
    # Ensure the HEX code has exactly 6 characters
    if len(hex_color) != 6:
        raise ValueError("Hex color must be a valid 6-character string.")
    
    # Convert HEX to RGB components
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    
    # Return the RGB in the desired format: rgb(r, g, b)
    return f"rgb({r}, {g}, {b})"

def hsl_to_rgb(hsl_color):
    import re
    match = re.match(r"hsl\((\d+),\s*(\d+)%,\s*(\d+)%\)", hsl_color)
    if not match:
        raise ValueError("Invalid HSL format. Please provide input as 'hsl(h, s%, l%)'.")

    h, s, l = map(int, match.groups())
    s /= 100
    l /= 100

    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2

    r, g, b = 0, 0, 0
    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    elif 300 <= h < 360:
        r, g, b = c, 0, x

    r = round((r + m) * 255)
    g = round((g + m) * 255)
    b = round((b + m) * 255)

    return f"rgb({r}, {g}, {b})"

def rgb_to_hex(rgb_string):
    # Use regex to extract numbers from "rgb(255, 255, 255)"
    match = re.match(r"rgb\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)", rgb_string)
    if not match:
        raise ValueError("RGB input must be in the format 'rgb(r, g, b)' with values 0-255")
    
    r, g, b = map(int, match.groups())
    # Ensure RGB values are within the valid range
    if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
        raise ValueError("RGB values must be between 0 and 255")
    
    # Convert to HEX
    return f"#{r:02x}{g:02x}{b:02x}".upper()


def hsl_to_hex(hsl_color):
    rgb_color = hsl_to_rgb(hsl_color)
    return rgb_to_hex(rgb_color)

def rgb_to_hsl(rgb_color):
    import re
    match = re.findall(r"\d+", rgb_color)
    r, g, b = map(int, match)

    r /= 255
    g /= 255
    b /= 255

    max_val = max(r, g, b)
    min_val = min(r, g, b)
    l = (max_val + min_val) / 2

    if max_val == min_val:
        h = s = 0
    else:
        d = max_val - min_val
        s = d / (2 - max_val - min_val) if l > 0.5 else d / (max_val + min_val)
        if max_val == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif max_val == g:
            h = (b - r) / d + 2
        else:
            h = (r - g) / d + 4
        h /= 6

    h = round(h * 360)
    s = round(s * 100)
    l = round(l * 100)

    return f"hsl({h}, {s}%, {l}%)"
