import math

from .functions import get_battle_list, get_cup_list, get_max_trophies, get_track_list, num_difficulties

# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from worlds.AutoWorld import World
from BaseClasses import MultiWorld, CollectionState, Item

# Object classes from Manual -- extending AP core -- representing items and locations that are used in generation
from ..Items import ManualItem
from ..Locations import ManualLocation

# Raw JSON data from the Manual apworld, respectively:
#          data/game.json, data/items.json, data/locations.json, data/regions.json
#
from ..Data import game_table, item_table, location_table, region_table

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_category_enabled,is_option_enabled, get_option_value, format_state_prog_items_key, ProgItemsCat

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

# Use this function to change the valid filler items to be created to replace item links or starting items.
# Default value is the `filler_item_name` from game.json
def hook_get_filler_item_name(world: World, multiworld: MultiWorld, player: int) -> str | bool:
    return False

# Called before regions and locations are created. Not clear why you'd want this, but it's here. Victory location is included, but Victory event is not placed yet.
def before_create_regions(world: World, multiworld: MultiWorld, player: int):
    # Get goal location index
    if get_option_value(multiworld, player, "unlock_mode") == 1: 
        # If using Chunks, the goal is always the Final Challenge
        goal_index = world.victory_names.index("Goal (Final Challenge)")
    elif get_option_value(multiworld, player, "goal_type") == 0:
        # Get the number of trophies needed to win
        max_trophies = get_max_trophies(multiworld, player)
        multiplier = get_option_value(multiworld, player, "percentage_trophies")
        trophies = round(max_trophies * multiplier / 100)
        # If trophies is 0, set it to 1
        if trophies <= 0:
            trophies = 1
        if trophies == 1:
            goal_index = world.victory_names.index(f"Goal (Gather 1 Trophy)")
        else:
            goal_index = world.victory_names.index(f"Goal (Gather {trophies} Trophies)")
    else:
        # If using the Final Challenge, the goal is always the Final Challenge
        goal_index = world.victory_names.index("Goal (Final Challenge)")

    # Set goal location
    world.options.goal.value = goal_index

# Called after regions and locations are created, in case you want to see or modify that information. Victory location is included.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to remove locations from the world
    locationNamesToRemove: list[str] = [] # List of location names

    # Add your code here to calculate which locations to remove
    chunks = is_category_enabled(multiworld, player, "Chunks")
    
    if chunks is True:

        numTracks = len(get_track_list(multiworld, player))
        numCups = len(get_cup_list(multiworld, player))

        countLeft = numTracks
        for i in range(1, numCups + 1):
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
    # if hasattr(multiworld, "clear_location_cache"):
    #     multiworld.clear_location_cache()

# This hook allows you to access the item names & counts before the items are created. Use this to increase/decrease the amount of a specific item in the pool
# Valid item_config key/values:
# {"Item Name": 5} <- This will create qty 5 items using all the default settings
# {"Item Name": {"useful": 7}} <- This will create qty 7 items and force them to be classified as useful
# {"Item Name": {"progression": 2, "useful": 1}} <- This will create 3 items, with 2 classified as progression and 1 as useful
# {"Item Name": {0b0110: 5}} <- If you know the special flag for the item classes, you can also define non-standard options. This setup
#       will create 5 items that are the "useful trap" class
# {"Item Name": {ItemClassification.useful: 5}} <- You can also use the classification directly
def before_create_items_all(item_config: dict[str, int|dict], world: World, multiworld: MultiWorld, player: int) -> dict[str, int|dict]:
    return item_config

