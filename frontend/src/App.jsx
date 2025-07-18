import React, { useState } from "react";
import "./Chat.css";

function App() {
  const [q, setQ] = useState("");
  const [chat, setChat] = useState([]);

  const send = async () => {
    if (!q) return;
    try {
      const res = await fetch("/ask", {
        method: "POST",
        body: JSON.stringify({ question: q }),
        headers: { "Content-Type": "application/json" },
      });
      const js = await res.json();
      if (res.ok) {
        setChat([...chat, { q, a: js.answer }]);
      } else {
        console.error("Backend error:", js.error);
      }
    } catch (e) {
      console.error("Network error:", e);
    }
    setQ("");
  };

  return (
    <div className="chat-container">
      <h1>College Bot</h1>
      <div className="conversation">
        {chat.map((c, i) => (
          <div key={i}>
            <div className="user">You: {c.q}</div>
            <div className="bot">Bot: {c.a}</div>
          </div>
        ))}
      </div>
      <div className="input-area">
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Ask me..."
          onKeyDown={(e) => e.key === "Enter" && send()}
        />
        <button onClick={send}>Send</button>
      </div>
    </div>
  );
}

export default App;
