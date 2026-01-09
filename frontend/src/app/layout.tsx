import "./globals.css";
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { AuthProvider } from "@/context/AuthContext";
import { HabitProvider } from "@/context/HabitContext";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "RoboHabit | Upgrade Your Defaults",
  description: "VIP-style habit tracking for high-performance individuals.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-brand-dark text-white`}>
        <AuthProvider>
          <HabitProvider>
            {children}
          </HabitProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
