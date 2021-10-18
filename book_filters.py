def book_passes_filters(book, filters):
    """
    Checks if a book passes a set of filters

    :param book: Book to check
    :param filters: Dictionary of filters
    :return: True if book passes the filters, false otherwise
    """
    allowed_series_ids = filters.get("series_ids")
    allowed_languages = filters.get("languages")

    # Checking that the series id is in the list of wanted series ids
    if allowed_series_ids:
        if "series" not in book:
            return False

        for series in book["series"]:
            if series["asin"] in allowed_series_ids:
                break
        else:
            return False

    if allowed_languages:
        book_language = book["language"].lower()
        for language in allowed_languages:
            if language.lower() == book_language:
                break
        else:
            return False

    return True
