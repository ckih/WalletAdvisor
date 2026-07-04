"use client";

import { useEffect, useState, useCallback, useRef } from "react";
import api from "@/lib/api";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Wallet, Target, TrendingUp, ShieldCheck } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";

interface Goal {
  id: number;
  name: string;
  target_amount: number;
  current_amount: number;
}

interface Profile {
  category: string;
  explanation: string;
}

export default function DashboardPage() {
  const [goals, setGoals] = useState<Goal[]>([]);
  const [profile, setProfile] = useState<Profile | null>(null);
  const [netWorth, setNetWorth] = useState(0);
  const hasFetched = useRef(false);

  const fetchData = useCallback(async () => {
    try {
      const goalsRes = await api.get("/goals/");
      setGoals(goalsRes.data);

      const profileRes = await api.get("/risk/profile");
      setProfile(profileRes.data);

      const total = goalsRes.data.reduce((acc: number, g: Goal) => acc + g.current_amount, 0);
      setNetWorth(total);
    } catch (error) {
      console.error("Dashboard data fetch failed", error);
    }
  }, []);

  useEffect(() => {
    if (hasFetched.current) return;
    fetchData();
    hasFetched.current = true;
  }, [fetchData]);

  return (
    <div className="space-y-8">
      <h1 className="text-3xl font-bold">Financial Overview</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500">Net Worth</p>
                <p className="text-2xl font-bold">${netWorth.toLocaleString()}</p>
              </div>
              <div className="p-3 bg-green-100 rounded-full">
                <Wallet className="text-green-600 h-6 w-6" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500">Active Goals</p>
                <p className="text-2xl font-bold">{goals.length}</p>
              </div>
              <div className="p-3 bg-blue-100 rounded-full">
                <Target className="text-blue-600 h-6 w-6" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-500">Risk Profile</p>
                <p className="text-2xl font-bold">{profile?.category || "TBD"}</p>
              </div>
              <div className="p-3 bg-purple-100 rounded-full">
                <TrendingUp className="text-purple-600 h-6 w-6" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>Goal Progress</CardTitle>
            <Link href="/goals">
              <Button variant="link">View All</Button>
            </Link>
          </CardHeader>
          <CardContent className="space-y-6">
            {goals.length === 0 && <p className="text-gray-500 text-center py-8">No goals set yet.</p>}
            {goals.slice(0, 3).map(goal => (
              <div key={goal.id} className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="font-medium">{goal.name}</span>
                  <span className="text-gray-500">${goal.current_amount.toLocaleString()} / ${goal.target_amount.toLocaleString()}</span>
                </div>
                <div className="w-full bg-gray-100 rounded-full h-2">
                  <div
                    className="bg-primary h-2 rounded-full transition-all"
                    style={{ width: `${Math.min((goal.current_amount / goal.target_amount) * 100, 100)}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <ShieldCheck className="mr-2 h-5 w-5 text-primary" />
              Your Financial DNA
            </CardTitle>
          </CardHeader>
          <CardContent>
            {profile ? (
              <div className="space-y-4">
                <div className="p-4 bg-gray-50 rounded-lg border">
                  <p className="font-bold text-xl text-primary">{profile.category}</p>
                  <p className="text-sm text-gray-600 mt-2">{profile.explanation}</p>
                </div>
                <p className="text-xs text-gray-500">
                  Your risk profile determines how the AI adviser structures its recommendations.
                  You can update this at any time in your profile settings.
                </p>
              </div>
            ) : (
              <div className="text-center py-8">
                <p className="text-gray-500 mb-4">You haven&apos;t completed your risk profile yet.</p>
                <Link href="/onboarding">
                  <Button>Start Onboarding</Button>
                </Link>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
