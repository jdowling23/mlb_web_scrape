import statsapi
import pandas as pd
from datetime import date

todays_date = date.today()
print(todays_date)

#Tampa bay rays team_id 139
#statsapi.schedule(date=None, start_date=None, end_date=None, team="", opponent="", sportId=1, game_id=777353, season=None, include_series_status=True)

#print(statsapi.get("schedule", {"sportId":1, "startDate":"03/27/2025", "endDate": todays_date, "fields": "dates, date, games, gamePk"}))

#team lookup
team = statsapi.lookup_team('TB')
#print(team)

#get the Tampa Bay Rays metadata
tb = statsapi.get('team', {'teamId':139})
#print(tb)

#pull 2025 game results for TB Rays
tb_sched_list = statsapi.schedule(date=None, start_date="03/27/2025", end_date=todays_date, team="139", opponent="", sportId=1, game_id=None, season=None, include_series_status=True)

tb_sched_df = pd.DataFrame(tb_sched_list)
#print(tb_sched_df)


game_1 = pd.DataFrame(statsapi.boxscore_data(778560, timecode=None))
print(game_1)

#output xlsx spreadsheet of data
path = r'C:\\Users\jdowl\Python\TB Stats.xlsx'
writer = pd.ExcelWriter(path, engine = 'xlsxwriter')
tb_sched_df.to_excel(writer, sheet_name='TB Rays 2025')
writer.close()
