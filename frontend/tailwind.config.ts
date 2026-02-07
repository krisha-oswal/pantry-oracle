import type { Config } from "tailwindcss";

export default {
    content: [
        "./pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./components/**/*.{js,ts,jsx,tsx,mdx}",
        "./app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            colors: {
                // Gen Z Neon Pastel Palette
                'neon-pink': '#FF6EC7',
                'neon-purple': '#B794F6',
                'neon-blue': '#60D5FF',
                'neon-green': '#7FFF9F',
                'neon-yellow': '#FFE66D',
                'neon-orange': '#FF9A56',

                // Dark mode colors
                'dark-bg': '#0F0F1E',
                'dark-card': '#1A1A2E',
                'dark-border': '#2D2D44',

                // Light mode colors
                'light-bg': '#F8F9FF',
                'light-card': '#FFFFFF',
                'light-border': '#E5E7EB',
            },
            backgroundImage: {
                'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
                'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
                'gradient-neon': 'linear-gradient(135deg, #FF6EC7 0%, #B794F6 50%, #60D5FF 100%)',
                'gradient-warm': 'linear-gradient(135deg, #FFE66D 0%, #FF9A56 100%)',
            },
            animation: {
                'bounce-slow': 'bounce 3s infinite',
                'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                'float': 'float 6s ease-in-out infinite',
                'glow': 'glow 2s ease-in-out infinite alternate',
            },
            keyframes: {
                float: {
                    '0%, 100%': { transform: 'translateY(0px)' },
                    '50%': { transform: 'translateY(-20px)' },
                },
                glow: {
                    '0%': { boxShadow: '0 0 5px rgba(255, 110, 199, 0.5)' },
                    '100%': { boxShadow: '0 0 20px rgba(255, 110, 199, 0.8), 0 0 30px rgba(183, 148, 246, 0.6)' },
                },
            },
            fontFamily: {
                sans: ['var(--font-inter)', 'system-ui', 'sans-serif'],
            },
        },
    },
    plugins: [],
} satisfies Config;
