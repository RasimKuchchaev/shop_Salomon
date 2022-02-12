import requests
import json

header = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
    "bx-ajax": "true"
}


def colection_data():
    url = "https://salomon.ru/catalog/muzhchiny/obuv/filter/available-is-y/size-is-10%20uk-or-10.5%20uk/apply/?PAGEN_1=2"

    response = requests.get(url=url, headers=header)

    # with open("rezult.json", "w") as file:
    #     json.dump(response.json(), file, indent=4, ensure_ascii=False)

    data = response.json()
    count_page = data.get("pagination").get("pageCount")

    rezult_data = []
    data_link = []

    for page in range(1, count_page + 1):
        response = requests.get(
            url=f"https://salomon.ru/catalog/muzhchiny/obuv/filter/available-is-y/size-is-10%20uk-or-10.5%20uk/apply/?PAGEN_1={page}",
            headers=header)
        data = response.json()

        products = data.get("products")

        for product in products:
            product_colors = product.get("colors")

            for pc in product_colors:
                title = pc.get("title")
                link = pc.get("link")
                category = pc.get("category")

                price_base = pc.get("price").get("base")
                price_sale = pc.get("price").get("sale")
                discountpercent = pc.get("price").get("discountPercent")

                if discountpercent != 0 and link not in data_link:
                    data_link.append(link)

                    rezult_data.append(
                        {"title": title,
                         "link": f'https://salomon.ru{link}',
                         "category": category,
                         "price_base": price_base,
                         "price_sale": price_sale,
                         "discountPercent": discountpercent
                         }
                    )
        print(f"{page}/{count_page}")

    with open("data.json", "w") as file:
        json.dump(rezult_data, file, indent=4, ensure_ascii=False)


def main():
    colection_data()


if __name__ == '__main__':
    main()
