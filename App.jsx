import { useState } from "react";
import api from "./services/api";
import "./App.css";

export default function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "👋 Welcome to NIT AI Assistant. Ask me anything about college regulations.",
    },
  ]);
  const [loading, setLoading] = useState(false);

 const suggestions = [
  "Admission",
  "Attendance",
  "Examination",
  "Hostel",
];

  const sendMessage = async (customQuestion = null) => {
    const q = customQuestion || question;

    if (!q.trim()) return;

   setMessages((prev) => [
  ...prev,
  {
    sender: "user",
    text: q,
    time: new Date().toLocaleTimeString()
  }
]);
    setQuestion("");
    setLoading(true);

    try {
      const response = await api.post("/chat", {
        question: q,
      });

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: response.data.answer,
          rule: response.data.rule_number,
          source: response.data.source_document,
          time: new Date().toLocaleTimeString(),
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "⚠ Unable to connect to backend",
           time: new Date().toLocaleTimeString(),
        },
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="app">
      <aside className="sidebar">
        <h2>🎓 NIT AI</h2>

        <div className="menu">
          <button className="menu-btn"
  onClick={() => {
    setMessages([]);
  }}
>
  💬 New Chat
</button>
          <button className="menu-btn"
  onClick={() => {
    alert("Uploaded Documents: 1");
  }}
>
  📚 Documents
</button>
          <button className="menu-btn"
  onClick={() => {
    alert("Rules indexed successfully in ChromaDB");
  }}
>
  📖 Rules
</button>
          <button className="menu-btn"
  onClick={() => {
    alert(
      "AI Model: Llama3\nVector DB: ChromaDB\nBackend: FastAPI"
    );
  }}
>
  ⚙ Settings
</button>
        </div>

        <div className="stats">
          <h4>Project Stats</h4>
          <p>📄 Documents: 1</p>
          <p>🤖 AI Model: Llama3</p>
          <p>🔍 Search: ChromaDB</p>


          <h4>Technologies</h4>
          <p>⚛ React.js</p>
          <p>⚡ FastAPI</p>
          <p>🤖 Llama3</p>
          <p>🗄 ChromaDB</p>
          <p>📄 PDF Parsing</p>
          <p>🔍 RAG Search</p>
        </div>
      </aside>

      <main className="chat-container">
        <div className="header">
          <h1>NIT College AI Assistant</h1>
          <p>AI-Powered Regulation & Policy Assistant</p>
          <div className="dashboard">
  <div className="card">
    <h3>📄 Documents</h3>
    <p>1</p>
  </div>

  <div className="card">
    <h3>📚 Rules Indexed</h3>
    <p>500+</p>
  </div>

  <div className="card">
    <h3>🤖 AI Model</h3>
    <p>Llama3</p>
  </div>

  <div className="card">
    <h3>⚡ Status</h3>
    <p>Online</p>
  </div>
</div>
        </div>

        <div className="suggestions">
          {suggestions.map((item, index) => (
            <button
              key={index}
              onClick={() => sendMessage(item)}
            >
              {item}
            </button>
          ))}
        </div>

        <div className="chat-box">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`message ${msg.sender}`}
            >
              <div className="bubble">

  <div className="message-header">
    {msg.sender === "user"
      ? "👤 You"
      : "🤖 NIT AI"}
  </div>

  <p>{msg.text}</p>

  {msg.rule && (
    <div className="meta">
      <div>📖 Rule: {msg.rule}</div>
      <div>📄 Source: {msg.source}</div>
    </div>
  )}

  <div className="timestamp">
    {msg.time}
  </div>

</div>
            </div>
          ))}

          {loading && (
            <div className="message bot">
              <div className="bubble">
                🤖 Searching regulations...
              </div>
            </div>
          )}
        </div>

       <button
  className="demo-btn"
  onClick={() =>
    sendMessage("What are the admission rules?")
  }
>
  🚀 Demo Query
</button>

<div className="input-area">
  <button className="plus-btn">➕</button>
  <input
    value={question}
    onChange={(e) => setQuestion(e.target.value)}
    placeholder="Ask about college rules..."
  />

  <button onClick={() => sendMessage()}>
    Send
  </button>
</div>
      </main>
    </div>
  );
}