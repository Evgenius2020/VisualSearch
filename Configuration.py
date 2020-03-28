class Configuration:
    CONJUNCTION_CONDITION_NAME = "CONJUNCTION"
    SWITCH_CONDITION_NAME = "SWITCH"
    STREAK_CONDITION_NAME = "STREAK"
    RANDOM_CONDITION_NAME = "RANDOM"

    CONJUNCTION_CONDITION_BLOCKS_NUMBER = 3
    SWITCH_CONDITION_BLOCKS_NUMBER = 3
    STREAK_CONDITION_BLOCKS_NUMBER = 8
    RANDOM_CONDITION_BLOCKS_NUMBER = 3

    TRIALS_PER_BLOCK = 100

    BLOCK_START_DURATION = 3000
    FIXATION_DURATION = 500
    FEEDBACK_DURATION = 1000

    KEYBOARD_KEY_1 = "N"
    KEYBOARD_KEY_2 = "M"
    KEYBOARD_KEY_FOR_PRESENTED = None
    KEYBOARD_KEY_FOR_ABSENT = None

    INTRO_TEXT = "In this experiment, RED and GREEN bars will be presented on screen.\n" \
                 "Your TARGET is a RED bar whose orientation is different from other RED bars on the screen\n" \
                 "TARGET may be absent on screen.\n" \
                 "You should determine whether TARGET is presented on screen."
    KEY_BINDINGS_FORMAT_STRING = "Press '%s' if TARGET is presented on screen.\n " \
                                 "Press '%s' if TARGET is absent on screen."
    FEEDBACK_CORRECT_TEXT = "Right!"
    FEEDBACK_INCORRECT_TEXT = "Wrong!"
