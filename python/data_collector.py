from urllib.request import urlopen

url = "https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/event.aspx?eventid=1105"

page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")

# --- Event Title ---

log_title_index = html.find('<p class="hey">')
log_title_start_index = log_title_index + len('<p class="hey">')
log_title_end_index = html.find("</p>")
log_title = html[log_title_start_index:log_title_end_index].strip()

# --- Description Paragraph --- 

p_index = html.index('</p>')

print(log_title)
print(p_index)

#print(span) // Windows Security Log Event ID 1105
# <div id="contentMargin">

'''
<p class="hey">
        1105: Event log automatic backup
    </p>

    <p>
'''