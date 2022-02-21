import sys
from src.colors import *

# Function that get user confirmation (yes or no) to the 
# corresponding question.
def userConfirmation(question, default="no"):
  valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
  while True:
    sys.stdout.write(question + " [y/n] ")
    choice = input().lower()
    if default is not None and choice == "":
        return False
    elif choice in valid and valid[choice] == True:
        return True
    elif choice in valid and valid[choice] == False:
        return False
    else:
        sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")
