import random
from image_creation import *
from constants import *

def get_response(message: str) -> str:
    p_message = message.lower()
    command = p_message.split()

    if command[0] == 'help':
        response = '+help              - Shows the list of all Tacobo commands\n'
        response += '+roll <end>        - Rolls a random integer from 1 to <end>. <end> = 100 by default.\n'
        response += '+image <map_link>  - Generates an image preview of an osu!taiko map. (beta - Not optimized for maps with rapid timimg point changes)'
        return f'```{response}```'

    elif command[0] == 'roll':
        end = 100 if len(command) == 1 else int(command[1])
        return random.randint(1, end)

    elif command[0] == 'image':
        if len(command) == 1:
            return INVALID_OSU_LINK

        trial = re.search(r'sets/(.*?)#', command[1])
        if trial == None:
            return INVALID_OSU_LINK

        return 'Processing...'

    else:
        return 'Command not recognized. Try `+help` for a list of Tacobo commands.'