# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
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
from ..Helpers import is_option_enabled, get_option_value, is_category_enabled

import random

########################################################################################
## Order of method calls when the world generates:
##    1. create_regions - Creates regions and locations
##    2. set_rules - Creates rules for accessing regions and locations
##    3. generate_basic - Creates the item pool and runs any place_item options
##    4. pre_fill - Creates the victory location
##
## The create_item method is used by plando and start_inventory settings to create an item from an item name.
## The fill_slot_data method will be used to send data to the Manual client for later use, like deathlink.
########################################################################################



# Called before regions and locations are created. Not clear why you'd want this, but it's here.
def before_create_regions(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after regions and locations are created, in case you want to see or modify that information.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to remove locations from the world
    locationNamesToRemove = [] # List of location names
    
    # Add your code here to calculate which locations to remove
    
    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in locationNamesToRemove:
                    region.locations.remove(location)
    if hasattr(multiworld, "clear_location_cache"):
        multiworld.clear_location_cache()

# Called before rules for accessing regions and locations are created. Not clear why you'd want this, but it's here.
def before_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after rules for accessing regions and locations are created, in case you want to see or modify that information.
def after_set_rules(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to modify the access rules for a given location
    
    def Example_Rule(state: CollectionState) -> bool:
        # Calculated rules take a CollectionState object and return a boolean 
        # True if the player can access the location
        # CollectionState is defined in BaseClasses
        return True
    
    ## Common functions:
    # location = world.get_location(location_name, player)
    # location.access_rule = Example_Rule
    
    ## Combine rules:
    # old_rule = location.access_rule
    # location.access_rule = lambda state: old_rule(state) and Example_Rule(state)
    # OR
    # location.access_rule = lambda state: old_rule(state) or Example_Rule(state)

# The complete item pool prior to being set for generation is provided here, in case you want to make changes to it
def before_generate_basic(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
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
    timeTrial = is_category_enabled(multiworld, player, "Time Trial")
    battle = is_category_enabled(multiworld, player, "Battle")

    if not tracksIncluded and not cups and not battle:
        raise Exception("No mode set for play!")

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

    timetrial = 0
    if timeTrial is True:
        timetrial = len(track_list)

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

    difficulties = 0
    if easy is True:
        difficulties += 1
    if medium is True:
        difficulties += 1
    if hard is True:
        difficulties += 1

    max_trophies = round((tracks * 3 * difficulties) - tracks - (difficulties * tracks / 3))
    multiplier = get_option_value(multiworld, player, "percentage_trophies")
    trophies = round(max_trophies * multiplier / 100)

    bad_trophies = 500-max_trophies
    for i in range(bad_trophies):
        item = next(i for i in item_pool if i.name == "Trophy")
        item_pool.remove(item)
        #itemNamesToRemove.append("Trophy")

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

    # get the final track/cup name, add the unneeded locations to the gather_loc_list for deletion
    if cups is True:
        final_track_name = random.choice(list(cups_list))
        for d in ["Easy", "Medium", "Hard"]:
            if locals()[d.lower()] is True:
                for p in ["5th", "3rd", "1st"]:
                    gather_loc_list.append(f"{final_track_name} - {d} - {p}")
    else:
        final_track_name = random.choice(track_list)
        for d in ["Easy", "Medium", "Hard"]:
            if locals()[d.lower()] is True:
                for p in ["5th", "3rd", "1st"]:
                    gather_loc_list.append(f"{final_track_name} - {d} - {p}")

    # assign Ultimate Trophy item and final track item to the final track and gather locations respectively
    final_track_location_name = gather_loc_list[-1]
    final_track_location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == final_track_location_name)
    final_track_item = next(i for i in item_pool if i.name == final_track_name)
    item_pool.remove(final_track_item)
        
    gather_location_name = gather_loc_list[victory_id]
    gather_location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == gather_location_name)
    gather_location.place_locked_item(final_track_item)
    final_track_location.place_locked_item(victory_item)

    # Remove the extra gather locations and unneeded final track locations
    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in gather_loc_list and location.name != gather_location_name and location.name != final_track_location_name:
                    region.locations.remove(location)

    #for itemName in itemNamesToRemove:
    #    item = next(i for i in item_pool if i.name == itemName)
    #    item_pool.remove(item)
    
    return item_pool
    
    # Some other useful hook options:
    
    ## Place an item at a specific location
    # location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == "Location Name")
    # item_to_place = next(i for i in item_pool if i.name == "Item Name")
    # location.place_locked_item(item_to_place)
    # item_pool.remove(item_to_place)

# This method is run at the very end of pre-generation, once the place_item options have been handled and before AP generation occurs
def after_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This method is called before the victory location has the victory event placed and locked
def before_pre_fill(world: World, multiworld: MultiWorld, player: int):
    pass

# This method is called after the victory location has the victory event placed and locked
def after_pre_fill(world: World, multiworld: MultiWorld, player: int):
    pass

# The item name to create is provided before the item is created, in case you want to make changes to it
def before_create_item(item_name: str, world: World, multiworld: MultiWorld, player: int) -> str:
    return item_name

# The item that was created is provided after creation, in case you want to modify the item
def after_create_item(item: ManualItem, world: World, multiworld: MultiWorld, player: int) -> ManualItem:
    return item

# This is called before slot data is set and provides an empty dict ({}), in case you want to modify it before Manual does
def before_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called after slot data is set and provides the slot data at the time, in case you want to check and modify it after Manual is done with it
def after_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data