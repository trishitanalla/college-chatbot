// App.jsx
import React, { useState, useRef, useEffect } from "react";
import "./Chat.css"; // Make sure you have some basic styling

function App() {
  const [q, setQ] = useState("");
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  // Automatically scroll to the bottom of the chat
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chat]);

  const send = async () => {
    if (!q || loading) return;
    setLoading(true);

    // Add user's question to the chat immediately
    const userMessage = { type: "user", text: q };
    setChat(prevChat => [...prevChat, userMessage]);
    setQ(""); // Clear input field

    try {
      const res = await fetch("http://localhost:5000/ask", { // Use full URL for clarity
        method: "POST",
        body: JSON.stringify({ question: q }),
        headers: { "Content-Type": "application/json" },
      });
      const js = await res.json();
      
      let botMessage;
      if (res.ok) {
        botMessage = { type: "bot", text: js.answer, sources: js.sources };
      } else {
        botMessage = { type: "bot", text: `Error: ${js.error}`, sources: [] };
        console.error("Backend error:", js.error);
      }
      setChat(prevChat => [...prevChat, botMessage]);

    } catch (e) {
      const errorMessage = { type: "bot", text: "Network error. Could not connect to the backend.", sources: [] };
      setChat(prevChat => [...prevChat, errorMessage]);
      console.error("Network error:", e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <h1>Sri Vasavi Engg. College Bot</h1>
      <div className="conversation">
        {chat.map((c, i) => (
          <div key={i} className={`message ${c.type}`}>
            <div className="message-text">{c.text}</div>
            {c.type === "bot" && c.sources && c.sources.length > 0 && (
              <div className="sources">
                <strong>Sources:</strong>
                <ul>
                  {c.sources.map((source, idx) => (
                    <li key={idx}>
                      <a href={source.source} target="_blank" rel="noopener noreferrer">
                        {source.source}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
        {loading && <div className="message bot"><em>Bot is thinking...</em></div>}
        <div ref={chatEndRef} />
      </div>
      <div className="input-area">
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Ask about courses, faculty, etc."
          onKeyDown={(e) => e.key === "Enter" && send()}
          disabled={loading}
        />
        <button onClick={send} disabled={loading}>
          {loading ? "Wait..." : "Send"}
        </button>
      </div>
    </div>
  );
}

export default App;