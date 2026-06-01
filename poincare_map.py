import numpy as np
import sys
from PIL import Image

TARGET_SIZE = 500
INPUT_SIZE = 2500

def load_and_preprocess_image(image_path):
    img = Image.open(image_path)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    width, height = img.size
    size = min(width, height)

    left = (width - size) // 2
    top = (height - size) // 2
    right = left + size
    bottom = top + size

    img_cropped = img.crop((left, top, right, bottom))

    img_resized = img_cropped.resize((INPUT_SIZE, INPUT_SIZE), Image.Resampling.LANCZOS)

    return img_resized

def apply_poincare_transform(img):
    img_array = np.array(img)
    h, w = img_array.shape[:2]

    result_array = np.zeros((TARGET_SIZE, TARGET_SIZE, 4), dtype=np.float32)

    plane_half = INPUT_SIZE // 2
    plane_range = np.linspace(-plane_half, plane_half, INPUT_SIZE)

    for i in range(TARGET_SIZE):
        for j in range(TARGET_SIZE):
            disk_x = (i / (TARGET_SIZE - 1)) * 2 - 1
            disk_y = (j / (TARGET_SIZE - 1)) * 2 - 1

            disk_r_sq = disk_x**2 + disk_y**2
            if disk_r_sq > 1.0:
                continue

            disk_r = np.sqrt(disk_r_sq)
            if disk_r > 1e-10:
                plane_r = 2 * np.arctanh(disk_r)
                scale = plane_r / disk_r
                plane_x = disk_x * scale
                plane_y = disk_y * scale
            else:
                plane_x, plane_y = 0.0, 0.0

            src_x = (plane_x + plane_half) / INPUT_SIZE * (INPUT_SIZE - 1)
            src_y = (plane_y + plane_half) / INPUT_SIZE * (INPUT_SIZE - 1)

            src_x = np.clip(src_x, 0, INPUT_SIZE - 1)
            src_y = np.clip(src_y, 0, INPUT_SIZE - 1)

            x0, y0 = int(src_x), int(src_y)
            x1, y1 = min(x0 + 1, INPUT_SIZE - 1), min(y0 + 1, INPUT_SIZE - 1)

            fx = src_x - x0
            fy = src_y - y0

            c00 = img_array[y0, x0].astype(np.float32)
            c10 = img_array[y1, x0].astype(np.float32)
            c01 = img_array[y0, x1].astype(np.float32)
            c11 = img_array[y1, y1].astype(np.float32)

            result_array[i, j] = (1 - fx) * (1 - fy) * c00 + \
                                 fx * (1 - fy) * c10 + \
                                 (1 - fx) * fy * c01 + \
                                 fx * fy * c11

    result_array = np.clip(result_array, 0, 255).astype(np.uint8)
    return Image.fromarray(result_array)

def create_disk_mask(size=500):
    y, x = np.ogrid[:size, :size]
    center = size // 2
    radius = size // 2
    mask = (x - center)**2 + (y - center)**2 <= radius**2
    return mask

def apply_disk_mask(img):
    img_array = np.array(img)
    mask = create_disk_mask(TARGET_SIZE)

    result_array = np.zeros_like(img_array)
    result_array[mask] = img_array[mask]

    return Image.fromarray(result_array)

def main():
    if len(sys.argv) < 2:
        print(f"Usage: python poincare_map.py <pngpath>")
        sys.exit(1)

    image_path = sys.argv[1]

    print(f"Loading and preprocessing image: {image_path}")
    img = load_and_preprocess_image(image_path)

    print(f"Applying Poincaré transformation...")
    transformed_img = apply_poincare_transform(img)

    print(f"Applying disk mask...")
    final_img = apply_disk_mask(transformed_img)

    output_path = image_path.rsplit('.', 1)[0] + '_poincare.png'
    final_img.save(output_path)
    print(f"Result saved to: {output_path}")

if __name__ == '__main__':
    main()