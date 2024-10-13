# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
import math
import random
from worlds.AutoWorld import World
from BaseClasses import MultiWorld, CollectionState

# Object classes from Manual -- extending AP core -- representing items and locations that are used in generation
from ..Items import ManualItem
from ..Locations import ManualLocation

# Raw JSON data from the Manual apworld, respectively:
#          data/game.json, data/items.json, data/locations.json, data/regions.json
#
from ..Data import game_table, item_table, location_table, region_table

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_category_enabled, is_option_enabled, get_option_value

# calling logging.info("message") anywhere below in this file will output the message to both console and log file
import logging

########################################################################################
## Order of method calls when the world generates:
##    1. create_regions - Creates regions and locations
##    2. create_items - Creates the item pool
##    3. set_rules - Creates rules for accessing regions and locations
##    4. generate_basic - Runs any post item pool options, like place item/category
##    5. pre_fill - Creates the victory location
##
## The create_item method is used by plando and start_inventory settings to create an item from an item name.
## The fill_slot_data method will be used to send data to the Manual client for later use, like deathlink.
########################################################################################



# Called before regions and locations are created. Not clear why you'd want this, but it's here. Victory location is included, but Victory event is not placed yet.
def before_create_regions(world: World, multiworld: MultiWorld, player: int):
    # Get goal location index
    if get_option_value(multiworld, player, "unlock_mode") == 1:
        goal_index = world.victory_names.index("Goal (Final Challenge)")
    elif get_option_value(multiworld, player, "goal_type") == 0:
        goal_index = world.victory_names.index("Goal (Trophy Hunt)")
    else:
        goal_index = world.victory_names.index("Goal (Final Challenge)")

    # Set goal location
    world.options.goal.value = goal_index

# Called after regions and locations are created, in case you want to see or modify that information. Victory location is included.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to remove locations from the world
    locationNamesToRemove = [] # List of location names

    # Add your code here to calculate which locations to remove
    chunks = is_category_enabled(multiworld, player, "Chunks")
    
    if chunks is True:
        classic = is_category_enabled(multiworld, player, "Classic")
        nitro = is_category_enabled(multiworld, player, "Nitro")
        bonus = is_category_enabled(multiworld, player, "Bonus")
        tracksIncluded = is_category_enabled(multiworld, player, "Tracks")
        cups = is_category_enabled(multiworld, player, "Cups")
        timeTrial = is_category_enabled(multiworld, player, "Time Trial")
        battle = is_category_enabled(multiworld, player, "Battle")

        numTracks = 0
        if tracksIncluded is True:
            if classic is True:
                numTracks += 18
            if nitro is True:
                numTracks += 13
            if bonus is True:
                numTracks += 8

        numCups = 0
        if cups is True:
            if classic is True:
                numCups += 4
            if nitro is True:
                numCups += 3
            if bonus is True:
                numCups += 1
                if classic is True and nitro is True:
                    numCups += 3

        countLeft = numTracks
        for i in range(1, numCups+1):
            chunkTracks = math.ceil(countLeft/(numCups-(i-1)))
            countLeft -= chunkTracks
            for j in range(chunkTracks+1, 9):
                locationNamesToRemove.append(f"Chunk {i} Track {j}")
        for i in range(numCups+1, 12):
            for j in range(1, 9):
                locationNamesToRemove.append(f"Chunk {i} Track {j}")
        for i in range(numCups, 12):
            locationNamesToRemove.append(f"Chunk {i} Cup")
    
    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in locationNamesToRemove:
                    region.locations.remove(location)
    if hasattr(multiworld, "clear_location_cache"):
        multiworld.clear_location_cache()

