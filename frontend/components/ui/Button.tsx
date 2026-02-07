import React, { ButtonHTMLAttributes } from 'react';
import { LucideIcon } from 'lucide-react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
    size?: 'sm' | 'md' | 'lg';
    icon?: LucideIcon;
    children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
    variant = 'primary',
    size = 'md',
    icon: Icon,
    children,
    className = '',
    ...props
}) => {
    const baseStyles = 'inline-flex items-center justify-center gap-2 font-semibold rounded-full transition-all duration-200 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed';

    const variants = {
        primary: 'bg-gradient-neon text-white hover:scale-105 shadow-lg hover:shadow-neon-pink/50',
        secondary: 'bg-gradient-warm text-white hover:scale-105 shadow-lg hover:shadow-neon-orange/50',
        outline: 'border-2 border-neon-purple text-neon-purple hover:bg-neon-purple hover:text-white',
        ghost: 'text-neon-purple hover:bg-neon-purple/10',
    };

    const sizes = {
        sm: 'px-4 py-2 text-sm',
        md: 'px-6 py-3 text-base',
        lg: 'px-8 py-4 text-lg',
    };

    return (
        <button
            className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`}
            {...props}
        >
            {Icon && <Icon size={size === 'sm' ? 16 : size === 'md' ? 20 : 24} />}
            {children}
        </button>
    );
};
