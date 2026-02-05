from PIL import Image
import os

def make_transparent(file_path):
    if not os.path.exists(file_path):
        return
    
    img = Image.open(file_path).convert("RGBA")
    datas = img.getdata()

    new_data = []
    for item in datas:
        # If the pixel is white or very close to white, make it transparent
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    img.putdata(new_data)
    img.save(file_path, "PNG")
    print(f"Made {file_path} transparent.")

brand_dir = "brand"
files = ["icon.png", "icon@2x.png", "logo.png", "logo@2x.png"]

for f in files:
    make_transparent(os.path.join(brand_dir, f))
