#: id: ip12-11
#: group: dataframe
#: title: Use label-based indexing (loc), position-based indexing (iloc) and Boolean indexing on a DataFrame of players.
#: title_hi: खिलाड़ियों के डेटाफ़्रेम पर लेबल-आधारित (loc), स्थिति-आधारित (iloc) और बूलियन इंडेक्सिंग कीजिए।
# Program 11: loc, iloc and Boolean indexing
import pandas as pd

players = pd.DataFrame({
    "Team": ["India", "Australia", "India", "England", "India"],
    "Runs": [512, 430, 610, 388, 275],
    "Matches": [10, 9, 11, 8, 7],
}, index=["Virat", "Steve", "Shubman", "Joe", "Rishabh"])
print(players)
print("\nloc - rows Steve to Joe, columns Runs and Matches:")
print(players.loc["Steve":"Joe", ["Runs", "Matches"]])
print("\niloc - first two rows, first two columns:")
print(players.iloc[0:2, 0:2])
print("\nPlayers with more than 400 runs:")
print(players[players["Runs"] > 400])
print("\nIndian players with more than 300 runs:")
print(players[(players["Team"] == "India") & (players["Runs"] > 300)])
