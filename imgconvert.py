import pathlib
import shutil

base_path = pathlib.Path(__file__).parent.resolve()
IMG_FOLDER = f"{base_path}/images/"
REBUILD_FOLDER = f"{base_path}/rebuild/"
images = pathlib.Path(IMG_FOLDER)

for image in images.iterdir():
    name_list = image.name.split(".")
    if len(name_list) == 1:
        destination = f"{REBUILD_FOLDER}{name_list[0]}.png"
        shutil.copyfile(src=str(image), dst=destination)


