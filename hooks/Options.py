# Object classes from AP that represent different types of options that you can create
from Options import FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, SpecialRange

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value



####################################################################
# NOTE: At the time that options are created, Manual has no concept of the multiworld or its own world. 
#       Options are defined before the world is even created.
#
# Example of creating your own option:
#
#   class MakeThePlayerOP(Toggle):
#       """Should the player be overpowered? Probably not, but you can choose for this to do... something!"""
#       display_name = "Make me OP"
#
#   options["make_op"] = MakeThePlayerOP
#
#
# Then, to see if the option is set, you can call is_option_enabled or get_option_value.
#####################################################################


# To add an option, use the before_options_defined hook below and something like this:
#   options["total_characters_to_win_with"] = TotalCharactersToWinWith
#
class game_version(Choice):
    """
    Select what version of Crash Team Racing you are playing.
    classic_ctr is the original PS1 version of Crash Team Racing
    ctr_nf is the modern Crash Team Racing: Nitro Fueled

    If playing Classic CTR, it may be necessary to enter the following code at the main menu to unlock Turbo Track and all the battle arenas:
    Hold L1+R1 and Press Right (x2), Left, Triangle, Right, Down (x2)
    """
    display_name = "Game Version"
    option_classic_ctr = 0
    option_ctr_nf = 1
    default = 1

class include_single_race(Choice):
    """
    Choose whether to include Single Race arcade mode.
    At least one game mode must be included to generate.
    """
    display_name = "Include Single Race Mode?"
    option_true = 0
    option_false = 1
    default = 0

class select_race_tracks(Choice):
    """
    Select what track sets are included in the randomizer. 
    Classic adds 18 tracks
    Nitro adds 13 tracks
    Bonus adds 8 tracks

    If include_single_race is false, this option does nothing.
    If Game Version is set to classic_ctr, this option is forced to classic.
    """
    display_name = "Select Race Track Set(s) to include"
    option_classic = 0
    option_nitro = 1
    option_bonus = 2
    option_classic_nitro = 3
    option_classic_bonus = 4
    option_nitro_bonus = 5
    option_all = 6
    default = 0

class include_battle(Choice):
    """
    Choose whether to include Battle arcade mode.
    """
    display_name = "Include Battle Mode?"
    option_true = 0
    option_false = 1
    default = 0


class select_battle_tracks(Choice):
    """
    Select what battle sets are included in the randomizer. If using the PS1 CTR, only use Classic.
    Classic adds 7 battle tracks
    Nitro adds 5 battle tracks
    """
    display_name = "Select Battle Track Set(s) to include"
    option_classic = 0
    option_nitro = 1
    option_classic_nitro = 2
    default = 0

class select_difficulty(Choice):
    """
    Select what difficulty locations are included in the randomizer.
    Each difficulty adds three checks per race track.
    Each difficulty adds five checks per battle track.
    """
    display_name = "Select Difficulties to include"
    option_easy = 0
    option_medium = 1
    option_hard = 2
    option_easy_medium = 3
    option_easy_hard = 4
    option_medium_hard = 5
    option_all = 6
    default = 2

class percentage_trophies(Range):
    """
    Select what percentage (1-100) of trophies are needed to achieve the goal.
    100 is all available trophies are required for the goal.
    """
    display_name = "What percentage of trophies to collect?"
    range_start = 1
    range_end = 100
    default = 100

# This is called before any manual options are defined, in case you want to define your own with a clean slate or let Manual define over them
def before_options_defined(options: dict) -> dict:
    options["game_version"] = game_version
    options["percentage_trophies"] = percentage_trophies
    options["select_difficulty"] = select_difficulty
    options["include_single_race"] = include_single_race
    options["select_race_tracks"] = select_race_tracks
    options["select_battle_tracks"] = select_battle_tracks
    return options

# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: dict) -> dict:
    #print(options["easy_difficulty_enabled"])
    #input("Press enter...")
    return options