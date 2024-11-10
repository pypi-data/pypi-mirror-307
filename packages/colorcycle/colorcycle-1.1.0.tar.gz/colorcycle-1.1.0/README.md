# ColorCycle - Random Color Generator

**ColorCycle** is a Python package that helps developers easily convert color formats between Hex, RGB, and HSL. This tool is ideal for designers and developers working on color management for websites, applications, and graphical projects. Simply provide a color in any of the supported formats, and ColorCycle will convert it into the others.



## Installation

To install this package:

```bash
pip install colorcycle
```



## Features

- **Color Format Conversion**: Convert between HEX, RGB, and HSL color formats.
- **Random Color Generation**: Generate random colors in HEX format for UI elements and design projects.
- **Color Name Parsing**: Parse common color names (e.g., "red", "blue", "magenta") into their corresponding HEX, RGB, and HSL values.
- **Color Brightness Adjustment**: Easily adjust the brightness of any color by a specified percentage.
- **Web Safe Color Palette**: Get the closest web-safe color palette for any input color.
- **Color Contrast Calculation**: Calculate the contrast ratio between two colors, useful for ensuring accessibility (WCAG compliance).
- **Color Scheme Generation**: Automatically generate color schemes such as monochromatic, complementary, triadic, and analogous from a base color.



## Color Conversion Functions

This document provides details for various color conversion functions that can convert between HEX, RGB, and HSL formats. Each function is described along with its usage and an example.

| **Method**                  | **Description**                                                                                                                                 | **Example**                                                         |
|-----------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------|
| `hex_to_hsl(hex_color)`      | Converts a HEX color code to HSL format. It accepts a string representing the HEX code (e.g., `#RRGGBB`) and returns a string in `hsl(h, s%, l%)` format. | `hex_to_hsl('#FF5733')` → `hsl(9, 100%, 60%)`                      |
| `hex_to_rgb(hex_color)`      | Converts a HEX color code to RGB format. It accepts a string representing the HEX code and returns a string in `rgb(r, g, b)` format.           | `hex_to_rgb('#FF5733')` → `rgb(255, 87, 51)`                       |
| `hsl_to_rgb(hsl_color)`      | Converts an HSL color value to RGB format. It accepts a string in `hsl(h, s%, l%)` format and returns the RGB equivalent in `rgb(r, g, b)` format. | `hsl_to_rgb('hsl(9, 100%, 60%)')` → `rgb(255, 87, 51)`             |
| `hsl_to_hex(hsl_color)`      | Converts an HSL color value to HEX format. It accepts a string in `hsl(h, s%, l%)` format and returns the HEX equivalent as a string `#RRGGBB`.   | `hsl_to_hex('hsl(9, 100%, 60%)')` → `#FF5733`                       |
| `rgb_to_hex(rgb_string)`     | Converts an RGB color value to HEX format. It accepts a string in `rgb(r, g, b)` format and returns the HEX equivalent in `#RRGGBB`.              | `rgb_to_hex('rgb(255, 87, 51)')` → `#FF5733`                        |
| `rgb_to_hsl(rgb_color)`      | Converts an RGB color value to HSL format. It accepts a string in `rgb(r, g, b)` format and returns the HSL equivalent in `hsl(h, s%, l%)`.        | `rgb_to_hsl('rgb(255, 87, 51)')` → `hsl(9, 100%, 60%)`              |
| `color_parser(color_name)`    | Accepts a color name (e.g., `"red"`, `"blue"`) and returns the corresponding HEX, RGB, and HSL values based on a predefined dictionary of color names. | `color_parser('red')` → `{'color_name': 'red', 'hex': '#FF0000', 'rgb': 'rgb(255, 0, 0)', 'hsl': 'hsl(0, 100%, 50%)'}` |
| `generate_random_color()`     | Generates a random color and returns it in HEX, RGB, and HSL formats. The generated values are random for red, green, and blue components.       | `generate_random_color()` → `{'hsl': 'hsl(180, 50%, 60%)', 'rgb': 'rgb(128, 255, 255)', 'hex': '#80FFFF'}` |

---

### Additional Notes

