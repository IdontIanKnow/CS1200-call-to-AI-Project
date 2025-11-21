async function sendToAI() {
    const userInput = document.getElementById("prompt").value;

    const res = await fetch("https://api.openai.com/v1/chat/completions", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer YOUR_KEY"
        },
        body: JSON.stringify({
            model: "gpt-4o-mini",
            max_tokens: 150, // keeps response under ~200 words
            messages: [
                { role: "user", content: userInput }
            ]
        })
    });

    const data = await res.json();
    const message = data.choices[0].message.content;

    document.getElementById("response").innerText = message;
}
