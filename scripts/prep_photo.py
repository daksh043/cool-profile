import sys
import os
from pathlib import Path
from PIL import Image
import numpy as np
import cv2
import rembg
import io

def prep_photo(input_path: str):
    print(f"Processing {input_path}...")
    
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        sys.exit(1)
        
    # Read the image
    with open(input_path, 'rb') as f:
        input_data = f.read()

    from rembg import remove, new_session
    print("Removing background using u2net model...")
    session = new_session("u2net")
    subject_data = remove(input_data, session=session)
    subject_img = Image.open(io.BytesIO(subject_data)).convert("RGBA")

    # Convert to numpy array for OpenCV
    img_np = np.array(subject_img)
    
    # Extract RGB and Alpha
    rgb = img_np[:, :, :3]
    alpha = img_np[:, :, 3]
    
    # Convert RGB to Grayscale
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    
    # Apply CLAHE
    print("Applying CLAHE...")
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl1 = clahe.apply(gray)
    
    # Composite onto pure white background
    print("Compositing...")
    white_bg = np.ones_like(rgb) * 255
    alpha_factor = alpha[:, :, np.newaxis] / 255.0
    
    # Blend
    cl1_rgb = cv2.cvtColor(cl1, cv2.COLOR_GRAY2RGB)
    composited = (cl1_rgb * alpha_factor + white_bg * (1 - alpha_factor)).astype(np.uint8)
    
    # Save output
    out_dir = Path("data")
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / "source-prepped.png"
    
    # Save it as grayscale (since we'll just read brightness anyway)
    composited_gray = cv2.cvtColor(composited, cv2.COLOR_RGB2GRAY)
    cv2.imwrite(str(out_path), composited_gray)
    print(f"Saved prepped image to {out_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/prep_photo.py <source-photo.jpg>")
        sys.exit(1)
    prep_photo(sys.argv[1])
