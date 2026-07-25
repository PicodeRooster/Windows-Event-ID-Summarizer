import ollama from 'ollama';

const input = document.getElementById("event_id");
const button = document.getElementById("search");
const results = document.getElementById("results");

button.addEventListener("click", async (event) => {
    event.preventDefault();

    const eventId = input.value;
    if (!eventId) return;

    results.textContent = "Loading...";

    try {
        const response = await ollama.chat({
            model: "qwen3.6",
            messages: [{
                role: "user",
                content: `Explain Windows Security Log event ID ${eventId}: what it means and why it might occur.`
            }],
            stream: false
        });

        results.textContent = "";
        const heading = document.createElement("strong");
        heading.textContent = "Results";
        results.appendChild(heading);
        results.appendChild(document.createElement("br"));
        results.appendChild(document.createTextNode(response.message.content));
    } catch (err) {
        results.textContent = `Error: ${err.message}`;
    }
});
