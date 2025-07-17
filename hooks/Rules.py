from typing import Optional
from worlds.AutoWorld import World
from ..Helpers import clamp, get_items_with_value, get_option_value, is_category_enabled
from BaseClasses import MultiWorld, CollectionState

import re

# Sometimes you have a requirement that is just too messy or repetitive to write out with boolean logic.
# Define a function here, and you can use it in a requires string with {function_name()}.
def overfishedAnywhere(world: World, state: CollectionState, player: int):
    """Has the player collected all fish from any fishing log?"""
    for cat, items in world.item_name_groups:
        if cat.endswith("Fishing Log") and state.has_all(items, player):
            return True
    return False

# You can also pass an argument to your function, like {function_name(15)}
# Note that all arguments are strings, so you'll need to convert them to ints if you want to do math.
def anyClassLevel(state: CollectionState, player: int, level: str):
    """Has the player reached the given level in any class?"""
    for item in ["Figher Level", "Black Belt Level", "Thief Level", "Red Mage Level", "White Mage Level", "Black Mage Level"]:
        if state.count(item, player) >= int(level):
            return True
    return False

# You can also return a string from your function, and it will be evaluated as a requires string.
def requiresMelee():
    """Returns a requires string that checks if the player has unlocked the tank."""
    return "|Figher Level:15| or |Black Belt Level:15| or |Thief Level:15|"

# Rule for is category enabled
def CupItemsEnabled(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    """Is a category option enabled?"""
    if get_option_value(multiworld, player, "cups_unlock_method") == 1: # Cups Items
        return True
    elif get_option_value(multiworld, player, "unlock_mode") == 1: # Chunks
        return True
    elif get_option_value(multiworld, player, "include_single_race") == 0: # Tracks not included
        return True
    elif get_option_value(multiworld, player, "goal_type") == 1: # Final Challenge:
        return True
    else:
        return False
    #return is_category_enabled(multiworld, player, param)

# Rule for is category disabled
def CupItemsDisabled(world: World, multiworld: MultiWorld, state: CollectionState, player: int) -> bool:
    """Is a category option disabled?"""
    if get_option_value(multiworld, player, "cups_unlock_method") == 1: # Cups Items
        return not True
    elif get_option_value(multiworld, player, "unlock_mode") == 1: # Chunks
        return not True
    elif get_option_value(multiworld, player, "include_single_race") == 0: # Tracks not included
        return not True
    elif get_option_value(multiworld, player, "goal_type") == 1: # Final Challenge:
        return not True
    else:
        return not False