import sys
import argparse
from PIL import Image

# Characters from dark -> light (dense -> sparse)
DEFAULT_RAMP = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'. "


def image_to_ascii(img_path, width=100, invert=False, ramp=DEFAULT_RAMP):
    img = Image.open(img_path).convert("L")  # convert to grayscale

    # terminal characters are taller than they are wide; apply correction
    aspect_correction = 0.55  # tweak if characters in your terminal look stretched
    w_orig, h_orig = img.size
    # compute new height to preserve aspect ratio
    height = max(1, int((h_orig / w_orig) * width * aspect_correction))

    img = img.resize((width, height))
    pixels = img.getdata()
    chars = []

    ramp_len = len(ramp)
    for p in pixels:
        # p is 0..255, map to ramp index
        if invert:
            p = 255 - p
        idx = int((p / 255) * (ramp_len - 1))
        chars.append(ramp[idx])

    # join into lines
    lines = []
    for row in range(height):
        start = row * width
        lines.append("".join(chars[start:start + width]))
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Convert an image to ASCII art (terminal).")
    parser.add_argument("input", help="Input image path (jpg, png, etc.)")
    parser.add_argument("--width", "-w", type=int, default=100, help="Output text width in characters (default 100)")
    parser.add_argument("--invert", action="store_true", help="Invert brightness mapping")
    parser.add_argument("--outfile", "-o", default=None, help="Save ASCII art to file (otherwise print to stdout)")
    parser.add_argument("--ramp", "-r", default=None, help="Custom char ramp (dark->light). e.g. '@%#*+=-:. '")
    args = parser.parse_args()

    ramp = args.ramp if args.ramp is not None else DEFAULT_RAMP

    try:
        ascii_art = image_to_ascii(args.input, width=args.width, invert=args.invert, ramp=ramp)
    except Exception as e:
        print("Error loading/converting image:", e, file=sys.stderr)
        sys.exit(2)

    if args.outfile:
        with open(args.outfile, "w", encoding="utf-8") as f:
            f.write(ascii_art)
        print(f"Saved ASCII art to {args.outfile}")
    else:
        print(ascii_art)

if __name__ == "__main__":
    main()

"""
# Basic usage
python img2ascii.py image.jpg

# Save ASCII output to file
python img2ascii.py image.jpg > output.txt

# Set custom width
python img2ascii.py image.jpg --width 120

# Use custom ASCII ramp
python img2ascii.py image.jpg --ramp "@%#*+=-:. "

# Best quality ramp (recommended)
python img2ascii.py image.jpg --ramp "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# Invert brightness
python img2ascii.py image.jpg --invert

# Change output height scaling
python img2ascii.py image.jpg --scale 0.6
"""