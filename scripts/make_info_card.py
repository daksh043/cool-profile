import os
from pathlib import Path

def generate_info_card():
    static = os.environ.get("STATIC", "0") == "1"
    
    title = "daksh043@github"
    separator = "-" * len(title)
    
    fields = [
        ("OS", "Windows 11 / Linux", "#58a6ff"),
        ("Host", "GitHub Profile", "#58a6ff"),
        ("Now", "Building cool things", "#3fb950"),
        ("Prev", "Software Engineer at TechCorp", "#d2a8ff"),
        ("Stack", "Python, React, TypeScript", "#ff7b72"),
        ("Highlights", "Shipped 10+ projects, open-source contributor", "#f0883e"),
    ]
    
    width = 490
    height = 500
    line_h = 24
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
    <style>
        .text {{
            font-family: 'Courier New', Courier, monospace;
            font-size: 14px;
            fill: #c9d1d9;
        }}
        .title {{
            fill: #58a6ff;
            font-weight: bold;
        }}
        @keyframes fadeSlide {{
            0% {{ opacity: 0; transform: translateX(-10px); }}
            100% {{ opacity: 1; transform: translateX(0); }}
        }}
        .row {{
            opacity: {1 if static else 0};
            {"" if static else "animation: fadeSlide 0.5s ease forwards;"}
        }}
    </style>
    <rect width="{width}" height="{height}" fill="transparent" />
'''
    
    y = 40
    start_x = 20
    
    svg += f'    <text class="text title row" x="{start_x}" y="{y}" style="animation-delay: 0.1s">{title}</text>\n'
    y += line_h
    svg += f'    <text class="text row" x="{start_x}" y="{y}" style="animation-delay: 0.2s">{separator}</text>\n'
    y += line_h
    
    delay = 0.3
    for key, value, color in fields:
        y += line_h
        svg += f'''    <g class="row" style="animation-delay: {delay}s">
        <text class="text" x="{start_x}" y="{y}" fill="{color}" font-weight="bold">{key}</text>
        <text class="text" x="{start_x + 100}" y="{y}">: {value}</text>
    </g>\n'''
        delay += 0.1
        
    svg += '</svg>'
    
    out_path = Path("info-card.svg")
    out_path.write_text(svg)
    print(f"Generated {out_path}")

if __name__ == "__main__":
    generate_info_card()
