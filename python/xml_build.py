import os
import re

fp = open(os.path.join(os.path.dirname(__file__), "..", "assets", "events.html"), "r", encoding="utf-8")
ft = open(os.path.join(os.path.dirname(__file__), "..", "assets", "events.xml"), "w", encoding="utf-8")

ft.write("""<?xml version"1.0"?>
 <eventIdListings title="Windows Security Events">""")

pattern = r'<td>(.*?)</td>'
pos = 0
for line in fp:
    stripped = line.strip()
    if stripped == "":
        pos = 0
        continue
    if pos in (0, 3):
        new_line = re.findall(pattern, line, flags=re.DOTALL)
        if pos == 0:
            id = f"<id>{new_line[0]}</id>"
#            print(f"<id>{new_line[0]}</id>")
        if pos == 3:
            description = f"<description>{new_line[0]}</description>"
#            print(f"<description>{new_line[0]}</description>")
#        print("".join(new_line))
            ft.writelines(f"""
<event>
 {id}      
 {description}       
 </event>
""")
    pos += 1

fp.close()
ft.close()