import os
import re

fp = open(os.path.join(os.path.dirname(__file__), "..", "assets", "events.html"), "r", encoding="utf-8")
pos = 0
pattern = r'<td>(.*?)</td>'

for line in fp:
    stripped = line.strip()
    if stripped == "":
        pos = 0
        continue
    if pos in (0, 3):
        new_line = re.findall(pattern, line, flags=re.DOTALL)
        if pos == 0:
            print(f"<id>{new_line[0]}</id>")
        if pos == 3:
            print(f"  <description>{new_line[0]}</description>")
#        print("".join(new_line))
    pos += 1

fp.close()