from urllib.request import urlopen
import re
import os

'''
User Security Encyclopedia for log name
Use Windows learn for event description
'''
'''
#List of all Windows Security Event IDs
with open(os.path.join(os.path.dirname(__file__), "..", "assets", "full-list.md"), "r", encoding="utf-8") as f:
    event_ids = f.read().splitlines()
'''
def scrape_content(event_id):
    base_url = "https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/event.aspx"
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

    event = dict([('event_id', event_id), ('log', log)])
    return event
    # The main content is located in a <div> with a class "contentMargin"
    # This websites developer skipped using identifiers for any of the content that matters for this project
    # Due to this, I had to get a bit creative on where to start and end indexes 
    # I DO NOT recommend this approach
    # When available, always scrape content using HTML identifiers

    # --- Goofy Code --- NOT RECOMMENDED --- This might be what can be replaced with Windows Learn
    #html.find("<td>eventId</td>")
    #stopPoint = """
    #</td>
    #</tr>
    # """
'''
    stopPoint_contentMargin = """
      </div>
    </div>
    """

    contentMargin_index = html.find('<div id="contentMargin">')
    contentMargin_start_index = contentMargin_index + len('<div id="contentMargin">')
    contentMargin_end_index = html.find(stopPoint_contentMargin, contentMargin_start_index)
    contentMargin = html[contentMargin_start_index:contentMargin_end_index]

    

    startingPoint_description= "<p>\n"
    stopPoint_description = ("</p>\n")
    description_index = contentMargin.find(startingPoint_description)
    description_start_index = description_index + len(startingPoint_description)
    description_end_index = contentMargin.find(stopPoint_description, description_start_index)
    description = contentMargin[description_start_index:description_end_index].strip()
    description = re.sub(r'^<p>', '', description) # <--- Claude Code wrote with this line


    The value for "description" gets reassigned here as it is the easiest way of removing the <p> tag that prints. 
    Again, this is certainly not the best coding practice, it is the only work-around I could find to manage the lack of named tags in the HTML code.
'''

print(scrape_content("4608"))