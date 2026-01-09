"use client";

import { useEffect, useRef } from "react";
import gsap from "gsap";
import { HabitCards } from "@/components/ui/HabitCards";
import { Navbar } from "@/components/ui/Navbar";
import { Footer } from "@/components/ui/Footer";

export default function ProtocolsPage() {
  const containerRef = useRef(null);

  useEffect(() => {
    gsap.from(".protocol-title", {
      y: 50,
      opacity: 0,
      duration: 1.2,
      ease: "expo.out",
    });
  }, []);

  return (
    <main ref={containerRef} className="min-h-screen vip-gradient-bg">
      <Navbar />
      <div className="pt-32 px-10">
        <div className="max-w-7xl mx-auto">
          <h1 className="protocol-title text-6xl font-black text-white mb-4">
            SYSTEM <span className="text-gradient">PROTOCOLS</span>
          </h1>
          <p className="protocol-title text-gray-500 max-w-2xl text-lg mb-16">
            Access the core logic that drives high-performance robotic consistency.
          </p>
        </div>
        <HabitCards />
      </div>
      <Footer />
    </main>
  );
}