# The item pool before starting items are processed, in case you want to see the raw item pool at that stage
def before_create_items_starting(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

# The item pool after starting items are processed but before filler is added, in case you want to see the raw item pool at that stage
def before_create_items_filler(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    # Use this hook to remove items from the item pool
    itemNamesToRemove = [] # List of item names

    # Add your code here to calculate which items to remove.
    #
    # Because multiple copies of an item can exist, you need to add an item name
    # to the list multiple times if you want to remove multiple copies of it.
    
    # Get Trophy Information
    classic = is_category_enabled(multiworld, player, "Classic")
    nitro = is_category_enabled(multiworld, player, "Nitro")
    bonus = is_category_enabled(multiworld, player, "Bonus")
    easy = is_category_enabled(multiworld, player, "Easy")
    medium = is_category_enabled(multiworld, player, "Medium")
    hard = is_category_enabled(multiworld, player, "Hard")
    tracksIncluded = is_category_enabled(multiworld, player, "Tracks")
    cups = is_category_enabled(multiworld, player, "Cups")
    cups_items = is_category_enabled(multiworld, player, "Cups Items")
    timeTrial = is_category_enabled(multiworld, player, "Time Trial")
    battle = is_category_enabled(multiworld, player, "Battle")
    chunks = is_category_enabled(multiworld, player, "Chunks")
    final_challenge = get_option_value(multiworld, player, "goal_type")
    if chunks:
        final_challenge = 1
    characters = is_category_enabled(multiworld, player, "Characters")
    oxide_edition = get_option_value(multiworld, player, "oxide_edition")
    
    if not tracksIncluded and not cups and not battle:
        raise Exception("No valid mode set for play! Single race and/or Cups must be enabled.")

    track_list = []
    if tracksIncluded is True:
        if classic is True:
            track_list.append("Crash Cove")
            track_list.append("Mystery Caves")
            track_list.append("Sewer Speedway")
            track_list.append("Roo's Tubes")
            track_list.append("Coco Park")
            track_list.append("Tiger Temple")
            track_list.append("Papu's Pyramid")
            track_list.append("Dingo Canyon")
            track_list.append("Polar Pass")
            track_list.append("Tiny Arena")
            track_list.append("Dragon Mines")
            track_list.append("Blizzard Bluff")
            track_list.append("Hot Air Skyway")
            track_list.append("Cortex Castle")
            track_list.append("N. Gin Labs")
            track_list.append("Slide Coliseum")
            track_list.append("Turbo Track")
            track_list.append("Oxide Station")
        if nitro is True:
            track_list.append("Inferno Island")
            track_list.append("Jungle Boogie")
            track_list.append("Clockwork Wumpa")
            track_list.append("Android Alley")
            track_list.append("Electron Avenue")
            track_list.append("Deep Sea Driving")
            track_list.append("Thunder Struck")
            track_list.append("Tiny Temple")
            track_list.append("Meteor Gorge")
            track_list.append("Barin Ruins")
            track_list.append("Out Of Time")
            track_list.append("Assembly Lane")
            track_list.append("Hyper Spaceway")
        if bonus is True:
            track_list.append("Twilight Tour")
            track_list.append("Prehistoric Playground")
            track_list.append("Spyro Circuit")
            track_list.append("Nina's Nightmare")
            track_list.append("Koala Carnival")
            track_list.append("Gingerbread Joyride")
            track_list.append("Megamix Mania")
            track_list.append("Drive-Thru Danger")

    timetrial_locs = 0
    if timeTrial is True:
        ghosts = get_option_value(multiworld, player, "included_ghosts") + 1
        timetrial_locs = len(track_list) * ghosts

    cups_list = []
    if cups is True:
        if classic is True:
            cups_list.append("Wumpa Cup")
            cups_list.append("Nitro Cup")
            cups_list.append("Crystal Cup")
            cups_list.append("Crash Cup")
        if nitro is True:
            cups_list.append("Velo Cup")
            cups_list.append("Aku Cup")
            cups_list.append("Uka Cup")
        if bonus is True:
            cups_list.append("Bonus Cup")
            if classic is True and nitro is True:
                cups_list.append("Lost Cup")
                cups_list.append("Desert Cup")
                cups_list.append("Space Cup")

    battle_list = []
    if battle is True:
        if classic is True:
            battle_list.append("Skull Rock")
            battle_list.append("Nitro Court")
            battle_list.append("Parking Lot")
            battle_list.append("Rocky Road")
            battle_list.append("Lab Basement")
            battle_list.append("Rampage Ruins")
            battle_list.append("The North Bowl")
        if nitro is True:
            battle_list.append("Temple Turmoil")
            battle_list.append("Frozen Frenzy")
            battle_list.append("Desert Storm")
            battle_list.append("Magnetic Mayhem")
            battle_list.append("Terra Drome")
    
    tracks = len(track_list) + len(cups_list) + len(battle_list) - 1
    if chunks is True:
        tracks = len(track_list) + len(battle_list)

    difficulties = 0
    if easy is True:
        difficulties += 1
    if medium is True:
        difficulties += 1
    if hard is True:
        difficulties += 1

    if not chunks:
        max_trophies = round((tracks * 3 * difficulties) - tracks - (difficulties * tracks / 3))
    else:
        max_trophies = round(((tracks * 3 * difficulties) + timetrial_locs) * 8 / 9)
    multiplier = get_option_value(multiworld, player, "percentage_trophies")
    trophies = round(max_trophies * multiplier / 100)
    
    bad_trophies = 500-max_trophies
    for _ in range(bad_trophies):
        itemNamesToRemove.append("Trophy")
    
    # Get the victory item out of the pool:
    victory_item = next(i for i in item_pool if i.name == "Ultimate Trophy (Victory)")
    item_pool.remove(victory_item)
    
    # Get the victory location and place the victory item there
    gather_loc_list = ["Gather 1 Trophy"] # A list of all the victory location names in order
    for i in range(2, 501):
        gather_loc_list.append(f"Gather {i} Trophies")
    
    for i in range(len(gather_loc_list)):
        if str(trophies) in gather_loc_list[i]:
            victory_id = i
            break

    gather_location_name = gather_loc_list[victory_id]
    gather_location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == gather_location_name)
    final_track_location_name = ""

    # get the final track/cup name, add the unneeded locations to the gather_loc_list for deletion
    if final_challenge:
        if cups is True:
            final_track_name = random.choice(list(cups_list))
            for d in ["Easy", "Medium", "Hard"]:
                if locals()[d.lower()] is True:
                    for p in ["Top 5", "Top 3", "1st"]:
                        gather_loc_list.append(f"{final_track_name} - {d} - {p}")
        else:
            final_track_name = random.choice(track_list)
            for d in ["Easy", "Medium", "Hard"]:
                if locals()[d.lower()] is True:
                    for p in ["Top 5", "Top 3", "1st"]:
                        gather_loc_list.append(f"{final_track_name} - {d} - {p}")

        # assign Ultimate Trophy item and final track item to the final track and gather locations respectively
        final_track_location_name = gather_loc_list[-1]
        final_track_location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == final_track_location_name)
        final_track_item = next(i for i in item_pool if i.name == final_track_name)
        item_pool.remove(final_track_item)

        gather_location.place_locked_item(final_track_item)
        final_track_location.place_locked_item(victory_item)
    else:
        gather_location.place_locked_item(victory_item)
    
    #If using Chunks, remove eccess Chunk Unlocks, then assign the rest to the cup locations.
    if chunks is True:
        diff = ""
        if hard:
            diff = "Hard"
        elif medium:
            diff = "Medium"
        elif easy:
            diff = "Easy"
        
        for _ in range(len(cups_list), 11): # Remove excess Chunk Unlock items
            item = next(i for i in item_pool if i.name == "Chunk Unlock")
            item_pool.remove(item)
        for cup in cups_list: # Assign the remaining Chunk Unlock items to the cup locations
            if cup in final_track_location_name:
                continue
            location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == f"{cup} - {diff} - 1st")
            item = next(i for i in item_pool if i.name == "Chunk Unlock")
            item_pool.remove(item)
            location.place_locked_item(item)
            # add extra cup locations to gather_loc_list for deletion
            if easy:
                if medium or hard:
                    gather_loc_list.append(f"{cup} - Easy - 1st")
            if medium:
                if hard:
                    gather_loc_list.append(f"{cup} - Medium - 1st")

    
    # Remove the extra gather locations and unneeded final track locations
    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in gather_loc_list and location.name != gather_location_name and location.name != final_track_location_name:
                    region.locations.remove(location)

    # Handle Nitros Oxide Edition characters
    if characters:
        if (not oxide_edition) and characters < 3 and classic:
            itemNamesToRemove.append("Nitros Oxide")
        if (not oxide_edition) and characters < 4 and nitro:
            itemNamesToRemove.append("Zam")
            itemNamesToRemove.append("Zem")

    for itemName in itemNamesToRemove:
        item = next(i for i in item_pool if i.name == itemName)
        item_pool.remove(item)
    
    return item_pool

    # Some other useful hook options:

    ## Place an item at a specific location
    # location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == "Location Name")
    # item_to_place = next(i for i in item_pool if i.name == "Item Name")
    # location.place_locked_item(item_to_place)
    # item_pool.remove(item_to_place)

