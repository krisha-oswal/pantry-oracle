'use client';

import React from 'react';
import { Clock, Users, Flame, ChefHat, ListChecks } from 'lucide-react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

interface RecipeDetailProps {
    recipe: {
        id: number;
        name: string;
        description?: string;
        ingredients: string[];
        steps: string[];
        nutrition: {
            calories: number;
            protein: number;
            carbs: number;
            fat: number;
        };
        time_minutes: number;
        servings: number;
        tags?: string[];
    };
}

export const RecipeDetail: React.FC<RecipeDetailProps> = ({ recipe }) => {
    const nutritionData = [
        { name: 'Protein', value: recipe.nutrition.protein, color: '#7FFF9F' },
        { name: 'Carbs', value: recipe.nutrition.carbs, color: '#60D5FF' },
        { name: 'Fat', value: recipe.nutrition.fat, color: '#FFE66D' },
    ];

    return (
        <div className="max-w-6xl mx-auto p-6 space-y-8">
            {/* Header */}
            <div className="glass-card">
                <div className="flex items-start justify-between mb-4">
                    <div>
                        <h1 className="text-4xl font-bold gradient-text mb-2">{recipe.name}</h1>
                        {recipe.description && (
                            <p className="text-gray-600 dark:text-gray-400">{recipe.description}</p>
                        )}
                    </div>
                    <div className="text-6xl animate-float">🍳</div>
                </div>

                {/* Quick Stats */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
                    <StatCard icon={Clock} label="Cook Time" value={`${recipe.time_minutes} min`} />
                    <StatCard icon={Users} label="Servings" value={recipe.servings.toString()} />
                    <StatCard icon={Flame} label="Calories" value={`${recipe.nutrition.calories}`} color="neon-orange" />
                    <StatCard icon={ChefHat} label="Difficulty" value="Medium" />
                </div>

                {/* Tags */}
                {recipe.tags && recipe.tags.length > 0 && (
                    <div className="flex flex-wrap gap-2 mt-4">
                        {recipe.tags.slice(0, 6).map((tag, idx) => (
                            <span key={idx} className="px-3 py-1 rounded-full bg-gradient-neon text-white text-sm">
                                {tag}
                            </span>
                        ))}
                    </div>
                )}
            </div>

            <div className="grid md:grid-cols-3 gap-6">
                {/* Ingredients */}
                <div className="md:col-span-1 glass-card">
                    <div className="flex items-center gap-2 mb-6">
                        <ListChecks className="text-neon-purple" size={24} />
                        <h2 className="text-2xl font-bold">Ingredients</h2>
                    </div>
                    <ul className="space-y-3">
                        {recipe.ingredients.map((ingredient, idx) => (
                            <li key={idx} className="flex items-start gap-3">
                                <span className="text-neon-pink mt-1 text-lg">•</span>
                                <span className="flex-1 text-base leading-relaxed">{ingredient}</span>
                            </li>
                        ))}
                    </ul>
                </div>

                {/* Steps & Nutrition */}
                <div className="md:col-span-2 space-y-6">
                    {/* Cooking Steps */}
                    <div className="glass-card">
                        <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
                            <ChefHat className="text-neon-blue" size={24} />
                            Cooking Steps
                        </h2>
                        <ol className="space-y-6">
                            {recipe.steps.map((step, idx) => (
                                <li key={idx} className="flex gap-4 pb-6 border-b border-white/10 last:border-b-0 last:pb-0">
                                    <div className="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-neon flex items-center justify-center text-white font-bold text-lg shadow-lg">
                                        {idx + 1}
                                    </div>
                                    <p className="flex-1 pt-2 text-base leading-relaxed text-gray-700 dark:text-gray-300">
                                        {step}
                                    </p>
                                </li>
                            ))}
                        </ol>
                    </div>

                    {/* Nutrition Chart */}
                    <div className="glass-card">
                        <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
                            <Flame className="text-neon-orange" size={24} />
                            Nutrition Breakdown
                        </h2>

                        <div className="grid md:grid-cols-2 gap-6">
                            {/* Pie Chart */}
                            <div className="h-64">
                                <ResponsiveContainer width="100%" height="100%">
                                    <PieChart>
                                        <Pie
                                            data={nutritionData}
                                            cx="50%"
                                            cy="50%"
                                            labelLine={false}
                                            label={({ name, value }) => `${name}: ${value}g`}
                                            outerRadius={80}
                                            fill="#8884d8"
                                            dataKey="value"
                                        >
                                            {nutritionData.map((entry, index) => (
                                                <Cell key={`cell-${index}`} fill={entry.color} />
                                            ))}
                                        </Pie>
                                        <Tooltip />
                                    </PieChart>
                                </ResponsiveContainer>
                            </div>

                            {/* Nutrition Details */}
                            <div className="space-y-4">
                                <NutritionRow label="Total Calories" value={`${recipe.nutrition.calories} kcal`} />
                                <NutritionRow label="Protein" value={`${recipe.nutrition.protein}g`} color="neon-green" />
                                <NutritionRow label="Carbohydrates" value={`${recipe.nutrition.carbs}g`} color="neon-blue" />
                                <NutritionRow label="Fat" value={`${recipe.nutrition.fat}g`} color="neon-yellow" />

                                <div className="pt-4 border-t border-white/20">
                                    <p className="text-sm text-gray-500 dark:text-gray-400">Per Serving</p>
                                    <p className="text-2xl font-bold gradient-text">
                                        {Math.round(recipe.nutrition.calories / recipe.servings)} cal
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

const StatCard: React.FC<{ icon: any; label: string; value: string; color?: string }> = ({
    icon: Icon,
    label,
    value,
    color = 'neon-purple'
}) => (
    <div className="text-center p-4 rounded-xl bg-white/5 dark:bg-white/5 border border-white/10">
        <Icon className={`text-${color} mx-auto mb-2`} size={24} />
        <p className="text-sm text-gray-500 dark:text-gray-400">{label}</p>
        <p className="text-xl font-bold">{value}</p>
    </div>
);

const NutritionRow: React.FC<{ label: string; value: string; color?: string }> = ({
    label,
    value,
    color
}) => (
    <div className="flex justify-between items-center">
        <span className="text-gray-600 dark:text-gray-400">{label}</span>
        <span className={`font-bold ${color ? `text-${color}` : ''}`}>{value}</span>
    </div>
);
