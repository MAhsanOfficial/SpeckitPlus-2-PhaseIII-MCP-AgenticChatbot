/**
 * ChatContainer Component for Phase III Chatbot.
 *
 * Agentic chatbot for natural language habit management.
 * Matches the dashboard's cyberpunk theme.
 */
'use client';

import { useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChatMessage } from './ChatMessage';
import { ChatInput } from './ChatInput';
import { useChat } from '@/services/chatApi';
import { useHabits } from '@/context/HabitContext';
import { MessageSquare, Sparkles, X, RotateCcw } from 'lucide-react';

interface ChatContainerProps {
  userId: string;
  isOpen: boolean;
  onClose: () => void;
}

export function ChatContainer({ userId, isOpen, onClose }: ChatContainerProps) {
  const {
    messages,
    isLoading,
    isTyping,
    suggestions,
    error,
    sendMessage,
    clearChat,
    clearSuggestions,
  } = useChat(userId);

  const { refreshHabits } = useHabits();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  // Refresh habits when new assistant message arrives (chatbot performed action)
  useEffect(() => {
    const lastMessage = messages[messages.length - 1];
    if (lastMessage && lastMessage.role === 'assistant') {
      // Aggressive refresh - multiple times to ensure UI updates
      console.log('[ChatContainer] Refreshing dashboard...');
      refreshHabits();
      setTimeout(() => refreshHabits(), 100);
      setTimeout(() => refreshHabits(), 250);
      setTimeout(() => refreshHabits(), 500);
      setTimeout(() => refreshHabits(), 1000);
      setTimeout(() => refreshHabits(), 2000);
    }
  }, [messages, refreshHabits]);

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95, y: 20 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.95, y: 20 }}
      className="fixed bottom-24 right-6 z-[99] w-[400px] h-[600px] flex flex-col bg-brand-card/95 backdrop-blur-xl rounded-3xl border border-brand-cyan/30 shadow-[0_0_50px_rgba(0,240,255,0.15)] overflow-hidden"
    >
      {/* Header */}
      <div className="flex items-center justify-between px-6 py-4 bg-gradient-to-r from-brand-cyan/20 to-brand-gold/10 border-b border-white/5">
        <div className="flex items-center gap-3">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            className="w-10 h-10 bg-brand-cyan/20 rounded-xl flex items-center justify-center border border-brand-cyan/30"
          >
            <Sparkles className="w-5 h-5 text-brand-cyan" />
          </motion.div>
          <div>
            <h2 className="text-white font-bold text-sm tracking-wide">HABIT AI</h2>
            <p className="text-gray-500 text-[10px] font-mono tracking-widest">NATURAL LANGUAGE CONTROL</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={clearChat}
            className="p-2 text-gray-500 hover:text-brand-cyan hover:bg-brand-cyan/10 rounded-lg transition-colors"
            title="New conversation"
          >
            <RotateCcw size={18} />
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={onClose}
            className="p-2 text-gray-500 hover:text-red-500 hover:bg-red-500/10 rounded-lg transition-colors"
            title="Close"
          >
            <X size={18} />
          </motion.button>
        </div>
      </div>

      {/* Error banner */}
      <AnimatePresence>
        {error && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="bg-red-500/10 px-4 py-2 text-red-400 text-xs text-center border-b border-red-500/20"
          >
            {error}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Messages area */}
      <div className="flex-1 overflow-y-auto px-4 py-6 bg-black/20">
        <AnimatePresence initial={false}>
          {messages.length === 0 ? (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="flex flex-col items-center justify-center h-full text-center px-6"
            >
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: 'spring', stiffness: 200, damping: 15 }}
                className="w-20 h-20 bg-gradient-to-br from-brand-cyan/20 to-brand-gold/20 rounded-2xl flex items-center justify-center mb-6 border border-brand-cyan/30 shadow-[0_0_30px_rgba(0,240,255,0.2)]"
              >
                <MessageSquare className="w-10 h-10 text-brand-cyan" />
              </motion.div>
              <h3 className="text-white font-bold mb-2 text-lg">HABIT COMMAND CENTER</h3>
              <p className="text-gray-500 text-sm mb-6">
                Natural language se apne habits manage karein
              </p>
              <div className="space-y-2 text-left w-full">
                <p className="text-[10px] font-bold text-gray-600 uppercase tracking-widest mb-3">TRY SAYING:</p>
                {[
                  "Show my habits",
                  "Add a new habit: Morning Exercise",
                  "Mark meditation as complete",
                  "Delete reading habit"
                ].map((example, i) => (
                  <motion.button
                    key={i}
                    whileHover={{ scale: 1.02, x: 5 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => sendMessage(example)}
                    className="w-full text-left px-4 py-3 bg-white/5 hover:bg-brand-cyan/10 border border-white/5 hover:border-brand-cyan/30 rounded-xl text-sm text-gray-400 hover:text-brand-cyan transition-all"
                  >
                    "{example}"
                  </motion.button>
                ))}
              </div>
            </motion.div>
          ) : (
            messages.map((message) => (
              <ChatMessage key={message.id} {...message} />
            ))
          )}
        </AnimatePresence>

        {/* Typing indicator */}
        <AnimatePresence>
          {isTyping && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="flex justify-start mb-4"
            >
              <div className="bg-white/5 border border-white/10 rounded-2xl rounded-bl-sm px-4 py-3">
                <div className="flex gap-1.5">
                  <motion.div
                    animate={{ scale: [1, 1.3, 1] }}
                    transition={{ repeat: Infinity, duration: 1, delay: 0 }}
                    className="w-2 h-2 bg-brand-cyan rounded-full"
                  />
                  <motion.div
                    animate={{ scale: [1, 1.3, 1] }}
                    transition={{ repeat: Infinity, duration: 1, delay: 0.2 }}
                    className="w-2 h-2 bg-brand-cyan rounded-full"
                  />
                  <motion.div
                    animate={{ scale: [1, 1.3, 1] }}
                    transition={{ repeat: Infinity, duration: 1, delay: 0.4 }}
                    className="w-2 h-2 bg-brand-cyan rounded-full"
                  />
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <ChatInput
        onSend={sendMessage}
        isLoading={isLoading}
        suggestions={suggestions}
        onSuggestionClick={(suggestion) => {
          sendMessage(suggestion);
        }}
        onClearSuggestions={clearSuggestions}
      />
    </motion.div>
  );
}
