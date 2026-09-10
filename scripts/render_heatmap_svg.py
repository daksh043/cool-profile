import json
from pathlib import Path

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

def render_heatmap():
    data_path = Path("data/contributions.json")
    if not data_path.exists():
        print("Error: data/contributions.json not found")
        return
        
    with open(data_path, "r") as f:
        data = json.load(f)
        
    days = data.get("days", [])
    
    weeks = []
    current_week = []
    for day in days:
        current_week.append(day)
        if len(current_week) == 7:
            weeks.append(current_week)
            current_week = []
    if current_week:
        weeks.append(current_week)
        
    box_size = 11
    gap = 4
    
    width = 860
    height = 180
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
    <style>
        .text {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            font-size: 12px;
            fill: #7d8590;
        }}
        @keyframes slideDown {{
            0% {{ opacity: 0; transform: translateY(-5px); }}
            100% {{ opacity: 1; transform: translateY(0); }}
        }}
        .box {{
            opacity: 0;
            animation: slideDown 0.5s forwards;
            rx: 2;
        }}
    </style>
    <rect width="{width}" height="{height}" fill="transparent" />
    <g transform="translate(20, 20)">
'''
    
    for col, week in enumerate(weeks):
        x = col * (box_size + gap)
        for row, day in enumerate(week):
            y = row * (box_size + gap)
            level = min(day["level"], len(PALETTE) - 1)
            color = PALETTE[level]
            
            delay = (col * 0.02) + (row * 0.02)
            svg += f'        <rect class="box" x="{x}" y="{y}" width="{box_size}" height="{box_size}" fill="{color}" style="animation-delay: {delay}s" />\n'

    stats_y = 7 * (box_size + gap) + 30
    total = data.get("total", 0)
    svg += f'        <text class="text" x="0" y="{stats_y}">{total} contributions in the last year</text>\n'
    
    legend_x = len(weeks) * (box_size + gap) - (5 * (box_size + gap)) - 40
    svg += f'        <text class="text" x="{legend_x - 30}" y="{stats_y}">Less</text>\n'
    for i, color in enumerate(PALETTE):
        svg += f'        <rect x="{legend_x + i * (box_size + gap)}" y="{stats_y - 10}" width="{box_size}" height="{box_size}" fill="{color}" rx="2" />\n'
    svg += f'        <text class="text" x="{legend_x + len(PALETTE) * (box_size + gap) + 5}" y="{stats_y}">More</text>\n'

    svg += '''    </g>
</svg>'''

    out_path = Path("contrib-heatmap.svg")
    out_path.write_text(svg)
    print(f"Generated {out_path}")

if __name__ == "__main__":
    render_heatmap()
