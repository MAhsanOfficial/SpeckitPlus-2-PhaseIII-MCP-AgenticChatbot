"use client";

import React, { createContext, useContext, useState, useEffect, useCallback } from "react";
import { useAuth } from "./AuthContext";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Remove trailing /api if present
const getBaseUrl = () => {
  let base = API_BASE;
  if (base.endsWith('/api')) {
    base = base.slice(0, -4);
  }
  return base;
};

export interface Habit {
    id: string;
    name: string;
    description: string;
    completed: boolean;
    streak: number;
}

interface HabitContextType {
    habits: Habit[];
    addHabit: (name: string, description: string) => Promise<void>;
    updateHabit: (id: string, updates: Partial<Habit>) => Promise<void>;
    deleteHabit: (id: string) => Promise<void>;
    toggleHabit: (id: string) => Promise<void>;
    refreshHabits: () => Promise<void>;
    isLoading: boolean;
}

const HabitContext = createContext<HabitContextType | undefined>(undefined);

export function HabitProvider({ children }: { children: React.ReactNode }) {
    const [habits, setHabits] = useState<Habit[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const { user } = useAuth();

    const getAuthHeaders = () => {
        const token = localStorage.getItem('auth_token');
        return {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
        };
    };

    // Fetch habits from database with today's completion status
    const fetchHabits = useCallback(async () => {
        if (!user?.id) {
            return;
        }
        
        try {
            const url = `${getBaseUrl()}/api/${user.id}/habits/`;
            
            const response = await fetch(url, {
                headers: getAuthHeaders(),
                cache: 'no-store',
            });

            if (response.ok) {
                const data = await response.json();
                
                const today = new Date().toISOString().split('T')[0];
                
                // Fetch today's completions for all habits
                const completionsResponse = await fetch(`${getBaseUrl()}/api/${user.id}/completions/?date=${today}`, {
                    headers: getAuthHeaders(),
                    cache: 'no-store',
                });
                
                let completionsMap: Record<string, boolean> = {};
                if (completionsResponse.ok) {
                    const completions = await completionsResponse.json();
                    completionsMap = completions.reduce((acc: any, c: any) => {
                        acc[c.habit_id] = c.status;
                        return acc;
                    }, {});
                }
                
                // Transform backend format to frontend format with real completion status
                const transformedHabits = data.map((h: any) => ({
                    id: h.id,
                    name: h.name,
                    description: h.description || "",
                    completed: completionsMap[h.id] || false,
                    streak: h.streak || 0,
                }));
                
                // Only update if habits changed
                setHabits(prev => {
                    // Filter out temp habits from comparison (they're being created)
                    const prevReal = prev.filter(h => !h.id.startsWith('temp-'));
                    const prevJson = JSON.stringify(prevReal);
                    const newJson = JSON.stringify(transformedHabits);
                    
                    if (prevJson !== newJson) {
                        console.log('[HabitContext] Habits updated!');
                        // Keep temp habits and merge with new data
                        const tempHabits = prev.filter(h => h.id.startsWith('temp-'));
                        return [...transformedHabits, ...tempHabits];
                    }
                    return prev;
                });
            }
        } catch (error) {
            console.error('[HabitContext] Error fetching habits:', error);
        }
    }, [user?.id]);

    // Initial fetch
    useEffect(() => {
        fetchHabits();
    }, [fetchHabits]);

    // Auto-refresh every 2 seconds (slower, less aggressive) for chatbot sync
    useEffect(() => {
        const interval = setInterval(() => {
            fetchHabits();
        }, 2000); // Changed from 500ms to 2000ms

        return () => clearInterval(interval);
    }, [fetchHabits]);

    const addHabit = async (name: string, description: string) => {
        if (!user?.id) {
            console.error('[HabitContext] No user ID available');
            return;
        }

        console.log('[HabitContext] Adding habit:', { name, description, userId: user.id });
        
        // Optimistic update - add immediately with temp ID
        const tempId = `temp-${Date.now()}`;
        const optimisticHabit: Habit = {
            id: tempId,
            name,
            description: description || "",
            completed: false,
            streak: 0,
        };
        setHabits(prev => [...prev, optimisticHabit]);
        
        try {
            const url = `${getBaseUrl()}/api/${user.id}/habits`;
            
            const response = await fetch(url, {
                method: 'POST',
                headers: getAuthHeaders(),
                body: JSON.stringify({ name, description }),
            });
            
            if (response.ok) {
                const data = await response.json();
                console.log('[HabitContext] Habit created:', data);
                // Replace temp habit with real one from server
                setHabits(prev => prev.map(h => 
                    h.id === tempId 
                        ? { 
                            id: data.id, 
                            name: data.name, 
                            description: data.description || "", 
                            completed: false,
                            streak: 0
                        }
                        : h
                ));
                // Refresh after 1 second to ensure sync
                setTimeout(() => fetchHabits(), 1000);
            } else {
                const errorText = await response.text();
                console.error('[HabitContext] Failed to add habit:', response.status, errorText);
                // Remove optimistic habit on error
                setHabits(prev => prev.filter(h => h.id !== tempId));
            }
        } catch (error) {
            console.error('[HabitContext] Error adding habit:', error);
            // Remove optimistic habit on error
            setHabits(prev => prev.filter(h => h.id !== tempId));
        }
    };

    const updateHabit = async (id: string, updates: Partial<Habit>) => {
        if (!user?.id) {
            console.error('[HabitContext] No user ID available for update');
            return;
        }

        console.log('[HabitContext] Updating habit:', { id, updates, userId: user.id });
        
        // Store previous state for rollback
        const previousHabits = habits;
        
        // Optimistic update for instant UI feedback
        setHabits(prevHabits => 
            prevHabits.map(h => 
                h.id === id ? { ...h, ...updates } : h
            )
        );

        try {
            const url = `${getBaseUrl()}/api/${user.id}/habits/${id}`;
            console.log('[HabitContext] PUT URL:', url);
            
            const response = await fetch(url, {
                method: 'PUT',
                headers: getAuthHeaders(),
                body: JSON.stringify({
                    name: updates.name,
                    description: updates.description,
                }),
            });

            console.log('[HabitContext] Update response status:', response.status);

            if (response.ok) {
                const data = await response.json();
                console.log('[HabitContext] Habit updated on server:', data);
                // Update with server data after 1 second
                setTimeout(() => fetchHabits(), 1000);
            } else {
                const errorText = await response.text();
                console.error('[HabitContext] Failed to update habit:', response.status, errorText);
                // Revert on error
                setHabits(previousHabits);
            }
        } catch (error) {
            console.error('[HabitContext] Error updating habit:', error);
            // Revert on error
            setHabits(previousHabits);
        }
    };

    const deleteHabit = async (id: string) => {
        if (!user?.id) {
            console.error('[HabitContext] No user ID available for delete');
            return;
        }

        console.log('[HabitContext] Deleting habit:', { id, userId: user.id });
        
        // Optimistic delete for instant UI feedback
        const previousHabits = habits;
        setHabits(prevHabits => prevHabits.filter(h => h.id !== id));

        try {
            const url = `${getBaseUrl()}/api/${user.id}/habits/${id}`;
            console.log('[HabitContext] DELETE URL:', url);
            
            const response = await fetch(url, {
                method: 'DELETE',
                headers: getAuthHeaders(),
            });

            console.log('[HabitContext] Delete response status:', response.status);

            if (response.ok || response.status === 204) {
                console.log('[HabitContext] Habit deleted successfully');
                // Refresh after 1 second to ensure sync
                setTimeout(() => fetchHabits(), 1000);
            } else {
                const errorText = await response.text();
                console.error('[HabitContext] Failed to delete habit:', response.status, errorText);
                // Revert on error
                setHabits(previousHabits);
            }
        } catch (error) {
            console.error('[HabitContext] Error deleting habit:', error);
            // Revert on error
            setHabits(previousHabits);
        }
    };

    const toggleHabit = async (id: string) => {
        if (!user?.id) return;

        // Store previous state
        const previousHabits = habits;

        // Optimistic UI update
        setHabits(prevHabits => 
            prevHabits.map(h => 
                h.id === id ? { ...h, completed: !h.completed } : h
            )
        );

        try {
            const today = new Date().toISOString().split('T')[0];
            const response = await fetch(`${getBaseUrl()}/api/${user.id}/habits/${id}/toggle`, {
                method: 'POST',
                headers: getAuthHeaders(),
                body: JSON.stringify({ date: today, status: true }),
            });

            if (response.ok) {
                console.log('[HabitContext] Toggle successful');
                // Refresh after 1 second to get updated streak
                setTimeout(() => fetchHabits(), 1000);
            } else {
                console.error('[HabitContext] Toggle failed');
                // Revert optimistic update on error
                setHabits(previousHabits);
            }
        } catch (error) {
            console.error('Error toggling habit:', error);
            // Revert optimistic update on error
            setHabits(previousHabits);
        }
    };

    const refreshHabits = async () => {
        await fetchHabits();
    };

    return (
        <HabitContext.Provider value={{ 
            habits, 
            addHabit, 
            updateHabit, 
            deleteHabit, 
            toggleHabit, 
            refreshHabits,
            isLoading 
        }}>
            {children}
        </HabitContext.Provider>
    );
}

export function useHabits() {
    const context = useContext(HabitContext);
    if (context === undefined) {
        throw new Error("useHabits must be used within a HabitProvider");
    }
    return context;
}
