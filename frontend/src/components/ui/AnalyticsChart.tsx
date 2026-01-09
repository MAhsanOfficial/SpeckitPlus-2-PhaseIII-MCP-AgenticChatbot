"use client";

import { ResponsiveContainer, AreaChart, Area, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, Legend } from "recharts";
import { Habit } from "@/context/HabitContext";

interface AnalyticsChartProps {
    habits: Habit[];
}

export function AnalyticsChart({ habits }: AnalyticsChartProps) {
    // Process data from habits
    const totalCompleted = habits.filter(h => h.completed).length;
    const totalActive = habits.filter(h => !h.completed).length;

    // Mock historical data for demonstration (since we don't store historical timeline in this simple app yet)
    // In a real app, this would come from a history log
    const data = [
        { day: "Analysis Point A", completed: Math.max(1, Math.floor(totalCompleted * 0.3)), missed: Math.max(0, Math.floor(totalActive * 0.5)) },
        { day: "Analysis Point B", completed: Math.max(1, Math.floor(totalCompleted * 0.6)), missed: Math.max(0, Math.floor(totalActive * 0.3)) },
        { day: "Analysis Point C", completed: totalCompleted, missed: totalActive },
    ];

    return (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Positive Analysis - Kinetic Output */}
            <div className="glass-morphism rounded-3xl p-6 border border-brand-cyan/20 bg-brand-cyan/5">
                <div className="flex justify-between items-center mb-6">
                    <h4 className="text-brand-cyan font-bold uppercase tracking-widest text-sm flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-brand-cyan shadow-[0_0_10px_#00F0FF]" />
                        Positive Analysis
                    </h4>
                    <span className="text-xs font-mono text-brand-cyan/70">EFFICIENCY RATE</span>
                </div>

                <div className="h-64 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                        <AreaChart data={data}>
                            <defs>
                                <linearGradient id="cyanGradient" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#00F0FF" stopOpacity={0.4} />
                                    <stop offset="95%" stopColor="#00F0FF" stopOpacity={0} />
                                </linearGradient>
                            </defs>
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                            <XAxis
                                dataKey="day"
                                stroke="#4B5563"
                                fontSize={10}
                                tickLine={false}
                                axisLine={false}
                                dy={10}
                            />
                            <YAxis
                                stroke="#4B5563"
                                fontSize={10}
                                tickLine={false}
                                axisLine={false}
                                dx={-10}
                            />
                            <Tooltip
                                contentStyle={{
                                    backgroundColor: "rgba(10, 10, 11, 0.9)",
                                    borderColor: "rgba(0, 240, 255, 0.3)",
                                    backdropFilter: "blur(10px)",
                                    borderRadius: "12px",
                                    color: "#fff"
                                }}
                                cursor={{ stroke: 'rgba(0, 240, 255, 0.2)', strokeWidth: 2 }}
                            />
                            <Area
                                type="monotone"
                                dataKey="completed"
                                stroke="#00F0FF"
                                strokeWidth={3}
                                fillOpacity={1}
                                fill="url(#cyanGradient)"
                                animationDuration={2000}
                            />
                        </AreaChart>
                    </ResponsiveContainer>
                </div>
            </div>

            {/* Negative Analysis - Variance Detection */}
            <div className="glass-morphism rounded-3xl p-6 border border-red-500/20 bg-red-500/5">
                <div className="flex justify-between items-center mb-6">
                    <h4 className="text-red-500 font-bold uppercase tracking-widest text-sm flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-red-500 shadow-[0_0_10px_#EF4444]" />
                        Negative Analysis
                    </h4>
                    <span className="text-xs font-mono text-red-500/70">PROTOCOL FAILURES</span>
                </div>

                <div className="h-64 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={data}>
                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                            <XAxis
                                dataKey="day"
                                stroke="#4B5563"
                                fontSize={10}
                                tickLine={false}
                                axisLine={false}
                                dy={10}
                            />
                            <YAxis
                                stroke="#4B5563"
                                fontSize={10}
                                tickLine={false}
                                axisLine={false}
                                dx={-10}
                            />
                            <Tooltip
                                cursor={{ fill: 'rgba(239, 68, 68, 0.05)' }}
                                contentStyle={{
                                    backgroundColor: "rgba(10, 10, 11, 0.9)",
                                    borderColor: "rgba(239, 68, 68, 0.3)",
                                    backdropFilter: "blur(10px)",
                                    borderRadius: "12px",
                                    color: "#fff"
                                }}
                            />
                            <Bar
                                dataKey="missed"
                                fill="#EF4444"
                                radius={[4, 4, 0, 0]}
                                animationDuration={2000}
                                barSize={20}
                            />
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
}
