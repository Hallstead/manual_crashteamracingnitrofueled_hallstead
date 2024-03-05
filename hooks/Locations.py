import csv
import pkgutil

# called after the locations.json has been imported, but before ids, etc. have been assigned
# if you need access to the locations after processing to add ids, etc., you should use the hooks in World.py
def before_location_table_processed(location_table: list) -> list:
    location = {}
    location["name"] = "Gather 1 Trophy"
    location["category"] = ["((~Goal~))"]
    location["requires"] = "|@Trophies:1|"
    location_table.append(location)
    for i in range(2, 501):
        location = {}
        location["name"] = f"Gather {i} Trophies"
        location["category"] = ["((~Goal~))"]
        location["requires"] = f"|@Trophies:{i}|"
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
    
    for i in range (1, 12):
        for j in range(1, 9):
            location = {}
            location["name"] = f"Chunk {i} Track {j}"
            location["category"] = ["Chunks", f"Chunk {i}"]
            location["requires"] = f"|Chunk Unlock:{i}|"
            location["place_item_category"] = ["Tracks", "Arenas"]
            location_table.append(location)
        location = {}
        location["name"] = f"Chunk {i} Cup"
        location["category"] = ["Chunks", f"Chunk {i}"]
        location["requires"] = []
        location["place_item_category"] = ["Cups"]
        location_table.append(location)

    return location_table
