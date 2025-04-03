# Object classes from AP that represent different types of options that you can create
from Options import Toggle, DefaultOnToggle, Choice, Range, Visibility

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld



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
class ctr_game(Choice):
    """
    This option tells generation what game you are playing.
    Classic CTR: This is the PS1 version of Crash Team Racing. Some options are not available with this option selected.
    CTR_NF: This is Crash Team Racing: Nitro Fueled.
    """
    display_name = "What game are you playing?"
    option_classic_ctr = 0
    option_ctr_nf = 1
    default = 1

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
    Select the number (1-3) of starting maps.
    """
    display_name = "Select the number of starting maps."
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
    CTR:NF only.
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

class include_turbo_track(DefaultOnToggle):
    """
    Choose whether to include Turbo Track in Single Race arcade mode.
    To unlock Turbo Track in Classic CTR, you can enter the following code at the main menu:
    Hold L1+R1 and Press Right (x2), Left, Triangle, Right, Down (x2)
    Turbo Track is already unlocked by default in CTR:NF.
    """
    display_name = "Include Turbo Track?"

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
    CTR:NF only.
    Choose whether to include Battle mode.
    At least one game mode must be included to generate.
    """
    display_name = "Include Battle Mode?"

class select_battle_tracks(Choice):
    """
    CTR:NF only.
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
    Only N. Tropy and N. Oxide are available in Classic CTR.
    """
    display_name = "Select Ghosts"
    option_none = 0
    option_n_tropy = 1
    option_n_oxide = 2
    option_emperor_velo_xxvii = 3
    option_beenox_developer = 4
    default = 2

class randomize_characters(Choice):
    """
    Characters or Driving Stykes are added into the item pool as filler. Depending on other settings, not all randomized characters may be available in a given seed.
    None: All characters are playable as the player chooses.
    Driving Styles: All characters are playable as the player chooses, but thefive driving styles are added to thr pool and can omly be used once found.
        This option not available in Classic CTR.
    Starter: The starter characters are randomized. Unlockable characters and characters from the pit stop are not playable in this option.
    Unlockable: Starter and Unlockable characters are randomized. Characters from the Pit Stop are not playable in this option.
    All Characters: All characters are randomized.
    """
    display_name = "Randomize Characters?"
    option_none = 0
    option_driving_styles = 1
    option_starter = 2
    option_unlockable = 3
    option_all = 4
    default = 0

class oxide_edition(Toggle):
    """
    CTR:NF only.
    Do you have the Nitros Oxide Edition?
    Setting this to true adds the related characters to the
      Starter character set when randomozing characters.
    """
    display_name = "Oxide Edition"

# This is called before any manual options are defined, in case you want to define your own with a clean slate or let Manual define over them
def before_options_defined(options: dict) -> dict:
    options["ctr_game"] = ctr_game
    options["goal_type"] = goal_type
    options["percentage_trophies"] = percentage_trophies
    options["unlock_mode"] = unlock_mode
    options["starting_locations"] = starting_locations
    options["select_difficulty"] = select_difficulty
    options["include_single_race"] = include_single_race
    options["select_race_tracks"] = select_race_tracks
    options["include_turbo_track"] = include_turbo_track
    options["include_cups"] = include_cups
    options["cups_unlock_method"] = cups_unlock_method
    #options["include_battle"] = include_battle
    #options["select_battle_tracks"] = select_battle_tracks
    options["include_time_trial"] = include_time_trial
    options["included_ghosts"] = included_ghosts
    options["randomize_characters"] = randomize_characters
    options["oxide_edition"] = oxide_edition

    return options

# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: dict) -> dict:
    options["goal"].visibility = Visibility.spoiler #spoiler
    return options