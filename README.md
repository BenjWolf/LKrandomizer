# LKrandomizer v0.8
~~~
Application written by: Benjamin Wolf
Assembly and memory assistance: Papaya (Initials: A.M.W.)
November 3, 2019
~~~
### [Download Here](https://github.com/BenjWolf/LKrandomizer/releases/download/v0.8/LKrandomizer_v0.8DOWNLOAD.rar)
## Description

This program takes a Lost Kingdoms (USA) .iso file and produces a new .iso with the card pickups randomized.

## How to Use This Program

* Download and extract LKrandomizer_v0.8DOWNLOAD.rar
* Keep LKrandomizer.exe and data folder in same directory
* Run LKrandomizer.exe
* Press 'Select .iso' button and choose a clean Lost Kingdoms disc image
* Choose the options you want to include
* Input a custom seed or leave it random
* Seeds must be between one to eight alphanumeric characters
* Press 'Start Randomization' button
* The button will turn to yellow, indicating your .iso is being copied and patched
* A message box will pop up once complete
* A new .iso and/or log.txt will show up in this directory

## Features

* Mix and match randomization options: starting deck, chest cards, shop cards, key items, etc.
* Main levels and side quests included in randomization.
* Difficulty options: deactivated deck points, no escaping battles
* Seed displayed in-game as default player name
* Spoiler log with descriptions of starting deck, chest contents, etc.

## Option Descriptions

### Randomization

* Starting deck: Randomizes 12 cards for your starting deck (see randomization style for more details)
* Chest cards: Card received from opening chest is randomized (includes coffin and sarcophagus)
* Hidden cards: Card hidden on the ground/under obstacles is randomized
* 'Level Bonus' cards: The face down cards you select when completing a level are randomized
* Shop cards: The cards that are purchasable in the Apothecary are randomized
* Red fairy rewards: The cards rewarded to you for trading in fairies is randomized
* Enemy attributes: The elemental type (fire, water, earth, wood, neutral) of enemies is randomized. This affects bosses and card users, as well. Neutral attribute is less likely to be selected.

### Key Items

* Must have randomized chests active to randomize key items
* All 15 items in the game are randomly placed in an accessible location (every seed is beatable)
~~~
Shayel Key, Fruit of Mandragora, Bark of Treant, Man Trap Leaf, Key of Castle Wyht, Red Candle, Blue Candle, Green Candle, Yellow Candle, Old Sheet Music, Stone of Cleansing, White Gem, Black Gem, Stone of Darkness, Necklace of the Pharaoh
~~~
* The original item location (including chests, reward for beating Mind Flayer, and Castle Wyht key giver) will have randomized contents
* The side levels and elemental temples may contain items
* The herb trees in Rohbach are deactivated, to complete the level you must have the 3 herbs in your inventory and reach the last herb tree
* After using an item, or leaving a level, all items stay in your inventory
* After completing a level, you can reenter it anytime so that you can't miss items
* Key items are not saved to memory card, so use save states if you want to save your game
* The pause menu will only show 5 of your items, so take notes

### NPCs that give hints about items:

* Alanjeh Castle - Warrior facing you at start
* Plains of Rowahl - 2 soldiers sitting around campfire
* Blessoon - Warrior by fountain, warrior by diary, Alexander
* Burial Grounds - Warrior near start, Lord Unther
* Castle Grayl - 3 warriors
* Dahl-nok - Border guard
* Kendarie Castle - Cutscene has 3 hints
* Lumsted - Gurd

### Difficulty

* Can't escape battles: Disables walking to edge of arena to leave battle
* Deactivate deck points: Deck points are no longer interactable, making it impossible to heal or edit deck within the level
* Fair Play cards only: Does not generate cards that are banned under the 2-player Fair Play rule

### Other

* LKII card changes: Replaces stone cost, attack power, etc. to match the card stats of Lost Kingdoms II. Some cards are buffed, others are nerfed. Wraith, Flayer Spawn, Lycanthrope, Birdman, Archer Tree, Blood Bush are now weapon cards. Read [here](https://github.com/BenjWolf/LKrandomizer/blob/master/lk2cardChanges.txt) for the full list of changes.
* LKII enemy changes: Replaces HP, defense, attack power to match the enemy stats of Lost Kingdoms II. In general, enemies will do more damage. Read [here](https://github.com/BenjWolf/LKrandomizer/blob/master/lk2enemyChanges.txt) for the full list of changes.

### Randomization Style

Full Random:
* Each card has same chance of being picked. For example, a chest in the first level is equally likely to be a Hobgoblin or God of Destruction. Unlike previous versions, it is now possible to get 12 unique cards in the starting deck. 

Balanced:
* The cards are grouped into 4 levels of rareness (determined in-game). When randomizing card pick-ups, the randomizer looks up what card you get in the original game and chooses a random card of the same rarity. For instance, if a chest gives you a Dragon Knight in the original game, it will be a random level 2 rareness card after randomization.
* Starting deck: Keeps original card distribution pattern (3x 3x 1x 1x 2x 1x 1x) and has a select list of cards to choose for each slot, trying to remain close to the utility of the original deck.

  3x of (lizardman, red lizard, mummy, orc, or ghoul)
  
  3x of (skeleton, hobgoblin, or man trap)
  
  1x of (fairy, rheebus)
  
  1x of (fire golem, lycanthrope, elephant, or chimera)
  
  2x of (dark raven, scythe beast, or flying ray)
  
  1x of (wraith, giant crab, birdman, or venus spider)
  
  1x of (ghost armor, basilisk, dragonoid, dragon knight, or great demon)

## F.A.Q.

* Will the same seed but different options have the same cards?

  All random options must be the same for the same result, but the difficulty options will not impact randomization.
  
* Are the fairy chests randomized?

  Not yet.
  
* Is it possible to start with an unviable deck?

  Yes, but rare.
  
* Why are some enemy attributes not randomized?

  There's a chance of the enemy keeping it's original attribute.

## Known Issues/Bugs

* Key items placed in card chests still show a card model and have incorrect animation
* Key items placed in non-vanilla key item chests show wrong model
* Cards placed in key item chests will not have a model
* Mind Flayer item always shows shayel key model
* Warrior of Wyht item always shows wyht key model 
* Key item inventory will carry between save games/new games, need to reset to empty inventory
* Pause menu only shows first 5 key items

## Special Thanks

* Lost Kingdoms Fastwalking: Discord channel - for being a repository of game knowledge and nice people
* Papaya - for his memory address knowledge, AR codes, function map, and general game expertise
* Dan Salvato's Intro to Wii Game Modding video series
* The guide authors at GameFAQs

## Feedback?

Contact me:
wolfbenjamin@protonmail.com
