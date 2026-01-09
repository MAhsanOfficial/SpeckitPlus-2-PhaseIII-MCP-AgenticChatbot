"use client";

import { Github, Twitter, Linkedin } from "lucide-react";

export function Footer() {
  return (
    <footer className="bg-brand-dark/90 backdrop-blur-xl border-t border-white/5 py-32 relative overflow-hidden z-20">
      {/* Glow Effect */}
      <div className="absolute top-0 left-1/4 w-96 h-1 bg-gradient-brand opacity-50 blur-[2px]" />

      <div className="container mx-auto px-10 flex flex-col md:flex-row justify-between items-center gap-8">
        <div className="text-center md:text-left">
          <h4 className="text-2xl font-black text-white tracking-tighter">
            ROBO<span className="text-brand-cyan">HABIT</span>
          </h4>
          <p className="text-gray-500 text-sm mt-3 font-mono">
            System version: 2.0.4 [STABLE]
          </p>
        </div>

        <div className="flex gap-6">
          {[
            { Icon: Github, href: "https://github.com/MAhsanOfficial" },
            { Icon: Twitter, href: "#" },
            { Icon: Linkedin, href: "https://www.linkedin.com/in/muhammad-ahsan-b26317296/" }
          ].map(({ Icon, href }, idx) => (
            <a
              key={idx}
              href={href}
              target="_blank"
              rel="noopener noreferrer"
              className="p-3 rounded-xl bg-white/5 hover:bg-brand-cyan/10 text-gray-400 hover:text-brand-cyan transition-all hover:-translate-y-1 hover:shadow-[0_0_15px_rgba(0,240,255,0.3)] border border-transparent hover:border-brand-cyan/20"
            >
              <Icon size={20} />
            </a>
          ))}
        </div>

        <div className="text-center md:text-right">
          <p className="text-gray-600 text-[10px] font-mono tracking-widest uppercase">
            Created by Muhammad Ahsan
            <br />
            © 2025 NEURAL SYSTEMS INC.
          </p>
        </div>
      </div>
    </footer>
  );
}
