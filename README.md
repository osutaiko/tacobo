# Tacobo
Discord utility bot for osu!taiko (very early in development)

## Commands
All commands start with the identifier `+`.

### Command List
| Command | Description |
| ------- | ----------- |
| `+help` | Shows a list of all supported Tacobo commands. |
| `+roll <end>` | Rolls a random integer from 1 to <end>. <end> = 100 by default. |
| `+image <map_link>` | Generates an image preview of an osu!taiko map. |

#### +image command
The command uses [Chimu.moe API](https://chimu.moe/) to download maps. When requesting a preview image, the osu! map link should have both the map ID and difficulty ID visible. (e.g. `https://osu.ppy.sh/beatmapsets/827049#taiko/1733135`) WIP or graveyarded maps on osu! probably won't work as they aren't supported in the Chimu.moe API.
The generated image displays changes in BPM or time signatures. The command is not implemented well, so refrain from requesting maps with unconventional or rapid timing point changes.

![image](https://github.com/osutaiko/Tacobo/assets/87028262/9225781b-ebba-4bc5-8f22-4d26533630a4)

![20230905010956148550](https://github.com/osutaiko/Tacobo/assets/87028262/54d2092f-5391-4153-8d61-d2981a533204)
