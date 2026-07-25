import ollama from 'ollama';

const input = document.getElementById("event_id");
const button = document.getElementById("search");
const results = document.getElementById("results");

let eventsXmlPromise = null;

function loadEventsXml() {
    if (!eventsXmlPromise) {
        eventsXmlPromise = fetch("assets/events.xml").then((res) => {
            if (!res.ok) throw new Error(`Failed to load events.xml (${res.status})`);
            return res.text();
        });
    }
    return eventsXmlPromise;
}

function extractTag(block, tag) {
    const match = block.match(new RegExp(`<${tag}>([\\s\\S]*?)</${tag}>`));
    return match ? match[1].replace(/\s+/g, " ").trim() : null;
}

// events.xml isn't well-formed XML (unescaped markup, unclosed root tag),
// so entries are pulled out with regex per-block rather than a DOM parser.
function findEventEntries(xmlText, eventId) {
    const entries = [];
    const blockPattern = /<event>([\s\S]*?)<\/event>/g;
    let match;
    while ((match = blockPattern.exec(xmlText)) !== null) {
        const block = match[1];
        const id = extractTag(block, "id");
        if (id !== eventId) continue;

        entries.push({
            source: extractTag(block, "source"),
            knowledge: extractTag(block, "knowledge"),
            description: extractTag(block, "description"),
        });
    }
    return entries;
}

function buildContext(eventId, entries) {
    return entries
        .map((entry, i) => {
            const lines = [`Entry ${i + 1} for event ID ${eventId}:`];
            if (entry.source) lines.push(`Source: ${entry.source}`);
            if (entry.description) lines.push(`Description: ${entry.description}`);
            if (entry.knowledge) lines.push(`Knowledge: ${entry.knowledge}`);
            return lines.join("\n");
        })
        .join("\n\n");
}

function renderResult(text) {
    results.textContent = "";
    const heading = document.createElement("strong");
    heading.textContent = "Results";
    results.appendChild(heading);
    results.appendChild(document.createElement("br"));
    results.appendChild(document.createTextNode(text));
}

button.addEventListener("click", async (event) => {
    event.preventDefault();

    const eventId = input.value.trim();
    if (!eventId) return;

    results.textContent = "Loading...";

    try {
        const xmlText = await loadEventsXml();
        const entries = findEventEntries(xmlText, eventId);

        if (entries.length === 0) {
            renderResult(`No entry found for event ID ${eventId} in events.xml.`);
            return;
        }

        const context = buildContext(eventId, entries);

        const response = await ollama.chat({
            model: "qwen3.6",
            messages: [
                {
                    role: "system",
                    content: "You are a Windows Security Log assistant. Only use the information " +
                        "given in the context below to answer. Do not add facts that are not present " +
                        "in the context, and do not rely on outside knowledge. If the context is " +
                        "incomplete, say 'This event is not well documented.' instead of guessing." +
                        "avoid saying 'Based on the provided context'",
                },
                {
                    role: "user",
                    content: `Context:\n${context}\n\n` +
                        `Explain Windows Security Log event ID ${eventId}: what it means and why it might occur.`,
                },
            ],
            stream: false,
        });

        renderResult(response.message.content);
    } catch (err) {
        results.textContent = `Error: ${err.message}`;
    }
});
