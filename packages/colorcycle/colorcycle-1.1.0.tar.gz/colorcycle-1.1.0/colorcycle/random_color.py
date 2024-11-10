import random
from colorcycle.color_convert import rgb_to_hex, rgb_to_hsl, hsl_to_hex

# Function to generate a random color in HEX, RGB, and HSL formats
def generate_random_color():
    # Generate random values for red, green, and blue
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    rgb = f"rgb({r}, {g}, {b})"
    # Convert RGB to HSL
    hsl = rgb_to_hsl(rgb)
    hex = hsl_to_hex(hsl)

    return {
        'hsl': hsl,
        'rgb': rgb,
        'hex': hex
    }