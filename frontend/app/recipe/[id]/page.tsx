'use client';

import { RecipeDetail } from '@/components/features/RecipeDetail';
import { useParams } from 'next/navigation';
import { useEffect, useState } from 'react';
import { Loader2 } from 'lucide-react';
import API_URL from '@/lib/api-config';

interface Recipe {
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
}

export default function RecipePage() {
    const params = useParams();
    const recipeId = params.id as string;

    const [recipe, setRecipe] = useState<Recipe | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchRecipe = async () => {
            try {
                setLoading(true);
                setError(null);

                const response = await fetch(`${API_URL}/api/recipes/${recipeId}`);

                if (!response.ok) {
                    throw new Error('Recipe not found');
                }

                const data = await response.json();
                setRecipe(data);
            } catch (err) {
                setError(err instanceof Error ? err.message : 'Failed to load recipe');
            } finally {
                setLoading(false);
            }
        };

        if (recipeId) {
            fetchRecipe();
        }
    }, [recipeId]);

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-center space-y-4">
                    <Loader2 className="w-12 h-12 text-pink-400 animate-spin mx-auto" />
                    <p className="text-pink-200 text-lg">Loading recipe...</p>
                </div>
            </div>
        );
    }

    if (error || !recipe) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="glass rounded-2xl p-12 text-center max-w-md">
                    <p className="text-3xl mb-4">😕</p>
                    <h2 className="text-2xl font-bold text-pink-100 mb-2">Recipe Not Found</h2>
                    <p className="text-pink-300 mb-6">{error || 'The recipe you\'re looking for doesn\'t exist.'}</p>
                    <a
                        href="/profile"
                        className="inline-block px-6 py-3 bg-gradient-to-r from-pink-500 to-pink-400 rounded-lg text-white font-semibold hover:shadow-lg hover:shadow-pink-500/50 transition-all"
                    >
                        Back to Profile
                    </a>
                </div>
            </div>
        );
    }

    return (
        <div className="py-8">
            <RecipeDetail recipe={recipe} />
        </div>
    );
}
