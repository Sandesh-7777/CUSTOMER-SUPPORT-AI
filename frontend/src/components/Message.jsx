import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";

const AGENT_LABELS = {
  billing: { label: "Billing", color: "#4338CA", bg: "#EEF2FF" },
  technical: { label: "Tech Support", color: "#15803D", bg: "#F0FDF4" },
  product: { label: "Product", color: "#C2410C", bg: "#FFF7ED" },
  complaint: { label: "Complaints", color: "#DC2626", bg: "#FEF2F2" },
  faq: { label: "FAQ", color: "#0369A1", bg: "#F0F9FF" },
};

export default function Message({ msg }) {
  const isUser = msg.role === "user";
  const agent = AGENT_LABELS[msg.agent];

  return (
    <div style={{ display: "flex", flexDirection: "column",
      alignItems: isUser ? "flex-end" : "flex-start", marginBottom: "16px" }}>
      {!isUser && agent && (
        <span style={{ fontSize: "11px", fontWeight: 500, padding: "2px 8px",
          borderRadius: "99px", backgroundColor: agent.bg, color: agent.color,
          marginBottom: "4px" }}>
          {agent.label} Agent
        </span>
      )}
      <div style={{
        maxWidth: isUser ? "75%" : "90%",   // wider bubble for AI so tables fit
        padding: "12px 16px",
        borderRadius: isUser ? "18px 18px 4px 18px" : "18px 18px 18px 4px",
        backgroundColor: isUser ? "#2563EB" : "#F3F4F6",
        color: isUser ? "#fff" : "#111827",
        fontSize: "15px", lineHeight: "1.6",
        overflowX: "auto",   // allows tables to scroll horizontally instead of breaking layout
      }}>
        {isUser ? (
          msg.content
        ) : (
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            rehypePlugins={[rehypeRaw]}
            components={{
              p: ({ children }) => <p style={{ margin: "0 0 8px" }}>{children}</p>,
              ul: ({ children }) => <ul style={{ margin: "4px 0", paddingLeft: "20px" }}>{children}</ul>,
              ol: ({ children }) => <ol style={{ margin: "4px 0", paddingLeft: "20px" }}>{children}</ol>,
              li: ({ children }) => <li style={{ marginBottom: "3px" }}>{children}</li>,
              table: ({ children }) => (
                <table style={{
                  borderCollapse: "collapse", width: "100%", margin: "8px 0", fontSize: "14px",
                }}>
                  {children}
                </table>
              ),
              th: ({ children }) => (
                <th style={{
                  border: "1px solid #D1D5DB", padding: "6px 10px",
                  backgroundColor: "#E5E7EB", textAlign: "left",
                }}>
                  {children}
                </th>
              ),
              td: ({ children }) => (
                <td style={{ border: "1px solid #D1D5DB", padding: "6px 10px", verticalAlign: "top" }}>
                  {children}
                </td>
              ),
              strong: ({ children }) => <strong style={{ fontWeight: 600 }}>{children}</strong>,
            }}
          >
            {msg.content}
          </ReactMarkdown>
        )}
      </div>
    </div>
  );
} 