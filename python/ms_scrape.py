from urllib.request import urlopen
import os
import re

url = "https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/appendix-l--events-to-monitor"
page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")

table_index = html.find("<tbody>")
table_start_index = table_index + len('<tbody>')
table_end_index = html.find("</tbody>")
table = html[table_start_index:table_end_index].strip()

pattern = r'<tr>(.*?)</tr>'
matches = re.findall(pattern, html, flags=re.DOTALL)

with open("events.html", "w", encoding="utf-8") as f:
    for match in matches:
        f.write(match + '\n')