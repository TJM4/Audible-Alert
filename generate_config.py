"""
Generate config script

This script provides an intuitive wizard to generate and edit the config.json file for this project
"""

import os.path
import json

config = {}


def load_config():
    # Loads the config into the config variable
    global config
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            config = json.load(f)
    else:
        config = {
            "discord_webhook_url": "",
            "watching": {}
        }
        save_config()


def save_config():
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)


def main_menu():
    # Displays the main menu
    print(f"(1) Discord webhook URL: {config['discord_webhook_url']}")
    print("(2) Edit authors")
    print("(3) Quit")

    option = input("> ")
    if option == "1":
        edit_webhook_url()
    elif option == "2":
        edit_authors()
    elif option == "3":
        quit()
    else:
        print("Invalid input, valid options: 1, 2")
        main_menu()


def edit_webhook_url():
    print("Please enter new Discord webhook URL")
    url = input("> ")
    if url == "":
        print("URL not changed")
    else:
        config["discord_webhook_url"] = url
        save_config()
    main_menu()


def edit_authors():
    # Shows the list of authors in the config, the user can select an author or add a new one
    authors = config["watching"]
    options = list(authors.keys()) + ["Add new author", "Return"]

    for index, option in enumerate(options):
        print(f"({index + 1}) {option}")

    selection = input("> ")

    try:
        selection = int(selection)
    except ValueError:
        print("Invalid number")
        edit_authors()
        return

    # Working out which option they picked (book or an option at the bottom)
    if selection < 1 or selection > len(authors) + 2:
        print("Option is out of range")
        edit_authors()
        return

    if selection <= len(authors):
        # They are selecting an author to edit
        edit_author(options[selection - 1])
        return

    if options[selection - 1] == "Add new author":
        add_author()
        return

    if options[selection - 1] == "Return":
        main_menu()
        return


def edit_author(author_name):
    def edit_languages():
        print("Please enter a list of comma seperated languages that audiobooks should be narrated in,"
              " or 'clear' to clear the list")
        languages = input("> ")

        if languages == "":
            edit_author(author_name)
            return
        elif languages.lower() == "clear":
            author_data["languages"] = []
        else:
            author_data["languages"] = languages.split(", ")

        save_config()
        edit_author(author_name)

    def edit_series_ids():
        print("Please enter a list of comma seperated series ids that audiobooks should belong to,"
              " or 'clear' to clear the list")
        print("To find a series ID, find the series page on Audible, it should follow the structure"
              "\nhttps://www.audible.co.uk/series/*SERIES NAME*/*SERIES ID*")
        series_ids = input("> ")

        if series_ids == "":
            edit_author(author_name)
            return
        elif series_ids.lower() == "clear":
            author_data["series_ids"] = []
        else:
            author_data["series_ids"] = series_ids.split(", ")

        save_config()
        edit_author(author_name)

    author_data = config["watching"][author_name]
    print(f"{author_name}:")
    print(f"(1) Whitelisted languages: {', '.join(author_data['languages'])}")
    print(f"(2) Whitelisted series IDs: {', '.join(author_data['series_ids'])}")
    print("(3) Delete author")
    print("(4) Return")

    selection = input("> ")
    if selection == "1":
        edit_languages()
    elif selection == "2":
        edit_series_ids()
    elif selection == "3":
        # Confirming deletion of author
        if input(f"Delete author {author_name}? (y/N)\n> ").lower() == "y":
            del config["watching"][author_name]
            save_config()
            edit_authors()
        else:
            edit_author(author_name)
    elif selection == "4":
        edit_authors()
    else:
        print("Invalid input")
        edit_author(author_name)


def add_author():
    print("What is the authors name?")
    name = input("> ")

    if name == "":
        print("Cancelled adding author")
        edit_authors()
        return

    if name in config["watching"]:
        print("You are already watching that authors books")
        edit_author(name)
        return

    config["watching"][name] = {"series_ids": [], "languages": []}
    save_config()

    edit_author(name)
    return


if __name__ == "__main__":
    # Loading the config and then launching the menu
    load_config()
    main_menu()
