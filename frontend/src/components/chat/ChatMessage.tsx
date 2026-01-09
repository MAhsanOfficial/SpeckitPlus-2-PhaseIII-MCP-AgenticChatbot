/**
 * ChatMessage Component for Phase III Chatbot.
 *
 * Displays individual chat messages with cyberpunk theme.
 */
'use client';

import { motion } from 'framer-motion';
import { format } from 'date-fns';
import { User, Sparkles } from 'lucide-react';

interface ChatMessageProps {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export function ChatMessage({ role, content, timestamp }: ChatMessageProps) {
  const isUser = role === 'user';

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -20, scale: 0.95 }}
      transition={{ duration: 0.3, ease: 'easeOut' }}
      className={`flex w-full ${isUser ? 'justify-end' : 'justify-start'} mb-4`}
    >
      <div className={`flex items-end gap-2 max-w-[85%] ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
        {/* Avatar */}
        <div className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${
          isUser 
            ? 'bg-brand-gold/20 border border-brand-gold/30' 
            : 'bg-brand-cyan/20 border border-brand-cyan/30'
        }`}>
          {isUser ? (
            <User size={14} className="text-brand-gold" />
          ) : (
            <Sparkles size={14} className="text-brand-cyan" />
          )}
        </div>

        {/* Message bubble */}
        <div
          className={`rounded-2xl px-4 py-3 ${
            isUser
              ? 'bg-brand-gold/20 border border-brand-gold/30 rounded-br-sm'
              : 'bg-white/5 border border-white/10 rounded-bl-sm'
          }`}
        >
          <p className={`text-sm leading-relaxed ${isUser ? 'text-brand-gold' : 'text-gray-300'}`}>
            {content}
          </p>
          <p className={`text-[10px] mt-2 font-mono ${isUser ? 'text-brand-gold/50' : 'text-gray-600'}`}>
            {format(new Date(timestamp), 'HH:mm')}
          </p>
        </div>
      </div>
    </motion.div>
  );
}
