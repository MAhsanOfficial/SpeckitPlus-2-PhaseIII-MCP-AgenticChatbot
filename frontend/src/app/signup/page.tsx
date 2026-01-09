"use client";

import { useState } from "react";
import Link from "next/link";
import { Navbar } from "@/components/ui/Navbar";
import { Footer } from "@/components/ui/Footer";
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";

export default function Signup() {
  const { login } = useAuth();
  const router = useRouter();
  const [formData, setFormData] = useState({
    name: "",
    phone: "",
    email: "",
    password: "",
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Simulate API call
    if (formData.email && formData.name) {
      // In a real app, we would validate phone number here
      login(formData.email, formData.name, formData.phone);
      router.push("/dashboard");
    }
  };

  return (
    <main className="min-h-screen vip-gradient-bg flex flex-col">
      <Navbar />
      <div className="flex-1 flex items-center justify-center px-10 pt-20">
        <div className="max-w-md w-full glass-morphism p-10 rounded-3xl border border-brand-blue/20 shadow-2xl">
          <div className="text-center mb-10">
            <h1 className="text-4xl font-bold text-white mb-2">INITIATE <span className="text-gradient">ACCOUNT</span></h1>
            <p className="text-gray-500">Enter your neural credentials</p>
          </div>

          <form className="space-y-6" onSubmit={handleSubmit}>
            <div>
              <label className="block text-gray-400 text-sm font-bold mb-2">Full Name</label>
              <input
                type="text"
                required
                className="w-full bg-black/40 border border-gray-800 rounded-xl px-4 py-3 text-white focus:border-brand-cyan transition-colors outline-none"
                placeholder="Ex. John Doe"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              />
            </div>
            <div>
              <label className="block text-gray-400 text-sm font-bold mb-2">Phone Number</label>
              <input
                type="tel"
                required
                className="w-full bg-black/40 border border-gray-800 rounded-xl px-4 py-3 text-white focus:border-brand-cyan transition-colors outline-none"
                placeholder="+1 555 0123"
                value={formData.phone}
                onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
              />
            </div>
            <div>
              <label className="block text-gray-400 text-sm font-bold mb-2">Email</label>
              <input
                type="email"
                required
                className="w-full bg-black/40 border border-gray-800 rounded-xl px-4 py-3 text-white focus:border-brand-cyan transition-colors outline-none"
                placeholder="user@example.com"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              />
            </div>
            <div>
              <label className="block text-gray-400 text-sm font-bold mb-2">Password</label>
              <input
                type="password"
                required
                className="w-full bg-black/40 border border-gray-800 rounded-xl px-4 py-3 text-white focus:border-brand-cyan transition-colors outline-none"
                placeholder="••••••••"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              />
            </div>

            <button type="submit" className="w-full py-4 bg-gradient-brand text-black font-black rounded-xl hover:scale-[1.02] active:scale-95 transition-all shadow-lg shadow-blue-500/20">
              CREATE PROTOCOLS
            </button>
          </form>

          <p className="text-center text-gray-500 mt-8 text-sm">
            ALREADY INITIALIZED? <Link href="/login" className="text-brand-gold font-bold hover:underline">ACCESS CORE</Link>
          </p>
        </div>
      </div>
      <Footer />
    </main>
  );
}
