from datetime import datetime, timedelta

tz = " +0200"

def build_time(date, time):
    return date.strftime("%Y%m%d") + time.replace(":", "") + "00"

channels = {}
programmes = []

print("START SCRIPT")

with open("schedule.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or "|" not in line:
            continue

        try:
            channel_id, rest, channel_name = line.split("|", 2)
            start, end, title = rest.split(" ", 2)

            channels[channel_id] = channel_name
            programmes.append((channel_id, start, end, title))

        except Exception as e:
            print("SKIP LINE:", line, e)

print("CHANNELS:", len(channels))
print("PROGRAMMES:", len(programmes))

with open("epg.xml", "w", encoding="utf-8") as out:
    out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    out.write("<tv>\n")

    for cid, cname in channels.items():
        out.write(f'<channel id="{cid}">\n')
        out.write(f"<display-name>{cname}</display-name>\n")
        out.write("</channel>\n")

    for i in range(7):
        day = datetime.now() + timedelta(days=i)

        for cid, start, end, title in programmes:
            start_time = build_time(day, start)
            end_time = build_time(day, end)

            out.write(f'<programme channel="{cid}" start="{start_time}{tz}" stop="{end_time}{tz}">\n')
            out.write(f"<title>{title}</title>\n")
            out.write("</programme>\n")

    out.write("</tv>\n")

print("DONE -> epg.xml created")
