"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import api from "@/lib/api";
import { useRouter } from "next/navigation";

export default function OnboardingPage() {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    income: "",
    expenses: "",
    savings: "",
    debts: "",
    time_horizon: "5",
    risk_tolerance: "5",
  });
  const [result, setResult] = useState<{ category: string, explanation: string } | null>(null);
  const router = useRouter();

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const nextStep = () => setStep(step + 1);
  const prevStep = () => setStep(step - 1);

  const handleSubmit = async () => {
    try {
      const response = await api.post("/risk/onboarding", {
        ...formData,
        income: parseFloat(formData.income),
        expenses: parseFloat(formData.expenses),
        savings: parseFloat(formData.savings),
        debts: parseFloat(formData.debts),
        time_horizon: parseInt(formData.time_horizon),
        risk_tolerance: parseInt(formData.risk_tolerance),
      });
      setResult(response.data);
    } catch (error) {
      alert("Onboarding failed");
    }
  };

  if (result) {
    return (
      <Card className="max-w-2xl mx-auto">
        <CardHeader>
          <CardTitle>Your Financial DNA: {result.category}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-lg">{result.explanation}</p>
          <Button onClick={() => router.push("/dashboard")} className="w-full">
            Go to Dashboard
          </Button>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="max-w-xl mx-auto space-y-6">
      <div className="flex justify-between items-center mb-8">
        {[1, 2, 3].map((s) => (
          <div
            key={s}
            className={`w-8 h-8 rounded-full flex items-center justify-center ${step >= s ? 'bg-primary text-white' : 'bg-gray-200'}`}
          >
            {s}
          </div>
        ))}
      </div>

      <Card>
        <CardContent className="pt-6">
          {step === 1 && (
            <div className="space-y-4">
              <h2 className="text-xl font-bold">Financial Snapshot</h2>
              <div className="space-y-2">
                <label>Annual Income ($)</label>
                <Input name="income" type="number" value={formData.income} onChange={handleInputChange} />
              </div>
              <div className="space-y-2">
                <label>Monthly Expenses ($)</label>
                <Input name="expenses" type="number" value={formData.expenses} onChange={handleInputChange} />
              </div>
              <Button onClick={nextStep} className="w-full">Next</Button>
            </div>
          )}

          {step === 2 && (
            <div className="space-y-4">
              <h2 className="text-xl font-bold">Assets & Debts</h2>
              <div className="space-y-2">
                <label>Total Savings ($)</label>
                <Input name="savings" type="number" value={formData.savings} onChange={handleInputChange} />
              </div>
              <div className="space-y-2">
                <label>Total Debts ($)</label>
                <Input name="debts" type="number" value={formData.debts} onChange={handleInputChange} />
              </div>
              <div className="flex space-x-2">
                <Button variant="outline" onClick={prevStep} className="flex-1">Back</Button>
                <Button onClick={nextStep} className="flex-1">Next</Button>
              </div>
            </div>
          )}

          {step === 3 && (
            <div className="space-y-4">
              <h2 className="text-xl font-bold">Horizon & Risk</h2>
              <div className="space-y-2">
                <label>Time Horizon (Years)</label>
                <Input name="time_horizon" type="number" value={formData.time_horizon} onChange={handleInputChange} />
              </div>
              <div className="space-y-2">
                <label>Risk Tolerance (1-10)</label>
                <Input name="risk_tolerance" type="number" min="1" max="10" value={formData.risk_tolerance} onChange={handleInputChange} />
              </div>
              <div className="flex space-x-2">
                <Button variant="outline" onClick={prevStep} className="flex-1">Back</Button>
                <Button onClick={handleSubmit} className="flex-1">Calculate Profile</Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
