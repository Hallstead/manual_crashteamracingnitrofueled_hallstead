from typing import Optional, TYPE_CHECKING
from BaseClasses import MultiWorld, Item, Location
from .. import Helpers
from .. import Data

if TYPE_CHECKING:
    from ..Items import ManualItem
    from ..Locations import ManualLocation

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the category, False to disable it, or None to use the default behavior
def before_is_category_enabled(multiworld: MultiWorld, player: int, category_name: str) -> Optional[bool]:
    nf = Helpers.get_option_value(multiworld, player, "ctr_game")
    chunks = Helpers.get_option_value(multiworld, player, "unlock_mode")
    if category_name == "NF":
        if nf:
            return True
        return False
    if category_name == "Classic" or category_name == "Nitro" or category_name == "Bonus":
        selection = Helpers.get_option_value(multiworld, player, "select_race_tracks")
        if category_name == "Classic":
            if selection == 0 or selection == 3 or selection == 4 or selection == 6:
                return True
            elif selection == 1 or selection == 2 or selection == 5:
                return False
        if category_name == "Nitro":
            if not nf:
                return False
            if selection == 1 or selection == 3 or selection == 5 or selection == 6:
                return True
            elif selection == 0 or selection == 2 or selection == 4:
                return False
        if category_name == "Bonus":
            if not nf:
                return False
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
        
    if category_name == "Tracks" or category_name == "Single":
        if Helpers.get_option_value(multiworld, player, "include_single_race") == 1:
            return True
        elif Helpers.get_option_value(multiworld, player, "include_time_trial") == 1:
            return True
        else:
            Data.category_table[category_name]["hidden"] = True
            return False
    
    if category_name == "Track - Turbo Track" or category_name == "Turbo Track":
        if Helpers.get_option_value(multiworld, player, "include_turbo_track") == 1:
            return True
        return False

    if category_name == "Cups":
        if Helpers.get_option_value(multiworld, player, "include_cups") == 1 and Helpers.get_option_value(multiworld, player, "cups_unlock_method") == 1: # Cups
            return True
        elif Helpers.get_option_value(multiworld, player, "unlock_mode") == 1: # Chunks
            return True
        else:
            Data.category_table[category_name]["hidden"] = True
            return False
        
    if category_name == "Cups_option":
        if Helpers.get_option_value(multiworld, player, "include_cups") == 1:
            return True
        elif Helpers.get_option_value(multiworld, player, "unlock_mode") == 1: # Chunks
            return True
        else:
            Data.category_table[category_name]["hidden"] = True
            return False
        
    if category_name == "Cups Items":
        if Helpers.get_option_value(multiworld, player, "cups_unlock_method") == 1: # Cups Items
            return True
        elif Helpers.get_option_value(multiworld, player, "unlock_mode") == 1: # Chunks
            return True
        elif Helpers.get_option_value(multiworld, player, "include_single_race") == 0: # Tracks not included
            return True
        elif Helpers.get_option_value(multiworld, player, "goal_type") == 1: # Final Challenge:
            return True
        else:
            Data.category_table[category_name]["hidden"] = True
            return False
        
    if category_name == "Battle" or category_name == "Arenas":
        if nf:
            if Helpers.get_option_value(multiworld, player, "include_battle") == 1:
                return True    
        Data.category_table[category_name]["hidden"] = True
        return False
    if category_name == "Classic Battle":
        if Helpers.get_option_value(multiworld, player, "include_battle") == 1:
            if Helpers.get_option_value(multiworld, player, "select_battle_arenas") in [0, 2]:
                return True
        Data.category_table[category_name]["hidden"] = True
        return False
    if category_name == "Nitro Battle":
        if nf:
            if Helpers.get_option_value(multiworld, player, "include_battle") == 1:
                if Helpers.get_option_value(multiworld, player, "select_battle_arenas") >= 1:
                    return True
        Data.category_table[category_name]["hidden"] = True
        return False
    if category_name == "Limit Battle":
        if nf:
            if Helpers.get_option_value(multiworld, player, "include_battle") == 1:
                if Helpers.get_option_value(multiworld, player, "include_limit_battle") == 1:
                    return True
        Data.category_table[category_name]["hidden"] = True
        return False
    if category_name == "Capture The Flag":
        if nf:
            if Helpers.get_option_value(multiworld, player, "include_battle") == 1:
                if Helpers.get_option_value(multiworld, player, "include_capture_the_flag") == 1:
                    return True
        Data.category_table[category_name]["hidden"] = True
        return False
    if category_name == "Crystal Grab":
        if nf:
            if Helpers.get_option_value(multiworld, player, "include_battle") == 1:
                if Helpers.get_option_value(multiworld, player, "include_crystal_grab") == 1:
                    return True
        Data.category_table[category_name]["hidden"] = True
        return False
    if category_name == "Last Kart Driving":
        if nf:
            if Helpers.get_option_value(multiworld, player, "include_battle") == 1:
                if Helpers.get_option_value(multiworld, player, "include_last_kart_driving") == 1:
                    return True
        Data.category_table[category_name]["hidden"] = True
        return False
    if category_name == "Steal The Bacon":
        if nf:
            if Helpers.get_option_value(multiworld, player, "include_battle") == 1:
                if Helpers.get_option_value(multiworld, player, "include_steal_the_bacon") == 1:
                    return True
        Data.category_table[category_name]["hidden"] = True
        return False
    
    if category_name in ["Time Trial", "Time Trial Option", "Time Trial Ghosts"]:
        if Helpers.get_option_value(multiworld, player, "include_time_trial") == 1:
            if category_name == "Time Trial Ghosts":
                if not chunks:
                    if Helpers.get_option_value(multiworld, player, "included_ghosts") > 0:
                        return True
            else:
                return True
        Data.category_table[category_name]["hidden"] = True
        return False
    if category_name == "Progressive Ghost":
        if Helpers.get_option_value(multiworld, player, "include_time_trial") == 1:
            if Helpers.get_option_value(multiworld, player, "included_ghosts") > 1:
                return True
        return False
    if category_name == "N. Tropy Item":
        if Helpers.get_option_value(multiworld, player, "include_time_trial") == 1:
            if Helpers.get_option_value(multiworld, player, "included_ghosts") == 1:
                return True
        return False
    if category_name == "No Ghost":
        if nf:
            return False
        if Helpers.get_option_value(multiworld, player, "include_time_trial") == 1:
            return True
        return False
    if category_name == "N. Tropy":
        if Helpers.get_option_value(multiworld, player, "include_time_trial") == 1:
            if Helpers.get_option_value(multiworld, player, "included_ghosts") >= 1:
                return True
        return False
    if category_name == "N. Oxide":
        if Helpers.get_option_value(multiworld, player, "include_time_trial") == 1:
            if Helpers.get_option_value(multiworld, player, "included_ghosts") >= 2:
                return True
        return False
    if category_name == "Velo":
        if not nf:
            return False
        if Helpers.get_option_value(multiworld, player, "include_time_trial") == 1:
            if Helpers.get_option_value(multiworld, player, "included_ghosts") >= 3:
                return True
        return False
    if category_name == "Dev":
        if not nf:
            return False
        if Helpers.get_option_value(multiworld, player, "include_time_trial") == 1:
            if Helpers.get_option_value(multiworld, player, "included_ghosts") >= 4:
                return True
        return False
    if category_name == "Chunks" or category_name == "Chunk Unlocks":
        if chunks == 1:
            return True
        Data.category_table[category_name]["hidden"] = True
        return False
    if category_name == "Not Chunks":
        if chunks == 0:
            return True
        return False
    chars = Helpers.get_option_value(multiworld,player, "randomize_characters")
    if category_name == "Driving Styles":
        if not nf:
            return False
        if chars == 1:
            return True
        Data.category_table[category_name]["hidden"] = True
        return False
    if category_name == "Characters":
        if chars >= 2:
            return True
        Data.category_table[category_name]["hidden"] = True
        return False
    if category_name == "Unlockable":
        if chars >= 3:
            return True
        return False
    if category_name == "Purchasable":
        if chars == 4:
            return True
        return False
    if category_name == "((~Objective~))":
        if chunks:
            return True
        if Helpers.get_option_value(multiworld, player, "goal_type") == 1:
            return True
        return False
    if category_name == "Win Condition - Final Challenge":
        if chunks:
            return True
        elif Helpers.get_option_value(multiworld, player, "goal_type") == 1:
            return True
        Data.category_table[category_name]["hidden"] = True
        return False
    return None

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the item, False to disable it, or None to use the default behavior
def before_is_item_enabled(multiworld: MultiWorld, player: int, item: "ManualItem") -> Optional[bool]:
    return None

# Use this if you want to override the default behavior of is_option_enabled
# Return True to enable the location, False to disable it, or None to use the default behavior
def before_is_location_enabled(multiworld: MultiWorld, player: int, location: "ManualLocation") -> Optional[bool]:
    return None
