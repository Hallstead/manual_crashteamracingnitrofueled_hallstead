# Object classes from AP that represent different types of options that you can create
from Options import FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, NamedRange

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

class goal_type(Choice):
    """
    This option determines the goal. if there is a final challenge after collecting the number of trophies.
    Trophy Hunt sets collecting the trophies to be the goal.
    Final Challenge still has you collect trophies, but after gathering the necessary amount, a random track
        or cup (if enabled) will be selected as a final challenge to beat.
        At this time, enabling this option forces cups_unlock_method to use Cup Items.
    """
    display_name = "Enable Final Challenge?"
    option_trophy_hunt = 0
    option_final_challenge = 1
    default = 0

class percentage_trophies(Range):
    """
    Select what percentage (1-100) of trophies are needed to achieve the goal.
    100 is all available trophies are required for the goal.
    """
    display_name = "What percentage of trophies to collect?"
    range_start = 1
    range_end = 100
    default = 80

class starting_locations(Range):
    """
    Select the number (1-3) of starting locations.
    """
    display_name = "Select the number of starting locations."
    range_start = 1
    range_end = 3
    default = 2

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

class unlock_mode(Choice):
    """
    Individual: Tracks are unlocked as their unlock item is obtained.
    Chunks: Tracks are unlocked in groups with cups unlocking the next chunk.
        This option forces Cups to be included with Cup Items in the pool.
        Final Challenge is the goal for this option.
    """
    display_name = "Game Unlock Mode"
    option_individual = 0
    option_chunks = 1
    default = 0

class include_single_race(DefaultOnToggle):
    """
    Choose whether to include Single Race arcade mode.
    At least one game mode must be included to generate.
    """
    display_name = "Include Single Race Mode?"

class select_race_tracks(Choice):
    """
    Select what track sets are included in the randomizer. 
    Classic adds 18 tracks
    Nitro adds 13 tracks
    Bonus adds 8 tracks

    If include_single_race is false, this option does nothing.
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

class include_cups(Toggle):
    """
    Choose whether to include Cup Race mode.
    At least one game mode must be included to generate.
    """
    display_name = "Include Cup Race Mode?"

class cups_unlock_method(Choice):
    """
    Choose the method for unlocking cups.
    Four Tracks uses the four tracks included in each cup to unlock it. Having access to all four tracks unlocks access to the corresponding cup.
    Cup Item adds a cup item to the pool for each cup that unlocks that cup. Having the cup item unlocks the cup regardless of if you have access to its four tracks.
    This setting does nothing if Cups are not included.
    """
    display_name = "Cups Unlock Method"
    option_four_tracks = 0
    option_cup_item = 1

class include_battle(Toggle):
    """
    Choose whether to include Battle mode.
    At least one game mode must be included to generate.
    """
    display_name = "Include Battle Mode?"

class select_battle_tracks(Choice):
    """
    Select what battle sets are included in the randomizer. If using the PS1 CTR, only use Classic.
    Classic adds 7 battle tracks
    Nitro adds 5 battle tracks

    If include_battle is false, this setting does nothing.
    """
    display_name = "Select Battle Track Set(s) to include"
    option_classic = 0
    option_nitro = 1
    option_classic_nitro = 2
    default = 0

class include_time_trial(Toggle):
    """
    Choose whether to include Time Trial mode.
    Presently, this mode also requires individual tracks to be on or generation will error.
    """
    display_name = "Include Time Trial Mode?"
    
class included_ghosts(Choice):
    """
    Choose whether to include Time Trial ghosts in the locations pool.
    Each ghost will also include the ghosts before it.
    This setting does nothing if Time Trial is not included.
    """
    display_name = "Select Ghosts"
    option_n_tropy = 0
    option_n_oxide = 1
    option_emperor_velo_xxvii = 2
    option_beenox_developer = 3
    default = 1

# This is called before any manual options are defined, in case you want to define your own with a clean slate or let Manual define over them
def before_options_defined(options: dict) -> dict:
    options["goal_type"] = goal_type
    options["percentage_trophies"] = percentage_trophies
    options["unlock_mode"] = unlock_mode
    options["starting_locations"] = starting_locations
    options["select_difficulty"] = select_difficulty
    options["include_single_race"] = include_single_race
    options["select_race_tracks"] = select_race_tracks
    options["include_cups"] = include_cups
    options["cups_unlock_method"] = cups_unlock_method
    #options["include_battle"] = include_battle
    #options["select_battle_tracks"] = select_battle_tracks
    options["include_time_trial"] = include_time_trial
    options["included_ghosts"] = included_ghosts

    return options

# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: dict) -> dict:
    options["goal"].visibility = 8 #hidden
    return options