
# Toon-specific default variables
DEFAULT_BEAN_COUNT = 0
DEFAULT_BEAN_LIMIT = 40
DEFAULT_HP = 15

# Astro-specific default variables
ASTRO_NAME = "Astro"
ASTRO_HP = 65
ASTRO_TRACK_EXPS = [7421, 0, 10101, 9443, 8690, 6862, 191]
ASTRO_GAG_COUNT = [[0,   0,  0,  5,  5,  3, -1],  # 0 Toon-up
                   [-1, -1, -1, -1, -1, -1, -1],  # 1 Trap (locked)
                   [0,   0,  0,  0,  5,  3,  1],  # 2 Lure
                   [0,   0,  0,  0,  5,  3, -1],  # 3 Sound
                   [0,   2,  1,  4,  4,  2, -1],  # 4 Throw
                   [0,   0,  0,  5,  5,  3, -1],  # 5 Squirt
                   [0,   9,  5, -1, -1, -1, -1]]  # 6 Drop
ASTRO_GAG_LIMIT = 70
# Astro-specific expected values
ASTRO_EXPECTED_TRACK_LEVELS = [5, -1, 6, 5, 5, 5, 2]
# TODO: Replace with list of Gags intead of an int
ASTRO_EXPECTED_UNLOCKED_GAGS = 34
# TODO: Replace with list of Gags intead of an int
ASTRO_EXPECTED_AVAILABLE_GAGS = 18

# Trapa-specific default variables
TRAPA_NAME = "Trapa"
TRAPA_HP = 65
TRAPA_TRACK_EXPS = [7421, 191, 10101, 9443, 8690, 6862, 0]
TRAPA_GAG_COUNT = [[0,   0,  0,  5,  5,  3, -1],  # 0 Toon-up
                   [1,   9,  5, -1, -1, -1, -1],  # 1 Trap
                   [1,   0,  0,  0,  5,  3,  1],  # 2 Lure
                   [0,   0,  0,  0,  5,  3, -1],  # 3 Sound
                   [1,   2,  1,  3,  3,  2, -1],  # 4 Throw
                   [0,   0,  0,  4,  4,  3, -1],  # 5 Squirt
                   [-1, -1, -1, -1, -1, -1, -1]]  # 6 Drop (locked)
TRAPA_GAG_LIMIT = 70
# Trapa-specific expected values
TRAPA_EXPECTED_TRACK_LEVELS = [5, 2, 6, 5, 5, 5, -1]
# TODO: Replace with list of Gags intead of an int
TRAPA_EXPECTED_UNLOCKED_GAGS = 34
# TODO: Replace with list of Gags intead of an int
TRAPA_EXPECTED_AVAILABLE_GAGS = 21
