"use client";
import { useState } from "react";
import { signup, login } from "../services/api";
import { useAuth } from "../context/AuthContext";

export default function AuthForm() {
  const [mode, setMode] = useState("login"); // "login" or "signup"
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login: setAuthState } = useAuth();

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const data = mode === "login"
        ? await login(email, password)
        : await signup(email, password, name);
      setAuthState(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{
      display: "flex", flexDirection: "column", justifyContent: "center",
      alignItems: "center", height: "100vh", fontFamily: "system-ui, sans-serif",
    }}>
      <div style={{ width: "320px" }}>
        <h1 style={{ fontSize: "20px", fontWeight: 600, marginBottom: "4px" }}>
          TechMart Support
        </h1>
        <p style={{ fontSize: "14px", color: "#6B7280", marginBottom: "24px" }}>
          {mode === "login" ? "Log in to continue" : "Create an account"}
        </p>

        <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
          {mode === "signup" && (
            <input
              type="text" placeholder="Name" value={name}
              onChange={e => setName(e.target.value)} required
              style={inputStyle}
            />
          )}
          <input
            type="email" placeholder="Email" value={email}
            onChange={e => setEmail(e.target.value)} required
            style={inputStyle}
          />
          <input
            type="password" placeholder="Password" value={password}
            onChange={e => setPassword(e.target.value)} required
            style={inputStyle}
          />

          {error && (
            <p style={{ color: "#DC2626", fontSize: "13px", margin: 0 }}>{error}</p>
          )}

          <button type="submit" disabled={loading} style={{
            padding: "10px", backgroundColor: "#2563EB", color: "#fff",
            border: "none", borderRadius: "10px", fontSize: "15px",
            fontWeight: 500, cursor: loading ? "not-allowed" : "pointer",
            marginTop: "6px",
          }}>
            {loading ? "Please wait…" : mode === "login" ? "Log in" : "Sign up"}
          </button>
        </form>

        <p style={{ fontSize: "13px", color: "#6B7280", marginTop: "16px", textAlign: "center" }}>
          {mode === "login" ? "Don't have an account? " : "Already have an account? "}
          <span
            onClick={() => { setMode(mode === "login" ? "signup" : "login"); setError(""); }}
            style={{ color: "#2563EB", cursor: "pointer", fontWeight: 500 }}
          >
            {mode === "login" ? "Sign up" : "Log in"}
          </span>
        </p>
      </div>
    </div>
  );
}

const inputStyle = {
  padding: "10px 12px", border: "1px solid #D1D5DB", borderRadius: "10px",
  fontSize: "14px", outline: "none", fontFamily: "inherit",
};