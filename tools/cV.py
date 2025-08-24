from PIL import Image
import numpy as np

# The palette is a list of target RGB colors.
PALETA_DE_CORES = [
    (218, 56, 50), (235, 173, 61), (157, 64, 179), (212, 101, 49),
    (193, 174, 74), (229, 213, 113), (229, 146, 169), (170, 170, 170),
    (244, 222, 93), (120, 120, 120), (210, 210, 210), (165, 252, 117),
    (152, 133, 63), (234, 135, 119), (107, 227, 134), (140, 244, 241),
    (255, 255, 255), (146, 195, 124), (85, 182, 112), (103, 147, 83),
    (200, 248, 242), (186, 38, 120), (99, 71, 55), (142, 106, 53),
    (80, 171, 165), (60, 60, 60), (86, 145, 222), (158, 176, 245),
    (145, 86, 76), (87, 13, 26), (239, 134, 64), (58, 127, 111),
    (103, 81, 237), (73, 66, 128), (214, 162, 243), (240, 185, 167),
    (238, 181, 128), (81, 106, 63), (50, 79, 153), (198, 132, 90),
    (52, 57, 64), (120, 113, 190), (152, 133, 110), (209, 182, 152),
    (119, 100, 84), (110, 117, 139), (107, 100, 68), (73, 50, 177),
    (180, 174, 236), (217, 57, 127), (246, 199, 170), (254, 250, 195),
    (211, 166, 109), (180, 185, 207), (151, 35, 37), (142, 197, 250),
    (198, 132, 123), (110, 25, 147), (104, 222, 191), (55, 119, 155),
    (147, 140, 111), (204, 197, 162), (220, 68, 62),
]

def color_distance_sq(c1, c2):
    """Calculates the squared Euclidean distance for efficiency."""
    # c1 and c2 are expected to be tuples/lists of standard Python integers.
    return sum((a - b) ** 2 for a, b in zip(c1, c2))

def find_closest_color_with_distance(cor_alvo, paleta_list):
    """
    Finds the closest color from a list and also returns its distance.
    """
    color_distances = ((p_color, color_distance_sq(cor_alvo, p_color)) for p_color in paleta_list)
    return min(color_distances, key=lambda item: item[1])

def smart_quantize(image, output_path, tolerance_sq):
    """
    Replaces only pixels that are within the tolerance distance to a palette color.
    This version fixes the uint8 arithmetic bug.
    """
    # Use a wider data type for the array to prevent overflow issues during processing
    data = np.array(image.copy())
    width, height = image.size
    pixels_changed = 0

    for y in range(height):
        for x in range(width):
            pixel_original = data[y, x]

            # 1. Skip fully transparent pixels
            if pixel_original[3] == 0:
                continue

            # 2. *** THE FIX IS HERE ***
            # Convert the pixel's RGB values from uint8 to standard Python integers before doing math.
            pixel_rgb_int = tuple(pixel_original[:3].astype(int))

            # 3. Find the closest palette color and the distance to it
            closest_color, distance = find_closest_color_with_distance(pixel_rgb_int, PALETA_DE_CORES)

            # 4. Only replace the pixel if the color is 'close enough'
            if distance <= tolerance_sq:
                data[y, x] = (*closest_color, pixel_original[3])
                pixels_changed += 1

    final_image = Image.fromarray(data)
    final_image.save(output_path, 'PNG')
    print(f"✅ Smart quantize complete. Changed {pixels_changed} pixels.")
    print(f"Saved to '{output_path}'")

# --- How to use it ---
if __name__ == '__main__':
    # You can adjust this value. A lower value is stricter.
    # Start with a higher value (e.g., 4000) to replace more colors, then lower it
    # to fine-tune and leave anti-aliasing alone.
    TOLERANCE = 0 # This corresponds to a squared distance of 3600
    
    input_file = 'takanaka og.jpeg'
    output_file = 'takanaka og.jpeg'

    try:
        with Image.open(input_file).convert('RGBA') as img:
            smart_quantize(img, output_file, tolerance_sq=TOLERANCE**2)
    except FileNotFoundError:
        print(f"❌ Error: The file '{input_file}' was not found.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
