"use client";
import { createContext, useContext, useState } from "react";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);   // { user_id, name, email }
  const [token, setToken] = useState(null);

  function login(authData) {
    // authData comes from /auth/login or /auth/signup response
    setUser({ user_id: authData.user_id, name: authData.name, email: authData.email });
    setToken(authData.token);
  }

  function logout() {
    setUser(null);
    setToken(null);
  }

  return (
    <AuthContext.Provider value={{ user, token, login, logout, isAuthenticated: !!token }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
  return ctx;
}