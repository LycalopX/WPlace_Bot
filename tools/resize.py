from PIL import Image

def resize_image(input_path, output_path, proportion):

    # 1. Open your image
    try:
        img = Image.open(input_path)
        img_size = img.size

        new_size = (int(img_size[0] * proportion), int(img_size[1] * proportion))

# 3. Resize using the NEAREST resampling filter
        resized_img = img.resize(new_size, resample=Image.Resampling.NEAREST)

# 4. Save the resized image
        resized_img.save(output_path)

    except FileNotFoundError:
        print(f"Error: Make sure '{input_path}' is in the same directory.")
        exit()



if __name__ == "__main__":
#    proportion = (1.02455357143 * 8 / 5)
#    proportion = (1/3.79439252336)
#    proportion = 16.6170212766
    proportion = 5
    resize_image("./takanaka_orang.png", "./wbu2.png", proportion)