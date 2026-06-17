from datetime import datetime, timedelta

tz = " +0200"

def build_time(date, time):
    return date.strftime("%Y%m%d") + time.replace(":", "") + "00"

channels = {}
programmes = []

with open("schedule.txt", "r", encoding="utf-8") as f:
    for line in f:
        channel_id, channel_name, rest = line.strip().split("|", 2)
        start, end, title = rest.split(" ", 2)

        # حفظ القنوات مرة واحدة فقط
        if channel_id not in channels:
            channels[channel_id] = channel_name

        programmes.append((channel_id, start, end, title))

with open("epg.xml", "w", encoding="utf-8") as out:
    out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    out.write("<tv>\n")

    # 1️⃣ القنوات
    for cid, cname in channels.items():
        out.write(f'<channel id="{cid}">\n')
        out.write(f"<display-name>{cname}</display-name>\n")
        out.write("</channel>\n")

    # 2️⃣ البرامج (7 أيام)
    for i in range(7):
        day = datetime.now() + timedelta(days=i)

        for cid, start, end, title in programmes:
            start_time = build_time(day, start)
            end_time = build_time(day, end)

            out.write(f'<programme channel="{cid}" start="{start_time}{tz}" stop="{end_time}{tz}">\n')
            out.write(f"<title>{title}</title>\n")
            out.write("</programme>\n")

    out.write("</tv>\n")
