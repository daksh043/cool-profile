import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime

USERNAME = "AVIVASHISHTA29"

def fetch_contributions():
    url = f"https://github.com/users/{USERNAME}/contributions"
    print(f"Fetching from {url}...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    cells = soup.find_all('td', class_='ContributionCalendar-day')
    
    days = []
    total_contributions = 0
    best_day_count = 0
    current_streak = 0
    longest_streak = 0
    
    temp_streak = 0
    
    for cell in cells:
        date_str = cell.get('data-date')
        if not date_str:
            continue
            
        level = int(cell.get('data-level', 0))
        
        cell_id = cell.get('id')
        count = 0
        if cell_id:
            tooltip = soup.find('tool-tip', {'for': cell_id})
            if tooltip:
                text = tooltip.text.strip()
                if text.lower().startswith("no"):
                    count = 0
                else:
                    try:
                        count = int(text.split(' ')[0].replace(',', ''))
                    except ValueError:
                        count = 0
        
        days.append({
            "date": date_str,
            "level": level,
            "count": count
        })
        
        total_contributions += count
        if count > best_day_count:
            best_day_count = count
            
        if count > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0

    current_streak = temp_streak

    data = {
        "total": total_contributions,
        "best_day": best_day_count,
        "longest_streak": longest_streak,
        "current_streak": current_streak,
        "days": days
    }
    
    out_dir = Path("data")
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "contributions.json"
    with open(out_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved contributions to {out_path}")
    print(f"Total: {total_contributions}, Longest Streak: {longest_streak}")

if __name__ == "__main__":
    fetch_contributions()