- The functions assume valid color inputs. For example, HEX codes should be in the format `#RRGGBB` and RGB values should be in the range of `0-255`.
- The `color_parser` method relies on a predefined dictionary of color names. Ensure that this dictionary is available and properly populated with color name-to-HEX mappings.




``` python
# Importing functions from the colorcycle package
from colorcycle import (
    hex_to_rgb,
    rgb_to_hex,
    rgb_to_hsl,
    hex_to_hsl,
    hsl_to_rgb,
    hsl_to_hex,
    color_parser,
    generate_random_color
)
```


### 1. Convert HEX to RGB
Converts a HEX color to an RGB object. We convert the HEX value "#FF5733" to its RGB components: 255 for Red, 87 for Green, and 51 for Blue.
``` python
print("1 HEX to RGB:")
hex_color = "#ff5733"
print(f"HEX: {hex_color} -> RGB: {hex_to_rgb(hex_color)}")
```

### 2. Convert RGB to HEX
Converts an RGB object to a HEX color. We convert the RGB values rgb(255, 87, 51) to the HEX color "#FF5733".
``` python
print("\n2 RGB to HEX:")
rgb_color = 'rgb(255, 87, 51)'
print(f"RGB {rgb_color} -> HEX {rgb_to_hex(rgb_color)}")
```

### 3. Convert RGB to HSL
Converts an RGB object to an HSL object. We convert the RGB color hsl(255, 87%, 51%) to HSL values: Hue = 9°, Saturation = 100%, Lightness = 60%.
``` python
print("\n3 RGB to HSL:")
print(f"RGB {rgb_color} -> HSL {rgb_to_hsl(rgb_color)}")
```

### 4. Convert HEX to HSL
Converts a HEX color to an HSL object. We convert the HEX color "#FF5733" to HSL values, where H is 9°, S is 100%, and L is 60%.
``` python
print("\n4 HEX to HSL:")
print(f"HEX {hex_color} -> HSL {hex_to_hsl(hex_color)}")
```

### 5. Convert HSL to RGB
Converts an HSL object to an RGB object. We convert the HSL color hsl(9, 100%, 60%) to the RGB color rgb(255, 87, 51).
``` python
print("\n5 HSL to RGB:")
hsl_color = 'hsl(11, 100%, 60%)'  # Assuming (H, S, L) format
print(f"HSL {hsl_color} -> RGB {hsl_to_rgb(hsl_color)}")
```

### 6. Convert HSL to HEX
Converts an HSL object to a HEX color. We convert the HSL color hsl(9, 100%, 60%) to the HEX color "#FF5733".
``` python
print("\n6 HSL to HEX:")
print(f"HSL {hsl_color} -> HEX {hsl_to_hex(hsl_color)}")
```

### 7. Color Parser (Identify color name and provide RGB, HEX, and HSL values)
Generates a random RGB, HEX and HSL color.
``` python
print("\n7 Color Parser:")
color_name = "light blue"  # Replace with any color name
color_data = color_parser(color_name)
print(color_data)
```

### 8. Generate a Random Color (RGB, HEX, HSL)
Parses common color names and returns the corresponding HEX, RGB, and HSL values. This function takes the color name "red" and returns its HEX, RGB, and HSL values.
``` python
print("\n8. Random Color Generator:")
random_color = generate_random_color()
print(f"{random_color}")

```


## Compatibility and Framework Support
`ColorCycle` is lightweight and framework-agnostic, but it works seamlessly with modern Python and JavaScript frameworks [pip install colorcycle](https://www.npmjs.com/package/colorcycle) like React, Vue.js, Angular, and Svelte.


## Community and Ecosystem

By using **ColorCycle**, you are joining a growing community of developers who are passionate about colors and design. We encourage you to share your experiences, ideas, and feedback on GitHub Discussions or any community platform of your choice.

- **GitHub Discussions**: Share use cases, report bugs, and suggest features.

We'd love to hear from you and see how you're using **ColorCycle** in your projects!


## Issues and Feedback
For issues, feedback, and feature requests, please open an issue on our [GitHub Issues page](https://github.com/krishnatadi/colorcycle-python/issues). We actively monitor and respond to community feedback.

