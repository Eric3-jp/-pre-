import sys
from PIL import Image, ImageDraw, ImageFont

TARGET_SIZE = 500

def text2png(text, output_path=None, img_size=None):
    if img_size is not None:
        target_size = img_size
    else:
        target_size = TARGET_SIZE

    if not (2 <= len(text) <= 3):
        print("Error: text must contain 2 or 3 characters")
        sys.exit(1)

    img = Image.new('RGBA', (target_size, target_size), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    font_size = int(target_size * 0.8)
    font = None
    while font_size > 50:
        try:
            font = ImageFont.truetype("msyh.ttc", font_size)
            break
        except:
            try:
                font = ImageFont.truetype("simhei.ttf", font_size)
                break
            except:
                try:
                    font = ImageFont.truetype("simsun.ttc", font_size)
                    break
                except:
                    try:
                        font = ImageFont.truetype("Arial Unicode.ttf", font_size)
                        break
                    except:
                        font_size -= 10
                        continue

    if font is None:
        font = ImageFont.load_default()

    char_count = len(text)
    spacing = 30
    max_text_width = target_size - 40

    total_width = 0
    char_widths = []
    for char in text:
        bbox = draw.textbbox((0, 0), char, font=font)
        w = bbox[2] - bbox[0]
        char_widths.append(w)
        total_width += w

    total_width += spacing * (char_count - 1)

    if total_width > max_text_width:
        scale = max_text_width / total_width
        font_size = int(font_size * scale)
        font = None
        while font_size > 50:
            try:
                font = ImageFont.truetype("msyh.ttc", font_size)
                break
            except:
                try:
                    font = ImageFont.truetype("simhei.ttf", font_size)
                    break
                except:
                    try:
                        font = ImageFont.truetype("simsun.ttc", font_size)
                        break
                    except:
                        try:
                            font = ImageFont.truetype("Arial Unicode.ttf", font_size)
                            break
                        except:
                            font_size -= 10
                            continue

        if font is None:
            font = ImageFont.load_default()

        total_width = 0
        char_widths = []
        for char in text:
            bbox = draw.textbbox((0, 0), char, font=font)
            w = bbox[2] - bbox[0]
            char_widths.append(w)
            total_width += w

        total_width += spacing * (char_count - 1)

    start_x = (target_size - total_width) // 2
    y = (target_size - int(target_size * 0.6)) // 2

    x = start_x
    for i, char in enumerate(text):
        draw.text((x, y), char, fill=(0, 0, 0, 255), font=font)
        x += char_widths[i] + spacing

    if output_path is None:
        output_path = f"{text}.png"

    img.save(output_path)
    print(f"Image saved to: {output_path}")
    return img

def main():
    if len(sys.argv) < 2:
        print(f"Usage: python text2png.py <text> [img_size]")
        print("  text: 2 or 3 Chinese characters")
        print("  img_size: optional, size of output image (e.g., 2500)")
        sys.exit(1)

    text = sys.argv[1]

    if len(text) < 2 or len(text) > 3:
        print("Error: text must contain exactly 2 or 3 characters")
        sys.exit(1)

    img_size = None
    if len(sys.argv) >= 3:
        try:
            img_size = int(sys.argv[2])
        except ValueError:
            print("Error: img_size must be an integer")
            sys.exit(1)

    text2png(text, img_size=img_size)

if __name__ == '__main__':
    main()