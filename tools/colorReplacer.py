from PIL import Image
import numpy as np

def replace_color_with_tolerance(image_path, target_color, new_color, output_path, tolerance=30):
    """
    Replaces colors within a certain tolerance of a target color,
    while preserving existing transparency.

    :param image_path: Path to the input image (e.g., a PNG).
    :param target_color: An RGB tuple of the color to be replaced.
    :param new_color: An RGB tuple of the new color.
    :param output_path: Path to save the modified image (must be .png).
    :param tolerance: An integer. A lower value is a stricter match.
    """
    try:
        # Open the image and ensure it's in RGBA format to handle transparency
        img = Image.open(image_path).convert('RGBA')
        
        # Convert the image to a NumPy array, using a wider type for calculations
        data = np.array(img, dtype=np.int16)
        
        # --- FIX IS HERE ---
        # Separate the RGB channels from the Alpha channel for comparison
        rgb_data = data[:, :, :3]
        target = np.array(target_color, dtype=np.int16)

        # Calculate the color difference using only the RGB channels
        color_distance = np.sum(np.abs(rgb_data - target), axis=-1)
        
        # Create a mask where the distance is within the tolerance
        mask = color_distance <= tolerance
        
        # Prepare the new color in RGBA format (fully opaque)
        new_color_rgba = (*new_color, 255)
        
        # Apply the new RGBA color to the pixels in the mask
        data[mask] = new_color_rgba
        
        # Convert the data back to a valid image format (uint8)
        new_img = Image.fromarray(data.astype(np.uint8))
        
        # Save the new image as PNG to preserve transparency
        new_img.save(output_path, 'PNG')

        print(f"✅ Successfully processed '{image_path}' (with tolerance) and saved to '{output_path}'.")
        
    except FileNotFoundError:
        print(f"❌ Error: The file '{image_path}' was not found.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

# --- How to use it ---
if __name__ == '__main__':
    # 1. Define the path to your input image (preferably a PNG)
    input_file = 'new_big_sceptile.png'

    # 2. Use a color picker to find the main color you want to replace
    color_to_replace = (21, 230, 123) 

    # 3. Set your new color
    new_replacement_color = (135, 255, 94) 

    # 4. Adjust the tolerance. Start low and increase if needed.
    color_tolerance = 3

    replace_color_with_tolerance(
        input_file, 
        color_to_replace, 
        new_replacement_color,
        'output.png', 
        tolerance=color_tolerance
    )
