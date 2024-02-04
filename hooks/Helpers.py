from typing import Optional
from BaseClasses import MultiWorld
from .. import Helpers


# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the category, False to disable it, or None to use the default behavior
def before_is_category_enabled(world: MultiWorld, player: int, category_name: str) -> Optional[bool]:
    if category_name == "Classic" or category_name == "Nitro" or category_name == "Bonus":
        selection = Helpers.get_option_value(world, player, "select_race_tracks")
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
        selection = Helpers.get_option_value(world, player, "select_difficulty")
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
        
    if category_name == "Battle":
        return False
    if category_name == "Battle Map":
        return False
    
    if category_name == "Cups" or category_name == "Cups_option":
        if Helpers.get_option_value(world, player, "include_cups") == 1:
            return True
        else:
            return False
    
    if category_name == "Time Trial":
        if Helpers.get_option_value(world, player, "include_time_trial") == 1:
            return True
        else:
            return False
    if category_name == "N. Tropy":
        if Helpers.get_option_value(world, player, "include_time_trial") == 1:
            if Helpers.get_option_value(world, player, "included_ghosts") >= 0:
                return True
        return False
    if category_name == "N. Oxide":
        if Helpers.get_option_value(world, player, "include_time_trial") == 1:
            if Helpers.get_option_value(world, player, "included_ghosts") >= 1:
                return True
    if category_name == "Velo":
        if Helpers.get_option_value(world, player, "include_time_trial") == 1:
            if Helpers.get_option_value(world, player, "included_ghosts") >= 2:
                return True
        return False
    if category_name == "Dev":
        if Helpers.get_option_value(world, player, "include_time_trial") == 1:
            if Helpers.get_option_value(world, player, "included_ghosts") >= 3:
                return True
        return False
    return None
