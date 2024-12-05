import requests
from bs4 import BeautifulSoup
import csv


def scrape_kilimall(search_term, pages=1):
    base_url = "https://www.kilimall.co.ke/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    products = []
    for page in range(1, pages + 1):
        search_url = f"{base_url}search?q={search_term.replace(' ', '+')}&page={page}"
        response = requests.get(search_url, headers=headers)
        page_soup = BeautifulSoup(response.content, "html.parser")

        # Extract product containers
        containers = page_soup.find_all("div", class_="product-item")

        for container in containers:
            # Extract product name
            brand = (
                container.find("p", class_="product-title").text.strip()
                if container.find("p", class_="product-title")
                else "No Title"
            )

            # Extract price
            price = (
                container.find("div", class_="product-price")
                .text.strip()
                .replace("KSh", "")
                .replace(",", "")
            )
            price = int(price.split()[0]) if price else 0

            # Extract image URL
            img_tag = container.find("img")
            image = (
                img_tag["data-src"]
                if img_tag and img_tag.get("data-src")
                else img_tag.get("src", "No Image")
            )
            if image and not image.startswith("http"):
                image = base_url + image

            # Extract product link
            link_tag = container.find("a", href=True)
            link = base_url + link_tag["href"] if link_tag else "No Link"

            # Extract rating
            rating_element = container.find("div", class_="rate")
            rating = rating_element.text.strip() if rating_element else "No Rating"

            product = {
                "Brand": brand,
                "Price": price,
                "Rating": rating,
                "Image": image,  # Image URL
                "Link": link,    # Product Link
            }
            products.append(product)

            print(
                f"Scraped: {brand} - Price: {price} - Rating: {rating} - Image: {image} - Link: {link}"
            )

    # Save to CSV
    filename = f"{search_term.replace(' ', '_')}_kilimall.csv"
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["Brand", "Price", "Rating", "Image", "Link"],  # Added Link
        )
        writer.writeheader()
        writer.writerows(products)

    print(f"\nData has been written to {filename}")
