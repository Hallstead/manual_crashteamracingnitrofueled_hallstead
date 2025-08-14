from ..Helpers import get_option_value, is_category_enabled
from BaseClasses import MultiWorld

debug = False  # Set to True to enable debug mode, which will print additional information during execution
trophies_in_pool = 650  # The number of trophies in the item pool, used for victory conditions

def get_track_list(multiworld: MultiWorld, player: int):
    classic = is_category_enabled(multiworld, player, "Classic")
    nitro = is_category_enabled(multiworld, player, "Nitro")
    bonus = is_category_enabled(multiworld, player, "Bonus")
    tracksIncluded = is_category_enabled(multiworld, player, "Tracks")
    
    track_list = []
    if tracksIncluded is True:
        if classic is True:
            track_list.append("Crash Cove")
            track_list.append("Mystery Caves")
            track_list.append("Sewer Speedway")
            track_list.append("Roo's Tubes")
            track_list.append("Coco Park")
            track_list.append("Tiger Temple")
            track_list.append("Papu's Pyramid")
            track_list.append("Dingo Canyon")
            track_list.append("Polar Pass")
            track_list.append("Tiny Arena")
            track_list.append("Dragon Mines")
            track_list.append("Blizzard Bluff")
            track_list.append("Hot Air Skyway")
            track_list.append("Cortex Castle")
            track_list.append("N. Gin Labs")
            track_list.append("Slide Coliseum")
            track_list.append("Oxide Station")
            if is_category_enabled(multiworld, player, "Turbo Track"):
                track_list.append("Turbo Track")
        if nitro is True:
            track_list.append("Inferno Island")
            track_list.append("Jungle Boogie")
            track_list.append("Clockwork Wumpa")
            track_list.append("Android Alley")
            track_list.append("Electron Avenue")
            track_list.append("Deep Sea Driving")
            track_list.append("Thunder Struck")
            track_list.append("Tiny Temple")
            track_list.append("Meteor Gorge")
            track_list.append("Barin Ruins")
            track_list.append("Out Of Time")
            track_list.append("Assembly Lane")
            track_list.append("Hyper Spaceway")
        if bonus is True:
            track_list.append("Twilight Tour")
            track_list.append("Prehistoric Playground")
            track_list.append("Spyro Circuit")
            track_list.append("Nina's Nightmare")
            track_list.append("Koala Carnival")
            track_list.append("Gingerbread Joyride")
            track_list.append("Megamix Mania")
            track_list.append("Drive-Thru Danger")
    
    return track_list
    
def get_cup_list(multiworld: MultiWorld, player: int):
    classic = is_category_enabled(multiworld, player, "Classic")
    nitro = is_category_enabled(multiworld, player, "Nitro")
    bonus = is_category_enabled(multiworld, player, "Bonus")
    cups = is_category_enabled(multiworld, player, "Cups")
    
    cups_list = []
    if cups is True:
        if classic is True:
            cups_list.append("Wumpa Cup")
            cups_list.append("Nitro Cup")
            cups_list.append("Crystal Cup")
            cups_list.append("Crash Cup")
        if nitro is True:
            cups_list.append("Velo Cup")
            cups_list.append("Aku Cup")
            cups_list.append("Uka Cup")
        if bonus is True:
            cups_list.append("Bonus Cup")
            if classic is True and nitro is True:
                cups_list.append("Lost Cup")
                cups_list.append("Desert Cup")
                cups_list.append("Space Cup")

    return cups_list

def get_battle_list(multiworld: MultiWorld, player: int):
    classic = is_category_enabled(multiworld, player, "Classic Battle")
    nitro = is_category_enabled(multiworld, player, "Nitro Battle")
    battle = is_category_enabled(multiworld, player, "Battle")
    
    battle_list = []
    if battle is True:
        if classic is True:
            battle_list.append("Skull Rock")
            battle_list.append("Nitro Court")
            battle_list.append("Parking Lot")
            battle_list.append("Rocky Road")
            battle_list.append("Lab Basement")
            battle_list.append("Rampage Ruins")
            battle_list.append("The North Bowl")
        if nitro is True:
            battle_list.append("Temple Turmoil")
            battle_list.append("Frozen Frenzy")
            battle_list.append("Desert Storm")
            battle_list.append("Magnetic Mayhem")
            battle_list.append("Terra Drome")

    return battle_list

def num_difficulties(multiworld: MultiWorld, player: int):
    easy = is_category_enabled(multiworld, player, "Easy")
    medium = is_category_enabled(multiworld, player, "Medium")
    hard = is_category_enabled(multiworld, player, "Hard")
    
    difficulties = 0
    if easy is True:
        difficulties += 1
    if medium is True:
        difficulties += 1
    if hard is True:
        difficulties += 1

    return difficulties

def get_max_trophies(multiworld: MultiWorld, player: int):
    nf = is_category_enabled(multiworld, player, "NF")
    timeTrial = is_category_enabled(multiworld, player, "Time Trial")
    chunks = is_category_enabled(multiworld, player, "Chunks")
    final_challenge = is_category_enabled(multiworld, player, "Final Challenge")

    battleModes = 0
    for mode in ["Limit Battle", "Capture The Flag", "Crystal Grab", "Last Kart Driving", "Steal The Bacon"]:
        if is_category_enabled(multiworld, player, mode):
            battleModes += 1
    
    track_list = get_track_list(multiworld, player)
    cup_list = get_cup_list(multiworld, player)
    battle_list = get_battle_list(multiworld, player)

    numTracks = len(track_list)
    numCups = len(cup_list)
    numBattles = len(battle_list)

    if numBattles > 0 and battleModes == 0:
        raise Exception("No battle modes selected, but battles are enabled. Please select at least one battle mode.")

    difficulties = num_difficulties(multiworld, player)

    # Time Trial calculation
    tt = 0
    timetrial_locs = 0
    if timeTrial:
        ghosts = 0
        for ghost in ["N. Tropy", "N. Oxide", "Velo", "Dev"]:
            if is_category_enabled(multiworld, player, ghost):
                ghosts += 1
        if not nf:
            tt = numTracks
            timetrial_locs = numTracks * (ghosts + 1)
        else:
            timetrial_locs = numTracks * ghosts

    # Total track-like locations
    if not chunks:
        totalLocations = ((numTracks + numCups) * 3 + (numBattles) * battleModes) * difficulties
    else:
        totalLocations = (numTracks * 3 + numBattles * battleModes) * difficulties
    if final_challenge and not chunks:
        if numTracks > 0 or numCups > 0:
            totalLocations -= (difficulties * 3 - 1)
        else:
            totalLocations -= (difficulties * battleModes - 1)

    totalItems = numTracks + numCups + numBattles

    if not chunks:
        if not nf:
            max_trophies = round((totalLocations + tt) * 8 / 9 - totalItems)
        else:
            max_trophies = round(totalLocations * 8 / 9 - totalItems)
    else:
        max_trophies = round((totalLocations + timetrial_locs) * 8 / 9)

    return max_trophies
