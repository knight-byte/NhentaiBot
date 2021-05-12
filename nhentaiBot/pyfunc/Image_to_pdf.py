# ---------- IMPORTS ----------
from PIL import Image
import requests
import io
import re

# -------- FUNCTIONS -----


def image_pdf(img_list, title):

    # opening raw images from URL
    raw_image = [Image.open(io.BytesIO(requests.get(url).content))
                 for url in img_list]
    print(raw_image)

    convert_rbg = [img.convert("RGB") for img in raw_image]
    print("after convert_rgb")
    rf = "".join(re.findall(r"[\w]+", string=title))
    temp_save = convert_rbg[0].save(
        f"nhentaiBot/tempdir/{rf}.pdf", save_all=True, append_images=convert_rbg[1:])
    return True