# The complete item pool prior to being set for generation is provided here, in case you want to make changes to it
def after_create_items(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    return item_pool

# Called before rules for accessing regions and locations are created. Not clear why you'd want this, but it's here.
def before_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after rules for accessing regions and locations are created, in case you want to see or modify that information.
def after_set_rules(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to modify the access rules for a given location

    multiplier = get_option_value(multiworld, player, "percentage_trophies")/100
    classic = is_category_enabled(multiworld, player, "Classic")
    nitro = is_category_enabled(multiworld, player, "Nitro")
    bonus = is_category_enabled(multiworld, player, "Bonus")
    easy = is_category_enabled(multiworld, player, "Easy")
    medium = is_category_enabled(multiworld, player, "Medium")
    hard = is_category_enabled(multiworld, player, "Hard")
    tracksIncluded = is_category_enabled(multiworld, player, "Tracks")
    cups = is_category_enabled(multiworld, player, "Cups")
    timeTrial = is_category_enabled(multiworld, player, "Time Trial")
    battle = is_category_enabled(multiworld, player, "Battle")
    chunks = is_category_enabled(multiworld, player, "Chunks")

    numTracks = 0
    if tracksIncluded is True:
        if classic is True:
            numTracks += 18
        if nitro is True:
            numTracks += 13
        if bonus is True:
            numTracks += 8

    timetrial_locs = 0
    if timeTrial is True:
        ghosts = get_option_value(multiworld, player, "included_ghosts") + 1
        timetrial_locs = numTracks * ghosts

    numCups = 0
    if cups is True:
        if classic is True:
            numCups += 4
        if nitro is True:
            numCups += 3
        if bonus is True:
            numCups += 1
            if classic is True and nitro is True:
                numCups += 3

    difficulties = 0
    if easy is True:
        difficulties += 1
    if medium is True:
        difficulties += 1
    if hard is True:
        difficulties += 1

    if not chunks:
        max_trophies = round((numTracks * 3 * difficulties) - numTracks - (difficulties * numTracks / 3))
    else:
        max_trophies = round(((numTracks * 3 * difficulties) + timetrial_locs) * 8 / 9)

    def needed_trophies(chunkNum):
        reqTrophies = round(multiplier * max_trophies / numCups * chunkNum)
        return reqTrophies

    def req_trophies1(state: CollectionState) -> bool:
        if state.count("Trophy", player) >= needed_trophies(1):
            return True
        return False
    
    def req_trophies2(state: CollectionState) -> bool:
        if state.count("Trophy", player) >= needed_trophies(2):
            return True
        return False
    
    def req_trophies3(state: CollectionState) -> bool:
        if state.count("Trophy", player) >= needed_trophies(3):
            return True
        return False
    
    def req_trophies4(state: CollectionState) -> bool:
        if state.count("Trophy", player) >= needed_trophies(4):
            return True
        return False
    
    def req_trophies5(state: CollectionState) -> bool:
        if state.count("Trophy", player) >= needed_trophies(5):
            return True
        return False
    
    def req_trophies6(state: CollectionState) -> bool:
        if state.count("Trophy", player) >= needed_trophies(6):
            return True
        return False
    
    def req_trophies7(state: CollectionState) -> bool:
        if state.count("Trophy", player) >= needed_trophies(7):
            return True
        return False
    
    def req_trophies8(state: CollectionState) -> bool:
        if state.count("Trophy", player) >= needed_trophies(8):
            return True
        return False
    
    def req_trophies9(state: CollectionState) -> bool:
        if state.count("Trophy", player) >= needed_trophies(9):
            return True
        return False
    
    def req_trophies10(state: CollectionState) -> bool:
        if state.count("Trophy", player) >= needed_trophies(10):
            return True
        return False
    
    def req_trophies11(state: CollectionState) -> bool:
        if state.count("Trophy", player) >= needed_trophies(11):
            return True
        return False
    
    
    if chunks is True:
        for i in range(1, numCups):
            chunk_loc = f"Chunk {i} Cup"
            req_func = f"req_trophies{i}"
            location = multiworld.get_location(chunk_loc, player)
            location.access_rule = locals()[req_func]

    ## Common functions:
    # location = world.get_location(location_name, player)
    # location.access_rule = Example_Rule

    ## Combine rules:
    # old_rule = location.access_rule
    # location.access_rule = lambda state: old_rule(state) and Example_Rule(state)
    # OR
    # location.access_rule = lambda state: old_rule(state) or Example_Rule(state)

# The item name to create is provided before the item is created, in case you want to make changes to it
def before_create_item(item_name: str, world: World, multiworld: MultiWorld, player: int) -> str:
    return item_name

# The item that was created is provided after creation, in case you want to modify the item
def after_create_item(item: ManualItem, world: World, multiworld: MultiWorld, player: int) -> ManualItem:
    return item

# This method is run towards the end of pre-generation, before the place_item options have been handled and before AP generation occurs
def before_generate_basic(world: World, multiworld: MultiWorld, player: int) -> list:
    pass

# This method is run at the very end of pre-generation, once the place_item options have been handled and before AP generation occurs
def after_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This is called before slot data is set and provides an empty dict ({}), in case you want to modify it before Manual does
def before_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called after slot data is set and provides the slot data at the time, in case you want to check and modify it after Manual is done with it
def after_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called right at the end, in case you want to write stuff to the spoiler log
def before_write_spoiler(world: World, multiworld: MultiWorld, spoiler_handle) -> None:
    pass
