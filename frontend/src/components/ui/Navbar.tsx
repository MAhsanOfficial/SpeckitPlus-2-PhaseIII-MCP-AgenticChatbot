"use client";

import { useEffect, useRef } from "react";
import Link from "next/link";
import Image from "next/image";
import gsap from "gsap";
import { useAuth } from "@/context/AuthContext";
import { LogOut, User } from "lucide-react";

export const Navbar = () => {
  const navRef = useRef(null);
  const { user, isAuthenticated, logout } = useAuth();

  useEffect(() => {
    gsap.fromTo(
      navRef.current,
      { y: -100, opacity: 0 },
      { y: 0, opacity: 1, duration: 1, ease: "power4.out", delay: 0.5 }
    );
  }, []);

  return (
    <nav
      ref={navRef}
      className="fixed top-0 w-full z-50 flex justify-between items-center px-6 lg:px-10 py-4 bg-brand-dark/80 backdrop-blur-xl border-b border-white/5 shadow-lg shadow-brand-cyan/5"
    >
      <div className="flex items-center gap-3">
        <div className="relative w-10 h-10 rounded-full overflow-hidden border border-brand-cyan shadow-[0_0_10px_rgba(0,240,255,0.5)]">
          <Image src="/logo.png" alt="RoboHabit Logo" layout="fill" objectFit="cover" />
        </div>
        <div className="hidden sm:block">
          <Link href="/">
            <span className="text-2xl font-black text-white tracking-tighter cursor-pointer">
              ROBO<span className="text-brand-gold">HABIT</span>
            </span>
          </Link>
        </div>
      </div>

      <div className="flex gap-6 items-center text-sm font-bold tracking-widest text-gray-400">
        <Link href="/dashboard" className="text-white hover:text-brand-cyan transition-colors">DASHBOARD</Link>
        {isAuthenticated ? (
          <>
            <div className="flex items-center gap-2 text-white bg-white/5 px-4 py-2 rounded-full border border-white/10 hidden md:flex">
              <User size={16} className="text-brand-gold" />
              <span className="text-brand-cyan font-mono">{user?.name}</span>
            </div>
            <button
              onClick={logout}
              className="flex items-center gap-2 hover:text-red-500 transition-colors"
            >
              <LogOut size={18} />
              <span className="hidden sm:inline">LOGOUT</span>
            </button>
          </>
        ) : (
          <>
            <Link href="/login" className="hover:text-brand-cyan transition-colors">LOGIN</Link>
            <Link href="/signup" className="px-6 py-2 bg-gradient-brand text-black rounded-full hover:scale-105 active:scale-95 transition-all shadow-lg shadow-cyan-500/20">
              JOIN VIP
            </Link>
          </>
        )}
      </div>
    </nav>
  );
};
