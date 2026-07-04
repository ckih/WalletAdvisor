"use client";

import { useAuth } from "@/context/AuthContext";
import Link from "next/link";
import { LayoutDashboard, Target, MessageSquare, LogOut, User } from "lucide-react";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { token, loading, logout, user } = useAuth();

  if (loading) return <div className="flex h-screen items-center justify-center">Loading...</div>;

  if (!token) {
    return <div className="min-h-screen bg-gray-50">{children}</div>;
  }

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r">
        <div className="p-6">
          <h1 className="text-2xl font-bold text-primary">AFA</h1>
        </div>
        <nav className="mt-6 px-4 space-y-2">
          <Link href="/dashboard" className="flex items-center space-x-3 p-3 rounded-lg hover:bg-gray-100 text-gray-700">
            <LayoutDashboard size={20} />
            <span>Dashboard</span>
          </Link>
          <Link href="/goals" className="flex items-center space-x-3 p-3 rounded-lg hover:bg-gray-100 text-gray-700">
            <Target size={20} />
            <span>Goals</span>
          </Link>
          <Link href="/chat" className="flex items-center space-x-3 p-3 rounded-lg hover:bg-gray-100 text-gray-700">
            <MessageSquare size={20} />
            <span>AI Adviser</span>
          </Link>
          <Link href="/profile" className="flex items-center space-x-3 p-3 rounded-lg hover:bg-gray-100 text-gray-700">
            <User size={20} />
            <span>Profile</span>
          </Link>
          <button
            onClick={logout}
            className="flex items-center space-x-3 p-3 rounded-lg hover:bg-red-50 text-red-600 w-full mt-10"
          >
            <LogOut size={20} />
            <span>Logout</span>
          </button>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto">
        <header className="bg-white border-b h-16 flex items-center justify-between px-8">
          <h2 className="text-xl font-semibold">Welcome Back</h2>
          <div className="flex items-center space-x-4">
            <span className="text-sm font-medium">{user?.full_name || user?.email}</span>
            <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-white text-xs">
              {user?.email?.[0]?.toUpperCase() || "U"}
            </div>
          </div>
        </header>
        <div className="p-8">
          {children}
        </div>
      </main>
    </div>
  );
}
