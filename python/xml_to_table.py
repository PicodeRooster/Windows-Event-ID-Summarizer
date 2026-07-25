import html
import os
import xml.etree.ElementTree as ET

events_xml = os.path.join(os.path.dirname(__file__), "..", "assets", "events.xml")
event_table_html = os.path.join(os.path.dirname(__file__), "..", "assets", "event_table.html")


def parse_events():
    tree = ET.parse(events_xml)
    events = []
    for event in tree.getroot().findall("event"):
        events.append({
            "id": (event.findtext("id") or "").strip(),
            "source": (event.findtext("source") or "").strip(),
            "description": (event.findtext("description") or "").strip(),
            "knowledge": (event.findtext("knowledge") or "").strip(),
        })
    return events


def write_out(events):
    with open(event_table_html, "w", encoding="utf-8") as fp:
        fp.write("<table>\n  <tr>\n    <th>Event Id</th>\n    <th>Source</th>\n    <th>Description</th>\n    <th>KB</th>\n  </tr>\n")
        for event in events:
            fp.write(
                f"  <tr>\n"
                f"    <td>{html.escape(event['id'])}</td>\n"
                f"    <td>{html.escape(event['source'])}</td>\n"
                f"    <td>{html.escape(event['description'])}</td>\n"
                f"    <td>{html.escape(event['knowledge'])}</td>\n"
                f"  </tr>\n"
            )
        fp.write("</table>\n")


if __name__ == "__main__":
    write_out(parse_events())
