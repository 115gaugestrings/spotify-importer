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

count = 0
for play in all_plays:
    artistName = play['artistName']
    trackName = play['trackName']
    msPlayed = play['msPlayed']
    if msPlayed > 30000 and artistName is not None and trackName is not None:
        count = count + 1
print(count)

endTime = all_plays[0]['endTime']
moment = datetime.strptime(endTime, "%Y-%m-%d %H:%M")
print(moment)

msPlayed = all_plays[0]['msPlayed']
start = moment - timedelta(milliseconds=msPlayed)
print(start)