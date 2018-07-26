# VillSorter
A python program based on Minecraft to determine the best cost for a particular enchantment out of the villagers given in a .txt file.

In it's current state, a .txt file with a number and ':' starting each line (up to the desired amount of villagers) will be used to store information about villagers.

The program will parse the .txt file and provide several desired statistics about enchantments and the villagers as output. This includes:
 - Enchantment name, current cheapest cost, difference between cost and minimum possible cost, and the villager with the cheapest trade
 - Villager number, a rating based on how many good trades they have, a list of their good trades, and the price of the trade.
 
Future changes include:
 - initializing the .txt file if it does not already exist
 - initializing a line with a number if it does not already have one
 - fixing the input for creating a villager for more versatility
 - an extra comparison step before officially adding a villager to the list
 - various bug fixes and code enhancement