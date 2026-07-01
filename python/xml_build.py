from urllib.request import urlopen
import os
import re

#--- Main URL ---

def ms_scrape():
    url = "https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/appendix-l--events-to-monitor"
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")

    table_index = html.find("<tbody>")
    table_start_index = table_index + len('<tbody>')
    table_end_index = html.find("</tbody>")
    table = html[table_start_index:table_end_index].strip()

    pattern = r'<tr>(.*?)</tr>'
    matches = re.findall(pattern, table, flags=re.DOTALL)

# --- Ouput to raw HTML file with incorrect tags ---
    html_path = os.path.join(os.path.dirname(__file__), "..", "assets", "events.html")
    with open(html_path, "w", encoding="utf-8") as f:
        for match in matches:
            f.write(match + '\n')

# --- Secondary URL ---

def uws_scrape(event_id):
    base_url = "https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/event.aspx"
    url = f"{base_url}?eventid={event_id}"
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")

    # This website's developer skipped using identifiers for any of the content that matters for this project
    # Due to this, I had to get a bit creative on where to start and end indexes 
    # I DO NOT recommend this approach
    # When available, always scrape content using HTML identifiers
       
    # --- Event Title ---
    log_index = html.find('<p class="hey">')
    log_start_index = log_index + len('<p class="hey">')
    log_end_index = html.find("</p>")
    log = html[log_start_index:log_end_index].strip()
    log = log[5:].strip()
    
    ''' The main content is located in a <div> with a class "contentMargin" 
    so we're using a longer approach to locate the tag holding the event description 
    
   # --- Event Description ---   
    stopPoint_contentMargin = """
      </div>
    </div>
    """

    contentMargin_index = html.find('<div id="contentMargin">')
    contentMargin_start_index = contentMargin_index + len('<div id="contentMargin">')
    contentMargin_end_index = html.find(stopPoint_contentMargin, contentMargin_start_index)
    contentMargin = html[contentMargin_start_index:contentMargin_end_index]
  
    # Using "contentMargin" as one of our only class names, we can use more sneaky tricks to locate the description
    startingPoint_description= "</ul>"
    stopPoint_description= "</p><h2>"
    description_index = contentMargin.find(startingPoint_description)
    description_start_index = description_index + len(startingPoint_description)
    description_end_index = contentMargin.find(stopPoint_description, description_start_index)
    description = contentMargin[description_start_index:description_end_index].strip()
    description = re.sub(r'^<p>', '', description) # <-- The value for "description" gets reassigned here as it is the easiest way of removing the <p> tag that prints. 
    
    # Again, these are work-arounds I used to manage the lack of named tags in the HTML code.
    # View `ms_scrape.py` for a better demonstration of web scraping code 
    '''
    event = dict([('event_id', event_id), ('log', log),])
    return event

def full_list_scrape():
    list_path = os.path.join(os.path.dirname(__file__), "..", "assets", "full-list.md")
    html_path = os.path.join(os.path.dirname(__file__), "..", "assets", "events.html")

    with open(list_path, "r", encoding="utf-8") as fp:
        event_ids = [line.strip() for line in fp if line.strip()]

    with open(html_path, "a", encoding="utf-8") as f:
        for event_id in event_ids:
            event = uws_scrape(event_id)
            f.write(f"""<td>{event_id}</td>
<td>N/A</td>
<td>N/A</td>
<td>{event['log']}</td>
\n""")

def write_out():

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
            if pos == 3:
                description = f"<description>{new_line[0]}</description>"
                ft.writelines(f"""
    <event>
     {id}      
      {description}       
     </event>
     """)
        pos += 1

    fp.close()
    ft.close()

ms_scrape()
full_list_scrape()
write_out()