'use client';

import React from 'react';
import Link from 'next/link';
import { ChefHat } from 'lucide-react';

export const Navbar: React.FC = () => {
    return (
        <nav className="sticky top-0 z-50 backdrop-blur-xl bg-black/30 border-b border-pink-400/20">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                    {/* Logo */}
                    <Link href="/" className="flex items-center space-x-2 group">
                        <ChefHat className="w-8 h-8 text-neon-pink group-hover:scale-110 transition-transform" />
                        <span className="text-xl font-bold gradient-text">Pantry Oracle</span>
                    </Link>

                    {/* Navigation Links */}
                    <div className="hidden md:flex items-center space-x-8">
                        <Link
                            href="/"
                            className="text-pink-200 hover:text-neon-pink transition-colors font-medium"
                        >
                            Home
                        </Link>
                        <Link
                            href="/profile"
                            className="text-pink-200 hover:text-neon-pink transition-colors font-medium"
                        >
                            Profile
                        </Link>
                        <Link
                            href="/pantry"
                            className="text-pink-200 hover:text-neon-pink transition-colors font-medium"
                        >
                            My Pantry
                        </Link>
                        <Link
                            href="/metrics"
                            className="text-pink-200 hover:text-neon-pink transition-colors font-medium"
                        >
                            Analytics
                        </Link>
                    </div>

                    {/* CTA Button */}
                    <Link
                        href="/profile"
                        className="px-6 py-2 bg-gradient-to-r from-neon-pink to-pink-400 rounded-full text-white font-semibold hover:shadow-lg hover:shadow-neon-pink/50 transition-all"
                    >
                        Get Started
                    </Link>
                </div>
            </div>
        </nav>
    );
};
