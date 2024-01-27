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
    
    # Get the victory item out of the pool:
    victory_item = next(i for i in item_pool if i.name == "Ultimate Trophy (Victory)")
    item_pool.remove(victory_item)
    
    # Get Trophy Information
    tracks = 0
    classic = is_category_enabled(multiworld, player, "Classic")
    nitro = is_category_enabled(multiworld, player, "Nitro")
    bonus = is_category_enabled(multiworld, player, "Bonus")

    if classic is True:
        tracks += 18
    if nitro is True:
        tracks += 13
    if bonus is True:
        tracks += 8

    timetrial = 0
    if is_category_enabled(multiworld, player, "Time Trial") is True:
        timetrial = tracks

    if is_category_enabled(multiworld, player, "Cups") is True:
        if classic is True:
            tracks += 4
        if nitro is True:
            tracks += 3
        if bonus is True:
            tracks += 1
            if classic is True and nitro is True:
                tracks += 3
    
    difficulties = 0
    if is_category_enabled(multiworld, player, "Easy") is True:
        difficulties += 1
    if is_category_enabled(multiworld, player, "Medium") is True:
        difficulties += 1
    if is_category_enabled(multiworld, player, "Hard") is True:
        difficulties += 1

    max_trophies = round((tracks * 3 * difficulties) - tracks - (difficulties * tracks / 3))
    multiplier = get_option_value(multiworld, player, "percentage_trophies")
    trophies = round(max_trophies * multiplier / 100)

    bad_trophies = 500-max_trophies
    for i in range(bad_trophies):
        item = next(i for i in item_pool if i.name == "Trophy")
        item_pool.remove(item)
        #itemNamesToRemove.append("Trophy")

    # Get the victory location and place the victory item there
    victory_loc_list = ["Gather 1 Trophy"] # A list of all the victory location names in order
    for i in range(2, 501):
        victory_loc_list.append(f"Gather {i} Trophies")
    
    for i in range(len(victory_loc_list)):
        if str(trophies) in victory_loc_list[i]:
            victory_id = i
            break

    #victory_id = get_option_value(multiworld, player, "victory_condition") # This needs to be added in the hooks/Options.py file
    victory_location_name = victory_loc_list[victory_id]
    victory_location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == victory_location_name)
    victory_location.place_locked_item(victory_item)
    
    # Remove the extra victory locations
    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in victory_loc_list and location.name != victory_location_name:
                    region.locations.remove(location)
    
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