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

    FIXATION_DURATION = 500
    FEEDBACK_DURATION = 1000

    KEYBOARD_KEY_1 = "N"
    KEYBOARD_KEY_2 = "M"

    FAST_MODE_BLOCKS_PER_CONDITION = 1
    FAST_MODE_TRIALS_PER_BLOCK = 4

    DEFAULT_SUBJECT_NAME = "subject"
    PROTOCOL_FILE_EXTENSION = ".csv"
    DEFAULT_PROTOCOL_FILENAME = DEFAULT_SUBJECT_NAME

    INTRO_TEXT = "In this experiment red and green bars will be presented on screen.\n" \
                 "Your TARGET is a red bar whose orientation is different from other red bars on the screen\n" \
                 "TARGET may be absent on screen.\n" \
                 "You should determine whether TARGET is presented on screen.\n" \
                 "Time for response is unlimited, but try to response as soon as possible."
    INTRO_TEXT_PRESS_SPACE_TEXT = "Press SPACE to start experiment."
    KEY_BINDINGS_PRESENTED_FORMAT_STRING = "Press '%s' if TARGET is presented on screen."
    KEY_BINDINGS_ABSENT_FORMAT_STRING = "Press '%s' if TARGET is absent on screen."
    FEEDBACK_CORRECT_TEXT = "Right!"
    FEEDBACK_INCORRECT_TEXT = "Wrong!"
    EXPERIMENT_END_TEXT = "Experiment complete. Thanks for participating!\nPress space to close program."
