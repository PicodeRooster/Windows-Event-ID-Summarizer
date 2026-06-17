# Windows Event ID Summarizer

Input Windows Event ID, return simplified summary. 
Web scrape 
Data should live in local folder - final product should work offline-free - probably JSON file
User inputs id number
Program returns full code text with summary
AI? Probably, just for personalized summary - info insn't exactly the same each time. 
Agent is narrow, trained only on its own data. 
Llama? It's free

For this setup, a small local model with a strict system prompt and RAG. The strictness of the system prompt is what prevents hallucination/external context — not the model's size.

### The simplest possible stack

**Ollama** (run the model locally, zero setup) + **a small model** + **a Python script that loads your JSON, finds the relevant bits, and stuffs them into the prompt.**

You don't even need a vector DB for this if your JSON isn't enormous. You can do it with pure Python.

#### Model recommendation

**Qwen2.5 3B or Mistral 7B via Ollama** — both are free, run locally, follow instructions well, and small enough to be fast on a regular machine. Qwen2.5 3B will run on basically anything.

---
```
response = requests.get(URL)
html_data = response.text
```
---
Target source. Terms of service mention nothing on webscraping:
`https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/default.aspx`

All event id links follow the pattern
`https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/event.aspx?eventid=<eventID>`

```
<div>contentMargin </div>
        <p class="hey">
        1105: Event log automatic backup
    </p>
    
    <p>This event is only logged when "When maximum log size is reached:" is set to "Archive the log when full, do not overwrite events". When the log reaches maximum size Windows saves it to %systemroot%\System32\Winevt\Logs\ with the file name Archive-Security-YYYY-MM-DD-HH-MM-SS-NNN.evtx.</p>

```

urllib building block

```
from urllib.request import urlopen

url = "https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/"
page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")

title_index = html.find("<title>")
start_index = title_index + len("<title>")
end_index = html.find("</title>")
title = html[start_index:end_index]

print(title) #Windows Security Log Encyclopedia
```