# The item pool before starting items are processed, in case you want to see the raw item pool at that stage
def before_create_items_starting(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    itemNamesToRemove = [] # List of item names
    
    debug = False

    classic = is_category_enabled(multiworld, player, "Classic")
    nitro = is_category_enabled(multiworld, player, "Nitro")
    easy = is_category_enabled(multiworld, player, "Easy")
    medium = is_category_enabled(multiworld, player, "Medium")
    hard = is_category_enabled(multiworld, player, "Hard")
    cups = is_category_enabled(multiworld, player, "Cups")
    cup_items = is_category_enabled(multiworld, player, "Cups Items")
    timeTrial = is_category_enabled(multiworld, player, "Time Trial")
    chunks = is_category_enabled(multiworld, player, "Chunks")
    final_challenge = get_option_value(multiworld, player, "goal_type")
    if chunks:
        final_challenge = 1
    characters = is_category_enabled(multiworld, player, "Characters")
    characters_value = get_option_value(multiworld, player, "randomize_characters")
    oxide_edition = get_option_value(multiworld, player, "oxide_edition")
    
    track_list = get_track_list(multiworld, player)
    cup_list = get_cup_list(multiworld, player)
    battle_list = get_battle_list(multiworld, player)
    
    if timeTrial:
        ghosts = get_option_value(multiworld, player, "included_ghosts")
         # Remove excess Progressive Time Trial Ghosts
        if ghosts >= 2 and not chunks:
            for track in track_list:
                for _ in range(ghosts, 4):
                    if debug:
                        print(f"Adding '{track} - Progressive Ghost' to itemNamesToRemove")
                    itemNamesToRemove.append(f"{track} - Progressive Ghost")

    # Starting Tracks
    starting_list = []
    starting_list.extend(track_list)
    if cup_items:
        starting_list.extend(cup_list)
    starting_list.extend(battle_list)
    num_starting_tracks = get_option_value(multiworld, player, "starting_locations")
    if chunks:
        num_starting_tracks = 0
    for _ in range(num_starting_tracks):
        strack = world.random.choice(list(starting_list))
        item = next(i for i in item_pool if i.name == strack)
        item_pool.remove(item)
        multiworld.push_precollected(item)
        if strack in track_list:
            track_list.remove(strack)
        if strack in cup_list:
            cup_list.remove(strack)
        if strack in battle_list:
            battle_list.remove(strack)
        starting_list.remove(strack)

    max_trophies = get_max_trophies(multiworld, player)
    multiplier = get_option_value(multiworld, player, "percentage_trophies")
    trophies = round(max_trophies * multiplier / 100)
    if trophies <= 0:
        trophies = 1
    
    bad_trophies = 500-max_trophies
    for _ in range(bad_trophies):
        itemNamesToRemove.append("Trophy")
    
    final_track_location_name = ""
    gather_loc_list = []
    if not hasattr(world.multiworld, "generation_is_fake"):
        if final_challenge:
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
            if cups is True:
                final_track_name = world.random.choice(list(cup_list))
                for d in ["Easy", "Medium", "Hard"]:
                    if locals()[d.lower()] is True:
                        for p in ["Top 5", "Top 3", "1st"]:
                            gather_loc_list.append(f"{final_track_name} - {d} - {p}")
            else:
                final_track_name = world.random.choice(track_list)
                if timeTrial and not chunks:
                    ghost_list = ["N. Tropy", "Nitros Oxide", "Emperor Velo XXVII", "Beenox Developer"]
                    for i in range(0, ghosts):
                        gather_loc_list.append(f"{final_track_name} Time Trial - Beat {ghost_list[i]}")
                        # Remove ghost items
                        if ghosts == 1:
                            if debug:
                                print(f"Adding {final_track_name} - N. Tropy to itemNamesToRemove")
                            itemNamesToRemove.append(f"{final_track_name} - N. Tropy")
                        else:
                            if debug:
                                print(f"Adding {final_track_name} - Progressive Ghost to itemNamesToRemove")
                            itemNamesToRemove.append(f"{final_track_name} - Progressive Ghost")
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
    
            #If using Chunks, remove eccess Chunk Unlocks, then assign the rest to the cup locations.
            if chunks is True:
                diff = ""
                if hard:
                    diff = "Hard"
                elif medium:
                    diff = "Medium"
                elif easy:
                    diff = "Easy"
                
                for _ in range(len(cup_list), 11): # Remove excess Chunk Unlock items
                    item = next(i for i in item_pool if i.name == "Chunk Unlock")
                    item_pool.remove(item)
                for cup in cup_list: # Assign the remaining Chunk Unlock items to the cup locations
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
                    pass

    # Handle Nitros Oxide Edition characters
    if characters:
        if (not oxide_edition) and characters_value < 3 and classic:
            itemNamesToRemove.append("Nitros Oxide")
        if (not oxide_edition) and characters_value < 4 and nitro:
            itemNamesToRemove.append("Zam")
            itemNamesToRemove.append("Zem")

    # Remove items from the pool
    if debug:
        print("Removing items from pool:")
    for itemName in itemNamesToRemove:
        if debug:
            print(itemName)
        item = next(i for i in item_pool if i.name == itemName)
        item_pool.remove(item)
    
    if debug:
        numTrophies = 0
        print()
        print("--Item Pool--")
        for item in item_pool:
            if item.name == "Trophy":
                numTrophies += 1
            else:
                print(item.name)
        print(f"Trophy x{numTrophies}")
        print()
        if not hasattr(world.multiworld, "generation_is_fake"):
            input("Press enter to continue...")
            print()

    return item_pool

# The item pool after starting items are processed but before filler is added, in case you want to see the raw item pool at that stage
def before_create_items_filler(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    # Use this hook to remove items from the item pool
    itemNamesToRemove: list[str] = [] # List of item names

    # Add your code here to calculate which items to remove.
    #
    # Because multiple copies of an item can exist, you need to add an item name
    # to the list multiple times if you want to remove multiple copies of it.

    debug = False
    
    if debug:
        print("Removing items from pool before filler:")
    for itemName in itemNamesToRemove:
        if debug:
            print(itemName)
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
    multiplier = get_option_value(multiworld, player, "percentage_trophies") / 100
    chunks = is_category_enabled(multiworld, player, "Chunks")
    numCups = len(get_cup_list(multiworld, player))
        
    max_trophies = get_max_trophies(multiworld, player)

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
def before_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This method is run at the very end of pre-generation, once the place_item options have been handled and before AP generation occurs
def after_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This method is run every time an item is added to the state, can be used to modify the value of an item.
# IMPORTANT! Any changes made in this hook must be cancelled/undone in after_remove_item
def after_collect_item(world: World, state: CollectionState, Changed: bool, item: Item):
    # the following let you add to the Potato Item Value count
    # if item.name == "Cooked Potato":
    #     state.prog_items[item.player][format_state_prog_items_key(ProgItemsCat.VALUE, "Potato")] += 1
    pass

# This method is run every time an item is removed from the state, can be used to modify the value of an item.
# IMPORTANT! Any changes made in this hook must be first done in after_collect_item
def after_remove_item(world: World, state: CollectionState, Changed: bool, item: Item):
    # the following let you undo the addition to the Potato Item Value count
    # if item.name == "Cooked Potato":
    #     state.prog_items[item.player][format_state_prog_items_key(ProgItemsCat.VALUE, "Potato")] -= 1
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

# This is called when you want to add information to the hint text
def before_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:

    ### Example way to use this hook:
    # if player not in hint_data:
    #     hint_data.update({player: {}})
    # for location in multiworld.get_locations(player):
    #     if not location.address:
    #         continue
    #
    #     use this section to calculate the hint string
    #
    #     hint_data[player][location.address] = hint_string

    pass

def after_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:
    pass
