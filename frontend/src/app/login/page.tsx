"use client";

import { useState } from "react";
import Link from "next/link";
import { Navbar } from "@/components/ui/Navbar";
import { Footer } from "@/components/ui/Footer";
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";

export default function Login() {
  const { login } = useAuth();
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Simulate login
    if (email) {
      login(email, "Agent");
      router.push("/dashboard");
    }
  };

  return (
    <main className="min-h-screen vip-gradient-bg flex flex-col">
      <Navbar />
      <div className="flex-1 flex items-center justify-center px-10 pt-20">
        <div className="max-w-md w-full glass-morphism p-10 rounded-3xl border border-brand-blue/20 shadow-2xl">
          <div className="text-center mb-10">
            <h1 className="text-4xl font-bold text-white mb-2">ACCESS <span className="text-gradient">CORE</span></h1>
            <p className="text-gray-500">Security handshake required</p>
          </div>

          <form className="space-y-6" onSubmit={handleSubmit}>
            <div>
              <label className="block text-gray-400 text-sm font-bold mb-2">NEURAL EMAIL</label>
              <input
                type="email"
                required
                className="w-full bg-black/40 border border-gray-800 rounded-xl px-4 py-3 text-white focus:border-brand-blue transition-colors outline-none"
                placeholder="user@neural.link"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div>
              <label className="block text-gray-400 text-sm font-bold mb-2">ACCESS OVERRIDE</label>
              <input
                type="password"
                required
                className="w-full bg-black/40 border border-gray-800 rounded-xl px-4 py-3 text-white focus:border-brand-blue transition-colors outline-none"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>

            <button type="submit" className="w-full py-4 bg-gradient-brand text-black font-black rounded-xl hover:scale-[1.02] active:scale-95 transition-all shadow-lg shadow-blue-500/20">
              LOG INTO SYSTEM
            </button>
          </form>

          <p className="text-center text-gray-500 mt-8 text-sm">
            NEW MISSION? <Link href="/signup" className="text-brand-cyan font-bold hover:underline">INITIATE ACCOUNT</Link>
          </p>
        </div>
      </div>
      <Footer />
    </main>
  );
}
