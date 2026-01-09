"use client";

import { useEffect, useRef } from "react";
import { Activity, Cpu, Brain, Sparkles } from "lucide-react";
import Image from "next/image";
import gsap from "gsap";

const cards = [
  {
    title: "KINETIC OUTPUT",
    desc: "Optimized physical movement protocols.",
    icon: <Activity className="text-brand-cyan" size={32} />,
    // Robot running/exercising
    img: "/images/robot_running_vip.png",
    stat: "STATUS: ACTIVE",
    color: "cyan"
  },
  {
    title: "DATA INGESTION",
    desc: "High-bandwidth knowledge acquisition.",
    icon: <Brain className="text-brand-blue" size={32} />,
    // Robot reading/learning with books
    img: "/images/robot_reading_vip.png",
    stat: "STATUS: LEARNING",
    color: "blue"
  },
  {
    title: "SYSTEM RECHARGE",
    desc: "Rapid energy recovery cycles.",
    icon: <Sparkles className="text-purple-400" size={32} />,
    // Robot meditating/charging/scrolling
    img: "/images/robot_scrolling_vip.png",
    stat: "STATUS: CHARGING",
    color: "purple"
  }
];

export function HabitCards() {
  const cardsRef = useRef<(HTMLDivElement | null)[]>([]);

  useEffect(() => {
    const cardElements = cardsRef.current.filter(Boolean) as HTMLDivElement[];

    if (cardElements.length === 0) return;

    // Animate cards entrance with stagger
    gsap.from(cardElements, {
      y: 100,
      scale: 0.8,
      duration: 1,
      stagger: 0.2,
      ease: "power4.out",
      delay: 0.3
    });

    // Setup hover animations for each card
    const cleanupFunctions: (() => void)[] = [];

    cardElements.forEach((card) => {
      if (!card) return;

      const handleMouseEnter = () => {
        gsap.to(card, {
          y: -15,
          scale: 1.02,
          duration: 0.5,
          ease: "power2.out"
        });

        const icon = card.querySelector(".card-icon");
        if (icon) {
          gsap.to(icon, {
            rotation: 360,
            scale: 1.2,
            duration: 0.6,
            ease: "back.out(1.7)"
          });
        }

        const img = card.querySelector(".card-img");
        if (img) {
          gsap.to(img, {
            scale: 1.15,
            duration: 0.6,
            ease: "power2.out"
          });
        }

        const glow = card.querySelector(".card-glow");
        if (glow) {
          gsap.to(glow, {
            opacity: 1,
            duration: 0.4
          });
        }
      };

      const handleMouseLeave = () => {
        gsap.to(card, {
          y: 0,
          scale: 1,
          duration: 0.5,
          ease: "power2.out"
        });

        const icon = card.querySelector(".card-icon");
        if (icon) {
          gsap.to(icon, {
            rotation: 0,
            scale: 1,
            duration: 0.4
          });
        }

        const img = card.querySelector(".card-img");
        if (img) {
          gsap.to(img, {
            scale: 1,
            duration: 0.6,
            ease: "power2.out"
          });
        }

        const glow = card.querySelector(".card-glow");
        if (glow) {
          gsap.to(glow, {
            opacity: 0,
            duration: 0.4
          });
        }
      };

      card.addEventListener("mouseenter", handleMouseEnter);
      card.addEventListener("mouseleave", handleMouseLeave);

      // Store cleanup function
      cleanupFunctions.push(() => {
        card.removeEventListener("mouseenter", handleMouseEnter);
        card.removeEventListener("mouseleave", handleMouseLeave);
      });
    });

    // Continuous pulse for status badges
    const statusElements = document.querySelectorAll(".card-status");
    gsap.to(statusElements, {
      opacity: 0.5,
      duration: 1.5,
      repeat: -1,
      yoyo: true,
      ease: "sine.inOut"
    });

    // Cleanup all event listeners
    return () => {
      cleanupFunctions.forEach(cleanup => cleanup());
    };
  }, []);

  return (
    <section className="py-20 px-6 lg:px-20 bg-brand-dark relative z-20 overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-brand-cyan/5 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/5 rounded-full blur-3xl animate-pulse" style={{ animationDelay: "1s" }} />
      </div>

      <div className="text-center mb-16 px-4 relative z-10">
        <div className="inline-block px-3 py-1 rounded-full border border-gray-800 bg-gray-900/50 backdrop-blur text-gray-400 text-[10px] font-bold tracking-[0.2em] mb-4">
          <Cpu className="inline w-3 h-3 mr-2 animate-spin" style={{ animationDuration: "3s" }} />
          MODULE SELECTION
        </div>
        <h2 className="text-4xl lg:text-5xl font-black text-white mb-4 uppercase tracking-tighter">
          CORE <span className="text-gradient">MODULES</span>
        </h2>
        <p className="text-gray-500 max-w-lg mx-auto">Select a protocol to enhance your daily output parameters.</p>
      </div>

      <div className="grid md:grid-cols-3 gap-8 max-w-7xl mx-auto relative z-10">
        {cards.map((card, idx) => (
          <div
            key={idx}
            ref={(el) => { cardsRef.current[idx] = el; }}
            className="group relative glass-morphism rounded-[2rem] p-1 overflow-hidden transition-all duration-500 cursor-pointer"
          >
            {/* Animated border glow */}
            <div className="card-glow absolute inset-0 bg-gradient-to-b from-brand-cyan/30 via-purple-500/20 to-transparent opacity-0 transition-opacity duration-500" />

            {/* Scan line effect */}
            <div className="absolute inset-0 overflow-hidden pointer-events-none">
              <div className="absolute w-full h-1 bg-gradient-to-r from-transparent via-brand-cyan to-transparent opacity-50 animate-scan" />
            </div>

            <div className="bg-brand-card rounded-[1.8rem] h-full p-6 flex flex-col relative z-10">
              <div className="flex justify-between items-start mb-8">
                <div className="card-icon p-3 rounded-2xl bg-white/5 border border-white/10 transition-all duration-300 shadow-inner relative overflow-hidden">
                  {/* Icon glow effect */}
                  <div className="absolute inset-0 bg-brand-cyan/20 blur-xl opacity-0 group-hover:opacity-100 transition-opacity" />
                  <div className="relative z-10">{card.icon}</div>
                </div>
                <span className="card-status text-[10px] font-bold text-gray-500 border border-gray-800 px-3 py-1 rounded-full uppercase tracking-widest transition-colors">
                  {card.stat}
                </span>
              </div>

              <div className="mb-6 relative h-56 w-full rounded-2xl overflow-hidden bg-black/50 border border-white/5 group-hover:border-brand-cyan/30 transition-colors">
                {/* Image overlay effects */}
                <div className="absolute inset-0 bg-gradient-to-t from-brand-card via-transparent to-transparent z-10" />
                <div className="absolute inset-0 bg-brand-cyan/10 mix-blend-overlay z-20 opacity-0 group-hover:opacity-100 transition-opacity" />

                {/* Grid overlay for tech feel */}
                <div className="absolute inset-0 z-30 opacity-20 group-hover:opacity-40 transition-opacity"
                  style={{
                    backgroundImage: "linear-gradient(rgba(0,240,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(0,240,255,0.1) 1px, transparent 1px)",
                    backgroundSize: "20px 20px"
                  }}
                />

                <img
                  src={card.img}
                  alt={card.title}
                  className="card-img w-full h-full object-cover transition-all duration-700 relative z-0"
                />

                {/* Corner accents */}
                <div className="absolute top-2 left-2 w-4 h-4 border-t-2 border-l-2 border-brand-cyan/50 opacity-0 group-hover:opacity-100 transition-opacity" />
                <div className="absolute top-2 right-2 w-4 h-4 border-t-2 border-r-2 border-brand-cyan/50 opacity-0 group-hover:opacity-100 transition-opacity" />
                <div className="absolute bottom-2 left-2 w-4 h-4 border-b-2 border-l-2 border-brand-cyan/50 opacity-0 group-hover:opacity-100 transition-opacity" />
                <div className="absolute bottom-2 right-2 w-4 h-4 border-b-2 border-r-2 border-brand-cyan/50 opacity-0 group-hover:opacity-100 transition-opacity" />
              </div>

              <h3 className="text-xl font-bold text-white mb-2 uppercase tracking-wide group-hover:text-brand-cyan transition-colors">
                {card.title}
              </h3>
              <p className="text-gray-400 text-sm leading-relaxed group-hover:text-gray-300 transition-colors">
                {card.desc}
              </p>

              {/* Bottom accent line */}
              <div className="mt-auto pt-4">
                <div className="h-1 w-0 bg-gradient-to-r from-brand-cyan to-purple-500 group-hover:w-full transition-all duration-700 rounded-full" />
              </div>
            </div>
          </div>
        ))}
      </div>

      <style jsx>{`
        @keyframes scan {
          0% {
            top: -10%;
          }
          100% {
            top: 110%;
          }
        }
        .animate-scan {
          animation: scan 3s linear infinite;
        }
      `}</style>
    </section>
  );
}
