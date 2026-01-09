"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { useRouter } from "next/navigation";

interface User {
    id: string;
    name: string;
    email: string;
    phone?: string;
}

interface AuthContextType {
    user: User | null;
    login: (email: string, name: string, phone?: string) => void;
    logout: () => void;
    isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);
    const router = useRouter();

    useEffect(() => {
        const storedUser = localStorage.getItem("auth_user");
        if (storedUser) {
            const parsedUser = JSON.parse(storedUser);
            // Generate ID for existing users who don't have one
            if (!parsedUser.id) {
                parsedUser.id = "user_" + Date.now().toString(36) + Math.random().toString(36).substr(2, 9);
                localStorage.setItem("auth_user", JSON.stringify(parsedUser));
            }
            setUser(parsedUser);
        }
        setLoading(false);
    }, []);

    const login = (email: string, name: string, phone?: string) => {
        const userId = "user_" + Date.now().toString(36) + Math.random().toString(36).substr(2, 9);
        const newUser = { id: userId, email, name, phone };
        setUser(newUser);
        localStorage.setItem("auth_user", JSON.stringify(newUser));
        
        // Generate proper JWT token for the user
        const JWT_SECRET = "a9f3c1e8b24f7d9c2e1f0b8a9d4c6e7f1234567890abcdef1234567890abcd";
        
        // Create JWT payload
        const header = { alg: "HS256", typ: "JWT" };
        const payload = {
            sub: userId,
            exp: Math.floor(Date.now() / 1000) + (24 * 60 * 60) // 24 hours
        };
        
        // Simple JWT encoding (for development)
        const base64UrlEncode = (str: string) => {
            return btoa(str)
                .replace(/\+/g, '-')
                .replace(/\//g, '_')
                .replace(/=/g, '');
        };
        
        const headerEncoded = base64UrlEncode(JSON.stringify(header));
        const payloadEncoded = base64UrlEncode(JSON.stringify(payload));
        const signatureInput = `${headerEncoded}.${payloadEncoded}`;
        
        // For development, we'll use a simple token format
        // In production, use proper JWT library
        const token = `${headerEncoded}.${payloadEncoded}.dev_signature`;
        
        localStorage.setItem("auth_token", token);
        console.log("Generated JWT token for user:", userId);
    };

    const logout = () => {
        setUser(null);
        localStorage.removeItem("auth_user");
        localStorage.removeItem("auth_token");
        router.push("/");
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, isAuthenticated: !!user }}>
            {!loading && children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error("useAuth must be used within an AuthProvider");
    }
    return context;
}
