"use client";

import { motion } from "framer-motion";
import { Check } from "lucide-react";

interface HabitItemProps {
  id: string;
  name: string;
  completed: boolean;
  onToggle: () => void;
}

export const HabitItem = ({ id, name, completed, onToggle }: HabitItemProps) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ scale: 1.01 }}
      className="flex items-center justify-between p-4 mb-3 bg-white rounded-xl shadow-sm border border-gray-100 hover:border-brand-yellow transition-colors"
    >
      <div className="flex items-center gap-4">
        <motion.button
          onClick={onToggle}
          whileTap={{ scale: 0.9 }}
          className={`w-7 h-7 rounded-full border-2 flex items-center justify-center transition-colors ${
            completed
              ? "bg-brand-orange border-brand-orange text-white"
              : "border-gray-200 hover:border-brand-yellow"
          }`}
        >
          {completed && (
            <motion.div
              initial={{ scale: 0, rotate: -45 }}
              animate={{ scale: 1, rotate: 0 }}
            >
              <Check size={16} strokeWidth={3} />
            </motion.div>
          )}
        </motion.button>
        <span className={`text-lg font-medium ${completed ? "text-gray-400 line-through" : "text-gray-700"}`}>
          {name}
        </span>
      </div>

      {/* Visual cue for streak or priority could go here */}
      <div className="w-2 h-2 rounded-full bg-brand-yellow" />
    </motion.div>
  );
};
