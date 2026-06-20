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


demo.py
Traceback (most recent call last):
  File "/media/pico/Coco1/Portfolio/Projects/Python/Windows-Event-ID-Summarizer/python/demo.py", line 1, in <module>
    with open("../assets/data.json", "a", encoding="utf-8") as f:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '../assets/data.json'
Let me check the file and project structure.

Read demo.py
Bash List project root directory
IN
ls /media/pico/Coco1/Portfolio/Projects/Python/Windows-Event-ID-Summarizer/

OUT
assets
python
README.md
references
The assets/ directory exists but data.json doesn't. The git status also shows assets/data.json as untracked, meaning it exists on disk now — let me check.

Bash List assets directory
IN
ls /media/pico/Coco1/Portfolio/Projects/Python/Windows-Event-ID-Summarizer/assets/

OUT
data.json
source.sh
assets/data.json exists. The problem is that ../assets/data.json is a relative path resolved from the current working directory when you run the script, not from the script's location. If you run demo.py from inside the python/ folder it works, but if you run it from the project root it looks for assets/ one level up from there (which doesn't exist).

The fix is to build the path relative to the script file itself: