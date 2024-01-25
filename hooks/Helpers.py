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
            if Helpers.get_option_value(world, player, "game_version") == 0: #Classic CTR
                return False
            if selection == 1 or selection == 3 or selection == 5 or selection == 6:
                return True
            elif selection == 0 or selection == 2 or selection == 4:
                return False
        if category_name == "Bonus":
            if Helpers.get_option_value(world, player, "game_version") == 0: #Classic CTR
                return False
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
        
    if category_name == "ExtraTrophies1":
        difficulties = 0
        if Helpers.is_category_enabled(world, player, "Easy") is True:
            difficulties += 1
        if Helpers.is_category_enabled(world, player, "Medium") is True:
            difficulties += 1
        if Helpers.is_category_enabled(world, player, "Hard") is True:
            difficulties += 1
        if difficulties >= 2:
            return True
        else:
            return False
    if category_name == "ExtraTrophies2":
        difficulties = 0
        if Helpers.is_category_enabled(world, player, "Easy") is True:
            difficulties += 1
        if Helpers.is_category_enabled(world, player, "Medium") is True:
            difficulties += 1
        if Helpers.is_category_enabled(world, player, "Hard") is True:
            difficulties += 1
        if difficulties == 3:
            return True
        else:
            return False
            
    return None
