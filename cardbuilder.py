from PIL import Image
import pathlib
import json


base_path = pathlib.Path(__file__).parent.resolve()
IMG_FOLDER = f"{base_path}/images/"
CARD_FILE = f"{base_path}/card.json"
ALBUM_FILE = f"{base_path}/album.json"
COLLECTION_FILE = f"{base_path}/collecion.json"

f = open(file=CARD_FILE)
data = json.load(f)
f.close

f = open(file=ALBUM_FILE)
album_data = json.load(f)
f.close

f = open(file=COLLECTION_FILE)
collection_data = json.load(f)
f.close

# print(data)
for each in data:
    image = each["assets"].get("img")
    if image:
        print(image)
        card_im = Image.open(f"{IMG_FOLDER}{image}_r")
        # card_im.show()
