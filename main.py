import audible_util
import json
import time
import os.path
import book_filters
import discord_webhook
import requests
import traceback
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Generating/loading program data file
if not os.path.exists("program_data.json"):
    with open("program_data.json", "w") as f:
        empty_program_data = {
            "seen_asin": {}
        }
        json.dump(empty_program_data, f)

with open("program_data.json", "r") as f:
    program_data = json.load(f)

while True:
    # Reload config after every iteration in case there were any changes
    with open("config.json", "r") as f:
        config = json.load(f)

    logger.info("Running search...")

    for author, search_filters in config["watching"].items():
        try:
            search_results = audible_util.fetch_books(author_name=author).json()
        except requests.exceptions.RequestException:
            traceback.print_exc()
            time.sleep(60)
            continue

        books = search_results["products"]
        save_program_data = False

        logger.debug(f"Fetched {len(books)} books for {author}")

        if author not in program_data["seen_asin"]:
            # We have not seen this author before, save all of the asin as seen
            logger.debug("New author entry in config file, saving current books to already seen")
            program_data["seen_asin"][author] = [book["asin"] for book in books]
            save_program_data = True
        else:
            # We have seen this author before, compare what we've seen with most recent
            seen_asin = program_data["seen_asin"][author]
            for book in books:
                book_asin = book["asin"]
                if book_asin not in seen_asin:
                    # New book!
                    logger.debug(f"New book found, ASIN: {book_asin}")
                    seen_asin.append(book_asin)
                    save_program_data = True

                    try:
                        book_detailed = audible_util.fetch_book(book_asin).json()["product"]
                    except requests.exceptions.RequestException:
                        traceback.print_exc()
                        time.sleep(60)
                        continue

                    if book_filters.book_passes_filters(book_detailed, search_filters):
                        logger.debug("Book passes filters, sending message to Discord")
                        try:
                            discord_webhook.send_book_alert(book_detailed, config["discord_webhook_url"])
                        except requests.exceptions.RequestException:
                            traceback.print_exc()
                            time.sleep(60)
                            continue
                    else:
                        logger.debug("Book does not pass filters")

        if save_program_data:
            with open("program_data.json", "w") as f:
                json.dump(program_data, f)

        time.sleep(30)
