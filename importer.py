import json
from pathlib import Path
from datetime import datetime, timedelta
import sys
DAILY_LIMIT = 2800
folder = Path.home() / "Desktop" / "spotify-data"
all_plays = []
for n in range(4):
    file = folder / f"StreamingHistory_music_{n}.json"
    print(file)
    with open(file, encoding="utf-8") as f:
        batch = json.load(f)
    all_plays.extend(batch)
    print(len(batch))
print(len(all_plays))

good_plays = []
for play in all_plays:
    artistName = play['artistName']
    trackName = play['trackName']
    msPlayed = play['msPlayed']
    if msPlayed > 30000 and artistName is not None and trackName is not None:
        moment = datetime.strptime(play['endTime'], "%Y-%m-%d %H:%M")
        start = moment - timedelta(milliseconds=msPlayed)
        play['startTime'] = start
        good_plays.append(play)
print(len(good_plays))
print(good_plays[0])

end = datetime.now()
progress_file = Path("progress.json")
if progress_file.exists():
    with open(progress_file, encoding="utf-8") as f:
        saved = json.load(f)
    start_index = saved['next_index']
    begin = datetime.fromisoformat(saved['last_end'])
else:
    start_index = 0
    begin = end - timedelta(hours=24)
print(start_index)

oldest_allowed = end - timedelta(days=13)
if begin < oldest_allowed:
    begin = oldest_allowed

todays_plays = good_plays[start_index : start_index + DAILY_LIMIT]
if len(todays_plays) == 0:
    sys.exit("All plays have been scrobbled :D")
gap = (end - begin) / len(todays_plays)
print(gap)
i = 0
for play in todays_plays:
    play['newTime'] = (begin + gap * i)
    i = i + 1
print(todays_plays[0]['newTime'])
print(todays_plays[-1]['newTime'])

progress = {'next_index': start_index + len(todays_plays), 'last_end': end.isoformat()}
print(progress)

with open("progress.json", "w", encoding="utf-8") as f:
    json.dump(progress, f)