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
    
    if is_category_enabled(multiworld, player, "Classic") is True:
        tracks += 18
    if is_category_enabled(multiworld, player, "Nitro") is True:
        tracks += 13
    if is_category_enabled(multiworld, player, "Bonus") is True:
        tracks += 8
    
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

    bad_trophies = 300-max_trophies
    for i in range(bad_trophies):
        itemNamesToRemove.append("Trophy")

    # Get the victory location and place the victory item there
    victory_loc_list = [  # A list of all the victory location names in order
        "Gather 1 Trophy",
        "Gather 2 Trophies",
        "Gather 3 Trophies",
        "Gather 4 Trophies",
        "Gather 5 Trophies",
        "Gather 6 Trophies",
        "Gather 7 Trophies",
        "Gather 8 Trophies",
        "Gather 9 Trophies",
        "Gather 10 Trophies",
        "Gather 11 Trophies",
        "Gather 12 Trophies",
        "Gather 13 Trophies",
        "Gather 14 Trophies",
        "Gather 15 Trophies",
        "Gather 16 Trophies",
        "Gather 17 Trophies",
        "Gather 18 Trophies",
        "Gather 19 Trophies",
        "Gather 20 Trophies",
        "Gather 21 Trophies",
        "Gather 22 Trophies",
        "Gather 23 Trophies",
        "Gather 24 Trophies",
        "Gather 25 Trophies",
        "Gather 26 Trophies",
        "Gather 27 Trophies",
        "Gather 28 Trophies",
        "Gather 29 Trophies",
        "Gather 30 Trophies",
        "Gather 31 Trophies",
        "Gather 32 Trophies",
        "Gather 33 Trophies",
        "Gather 34 Trophies",
        "Gather 35 Trophies",
        "Gather 36 Trophies",
        "Gather 37 Trophies",
        "Gather 38 Trophies",
        "Gather 39 Trophies",
        "Gather 40 Trophies",
        "Gather 41 Trophies",
        "Gather 42 Trophies",
        "Gather 43 Trophies",
        "Gather 44 Trophies",
        "Gather 45 Trophies",
        "Gather 46 Trophies",
        "Gather 47 Trophies",
        "Gather 48 Trophies",
        "Gather 49 Trophies",
        "Gather 50 Trophies",
        "Gather 51 Trophies",
        "Gather 52 Trophies",
        "Gather 53 Trophies",
        "Gather 54 Trophies",
        "Gather 55 Trophies",
        "Gather 56 Trophies",
        "Gather 57 Trophies",
        "Gather 58 Trophies",
        "Gather 59 Trophies",
        "Gather 60 Trophies",
        "Gather 61 Trophies",
        "Gather 62 Trophies",
        "Gather 63 Trophies",
        "Gather 64 Trophies",
        "Gather 65 Trophies",
        "Gather 66 Trophies",
        "Gather 67 Trophies",
        "Gather 68 Trophies",
        "Gather 69 Trophies",
        "Gather 70 Trophies",
        "Gather 71 Trophies",
        "Gather 72 Trophies",
        "Gather 73 Trophies",
        "Gather 74 Trophies",
        "Gather 75 Trophies",
        "Gather 76 Trophies",
        "Gather 77 Trophies",
        "Gather 78 Trophies",
        "Gather 79 Trophies",
        "Gather 80 Trophies",
        "Gather 81 Trophies",
        "Gather 82 Trophies",
        "Gather 83 Trophies",
        "Gather 84 Trophies",
        "Gather 85 Trophies",
        "Gather 86 Trophies",
        "Gather 87 Trophies",
        "Gather 88 Trophies",
        "Gather 89 Trophies",
        "Gather 90 Trophies",
        "Gather 91 Trophies",
        "Gather 92 Trophies",
        "Gather 93 Trophies",
        "Gather 94 Trophies",
        "Gather 95 Trophies",
        "Gather 96 Trophies",
        "Gather 97 Trophies",
        "Gather 98 Trophies",
        "Gather 99 Trophies",
        "Gather 100 Trophies",
        "Gather 101 Trophies",
        "Gather 102 Trophies",
        "Gather 103 Trophies",
        "Gather 104 Trophies",
        "Gather 105 Trophies",
        "Gather 106 Trophies",
        "Gather 107 Trophies",
        "Gather 108 Trophies",
        "Gather 109 Trophies",
        "Gather 110 Trophies",
        "Gather 111 Trophies",
        "Gather 112 Trophies",
        "Gather 113 Trophies",
        "Gather 114 Trophies",
        "Gather 115 Trophies",
        "Gather 116 Trophies",
        "Gather 117 Trophies",
        "Gather 118 Trophies",
        "Gather 119 Trophies",
        "Gather 120 Trophies",
        "Gather 121 Trophies",
        "Gather 122 Trophies",
        "Gather 123 Trophies",
        "Gather 124 Trophies",
        "Gather 125 Trophies",
        "Gather 126 Trophies",
        "Gather 127 Trophies",
        "Gather 128 Trophies",
        "Gather 129 Trophies",
        "Gather 130 Trophies",
        "Gather 131 Trophies",
        "Gather 132 Trophies",
        "Gather 133 Trophies",
        "Gather 134 Trophies",
        "Gather 135 Trophies",
        "Gather 136 Trophies",
        "Gather 137 Trophies",
        "Gather 138 Trophies",
        "Gather 139 Trophies",
        "Gather 140 Trophies",
        "Gather 141 Trophies",
        "Gather 142 Trophies",
        "Gather 143 Trophies",
        "Gather 144 Trophies",
        "Gather 145 Trophies",
        "Gather 146 Trophies",
        "Gather 147 Trophies",
        "Gather 148 Trophies",
        "Gather 149 Trophies",
        "Gather 150 Trophies",
        "Gather 151 Trophies",
        "Gather 152 Trophies",
        "Gather 153 Trophies",
        "Gather 154 Trophies",
        "Gather 155 Trophies",
        "Gather 156 Trophies",
        "Gather 157 Trophies",
        "Gather 158 Trophies",
        "Gather 159 Trophies",
        "Gather 160 Trophies",
        "Gather 161 Trophies",
        "Gather 162 Trophies",
        "Gather 163 Trophies",
        "Gather 164 Trophies",
        "Gather 165 Trophies",
        "Gather 166 Trophies",
        "Gather 167 Trophies",
        "Gather 168 Trophies",
        "Gather 169 Trophies",
        "Gather 170 Trophies",
        "Gather 171 Trophies",
        "Gather 172 Trophies",
        "Gather 173 Trophies",
        "Gather 174 Trophies",
        "Gather 175 Trophies",
        "Gather 176 Trophies",
        "Gather 177 Trophies",
        "Gather 178 Trophies",
        "Gather 179 Trophies",
        "Gather 180 Trophies",
        "Gather 181 Trophies",
        "Gather 182 Trophies",
        "Gather 183 Trophies",
        "Gather 184 Trophies",
        "Gather 185 Trophies",
        "Gather 186 Trophies",
        "Gather 187 Trophies",
        "Gather 188 Trophies",
        "Gather 189 Trophies",
        "Gather 190 Trophies",
        "Gather 191 Trophies",
        "Gather 192 Trophies",
        "Gather 193 Trophies",
        "Gather 194 Trophies",
        "Gather 195 Trophies",
        "Gather 196 Trophies",
        "Gather 197 Trophies",
        "Gather 198 Trophies",
        "Gather 199 Trophies",
        "Gather 200 Trophies",
        "Gather 201 Trophies",
        "Gather 202 Trophies",
        "Gather 203 Trophies",
        "Gather 204 Trophies",
        "Gather 205 Trophies",
        "Gather 206 Trophies",
        "Gather 207 Trophies",
        "Gather 208 Trophies",
        "Gather 209 Trophies",
        "Gather 210 Trophies",
        "Gather 211 Trophies",
        "Gather 212 Trophies",
        "Gather 213 Trophies",
        "Gather 214 Trophies",
        "Gather 215 Trophies",
        "Gather 216 Trophies",
        "Gather 217 Trophies",
        "Gather 218 Trophies",
        "Gather 219 Trophies",
        "Gather 220 Trophies",
        "Gather 221 Trophies",
        "Gather 222 Trophies",
        "Gather 223 Trophies",
        "Gather 224 Trophies",
        "Gather 225 Trophies",
        "Gather 226 Trophies",
        "Gather 227 Trophies",
        "Gather 228 Trophies",
        "Gather 229 Trophies",
        "Gather 230 Trophies",
        "Gather 231 Trophies",
        "Gather 232 Trophies",
        "Gather 233 Trophies",
        "Gather 234 Trophies",
        "Gather 235 Trophies",
        "Gather 236 Trophies",
        "Gather 237 Trophies",
        "Gather 238 Trophies",
        "Gather 239 Trophies",
        "Gather 240 Trophies",
        "Gather 241 Trophies",
        "Gather 242 Trophies",
        "Gather 243 Trophies",
        "Gather 244 Trophies",
        "Gather 245 Trophies",
        "Gather 246 Trophies",
        "Gather 247 Trophies",
        "Gather 248 Trophies",
        "Gather 249 Trophies",
        "Gather 250 Trophies",
        "Gather 251 Trophies",
        "Gather 252 Trophies",
        "Gather 253 Trophies",
        "Gather 254 Trophies",
        "Gather 255 Trophies",
        "Gather 256 Trophies",
        "Gather 257 Trophies",
        "Gather 258 Trophies",
        "Gather 259 Trophies",
        "Gather 260 Trophies",
        "Gather 261 Trophies",
        "Gather 262 Trophies",
        "Gather 263 Trophies",
        "Gather 264 Trophies",
        "Gather 265 Trophies",
        "Gather 266 Trophies",
        "Gather 267 Trophies",
        "Gather 268 Trophies",
        "Gather 269 Trophies",
        "Gather 270 Trophies",
        "Gather 271 Trophies",
        "Gather 272 Trophies",
        "Gather 273 Trophies",
        "Gather 274 Trophies",
        "Gather 275 Trophies",
        "Gather 276 Trophies",
        "Gather 277 Trophies",
        "Gather 278 Trophies",
        "Gather 279 Trophies",
        "Gather 280 Trophies",
        "Gather 281 Trophies",
        "Gather 282 Trophies",
        "Gather 283 Trophies",
        "Gather 284 Trophies",
        "Gather 285 Trophies",
        "Gather 286 Trophies",
        "Gather 287 Trophies",
        "Gather 288 Trophies",
        "Gather 289 Trophies",
        "Gather 290 Trophies",
        "Gather 291 Trophies",
        "Gather 292 Trophies",
        "Gather 293 Trophies",
        "Gather 294 Trophies",
        "Gather 295 Trophies",
        "Gather 296 Trophies",
        "Gather 297 Trophies",
        "Gather 298 Trophies",
        "Gather 299 Trophies"
    ]
    
    for i in range(len(victory_loc_list)-1):
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