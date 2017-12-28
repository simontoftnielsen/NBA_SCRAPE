####################################################################################

PURPOSE: <br />
To scrape team and player stats from NBA.com, for all games played within a specified period <br />

OUTPUT: <br />
a. A list of games played in the specified seasons. Containing an ID for the game, ID's for the teams, scores and result of the game <br />
b. A dictionary containing team and player stats per game <br />

INPUT NEEDED: <br />
game_list_path:       Path to store a pickle containing the list of games played <br />
data_path:            Path to store a pickle containing the dictionary of team and player stats <br />
start_year:           Earliest season from which you want to retrieve data [2000 season is the earliest] <br />
end_year:             Latest season <br />
games_actual_season:  Number of games played so far, if you are in mid-season [otherwise insert 'default'] <br />


OUTPUT DICTIONARY: <br />
The dictionary is built containing below levels: <br />
-> season_ID <br />
  -> team_ID <br />
    -> player_ID or 'team_stats' <br />
      -> game_ID <br />
        -> a list of data on the player or the team for the specific game <br />

####################################################################################
