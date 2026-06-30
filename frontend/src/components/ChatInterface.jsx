"use client";
import { useState, useEffect, useRef } from "react";
import Message from "./Message";
import InputBar from "./InputBar";
import { sendMessage } from "../services/api";
import { useAuth } from "../context/AuthContext";

export default function ChatInterface() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [error, setError] = useState(null);
  const bottomRef = useRef(null);
  const { user, token, logout } = useAuth();   // NEW

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function handleSend(text) {
    setError(null);
    setMessages(prev => [...prev, { role: "user", content: text }]);
    setLoading(true);
    try {
      const data = await sendMessage(text, sessionId, token);   // CHANGED: pass token
      if (!sessionId) setSessionId(data.session_id);
      setMessages(prev => [...prev, {
        role: "assistant", content: data.reply, agent: data.agent_used
      }]);
    } catch {
      setError("Could not reach the server. Is your backend running on port 8000?");
      setMessages(prev => prev.slice(0, -1));
    } finally {
      setLoading(false);
    }
  }

  function handleNewChat() {
    setMessages([]); setSessionId(null); setError(null);
  }

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100vh",
      maxWidth: "760px", margin: "0 auto", fontFamily: "system-ui, sans-serif" }}>
      
      <div style={{ padding: "16px 20px", borderBottom: "1px solid #E5E7EB",
        display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <h1 style={{ margin: 0, fontSize: "17px", fontWeight: 600 }}>TechMart Support</h1>
          <p style={{ margin: "2px 0 0", fontSize: "13px", color: "#6B7280" }}>
            {user?.name ? `Hi ${user.name}` : "Billing · Tech · Product · FAQ"}
          </p>
        </div>
        <div style={{ display: "flex", gap: "8px" }}>
          <button onClick={handleNewChat} style={btnStyle}>New chat</button>
          <button onClick={logout} style={btnStyle}>Log out</button>
        </div>
      </div>

      <div style={{ flex: 1, overflowY: "auto", padding: "20px" }}>
        {messages.length === 0 && (
          <div style={{ textAlign: "center", color: "#9CA3AF", marginTop: "80px" }}>
            <p style={{ fontSize: "28px", margin: "0 0 8px" }}>👋</p>
            <p style={{ fontSize: "16px", color: "#374151", margin: "0 0 6px", fontWeight: 500 }}>
              How can we help today?
            </p>
            <p style={{ fontSize: "14px", margin: 0 }}>
              Ask about billing, tech support, products, or anything else.
            </p>
          </div>
        )}
        {messages.map((msg, i) => <Message key={i} msg={msg} />)}
        {loading && (
          <div style={{ display: "flex", gap: "5px", padding: "12px 16px",
            backgroundColor: "#F3F4F6", borderRadius: "18px 18px 18px 4px",
            width: "fit-content" }}>
            {[0,1,2].map(i => (
              <span key={i} style={{ width: 8, height: 8, borderRadius: "50%",
                backgroundColor: "#9CA3AF", display: "block",
                animation: `bounce 1.2s ease-in-out ${i*0.2}s infinite` }} />
            ))}
          </div>
        )}
        {error && (
          <div style={{ padding: "10px 14px", backgroundColor: "#FEF2F2",
            color: "#DC2626", borderRadius: "8px", fontSize: "14px" }}>
            {error}
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <InputBar onSend={handleSend} disabled={loading} />

      <style>{`@keyframes bounce {
        0%,80%,100%{transform:translateY(0)} 40%{transform:translateY(-6px)}
      }`}</style>
    </div>
  );
}

const btnStyle = {
  fontSize: "13px", padding: "7px 14px", border: "1px solid #D1D5DB",
  borderRadius: "8px", background: "transparent", cursor: "pointer", color: "#374151",
};