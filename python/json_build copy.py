from urllib.request import urlopen
import re
import json
import os

base_url = "https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/event.aspx"

#List of all Windows Security Event IDs
with open(os.path.join(os.path.dirname(__file__), "..", "assets", "full-list.md"), "r", encoding="utf-8") as f:
    event_ids = f.read().splitlines()

def scrape_content(event_id):
    url = f"{base_url}?eventid={event_id}"
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")

    # --- Event Title ---
    log_index = html.find('<p class="hey">')
    log_start_index = log_index + len('<p class="hey">')
    log_end_index = html.find("</p>")
    log = html[log_start_index:log_end_index].strip()
    log = log[5:].strip()

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

    event_id = dict([('log', log), ('description', description)])
    return event_id

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "assets", "data.json")

data = {}

for id in event_ids:
    data[id] = scrape_content(id)

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)