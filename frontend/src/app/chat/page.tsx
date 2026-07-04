"use client";

import { useState, useRef, useEffect } from "react";
import api from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { Send, Bot, User, AlertTriangle } from "lucide-react";

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await api.post("/chat/", { message: input });
      const assistantMessage: Message = {
        role: 'assistant',
        content: response.data.response
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Chat failed", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-160px)]">
      <Card className="flex-1 flex flex-col overflow-hidden">
        <div className="bg-amber-50 p-3 border-b flex items-center text-amber-800 text-xs font-medium">
          <AlertTriangle size={14} className="mr-2" />
          DISCLAIMER: This is not licensed financial advice. This AI does not execute any transactions.
        </div>

        <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 && (
            <div className="h-full flex items-center justify-center text-gray-400">
              Ask me anything about your financial goals or roadmap!
            </div>
          )}
          {messages.map((m, i) => (
            <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`flex max-w-[80%] space-x-2 ${m.role === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center ${m.role === 'user' ? 'bg-primary' : 'bg-gray-200'}`}>
                  {m.role === 'user' ? <User size={16} className="text-white" /> : <Bot size={16} />}
                </div>
                <div className={`p-3 rounded-lg ${m.role === 'user' ? 'bg-primary text-white' : 'bg-gray-100'}`}>
                  <p className="text-sm whitespace-pre-wrap">{m.content}</p>
                </div>
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="flex space-x-2">
                <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center">
                  <Bot size={16} />
                </div>
                <div className="p-3 rounded-lg bg-gray-100 italic text-sm text-gray-500">
                  Thinking...
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="p-4 border-t">
          <form onSubmit={handleSend} className="flex space-x-2">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question..."
              disabled={isLoading}
            />
            <Button type="submit" disabled={isLoading}>
              <Send size={18} />
            </Button>
          </form>
        </div>
      </Card>
    </div>
  );
}
