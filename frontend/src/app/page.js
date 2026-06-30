"use client";
import { AuthProvider, useAuth } from "../context/AuthContext";
import AuthForm from "../components/AuthForm";
import ChatInterface from "../components/ChatInterface";

function AppContent() {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? <ChatInterface /> : <AuthForm />;
}

export default function Home() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}