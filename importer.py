import json
from pathlib import Path
from datetime import datetime, timedelta
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