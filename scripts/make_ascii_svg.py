import os
from pathlib import Path
from PIL import Image

RAMP = " .`:-=+*cs#%@"
TARGET_WIDTH = 100
TARGET_HEIGHT = 53

def generate_svg():
    in_path = Path("data/source-prepped.png")
    if not in_path.exists():
        print(f"Error: {in_path} not found. Run prep_photo.py first.")
        return

    img = Image.open(in_path).convert("L")
    img = img.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)
    pixels = img.getdata()
    
    lines = []
    for y in range(TARGET_HEIGHT):
        row = ""
        for x in range(TARGET_WIDTH):
            brightness = pixels[y * TARGET_WIDTH + x]
            idx = int((255 - brightness) / 255 * (len(RAMP) - 1))
            row += RAMP[idx]
        lines.append(row)
    
    char_w = 7.2
    char_h = 14
    width = TARGET_WIDTH * char_w
    height = TARGET_HEIGHT * char_h
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
    <style>
        .ascii {{
            font-family: monospace;
            font-size: 12px;
            fill: #8b949e;
            white-space: pre;
        }}
        @keyframes wipe {{
            0% {{ clip-path: inset(0 100% 0 0); }}
            100% {{ clip-path: inset(0 0 0 0); }}
        }}
        .line {{
            animation: wipe 1.5s steps({TARGET_WIDTH}, end) forwards;
            clip-path: inset(0 100% 0 0);
        }}
    </style>
'''
    stagger_delay = 0.05
    for i, line in enumerate(lines):
        y_pos = (i + 1) * char_h
        safe_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        delay = i * stagger_delay
        svg += f'    <text class="ascii line" x="0" y="{y_pos}" style="animation-delay: {delay}s">{safe_line}</text>\n'

    svg += '</svg>'
    
    out_path = Path("avi-ascii.svg")
    out_path.write_text(svg)
    print(f"Generated {out_path}")

if __name__ == "__main__":
    generate_svg()
