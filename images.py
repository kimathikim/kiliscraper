import requests
from bs4 import BeautifulSoup
import os


def imagedown(url, folder):
    try:
        os.mkdir(os.path.join(os.getcwd(), folder))
    except FileExistsError:
        pass
    os.chdir(os.path.join(os.getcwd(), folder))
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    images = soup.find_all("img")

    for image in images:
        name = image.get("alt", "image").replace(" ", "-").replace("/", "")
        link = image.get("src")

        if link and not link.startswith("data:image"):
            with open(name + ".jpg", "wb") as f:
                im = requests.get(link)
                f.write(im.content)
                print("writing:", name)
        else:
            print("Skipping base64 image:", name)


imagedown("https://www.jumia.co.ke/health-beauty/", "images")
