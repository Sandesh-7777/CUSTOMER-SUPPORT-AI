import { useRef } from "react";

export default function InputBar({ onSend, disabled }) {
  const ref = useRef(null);

  function handleKey(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  }

  function submit() {
    const val = ref.current?.value.trim();
    if (!val || disabled) return;
    onSend(val);
    ref.current.value = "";
    ref.current.style.height = "auto";
  }

  return (
    <div style={{ display: "flex", gap: "10px", padding: "16px 20px",
      borderTop: "1px solid #E5E7EB", alignItems: "flex-end" }}>
      <textarea ref={ref} onKeyDown={handleKey} placeholder="Type your message…"
        rows={1} style={{ flex: 1, resize: "none", border: "1px solid #D1D5DB",
          borderRadius: "12px", padding: "10px 14px", fontSize: "15px",
          fontFamily: "inherit", outline: "none", maxHeight: "120px" }}
        onInput={e => {
          e.target.style.height = "auto";
          e.target.style.height = Math.min(e.target.scrollHeight, 120) + "px";
        }} />
      <button onClick={submit} disabled={disabled}
        style={{ padding: "10px 20px", backgroundColor: disabled ? "#D1D5DB" : "#2563EB",
          color: "#fff", border: "none", borderRadius: "12px", fontSize: "15px",
          fontWeight: 500, cursor: disabled ? "not-allowed" : "pointer" }}>
        {disabled ? "…" : "Send"}
      </button>
    </div>
  );
}