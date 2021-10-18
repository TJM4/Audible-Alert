import requests


def fetch_books(author_name=None,
                query=None,
                sort_by="-ReleaseDate",
                response_groups=None,
                results=50,
                page=0):
    """
    Runs a search on audible

    See https://audible.readthedocs.io/en/latest/misc/external_api.html#get-1-0-catalog-products for documentation
    on endpoint

    :param author_name: Author name
    :param query: Search query
    :param sort_by: Results order
    :param response_groups: What information should be returned
    :param results: Number of results
    :param page: Results page
    :return: Response from Audible
    """
    if response_groups is None:
        response_groups = []

    params = {
        "response_groups": ",".join(response_groups),
        "author": author_name,
        "keywords": query,
        "products_sort_by": sort_by,
        "num_results": results,
        "page": page
    }
    return requests.get("https://api.audible.co.uk/1.0/catalog/products", params=params)


def fetch_book(asin, response_groups=None):
    """
    Fetch information available from Audible about specific book.

    :param asin: ASIN of the book
    :param response_groups: Information if be fetched. If None, all info will be fetched
    :return: Response from Audible
    """
    if response_groups is None:
        response_groups = ["contributors", "media", "product_attrs", "product_desc", "product_extended_attrs",
                           "product_plan_details", "product_plans", "rating", "review_attrs", "reviews", "sample",
                           "sku", "series"]
    params = {
        "response_groups": ",".join(response_groups)
    }

    return requests.get(f"https://api.audible.co.uk/1.0/catalog/products/{asin}", params=params)


if __name__ == "__main__":
    bobiverse_books = fetch_books(query="Spider Shepherd").json()
    print(bobiverse_books)

    print(fetch_book(bobiverse_books["products"][0]["asin"]).json())
