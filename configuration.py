# Names of conditions, used only in csv logging for name current experiment condition.
CONJUNCTION_CONDITION_NAME = "CONJUNCTION"
SWITCH_CONDITION_NAME = "SWITCH"
STREAK_CONDITION_NAME = "STREAK"
RANDOM_CONDITION_NAME = "RANDOM"

# Number of blocks of each trials. These values taken from section '2.3. Procedure'.
CONJUNCTION_CONDITION_BLOCKS_NUMBER = 3
SWITCH_CONDITION_BLOCKS_NUMBER = 3
STREAK_CONDITION_BLOCKS_NUMBER = 8
RANDOM_CONDITION_BLOCKS_NUMBER = 3

# Number of trials per block. This value taken from section '2.3. Procedure'.
TRIALS_PER_BLOCK = 100

# Duration, feedback and block end rest durations in milliseconds.
FIXATION_DURATION = 500
FEEDBACK_DURATION = 1000
BLOCK_END_REST_DURATION = 8000

# Keyboard keys for subjects responses at trials. This experiment requires two keys (not including 'SPACE' key).
KEYBOARD_KEY_1 = "N"
KEYBOARD_KEY_2 = "M"

# Number of trials in pre-experiment practice.
PRACTICE_TRIALS_NUMBER = 100

# Experiment settings for fast mode.
FAST_MODE_BLOCKS_PER_CONDITION = 1
FAST_MODE_TRIALS_PER_BLOCK = 4

# Default subject name and csv filename.
DEFAULT_SUBJECT_NAME = "subject"
DEFAULT_CSV_FILENAME = DEFAULT_SUBJECT_NAME

# Extension of csv files.
CSV_FILE_EXTENSION = ".csv"

# Experiment definition text  at 'Intro' page.
INTRO_TEXT = "In this experiment red and green bars will be presented on screen.\n" \
             "Your TARGET is a red bar whose orientation is different from other red bars on the screen\n" \
             "TARGET may be absent on screen.\n" \
             "You should determine whether TARGET is presented on screen.\n" \
             "Time for response is unlimited, but try to response as soon as possible."

# Format strings for key bindings for 'target presented/absent' responses at 'Intro' page.
KEY_BINDINGS_PRESENTED_FORMAT_STRING = "Press '%s' if TARGET is presented on screen."
KEY_BINDINGS_ABSENT_FORMAT_STRING = "Press '%s' if TARGET is absent on screen."

# Text at the end of 'Intro' page (no practice in fast mode).
INTRO_END_TEXT = "Now you will pass some practice rounds.\nPress SPACE to start practice."
INTRO_END_FAST_MODE_TEXT = "Press SPACE to start experiment."

# Text at 'Feedback correct/incorrect' pages.
FEEDBACK_CORRECT_TEXT = "Right!"
FEEDBACK_INCORRECT_TEXT = "Wrong!"

# Text at 'Practice start/end' pages.
PRACTICE_END_TEXT = "Practice rounds are complete.\nPress SPACE to start experiment."

# Text at 'Block end rest' page.
BLOCK_END_REST_TEXT = "Take a rest ..."

# Text at 'Experiment end' page.
EXPERIMENT_END_TEXT = "Experiment complete. Thanks for participating!\nPress SPACE to close program."
