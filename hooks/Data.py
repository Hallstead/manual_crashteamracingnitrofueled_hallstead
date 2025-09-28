import csv
import pkgutil
from .functions import trophies_in_pool

# called after the game.json file has been loaded
def after_load_game_file(game_table: dict) -> dict:
    return game_table
# called after the items.json file has been loaded, before any item loading or processing has occurred
# if you need access to the items after processing to add ids, etc., you should use the hooks in World.py
def after_load_item_file(item_table: list) -> list:
    return item_table

# NOTE: Progressive items are not currently supported in Manual. Once they are,
#       this hook will provide the ability to meaningfully change those.
def after_load_progressive_item_file(progressive_item_table: list) -> list:
    return progressive_item_table

# called after the locations.json file has been loaded, before any location loading or processing has occurred
# if you need access to the locations after processing to add ids, etc., you should use the hooks in World.py
def after_load_location_file(location_table: list) -> list:
    location = {}
    location["name"] = "Gather 1 Trophy"
    location["category"] = ["((~Objective~))"]
    location["requires"] = "|@Trophies:1|"
    location_table.append(location)
    for i in range(2, trophies_in_pool + 1):
        location = {}
        location["name"] = f"Gather {i} Trophies"
        location["category"] = ["((~Objective~))"]
        location["requires"] = f"|@Trophies:{i}|"
        location_table.append(location)

    location = {}
    location["name"] = "Goal (Gather 1 Trophy)"
    location["category"] = ["((~Goal~))"]
    location["requires"] = "|@Trophies:1|"
    location["victory"] = True
    location_table.append(location)
    for i in range(2, trophies_in_pool + 1):
        location = {}
        location["name"] = f"Goal (Gather {i} Trophies)"
        location["category"] = ["((~Goal~))"]
        location["requires"] = f"|@Trophies:{i}|"
        location["victory"] = True
        location_table.append(location)

    csvFile = csv.DictReader(pkgutil.get_data(__name__, "locations.csv").decode().splitlines(), delimiter=';')
    for line in csvFile:
        if line["name"] == "":
            continue
        location = {}
        location["name"] = line["name"]
        location["category"] = line["category"].split(", ")
        if line["requires"] != "":
            location["requires"] = line["requires"]
        else:
            location["requires"] = []
        if line["place_item"] != "":
            location["place_item"] = line["place_item"].split(", ")
        if line["place_item_category"] != "":
            location["place_item_category"] = line["place_item_category"].split(", ")
        location_table.append(location)
    
    return location_table

# called after the locations.json file has been loaded, before any location loading or processing has occurred
# if you need access to the locations after processing to add ids, etc., you should use the hooks in World.py
def after_load_region_file(region_table: dict) -> dict:
    return region_table

# called after the categories.json file has been loaded
def after_load_category_file(category_table: dict) -> dict:
    return category_table

# called after the categories.json file has been loaded
def after_load_option_file(option_table: dict) -> dict:
    # option_table["core"] is the dictionary of modification of existing options
    # option_table["user"] is the dictionary of custom options
    return option_table

# called after the meta.json file has been loaded and just before the properties of the apworld are defined. You can use this hook to change what is displayed on the webhost
# for more info check https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md#webworld-class
def after_load_meta_file(meta_table: dict) -> dict:
    return meta_table

# called when an external tool (eg Universal Tracker) ask for slot data to be read
# use this if you want to restore more data
# return True if you want to trigger a regeneration if you changed anything
def hook_interpret_slot_data(world, player: int, slot_data: dict[str, any]) -> dict | bool:
    return False
