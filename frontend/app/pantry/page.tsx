'use client';

import React, { useState, useEffect } from 'react';
import { PantryInput } from '@/components/features/PantryInput';
import { RecipeCard } from '@/components/features/RecipeCard';
import { Loader2 } from 'lucide-react';
import API_URL from '@/lib/api-config';

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

export default function PantryPage() {
    const [recipes, setRecipes] = useState<Recipe[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [searchPerformed, setSearchPerformed] = useState(false);

    const handleSearch = async (ingredients: string[], maxTime?: number, diet?: string) => {
        setLoading(true);
        setError(null);
        setSearchPerformed(true);

        try {
            const response = await fetch(`${API_URL}/api/recipes/search`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    ingredients,
                    maxTime,
                    diet,
                    page: 1,
                    limit: 20
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to fetch recipes');
            }

            const data = await response.json();
            setRecipes(data.recipes || []);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An error occurred');
            setRecipes([]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen py-12 px-4">
            {/* Floating Gradient Orbs */}
            <div className="gradient-orb w-96 h-96 bg-gradient-to-r from-pink-500/30 to-pink-300/30" style={{ top: '10%', left: '5%' }} />
            <div className="gradient-orb w-80 h-80 bg-gradient-to-r from-pink-400/20 to-pink-200/20" style={{ top: '60%', right: '10%', animationDelay: '2s' }} />

            <div className="relative z-10 max-w-7xl mx-auto space-y-12">
                {/* Pantry Input Section */}
                <PantryInput onSearch={handleSearch} />

                {/* Results Section */}
                {loading && (
                    <div className="flex flex-col items-center justify-center py-20 space-y-4">
                        <Loader2 className="w-12 h-12 text-pink-400 animate-spin" />
                        <p className="text-pink-200 text-lg">Finding perfect recipes for you...</p>
                    </div>
                )}

                {error && (
                    <div className="glass rounded-2xl p-8 text-center">
                        <p className="text-pink-300 text-lg">⚠️ {error}</p>
                        <p className="text-pink-200 mt-2">Make sure the backend server is running on port 5000</p>
                    </div>
                )}

                {!loading && searchPerformed && recipes.length === 0 && !error && (
                    <div className="glass rounded-2xl p-12 text-center space-y-4">
                        <p className="text-3xl">🔍</p>
                        <h3 className="text-2xl font-bold text-pink-100">No recipes found</h3>
                        <p className="text-pink-200">
                            Try adding more common ingredients or adjusting your filters
                        </p>
                    </div>
                )}

                {!loading && recipes.length > 0 && (
                    <div className="space-y-6">
                        <div className="text-center space-y-2">
                            <h2 className="text-3xl font-bold gradient-text">
                                Found {recipes.length} Recipe{recipes.length > 1 ? 's' : ''}
                            </h2>
                            <p className="text-pink-200">
                                Sorted by pantry coverage - recipes you can make with what you have!
                            </p>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {recipes.map((recipe) => (
                                <RecipeCard key={recipe.id} recipe={recipe} />
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
