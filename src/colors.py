# Colors and styles used in the printed text
# Using 256-color matte/muted tones instead of bright ANSI defaults
reset = "\x1b[0m"
bold = "\x1b[1m"
dim = "\x1b[2m"

# Muted palette (256-color)
slate   = "\x1b[38;5;103m"   # soft blue-grey for headers
sand    = "\x1b[38;5;180m"   # warm muted gold for labels
sage    = "\x1b[38;5;108m"   # soft green for success
rose    = "\x1b[38;5;167m"   # dusty red for errors
stone   = "\x1b[38;5;245m"   # neutral grey for secondary text
teal    = "\x1b[38;5;73m"    # muted teal for accents

LINE = f"{stone}{'─' * 50}{reset}"
DOUBLE_LINE = f"{stone}{'═' * 50}{reset}"
