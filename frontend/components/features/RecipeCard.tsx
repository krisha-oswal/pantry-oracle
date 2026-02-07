'use client';

import React from 'react';
import { Clock, Users, Flame } from 'lucide-react';
import Link from 'next/link';

interface Recipe {
    id: number;
    name: string;
    pantry_coverage: number;
    missing_ingredients: string[];
    nutrition: {
        calories: number;
        protein: number;
        carbs: number;
        fat: number;
    };
    time_minutes: number;
    servings: number;
    image?: string;
    tags?: string[];
}

interface RecipeCardProps {
    recipe: Recipe;
    onIndianize?: () => void;
}

export const RecipeCard: React.FC<RecipeCardProps> = ({ recipe, onIndianize }) => {
    const coveragePercentage = Math.round(recipe.pantry_coverage * 100);

    return (
        <Link href={`/recipe/${recipe.id}`}>
            <div className="feature-card card-hover cursor-pointer group relative overflow-hidden">
                {/* Recipe Image Placeholder */}
                <div className="relative h-48 rounded-xl overflow-hidden mb-4 bg-gradient-to-br from-neon-pink/20 to-neon-purple/20">
                    <div className="absolute inset-0 flex items-center justify-center text-6xl">
                        🍳
                    </div>
                    {/* Pantry Coverage Badge */}
                    <div className="absolute top-3 right-3 px-3 py-1 rounded-full bg-black/60 backdrop-blur-sm text-white text-sm font-semibold border border-neon-pink/30">
                        {coveragePercentage}% Match
                    </div>
                </div>

                {/* Recipe Name */}
                <h3 className="text-xl font-bold mb-3 text-pink-100 group-hover:gradient-text transition-all">
                    {recipe.name}
                </h3>

                {/* Quick Stats */}
                <div className="flex items-center gap-4 mb-4 text-sm text-pink-200">
                    <div className="flex items-center gap-1">
                        <Clock size={16} />
                        <span>{recipe.time_minutes} min</span>
                    </div>
                    <div className="flex items-center gap-1">
                        <Users size={16} />
                        <span>{recipe.servings} servings</span>
                    </div>
                    <div className="flex items-center gap-1">
                        <Flame size={16} className="text-neon-pink" />
                        <span className="text-neon-pink font-semibold">{recipe.nutrition.calories} cal</span>
                    </div>
                </div>

                {/* Missing Ingredients */}
                {recipe.missing_ingredients.length > 0 && (
                    <div className="mb-4">
                        <p className="text-xs text-pink-300 mb-2">Missing:</p>
                        <div className="flex flex-wrap gap-2">
                            {recipe.missing_ingredients.slice(0, 3).map((ing, idx) => (
                                <span key={idx} className="px-2 py-1 rounded-full bg-pink-500/20 border border-pink-400/40 text-pink-300 text-xs">
                                    {ing}
                                </span>
                            ))}
                            {recipe.missing_ingredients.length > 3 && (
                                <span className="px-2 py-1 rounded-full bg-gray-700/50 text-gray-400 text-xs">
                                    +{recipe.missing_ingredients.length - 3} more
                                </span>
                            )}
                        </div>
                    </div>
                )}

                {/* Nutrition Summary */}
                <div className="grid grid-cols-3 gap-2 mb-4">
                    <NutritionBadge label="Protein" value={`${recipe.nutrition.protein}g`} color="text-neon-green" />
                    <NutritionBadge label="Carbs" value={`${recipe.nutrition.carbs}g`} color="text-neon-blue" />
                    <NutritionBadge label="Fat" value={`${recipe.nutrition.fat}g`} color="text-neon-yellow" />
                </div>

                {/* Indianize Button */}
                {onIndianize && (
                    <button
                        onClick={(e) => {
                            e.preventDefault();
                            onIndianize();
                        }}
                        className="w-full mt-2 px-4 py-2 rounded-full border-2 border-neon-pink/50 text-neon-pink text-sm font-semibold hover:bg-neon-pink/10 transition-all"
                    >
                        🇮🇳 Indianize This Recipe
                    </button>
                )}
            </div>
        </Link>
    );
};

const NutritionBadge: React.FC<{ label: string; value: string; color: string }> = ({ label, value, color }) => (
    <div className="text-center">
        <p className="text-xs text-gray-500 mb-1">{label}</p>
        <p className={`text-sm font-bold ${color}`}>{value}</p>
    </div>
);
