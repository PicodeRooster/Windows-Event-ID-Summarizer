# Windows Event ID Summarizer

Look up a Windows Event ID and get a plain-language summary back — offline, with no external API calls at query time.

## How it works

1. **Build the reference data** (`python/xml_build.py`) — scrapes two sources and merges them into `assets/events.xml`:
   - **[Microsoft Learn — Appendix L: Events to Monitor](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/appendix-l--events-to-monitor)** (`ms_scrape()`) — the definitive list of *which* security Event IDs matter. No per-event description text.
   - **[Ultimate Windows Security Encyclopedia](https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/default.aspx)** (`uws_scrape()`) — looked up one Event ID at a time via `?eventid=<id>`, for the event title text.
2. **Summarize at query time** (planned) — a local LLM reads the relevant entry from `events.xml` and generates a natural-language summary, so wording varies without needing internet access or an external API.

## Current status

- The scrape pipeline (`ms_scrape → full_list_scrape → uws_scrape → write_out`) runs end-to-end and produces `assets/events.xml` (~500 event IDs).
- **Known limitation:** UWS's HTML has no reliable identifiers around the actual description paragraph, so only the short event *title* is captured today. The `<description>` field in `events.xml` currently holds that title, not the fuller description text. Fixing this scrape (or finding a better source) is the next step before the data is genuinely useful for summarization.

  This was the vision, workarounds and all, before ultimately realizing that each eventid link was too inconsistent with its usage of tags to make reliably scrape this section. It would have lead to more manual work to scrape with the fix I had and attempt to remove the unnecessary sections:

  ```python
  # The main content is located in a <div> with a class "contentMargin"
  # so we're using a longer approach to locate the tag holding the event description

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
  startingPoint_description = "</ul>"
  stopPoint_description = "</p><h2>"
  description_index = contentMargin.find(startingPoint_description)
  description_start_index = description_index + len(startingPoint_description)
  description_end_index = contentMargin.find(stopPoint_description, description_start_index)
  description = contentMargin[description_start_index:description_end_index].strip()
  description = re.sub(r'^<p>', '', description)  # easiest way to strip the leading <p> tag
  ```

  Full version, comments and all, still lives in [`uws_scrape()`](python/xml_build.py#L48-L75).
- The summarization/query side (LLM + lookup script) hasn't been built yet.

## Planned stack

**Ollama** (run a model locally) + a small instruction-tuned model + a Python script that loads `events.xml`, finds the relevant entry, and stuffs it into the prompt. No vector DB needed at this data size — a strict system prompt plus a small, well-scoped context (RAG in the loosest sense) is what keeps the model from hallucinating or pulling in outside context, not model size.

Candidate models: **Qwen2.5 3B** or **Mistral 7B** via Ollama — free, local, follow instructions well. Qwen2.5 3B is light enough to run on most hardware.

## Usage

```bash
python python/xml_build.py
```

Rebuilds `assets/events.html` and `assets/events.xml` from scratch by re-scraping both sources.

## Project layout

```
python/xml_build.py   scrape + build pipeline
assets/full-list.md    input list of Event IDs (from ms_scrape)
assets/events.html      intermediate scrape output
assets/events.xml       final merged ID + description data
assets/archive/         earlier scraping attempts, kept for reference
```

## Notes

- UWS's terms of service don't prohibit scraping; this project scrapes at a low, one-time build rate rather than per-query.
