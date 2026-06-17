from urllib.request import urlopen
url = "https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/event.aspx?eventid=1105"
page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")

h2_index = html.find("<h2>")
start_index = h2_index + len("<h2>")
end_index = html.find("</h2>")
h2 = html[start_index:end_index]

print(h2)