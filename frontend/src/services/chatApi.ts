/**
 * Chat API Client for Phase III Chatbot.
 *
 * Provides typed API calls to the stateless chat endpoint.
 */
import { useState, useCallback } from 'react';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

// Remove trailing /api if present to avoid double /api/api
const getBaseUrl = () => {
  let base = API_BASE;
  if (base.endsWith('/api')) {
    base = base.slice(0, -4);
  }
  return base;
};

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export interface ChatResponse {
  conversation_id: string;
  message: ChatMessage;
  suggestions: string[];
}

export interface Conversation {
  id: string;
  title: string | null;
  created_at: string;
  last_activity_at: string;
}

class ChatApiClient {
  private getAuthHeaders(): HeadersInit {
    // Get JWT from storage (Phase II auth)
    const token = typeof window !== 'undefined'
      ? localStorage.getItem('auth_token')
      : null;

    if (!token) {
      throw new Error('No authentication token found');
    }

    return {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    };
  }

  async sendMessage(
    userId: string,
    message: string,
    conversationId?: string
  ): Promise<ChatResponse> {
    const url = `${getBaseUrl()}/api/${userId}/chat`;
    console.log('Sending message to:', url);
    
    const response = await fetch(url, {
      method: 'POST',
      headers: this.getAuthHeaders(),
      body: JSON.stringify({ message, conversation_id: conversationId }),
    });

    console.log('Response status:', response.status);
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      console.error('API Error:', error);
      throw new Error(error.detail || 'Failed to send message');
    }

    return response.json();
  }

  async listConversations(
    userId: string,
    limit = 20,
    offset = 0
  ): Promise<{ conversations: Conversation[]; total: number }> {
    const response = await fetch(
      `${getBaseUrl()}/api/${userId}/chat/conversations?limit=${limit}&offset=${offset}`,
      {
        method: 'GET',
        headers: this.getAuthHeaders(),
      }
    );

    if (!response.ok) {
      throw new Error('Failed to list conversations');
    }

    return response.json();
  }

  async deleteConversation(
    userId: string,
    conversationId: string
  ): Promise<void> {
    const response = await fetch(
      `${getBaseUrl()}/api/${userId}/chat/conversations/${conversationId}`,
      {
        method: 'DELETE',
        headers: this.getAuthHeaders(),
      }
    );

    if (!response.ok) {
      throw new Error('Failed to delete conversation');
    }
  }
}

// Singleton instance
export const chatApi = new ChatApiClient();

// React hook for chat functionality
export function useChat(userId: string) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim() || isLoading) return;

    setIsLoading(true);
    setError(null);

    try {
      // Add user message immediately
      const userMessage: ChatMessage = {
        id: `temp-${Date.now()}`,
        role: 'user',
        content: content.trim(),
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, userMessage]);

      // Show typing indicator
      setIsTyping(true);

      // Send to API
      const response = await chatApi.sendMessage(userId, content.trim(), conversationId || undefined);

      // Update conversation ID if new
      if (!conversationId) {
        setConversationId(response.conversation_id);
      }

      // Add assistant message
      setMessages(prev => [...prev, response.message]);

      // Update suggestions
      setSuggestions(response.suggestions);

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send message');
    } finally {
      setIsLoading(false);
      setIsTyping(false);
    }
  }, [userId, conversationId, isLoading]);

  const clearChat = useCallback(() => {
    setMessages([]);
    setConversationId(null);
    setSuggestions([]);
    setError(null);
  }, []);

  const clearSuggestions = useCallback(() => {
    setSuggestions([]);
  }, []);

  return {
    messages,
    conversationId,
    isLoading,
    isTyping,
    suggestions,
    error,
    sendMessage,
    clearChat,
    clearSuggestions,
  };
}
