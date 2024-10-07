from typing import Optional
from BaseClasses import MultiWorld
from ..Locations import ManualLocation
from ..Items import ManualItem
from .. import Helpers

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the category, False to disable it, or None to use the default behavior
def before_is_category_enabled(multiworld: MultiWorld, player: int, category_name: str) -> Optional[bool]:
    if category_name == "Classic" or category_name == "Nitro" or category_name == "Bonus":
        selection = Helpers.get_option_value(multiworld, player, "select_race_tracks")
        if category_name == "Classic":
            if selection == 0 or selection == 3 or selection == 4 or selection == 6:
                return True
            elif selection == 1 or selection == 2 or selection == 5:
                return False
        if category_name == "Nitro":
            if selection == 1 or selection == 3 or selection == 5 or selection == 6:
                return True
            elif selection == 0 or selection == 2 or selection == 4:
                return False
        if category_name == "Bonus":
            if selection == 2 or selection == 4 or selection == 5 or selection == 6:
                return True
            elif selection == 0 or selection == 1 or selection == 3:
                return False
        
    if category_name == "Easy" or category_name == "Medium" or category_name == "Hard":
        selection = Helpers.get_option_value(multiworld, player, "select_difficulty")
        if category_name == "Easy":
            if selection == 0 or selection == 3 or selection == 4 or selection == 6:
                return True
            elif selection == 1 or selection == 2 or selection == 5:
                return False
        if category_name == "Medium":
            if selection == 1 or selection == 3 or selection == 5 or selection == 6:
                return True
            elif selection == 0 or selection == 2 or selection == 4:
                return False
        if category_name == "Hard":
            if selection == 2 or selection == 4 or selection == 5 or selection == 6:
                return True
            elif selection == 0 or selection == 1 or selection == 3:
                return False
        
    if category_name == "Tracks":
        if Helpers.get_option_value(multiworld, player, "include_single_race") == 1:
            return True
        elif Helpers.get_option_value(multiworld, player, "include_time_trial") == 1:
            return True
        else:
            return False

    if category_name == "Single":
        if Helpers.get_option_value(multiworld, player, "include_single_race") == 1:
            return True
        else:
            return False

    if category_name == "Cups" or category_name == "Cups_option":
        if Helpers.get_option_value(multiworld, player, "include_cups") == 1:
            return True
        elif Helpers.get_option_value(multiworld, player, "unlock_mode") == 1:
            return True
        else:
            return False
        
    if category_name == "Cups Items":
        if Helpers.get_option_value(multiworld, player, "include_cups") == 0: # Cups = False
            return False
        elif Helpers.get_option_value(multiworld, player, "cups_unlock_method") == 1: # Cups Items
            return True
        elif Helpers.get_option_value(multiworld, player, "unlock_mode") == 1: # Chunks
            return True
        else:
            return False
    
    if category_name == "Battle":
        return False
    if category_name == "Arenas":
        return False
    
    if category_name == "Time Trial" or category_name == "Time Trial Option":
        if Helpers.get_option_value(multiworld, player, "include_time_trial") == 1:
            return True
        else:
            return False
    if category_name == "N. Tropy":
        if Helpers.get_option_value(multiworld, player, "include_time_trial") == 1:
            if Helpers.get_option_value(multiworld, player, "included_ghosts") >= 0:
                return True
        return False
    if category_name == "N. Oxide":
        if Helpers.get_option_value(multiworld, player, "include_time_trial") == 1:
            if Helpers.get_option_value(multiworld, player, "included_ghosts") >= 1:
                return True
    if category_name == "Velo":
        if Helpers.get_option_value(multiworld, player, "include_time_trial") == 1:
            if Helpers.get_option_value(multiworld, player, "included_ghosts") >= 2:
                return True
        return False
    if category_name == "Dev":
        if Helpers.get_option_value(multiworld, player, "include_time_trial") == 1:
            if Helpers.get_option_value(multiworld, player, "included_ghosts") >= 3:
                return True
        return False
    if category_name == "SM2" or category_name == "SM3":
        if category_name == "SM2" and Helpers.get_option_value(multiworld, player, "starting_locations") >= 2:
            return True
        elif category_name == "SM3" and Helpers.get_option_value(multiworld, player, "starting_locations") >= 3:
            return True
        else:
            return False
    if category_name == "Chunks":
        if Helpers.get_option_value(multiworld, player, "unlock_mode") == 1:
            return True
        return False
    if category_name == "Not Chunks":
        if Helpers.get_option_value(multiworld, player, "unlock_mode") == 0:
            return True
        return False
    return None

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the item, False to disable it, or None to use the default behavior
def before_is_item_enabled(multiworld: MultiWorld, player: int, item: ManualItem) -> Optional[bool]:
    return None

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the location, False to disable it, or None to use the default behavior
def before_is_location_enabled(multiworld: MultiWorld, player: int, location: ManualLocation) -> Optional[bool]:
    return None
