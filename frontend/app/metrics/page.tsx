'use client';

import React from 'react';
import { MetricsDashboard } from '@/components/features/MetricsDashboard';

export default function MetricsPage() {
    return (
        <div className="min-h-screen py-12 px-4">
            {/* Floating Gradient Orbs */}
            <div className="gradient-orb w-96 h-96 bg-gradient-to-r from-pink-500/30 to-pink-300/30" style={{ top: '10%', left: '5%' }} />
            <div className="gradient-orb w-80 h-80 bg-gradient-to-r from-pink-400/20 to-pink-200/20" style={{ top: '60%', right: '10%', animationDelay: '2s' }} />

            <div className="relative z-10 max-w-7xl mx-auto">
                <MetricsDashboard />
            </div>
        </div>
    );
}
