from urllib.request import urlopen
import re
import json

url = "https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/event.aspx?eventid=1105"
#base_url = "https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/event.aspx"
#event_id = id_num from loop?
#url = f"{base_url}?eventid={event_id}"

'''

# Open the markdown file in read mode with UTF-8 encoding
with open("refences/full-list.md", "r", encoding="utf-8") as file:
    content = file.read()

# View the raw markdown text
print(content)
'''

with open("full-list.md", "r", encoding="utf-8") as file:
    content = file.read()

# View the raw markdown text
print(content)

page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")

# --- Event Title ---
log_title_index = html.find('<p class="hey">')
log_title_start_index = log_title_index + len('<p class="hey">')
log_title_end_index = html.find("</p>")
log_title = html[log_title_start_index:log_title_end_index].strip()

# The main content is located in a <div> with a class "contentMargin"
# This websites developer skipped using identifiers for any of the content that matters for this project
# Due to this, I had to get a bit creative on where to start and end indexes 
# I DO NOT recommend this approach
# When available, always scrape content using HTML identifiers

# --- Goofy Code --- NOT RECOMMENDED ---

stopPoint_contentMargin = """
  </div>
</div>
    """

contentMargin_index = html.find('<div id="contentMargin">')
contentMargin_start_index = contentMargin_index + len('<div id="contentMargin">')
contentMargin_end_index = html.find(stopPoint_contentMargin, contentMargin_start_index)
contentMargin = html[contentMargin_start_index:contentMargin_end_index]

startingPoint_description= "</ul>"
stopPoint_description= "</p><h2>"
description_index = contentMargin.find(startingPoint_description)
description_start_index = description_index + len(startingPoint_description)
description_end_index = contentMargin.find(stopPoint_description, description_start_index)
description = contentMargin[description_start_index:description_end_index].strip()
description = re.sub(r'^<p>', '', description) # <--- Claude Code wrote with this line

'''
The value for "description" gets reassigned here as it is the easiest way of removing the <p> tag that prints. 
Again, this is certainly not the best coding practice, it is the only work-around I could find to manage the lack of named tags in the HTML code.
'''

print(log_title)
print(description)

log_1105 = dict([('title', log_title), ('description', description)])
new_json_string = json.dumps(log_1105)
'''
print(log_1105)
print(new_json_string)


for each line in the file with all listed IDs
read the id num

base_url = "https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/event.aspx"
event_id = "1104"
url = f"{base_url}?eventid={event_id}"

create py dict
parse to json
'''