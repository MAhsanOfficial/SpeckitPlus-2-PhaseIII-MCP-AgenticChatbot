"use client";

import { useEffect, useRef } from "react";
import gsap from "gsap";
import Link from "next/link";
import { Navbar } from "@/components/ui/Navbar";

export default function Hero() {
  const heroRef = useRef(null);
  const textRef = useRef(null);
  const imageRef = useRef(null);

  useEffect(() => {
    const ctx = gsap.context(() => {
      // Text Entrance
      gsap.from(".hero-text", {
        y: 50,
        opacity: 0,
        duration: 1,
        stagger: 0.1,
        ease: "power3.out",
        delay: 0.2
      });

      // Image Entrance
      gsap.from(".hero-image", {
        x: 50,
        opacity: 0,
        duration: 1.2,
        delay: 0.5,
        ease: "power3.out"
      });

      // Floating animation for robot
      gsap.to(".hero-float", {
        y: -20,
        duration: 3,
        repeat: -1,
        yoyo: true,
        ease: "sine.inOut"
      });
    }, heroRef);

    return () => ctx.revert();
  }, []);

  return (
    <div ref={heroRef} className="relative min-h-screen flex flex-col vip-gradient-bg overflow-hidden">
      <Navbar />

      <div className="flex-1 flex flex-col lg:flex-row items-center justify-between px-6 lg:px-20 py-20 lg:py-0 relative z-10">

        {/* Text Section */}
        <div ref={textRef} className="lg:w-1/2 space-y-8 text-center lg:text-left z-20">
          <div className="hero-text inline-block px-4 py-2 rounded-full border border-brand-cyan/30 bg-brand-cyan/5 backdrop-blur-md">
            <span className="text-brand-cyan font-bold tracking-widest text-xs uppercase">Habit Tracking Upgrade Available</span>
          </div>

          <h1 className="hero-text text-5xl lg:text-7xl font-black text-white leading-tight drop-shadow-lg mb-4" data-text="UPGRADE YOUR">
            <span className="glitch" data-text="UPGRADE YOUR">UPGRADE YOUR</span> <br />
            <span className="text-gradient drop-shadow-lg filter glitch" data-text="DEFAULT HABITS">DEFAULT HABITS</span>
          </h1>

          <p className="hero-text text-gray-400 text-lg lg:text-xl max-w-xl mx-auto lg:mx-0 leading-relaxed font-light">
            Stop running outdated behavioral scripts. Install new protocols for high-performance living. Manage your habits with VIP precision.
          </p>

          <div className="hero-text flex flex-col sm:flex-row gap-4 justify-center lg:justify-start pt-4">
            <Link href="/signup" className="px-8 py-4 neon-btn text-black font-black rounded-xl text-center hover:scale-105 transition-transform flex items-center justify-center gap-2">
              START TRACKING
            </Link>
            <Link href="/login" className="px-8 py-4 border border-gray-700 hover:border-brand-cyan text-white font-bold rounded-xl text-center hover:bg-brand-cyan/5 transition-all">
              ACCESS DASHBOARD
            </Link>
          </div>
        </div>

        {/* Image Section */}
        <div ref={imageRef} className="lg:w-1/2 mt-10 lg:mt-0 relative flex justify-center hero-image z-10 w-full">
          {/* Background Glow */}
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-brand-cyan/10 blur-[120px] rounded-full pointer-events-none" />

          <img
            src="/hero-robot-showcase.png"
            alt="AI Robots Habit Showcase"
            className="hero-float relative z-10 w-full max-w-3xl drop-shadow-[0_20px_50px_rgba(0,240,255,0.15)] rounded-2xl border border-white/5"
          />
        </div>
      </div>
    </div>
  );
}
