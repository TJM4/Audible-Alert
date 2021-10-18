import requests
import urllib.parse


def send_book_alert(book, webhook_url):
    """
    Sends an alert to a Discord webhook about a book being released

    :param book: The book that has been released
    :param webhook_url: The Discord webhook URL to send the message to
    """
    embed_data = {
        "title": book.get("title"),
        "url": f"https://www.audible.co.uk/pd/{book['asin']}",
        "fields": [],
        "color": 16226588
    }

    if book.get("authors"):
        author_name = book["authors"][0]["name"]
        embed_data["author"] = {
            "name": author_name,
            "url": f"https://www.audible.co.uk/search?searchAuthor={urllib.parse.quote(author_name)}"
        }

    if book.get("product_images"):
        embed_data["thumbnail"] = {
            "url": list(book["product_images"].values())[0]
        }

    if book.get("issue_date"):
        embed_data["fields"].append({
            "name": "Release",
            "value": book["issue_date"],
            "inline": True
        })

    if book.get("series"):
        embed_data["fields"].append({
            "name": "Series",
            "value": book["series"][0]["title"],
            "inline": True
        })

    requests.post(webhook_url, json={
        "content": "@everyone",
        "embeds": [embed_data]
    })
