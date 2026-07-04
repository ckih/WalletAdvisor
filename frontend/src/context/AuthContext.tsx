"use client";

import React, { createContext, useContext, useEffect, useState, useCallback, useRef } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';

interface User {
  id: number;
  email: string;
  full_name: string | null;
  risk_score: string | null;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (token: string) => void;
  logout: () => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const hasInitialized = useRef(false);
  const router = useRouter();

  const fetchUser = useCallback(async () => {
    try {
      const response = await api.get('/auth/me');
      setUser(response.data);
    } catch (error) {
      console.error("Fetch user failed", error);
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
    router.push('/login');
  }, [router]);

  useEffect(() => {
    if (hasInitialized.current) return;
    hasInitialized.current = true;

    const storedToken = localStorage.getItem('token');
    if (storedToken) {
      setTimeout(() => {
        setToken(storedToken);
        fetchUser();
      }, 0);
    } else {
      setTimeout(() => {
        setLoading(false);
      }, 0);
    }
  }, [fetchUser]);


  const login = (newToken: string) => {
    localStorage.setItem('token', newToken);
    setToken(newToken);
    fetchUser();
    router.push('/dashboard');
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
