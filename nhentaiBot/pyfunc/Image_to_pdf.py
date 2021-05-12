# ---------- IMPORTS ----------
from PIL import Image
import requests
import io

# -------- FUNCTIONS -----


async def image_pdf(img_list, title):

    # opening raw images from URL
    raw_image = [Image.open(io.BytesIO(requests.get(url).content))
                 for url in img_list]
    print(raw_image)

    convert_rbg = [img.convert("RGB") for img in raw_image]
    print("after convert_rgb")
    temp_save = convert_rbg[0].save(
        f"nhentaiBot/tempdir/{title}.pdf", save_all=True, append_images=convert_rbg[1:])
    return True
