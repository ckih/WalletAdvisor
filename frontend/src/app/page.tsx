"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";

export default function HomePage() {
  const { token, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading) {
      if (token) {
        router.push("/dashboard");
      } else {
        router.push("/login");
      }
    }
  }, [token, loading, router]);

  return <div className="flex h-screen items-center justify-center">Redirecting...</div>;
}
