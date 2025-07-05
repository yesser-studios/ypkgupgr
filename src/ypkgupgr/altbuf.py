import sys

# Alternate buffers

ALTERNATE_BUFFER_ENTER = "\x1b[?1049h"
ALTERNATE_BUFFER_EXIT = "\x1b[?1049l"

def enter_alternate_buffer():
    sys.stdout.write(ALTERNATE_BUFFER_ENTER)
    sys.stdout.flush()

def exit_alternate_buffer():
    sys.stdout.write(ALTERNATE_BUFFER_EXIT)
    sys.stdout.flush()
