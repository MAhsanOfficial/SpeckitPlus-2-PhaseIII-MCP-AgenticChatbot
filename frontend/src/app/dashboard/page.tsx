"use client";

import { useEffect, useRef, useState } from "react";
import gsap from "gsap";
import { AnimatePresence } from "framer-motion";
import { Navbar } from "@/components/ui/Navbar";
import { Footer } from "@/components/ui/Footer";
import { AnalyticsChart } from "@/components/ui/AnalyticsChart";
import { ChatContainer } from "@/components/chat";
import { Plus, LayoutDashboard, Settings, LogOut, Cpu, TrendingUp, X, Sparkles, BrainCircuit, ArrowLeft, Trash2, Edit, MessageSquare } from "lucide-react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { useHabits, Habit } from "@/context/HabitContext";

export default function Dashboard() {
  const { habits, addHabit, deleteHabit, toggleHabit, updateHabit } = useHabits();
  const { user, logout, isAuthenticated } = useAuth();
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  // UI State
  const [showAddModal, setShowAddModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [editingHabit, setEditingHabit] = useState<Habit | null>(null);
  const [habitForm, setHabitForm] = useState({ name: "", desc: "" });
  const [analyzing, setAnalyzing] = useState<string | null>(null);
  const [aiAnalysis, setAiAnalysis] = useState<{ feedback: string, pros: string[], cons: string[] } | null>(null);
  const [selectedHabitForAnalysis, setSelectedHabitForAnalysis] = useState<Habit | null>(null);
  const [showChatbot, setShowChatbot] = useState(false);
  const [selectedHabit, setSelectedHabit] = useState<string | null>(null);

  // Handle habit selection
  const handleHabitSelect = (habit: Habit) => {
    console.log('[Dashboard] Habit clicked:', habit.id, habit.name);
    if (selectedHabit === habit.id) {
      console.log('[Dashboard] Deselecting habit');
      setSelectedHabit(null); // Deselect if already selected
    } else {
      console.log('[Dashboard] Selecting habit:', habit.id);
      setSelectedHabit(habit.id);
    }
  };

  const openEditModal = (habit: Habit) => {
    setEditingHabit(habit);
    setHabitForm({ name: habit.name, desc: habit.description || "" });
    setShowEditModal(true);
  };

  const handleUpdateHabit = (e: React.FormEvent) => {
    e.preventDefault();
    if (editingHabit && habitForm.name) {
      updateHabit(editingHabit.id, { name: habitForm.name, description: habitForm.desc });
      setShowEditModal(false);
      setEditingHabit(null);
      setHabitForm({ name: "", desc: "" });
    }
  };

  useEffect(() => {
    const checkAuth = async () => {
      await new Promise(r => setTimeout(r, 500));
      if (!isAuthenticated && !localStorage.getItem("auth_token")) {
        router.push("/login");
      } else {
        setLoading(false);
        gsap.from(".dash-card", {
          y: 30, opacity: 0, duration: 1, stagger: 0.1, ease: "power4.out", delay: 0.2
        });
      }
    };
    checkAuth();
  }, [isAuthenticated, router]);

  const handleCreateHabit = (e: React.FormEvent) => {
    e.preventDefault();
    if (habitForm.name) {
      addHabit(habitForm.name, habitForm.desc);
      setShowAddModal(false);
      setHabitForm({ name: "", desc: "" });
    }
  };

  const analyzeHabit = async (habit: Habit) => {
    // Toggle if clicking the same habit
    if (analyzing === habit.id) return;

    // valid toggle off
    if (selectedHabitForAnalysis?.id === habit.id) {
      setSelectedHabitForAnalysis(null);
      setAiAnalysis(null);
      return;
    }

    setAnalyzing(habit.id);
    setSelectedHabitForAnalysis(habit);
    setAiAnalysis(null);

    try {
      const res = await fetch("/api/analyze", {
        method: "POST",
        body: JSON.stringify({ habitName: habit.name, habitDesc: habit.description })
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({ error: "Unknown Error" }));
        throw new Error(errData.details || errData.error || "Analysis failed");
      }

      const data = await res.json();
      setAiAnalysis(data);
    } catch (e: any) {
      console.error(e);
      setAiAnalysis({
        feedback: `Error: ${e.message}`,
        pros: [],
        cons: []
      });
    } finally {
      setAnalyzing(null);
    }
  };

  if (loading) return (
    <div className="min-h-screen bg-brand-dark flex flex-col items-center justify-center gap-4">
      <Cpu className="text-brand-cyan animate-spin" size={48} />
      <p className="text-brand-cyan font-mono text-sm tracking-widest animate-pulse">VERIFYING BIOMETRICS...</p>
    </div>
  );

  return (
    <div className="min-h-screen bg-brand-dark flex flex-col vip-gradient-bg">
      <Navbar />

      <div className="flex flex-1 pt-20">
        <aside className="w-72 border-r border-white/5 p-8 flex flex-col gap-10 hidden lg:flex bg-black/20 backdrop-blur-xl">
          <div className="space-y-2">
            <div className="inline-block px-3 py-1 rounded-full border border-gray-800 bg-gray-900/50 text-[10px] font-bold tracking-[0.2em] text-gray-400 mb-4">
              SYSTEM CONTROL
            </div>
            <button className="w-full flex items-center gap-3 px-5 py-4 bg-brand-cyan/10 text-brand-cyan rounded-2xl font-bold border border-brand-cyan/20 shadow-[0_0_20px_rgba(0,240,255,0.1)]">
              <LayoutDashboard size={20} /> DASHBOARD
            </button>
            <button onClick={() => router.push("/")} className="w-full flex items-center gap-3 px-5 py-4 text-gray-500 hover:text-white rounded-2xl font-bold transition-all hover:bg-white/5">
              <ArrowLeft size={20} /> BACK TO BASE
            </button>
          </div>
          <button onClick={logout} className="mt-auto flex items-center gap-3 px-5 py-4 text-red-500/70 hover:text-red-500 rounded-2xl font-bold transition-all hover:bg-red-500/5">
            <LogOut size={20} /> TERMINATE
          </button>
        </aside>

        <main className="flex-1 p-6 lg:p-12 overflow-y-auto">
          <header className="flex flex-col xl:flex-row justify-between items-start xl:items-center gap-6 mb-12 dash-card">
            <div>
              <h1 className="text-4xl lg:text-5xl font-black text-white mb-2 uppercase tracking-tight">
                HABIT <span className="text-gradient">COMMAND</span>
              </h1>
              <p className="text-gray-500 font-medium tracking-wide font-mono text-sm">Welcome, Unit {user?.name.toUpperCase()}</p>
            </div>
            <button onClick={() => setShowAddModal(true)} className="px-8 py-4 neon-btn text-black font-black rounded-2xl flex items-center gap-3 hover:scale-105 transition-transform shadow-lg shadow-cyan-500/20">
              <Plus size={24} strokeWidth={3} /> NEW HABIT
            </button>
          </header>

          <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
            {/* Habits List */}
            <section className="xl:col-span-2 space-y-6">
              <div className="grid gap-4">
                {habits.map((habit) => (
                  <div 
                    key={habit.id} 
                    onClick={(e) => {
                      // Only select if clicking on the card itself, not buttons
                      const target = e.target as HTMLElement;
                      if (!target.closest('button')) {
                        handleHabitSelect(habit);
                      }
                    }}
                    className={`dash-card bg-brand-card/50 backdrop-blur border p-6 rounded-3xl transition-all group relative overflow-hidden cursor-pointer ${
                      selectedHabit === habit.id 
                        ? 'border-brand-cyan shadow-[0_0_20px_rgba(0,240,255,0.3)] ring-2 ring-brand-cyan/50 scale-[1.01]' 
                        : 'border-white/5 hover:border-brand-cyan/30'
                    }`}
                  >
                    {/* Selection indicator */}
                    {selectedHabit === habit.id && (
                      <div className="absolute top-0 left-0 w-1 h-full bg-brand-cyan rounded-l-3xl" />
                    )}
                    
                    <div className={`absolute top-0 right-0 p-4 transition-opacity flex gap-2 ${selectedHabit === habit.id ? 'opacity-100' : 'opacity-0 group-hover:opacity-100'}`}>
                      <button onClick={(e) => { e.stopPropagation(); openEditModal(habit); }} className="p-2 bg-brand-cyan/10 text-brand-cyan rounded-lg hover:bg-brand-cyan hover:text-black transition-colors"><Edit size={16} /></button>
                      <button onClick={(e) => { e.stopPropagation(); deleteHabit(habit.id); }} className="p-2 bg-red-500/10 text-red-500 rounded-lg hover:bg-red-500 hover:text-white transition-colors"><Trash2 size={16} /></button>
                    </div>

                    <div className="flex items-center gap-6">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          toggleHabit(habit.id);
                        }}
                        className={`w-12 h-12 rounded-2xl flex items-center justify-center border-2 transition-all flex-shrink-0 ${habit.completed ? 'bg-brand-cyan border-brand-cyan shadow-[0_0_15px_#00F0FF]' : 'border-gray-700 hover:border-brand-cyan/50'}`}
                      >
                        {habit.completed && <Sparkles className="text-black" size={24} />}
                      </button>
                      <div className="flex-1 min-w-0">
                        <h3 className={`text-xl font-bold mb-1 truncate ${habit.completed ? 'text-brand-cyan' : selectedHabit === habit.id ? 'text-brand-cyan' : 'text-white'} transition-colors`}>{habit.name}</h3>
                        <p className="text-gray-500 text-sm truncate">{habit.description || "No description provided."}</p>
                      </div>
                      <div className="text-right hidden sm:block flex-shrink-0">
                        <p className="text-[10px] font-bold text-gray-500 uppercase tracking-widest">STREAK</p>
                        <p className="text-2xl font-mono font-bold text-brand-gold">{habit.streak} DAYS</p>
                      </div>
                    </div>

                    <div className="mt-6 pt-4 border-t border-white/5 flex gap-4">
                      <button
                        onClick={() => analyzeHabit(habit)}
                        disabled={analyzing === habit.id}
                        className="text-xs font-bold flex items-center gap-2 text-brand-cyan hover:text-white px-4 py-2 rounded-lg bg-brand-cyan/5 hover:bg-brand-cyan/20 transition-all ml-auto disabled:opacity-50"
                      >
                        {analyzing === habit.id ? <Cpu className="animate-spin" size={14} /> : <BrainCircuit size={14} />}
                        {analyzing === habit.id ? "ANALYZING..." : "RUN AI ANALYSIS"}
                      </button>
                    </div>

                    {/* Analysis Result Display Inline */}
                    {/* Analysis Result Display Inline */}
                    {selectedHabitForAnalysis?.id === habit.id && aiAnalysis && (
                      <div className="mt-4 bg-black/40 rounded-xl p-6 border border-brand-cyan/20 animate-in fade-in slide-in-from-top-2 relative overflow-hidden">
                        <div className="absolute top-0 right-0 p-4">
                          <Sparkles size={16} className="text-brand-gold animate-pulse" />
                        </div>
                        <div className="mb-4">
                          <h4 className="text-[10px] font-bold text-gray-500 uppercase tracking-widest mb-1">AI FEEDBACK</h4>
                          <p className="text-lg font-black text-white italic">"{aiAnalysis.feedback}"</p>
                        </div>
                        <div className="grid md:grid-cols-2 gap-6">
                          <div>
                            <h4 className="text-brand-cyan text-xs font-bold uppercase mb-2 flex items-center gap-2">
                              <div className="w-1.5 h-1.5 rounded-full bg-brand-cyan" /> ADVANTAGES
                            </h4>
                            <ul className="text-xs text-gray-400 space-y-2">
                              {aiAnalysis.pros?.length > 0 ? (
                                aiAnalysis.pros.map((p, i) => <li key={i} className="flex gap-2"><span>•</span> {p}</li>)
                              ) : (
                                <li className="text-gray-600 italic">No advantages analyzed.</li>
                              )}
                            </ul>
                          </div>
                          <div>
                            <h4 className="text-red-400 text-xs font-bold uppercase mb-2 flex items-center gap-2">
                              <div className="w-1.5 h-1.5 rounded-full bg-red-400" /> DISADVANTAGES
                            </h4>
                            <ul className="text-xs text-gray-400 space-y-2">
                              {aiAnalysis.cons?.length > 0 ? (
                                aiAnalysis.cons.map((c, i) => <li key={i} className="flex gap-2"><span>•</span> {c}</li>)
                              ) : (
                                <li className="text-gray-600 italic">No disadvantages analyzed.</li>
                              )}
                            </ul>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </section>
          </div>

          {/* Aggregated Analytics Section */}
          <section className="mt-12 dash-card">
            <div className="glass-morphism rounded-[2.5rem] p-10 border border-brand-cyan/20 relative overflow-hidden bg-brand-card/30 backdrop-blur-2xl">
              <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-10 gap-6">
                <div>
                  <h3 className="text-3xl font-black text-white uppercase tracking-tight flex items-center gap-3">
                    <TrendingUp className="text-brand-gold" size={32} /> System <span className="text-gradient">Performance</span>
                  </h3>
                  <p className="text-gray-500 font-mono text-sm mt-2">REAL-TIME BEHAVIORAL DATA AGGREGATION</p>
                </div>
                <div className="flex gap-4">
                  <div className="px-6 py-3 rounded-2xl bg-brand-cyan/10 border border-brand-cyan/20">
                    <p className="text-[10px] text-brand-cyan font-bold uppercase tracking-widest mb-1">Total Efficiency</p>
                    <p className="text-2xl font-black text-white">{habits.length > 0 ? Math.round((habits.filter(h => h.completed).length / habits.length) * 100) : 0}%</p>
                  </div>
                </div>
              </div>

              <AnalyticsChart habits={habits} />
            </div>
          </section>
        </main>
      </div>

      {/* Add Habit Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in">
          <div className="bg-brand-card w-full max-w-md rounded-3xl p-8 border border-brand-cyan/30 shadow-[0_0_50px_rgba(0,240,255,0.2)]">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-black text-white">NEW HABIT</h2>
              <button onClick={() => setShowAddModal(false)} className="text-gray-500 hover:text-white"><X /></button>
            </div>
            <form onSubmit={handleCreateHabit} className="space-y-4">
              <input
                className="w-full bg-black/40 border border-gray-700 rounded-xl p-4 text-white focus:border-brand-cyan outline-none"
                placeholder="Habit Name (e.g. Early Rise)"
                value={habitForm.name}
                onChange={e => setHabitForm({ ...habitForm, name: e.target.value })}
                autoFocus
              />
              <textarea
                className="w-full bg-black/40 border border-gray-700 rounded-xl p-4 text-white focus:border-brand-cyan outline-none resize-none h-32"
                placeholder="Description / Frequency"
                value={habitForm.desc}
                onChange={e => setHabitForm({ ...habitForm, desc: e.target.value })}
              />
              <button type="submit" className="w-full py-4 bg-brand-cyan text-black font-black rounded-xl hover:bg-white transition-colors">
                INITIALIZE HABIT
              </button>
            </form>
          </div>
        </div>
      )}

      {/* Edit Habit Modal */}
      {showEditModal && editingHabit && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in">
          <div className="bg-brand-card w-full max-w-md rounded-3xl p-8 border border-brand-gold/30 shadow-[0_0_50px_rgba(255,215,0,0.2)]">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-black text-white">EDIT HABIT</h2>
              <button onClick={() => { setShowEditModal(false); setEditingHabit(null); setHabitForm({ name: "", desc: "" }); }} className="text-gray-500 hover:text-white"><X /></button>
            </div>
            <form onSubmit={handleUpdateHabit} className="space-y-4">
              <input
                className="w-full bg-black/40 border border-gray-700 rounded-xl p-4 text-white focus:border-brand-gold outline-none"
                placeholder="Habit Name"
                value={habitForm.name}
                onChange={e => setHabitForm({ ...habitForm, name: e.target.value })}
                autoFocus
              />
              <textarea
                className="w-full bg-black/40 border border-gray-700 rounded-xl p-4 text-white focus:border-brand-gold outline-none resize-none h-32"
                placeholder="Description / Frequency"
                value={habitForm.desc}
                onChange={e => setHabitForm({ ...habitForm, desc: e.target.value })}
              />
              <button type="submit" className="w-full py-4 bg-brand-gold text-black font-black rounded-xl hover:bg-white transition-colors">
                UPDATE HABIT
              </button>
            </form>
          </div>
        </div>
      )}

      {/* AI Chatbot */}
      <AnimatePresence>
        {showChatbot && (
          <ChatContainer 
            userId={user?.id || "guest"} 
            isOpen={showChatbot} 
            onClose={() => setShowChatbot(false)} 
          />
        )}
      </AnimatePresence>

      {/* Chatbot Toggle Button */}
      <button
        onClick={() => setShowChatbot(!showChatbot)}
        className={`fixed bottom-6 right-6 z-[100] w-16 h-16 rounded-2xl flex items-center justify-center transition-all duration-300 shadow-lg ${
          showChatbot 
            ? 'bg-red-500/20 border-2 border-red-500/50 hover:bg-red-500/30' 
            : 'bg-brand-cyan/20 border-2 border-brand-cyan/50 hover:bg-brand-cyan/30 shadow-[0_0_30px_rgba(0,240,255,0.3)]'
        }`}
      >
        {showChatbot ? (
          <X className="w-7 h-7 text-red-400" />
        ) : (
          <MessageSquare className="w-7 h-7 text-brand-cyan" />
        )}
      </button>

      <Footer />
    </div>
  );
}
