"use client";

import { useEffect, useState, useCallback, useRef } from "react";
import api from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Plus, Target, Calendar } from "lucide-react";

interface Goal {
  id: number;
  name: string;
  type: string;
  target_amount: number;
  current_amount: number;
  target_date: string;
}

export default function GoalsPage() {
  const [goals, setGoals] = useState<Goal[]>([]);
  const [isAdding, setIsAdding] = useState(false);
  const [newGoal, setNewGoal] = useState({
    name: "",
    type: "other",
    target_amount: "",
    target_date: "",
  });
  const hasFetched = useRef(false);

  const fetchGoals = useCallback(async () => {
    try {
      const response = await api.get("/goals/");
      setGoals(response.data);
    } catch (error) {
      console.error("Failed to fetch goals", error);
    }
  }, []);

  useEffect(() => {
    if (hasFetched.current) return;
    fetchGoals();
    hasFetched.current = true;
  }, [fetchGoals]);

  const handleCreateGoal = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post("/goals/", {
        ...newGoal,
        target_amount: parseFloat(newGoal.target_amount),
        target_date: new Date(newGoal.target_date).toISOString(),
      });
      setIsAdding(false);
      fetchGoals();
    } catch (error) {
      alert("Failed to create goal");
      console.error(error);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Financial Goals</h1>
        <Button onClick={() => setIsAdding(true)}>
          <Plus className="mr-2 h-4 w-4" /> Add Goal
        </Button>
      </div>

      {isAdding && (
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Create New Goal</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleCreateGoal} className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <label>Goal Name</label>
                <Input value={newGoal.name} onChange={(e) => setNewGoal({...newGoal, name: e.target.value})} required />
              </div>
              <div className="space-y-2">
                <label>Type</label>
                <select
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                  value={newGoal.type}
                  onChange={(e) => setNewGoal({...newGoal, type: e.target.value})}
                >
                  <option value="retirement">Retirement</option>
                  <option value="home_purchase">Home Purchase</option>
                  <option value="emergency_fund">Emergency Fund</option>
                  <option value="education">Education</option>
                  <option value="other">Other</option>
                </select>
              </div>
              <div className="space-y-2">
                <label>Target Amount ($)</label>
                <Input type="number" value={newGoal.target_amount} onChange={(e) => setNewGoal({...newGoal, target_amount: e.target.value})} required />
              </div>
              <div className="space-y-2">
                <label>Target Date</label>
                <Input type="date" value={newGoal.target_date} onChange={(e) => setNewGoal({...newGoal, target_date: e.target.value})} required />
              </div>
              <div className="col-span-2 flex justify-end space-x-2">
                <Button variant="outline" onClick={() => setIsAdding(false)}>Cancel</Button>
                <Button type="submit">Save Goal</Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {goals.map((goal) => (
          <Card key={goal.id}>
            <CardContent className="pt-6">
              <div className="flex justify-between items-start mb-4">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <Target className="text-blue-600 h-6 w-6" />
                </div>
                <div className="text-right">
                  <span className="text-xs font-semibold uppercase text-gray-500">{goal.type}</span>
                  <p className="text-xl font-bold">${goal.target_amount.toLocaleString()}</p>
                </div>
              </div>
              <h3 className="text-lg font-bold mb-2">{goal.name}</h3>
              <div className="w-full bg-gray-200 rounded-full h-2.5 mb-4">
                <div
                  className="bg-primary h-2.5 rounded-full"
                  style={{ width: `${Math.min((goal.current_amount / goal.target_amount) * 100, 100)}%` }}
                ></div>
              </div>
              <div className="flex justify-between text-sm text-gray-600">
                <div className="flex items-center">
                  <Calendar size={14} className="mr-1" />
                  {new Date(goal.target_date).toLocaleDateString()}
                </div>
                <span>{Math.round((goal.current_amount / goal.target_amount) * 100)}% complete</span>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
