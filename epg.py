from datetime import datetime, timedelta

tz = " +0200"

def build_time(date, time):
    return date.strftime("%Y%m%d") + time.replace(":", "") + "00"

channels = {}

with open("schedule.txt", "r", encoding="utf-8") as f:
    for line in f:
        channel, rest = line.strip().split("|", 1)
        start, end, title = rest.split(" ", 2)

        channels.setdefault(channel, []).append((start, end, title))

with open("epg.xml", "w", encoding="utf-8") as out:
    out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    out.write("<tv>\n")

    for i in range(7):
        day = datetime.now() + timedelta(days=i)

        for channel, items in channels.items():
            for start, end, title in items:

                start_time = build_time(day, start)
                end_time = build_time(day, end)

                out.write(f'<programme channel="{channel}" start="{start_time}{tz}" stop="{end_time}{tz}">\n')
                out.write(f"<title>{title}</title>\n")
                out.write("</programme>\n")

    out.write("</tv>\n")
