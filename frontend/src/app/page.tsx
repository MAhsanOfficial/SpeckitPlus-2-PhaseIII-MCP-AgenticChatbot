import Hero from "@/components/ui/Hero";
import { HabitCards } from "@/components/ui/HabitCards";
import { Footer } from "@/components/ui/Footer";

export default function Home() {
  return (
    <main className="bg-brand-dark">
      <Hero />
      <HabitCards />
      <Footer />
    </main>
  );
}
