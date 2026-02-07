'use client';

import React, { useState, useEffect } from 'react';
import { TrendingUp, Users, Clock, Star, MapPin, Target } from 'lucide-react';
import API_URL from '@/lib/api-config';

interface MetricsData {
    summary: {
        total_searches: number;
        total_indianizations: number;
        total_ocr_scans: number;
        total_feedback: number;
        avg_search_time_ms: number;
        avg_top_coverage: number;
        overall_avg_rating: number;
        indianization_by_region: Record<string, number>;
    };
    performance: {
        search_performance: {
            avg_time_ms: number;
            p95_time_ms: number;
            p99_time_ms: number;
        };
        ocr_performance: {
            avg_time_ms: number;
            avg_confidence: number;
            success_rate: number;
        };
    };
    satisfaction: {
        overall_satisfaction: number;
        by_category: Record<string, number>;
        rating_distribution: Record<string, number>;
    };
}

export const MetricsDashboard: React.FC = () => {
    const [metrics, setMetrics] = useState<MetricsData | null>(null);
    const [loading, setLoading] = useState(true);
    const [timeRange, setTimeRange] = useState(7);

    useEffect(() => {
        fetchMetrics();
    }, [timeRange]);

    const fetchMetrics = async () => {
        setLoading(true);
        try {
            const [summaryRes, performanceRes, satisfactionRes] = await Promise.all([
                fetch(`${API_URL}/api/metrics/summary?days=${timeRange}`),
                fetch(`${API_URL}/api/metrics/performance`),
                fetch(`${API_URL}/api/metrics/satisfaction`)
            ]);

            const summary = await summaryRes.json();
            const performance = await performanceRes.json();
            const satisfaction = await satisfactionRes.json();

            setMetrics({ summary, performance, satisfaction });
        } catch (error) {
            console.error('Error fetching metrics:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="text-pink-200 text-xl">Loading metrics...</div>
            </div>
        );
    }

    if (!metrics) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="text-pink-300">Failed to load metrics</div>
            </div>
        );
    }

    const { summary, performance, satisfaction } = metrics;

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-3xl font-bold gradient-text">Analytics Dashboard</h2>
                    <p className="text-pink-200 mt-1">Real-time performance metrics</p>
                </div>

                {/* Time Range Selector */}
                <div className="flex gap-2">
                    {[7, 30, 90].map((days) => (
                        <button
                            key={days}
                            onClick={() => setTimeRange(days)}
                            className={`px-4 py-2 rounded-lg font-semibold transition-all ${timeRange === days
                                ? 'bg-gradient-to-r from-pink-500 to-pink-400 text-white'
                                : 'bg-pink-950/30 text-pink-200 border border-pink-400/20 hover:border-pink-400/40'
                                }`}
                        >
                            {days}d
                        </button>
                    ))}
                </div>
            </div>

            {/* Key Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <MetricCard
                    icon={<TrendingUp className="w-6 h-6" />}
                    label="Total Searches"
                    value={summary.total_searches}
                    color="pink"
                />
                <MetricCard
                    icon={<Clock className="w-6 h-6" />}
                    label="Avg Search Time"
                    value={`${summary.avg_search_time_ms.toFixed(1)}ms`}
                    color="pink"
                />
                <MetricCard
                    icon={<Target className="w-6 h-6" />}
                    label="Avg Coverage"
                    value={`${(summary.avg_top_coverage * 100).toFixed(1)}%`}
                    color="pink"
                />
                <MetricCard
                    icon={<Star className="w-6 h-6" />}
                    label="User Rating"
                    value={`${summary.overall_avg_rating.toFixed(1)}/5`}
                    color="pink"
                />
            </div>

            {/* Performance Metrics */}
            <div className="glass rounded-2xl p-6 space-y-4">
                <h3 className="text-xl font-semibold text-pink-100 flex items-center gap-2">
                    <Clock className="w-5 h-5 text-pink-400" />
                    Performance Metrics
                </h3>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="bg-pink-950/30 rounded-xl p-4 border border-pink-400/20">
                        <div className="text-pink-300 text-sm mb-1">Average</div>
                        <div className="text-2xl font-bold text-pink-100">
                            {performance.search_performance.avg_time_ms.toFixed(1)}ms
                        </div>
                    </div>
                    <div className="bg-pink-950/30 rounded-xl p-4 border border-pink-400/20">
                        <div className="text-pink-300 text-sm mb-1">P95</div>
                        <div className="text-2xl font-bold text-pink-100">
                            {performance.search_performance.p95_time_ms.toFixed(1)}ms
                        </div>
                    </div>
                    <div className="bg-pink-950/30 rounded-xl p-4 border border-pink-400/20">
                        <div className="text-pink-300 text-sm mb-1">P99</div>
                        <div className="text-2xl font-bold text-pink-100">
                            {performance.search_performance.p99_time_ms.toFixed(1)}ms
                        </div>
                    </div>
                </div>
            </div>

            {/* Regional Indianization */}
            <div className="glass rounded-2xl p-6 space-y-4">
                <h3 className="text-xl font-semibold text-pink-100 flex items-center gap-2">
                    <MapPin className="w-5 h-5 text-pink-400" />
                    Indianization by Region
                </h3>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {Object.entries(summary.indianization_by_region || {}).map(([region, count]) => (
                        <div key={region} className="bg-pink-950/30 rounded-xl p-4 border border-pink-400/20">
                            <div className="text-pink-300 text-sm mb-1 capitalize">{region}</div>
                            <div className="text-2xl font-bold text-pink-100">{count}</div>
                        </div>
                    ))}
                </div>
            </div>

            {/* User Satisfaction */}
            <div className="glass rounded-2xl p-6 space-y-4">
                <h3 className="text-xl font-semibold text-pink-100 flex items-center gap-2">
                    <Star className="w-5 h-5 text-pink-400" />
                    User Satisfaction
                </h3>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Rating by Category */}
                    <div className="space-y-3">
                        <h4 className="text-pink-200 font-semibold">By Category</h4>
                        {Object.entries(satisfaction.by_category || {}).map(([category, rating]) => (
                            <div key={category} className="space-y-1">
                                <div className="flex items-center justify-between text-sm">
                                    <span className="text-pink-300 capitalize">{category}</span>
                                    <span className="text-pink-100 font-semibold">{rating.toFixed(1)}/5</span>
                                </div>
                                <div className="h-2 bg-pink-950/30 rounded-full overflow-hidden">
                                    <div
                                        className="h-full bg-gradient-to-r from-pink-500 to-pink-400"
                                        style={{ width: `${(rating / 5) * 100}%` }}
                                    />
                                </div>
                            </div>
                        ))}
                    </div>

                    {/* Rating Distribution */}
                    <div className="space-y-3">
                        <h4 className="text-pink-200 font-semibold">Rating Distribution</h4>
                        {Object.entries(satisfaction.rating_distribution || {})
                            .reverse()
                            .map(([stars, count]) => (
                                <div key={stars} className="flex items-center gap-3">
                                    <div className="text-pink-300 text-sm w-8">{stars}★</div>
                                    <div className="flex-1 h-6 bg-pink-950/30 rounded-full overflow-hidden">
                                        <div
                                            className="h-full bg-gradient-to-r from-pink-500 to-pink-400 flex items-center justify-end pr-2"
                                            style={{
                                                width: `${(count / Math.max(...Object.values(satisfaction.rating_distribution))) * 100}%`
                                            }}
                                        >
                                            <span className="text-xs text-white font-semibold">{count}</span>
                                        </div>
                                    </div>
                                </div>
                            ))}
                    </div>
                </div>
            </div>

            {/* Activity Summary */}
            <div className="glass rounded-2xl p-6">
                <h3 className="text-xl font-semibold text-pink-100 mb-4">Activity Summary</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="text-center">
                        <div className="text-3xl font-bold text-pink-100">{summary.total_searches}</div>
                        <div className="text-pink-300 text-sm mt-1">Searches</div>
                    </div>
                    <div className="text-center">
                        <div className="text-3xl font-bold text-pink-100">{summary.total_indianizations}</div>
                        <div className="text-pink-300 text-sm mt-1">Indianizations</div>
                    </div>
                    <div className="text-center">
                        <div className="text-3xl font-bold text-pink-100">{summary.total_ocr_scans}</div>
                        <div className="text-pink-300 text-sm mt-1">OCR Scans</div>
                    </div>
                    <div className="text-center">
                        <div className="text-3xl font-bold text-pink-100">{summary.total_feedback}</div>
                        <div className="text-pink-300 text-sm mt-1">Feedback</div>
                    </div>
                </div>
            </div>
        </div>
    );
};

// Helper component for metric cards
const MetricCard: React.FC<{
    icon: React.ReactNode;
    label: string;
    value: string | number;
    color: string;
}> = ({ icon, label, value, color }) => (
    <div className="glass rounded-xl p-6 space-y-2">
        <div className={`text-${color}-400`}>{icon}</div>
        <div className="text-pink-300 text-sm">{label}</div>
        <div className="text-2xl font-bold text-pink-100">{value}</div>
    </div>
);
