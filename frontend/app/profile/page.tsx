'use client';

import { useState } from 'react';
import { PantryInput } from '@/components/features/PantryInput';
import { OCRUpload } from '@/components/features/OCRUpload';
import { RecipeCard } from '@/components/features/RecipeCard';
import { MetricsDashboard } from '@/components/features/MetricsDashboard';
import { Loader2, Camera, Edit3, ChefHat, BarChart3, TrendingUp } from 'lucide-react';
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

type TabType = 'input' | 'ocr' | 'recipes' | 'metrics';

export default function ProfilePage() {
    const [activeTab, setActiveTab] = useState<TabType>('input');
    const [ingredients, setIngredients] = useState<string[]>([]);
    const [recipes, setRecipes] = useState<Recipe[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [searchPerformed, setSearchPerformed] = useState(false);

    const handleSearch = async (searchIngredients: string[], maxTime?: number, diet?: string) => {
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
                    ingredients: searchIngredients,
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
            setIngredients(searchIngredients);

            // Switch to recipes tab to show results
            setActiveTab('recipes');
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An error occurred');
            setRecipes([]);
        } finally {
            setLoading(false);
        }
    };

    const handleOCRExtraction = (extractedIngredients: string[]) => {
        // Merge with existing ingredients
        const merged = [...new Set([...ingredients, ...extractedIngredients])];
        setIngredients(merged);
    };

    const tabs = [
        { id: 'input' as TabType, label: 'Manual Input', icon: Edit3 },
        { id: 'ocr' as TabType, label: 'OCR Upload', icon: Camera },
        { id: 'recipes' as TabType, label: 'Recipes', icon: ChefHat, badge: recipes.length },
        { id: 'metrics' as TabType, label: 'Analytics', icon: TrendingUp },
    ];

    return (
        <div className="min-h-screen py-12 px-4">
            {/* Floating Gradient Orbs */}
            <div className="gradient-orb w-96 h-96 bg-gradient-to-r from-pink-500/30 to-pink-300/30" style={{ top: '10%', left: '5%' }} />
            <div className="gradient-orb w-80 h-80 bg-gradient-to-r from-pink-400/20 to-pink-200/20" style={{ top: '60%', right: '10%', animationDelay: '2s' }} />

            <div className="relative z-10 max-w-7xl mx-auto space-y-8">
                {/* Header */}
                <div className="text-center space-y-2">
                    <h1 className="text-5xl font-bold gradient-text">Your Pantry Profile</h1>
                    <p className="text-pink-200 text-lg">
                        Manage your ingredients, discover recipes, and track your nutrition
                    </p>
                </div>

                {/* Tab Navigation */}
                <div className="glass rounded-2xl p-2">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                        {tabs.map((tab) => {
                            const Icon = tab.icon;
                            const isActive = activeTab === tab.id;

                            return (
                                <button
                                    key={tab.id}
                                    onClick={() => setActiveTab(tab.id)}
                                    className={`relative px-6 py-4 rounded-xl font-semibold transition-all ${isActive
                                        ? 'bg-gradient-to-r from-pink-500 to-pink-400 text-white shadow-lg shadow-pink-500/50'
                                        : 'bg-pink-950/30 text-pink-200 hover:bg-pink-950/50 hover:text-pink-100'
                                        }`}
                                >
                                    <div className="flex items-center justify-center gap-2">
                                        <Icon className="w-5 h-5" />
                                        <span className="hidden sm:inline">{tab.label}</span>
                                        {tab.badge !== undefined && tab.badge > 0 && (
                                            <span className={`px-2 py-0.5 rounded-full text-xs font-bold ${isActive ? 'bg-white text-pink-500' : 'bg-pink-500 text-white'
                                                }`}>
                                                {tab.badge}
                                            </span>
                                        )}
                                    </div>
                                </button>
                            );
                        })}
                    </div>
                </div>

                {/* Tab Content */}
                <div className="min-h-[600px]">
                    {/* Manual Input Tab */}
                    {activeTab === 'input' && (
                        <div className="animate-fadeIn">
                            <PantryInput onSearch={handleSearch} />
                        </div>
                    )}

                    {/* OCR Upload Tab */}
                    {activeTab === 'ocr' && (
                        <div className="animate-fadeIn">
                            <OCRUpload onIngredientsExtracted={handleOCRExtraction} />

                            {/* Show extracted ingredients */}
                            {ingredients.length > 0 && (
                                <div className="mt-6 glass rounded-2xl p-6 space-y-4">
                                    <h3 className="text-xl font-semibold text-pink-100">
                                        Your Ingredients ({ingredients.length})
                                    </h3>
                                    <div className="flex flex-wrap gap-2">
                                        {ingredients.map((ingredient, index) => (
                                            <div
                                                key={index}
                                                className="px-4 py-2 bg-gradient-to-r from-pink-500/20 to-pink-400/20 border border-pink-400/30 rounded-full text-pink-100"
                                            >
                                                {ingredient}
                                            </div>
                                        ))}
                                    </div>
                                    <button
                                        onClick={() => {
                                            // Use current ingredients for search
                                            handleSearch(ingredients);
                                        }}
                                        className="w-full py-3 rounded-xl bg-gradient-to-r from-pink-500 to-pink-400 text-white font-semibold hover:shadow-lg hover:shadow-pink-500/50 transition-all"
                                    >
                                        Find Recipes with These Ingredients
                                    </button>
                                </div>
                            )}
                        </div>
                    )}

                    {/* Recipes Tab */}
                    {activeTab === 'recipes' && (
                        <div className="animate-fadeIn space-y-6">
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
                                        Try adding ingredients using the Manual Input or OCR Upload tabs
                                    </p>
                                    <div className="flex gap-4 justify-center">
                                        <button
                                            onClick={() => setActiveTab('input')}
                                            className="px-6 py-3 bg-gradient-to-r from-pink-500 to-pink-400 rounded-lg text-white font-semibold hover:shadow-lg hover:shadow-pink-500/50 transition-all"
                                        >
                                            Manual Input
                                        </button>
                                        <button
                                            onClick={() => setActiveTab('ocr')}
                                            className="px-6 py-3 bg-pink-950/30 border border-pink-400/30 rounded-lg text-pink-100 font-semibold hover:bg-pink-950/50 transition-all"
                                        >
                                            OCR Upload
                                        </button>
                                    </div>
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
                                        {ingredients.length > 0 && (
                                            <div className="flex flex-wrap gap-2 justify-center mt-4">
                                                <span className="text-pink-300">Using ingredients:</span>
                                                {ingredients.slice(0, 5).map((ing, i) => (
                                                    <span key={i} className="px-3 py-1 bg-pink-500/20 rounded-full text-pink-100 text-sm">
                                                        {ing}
                                                    </span>
                                                ))}
                                                {ingredients.length > 5 && (
                                                    <span className="px-3 py-1 bg-pink-500/20 rounded-full text-pink-100 text-sm">
                                                        +{ingredients.length - 5} more
                                                    </span>
                                                )}
                                            </div>
                                        )}
                                    </div>

                                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                        {recipes.map((recipe) => (
                                            <RecipeCard key={recipe.id} recipe={recipe} />
                                        ))}
                                    </div>
                                </div>
                            )}

                            {!loading && !searchPerformed && (
                                <div className="glass rounded-2xl p-12 text-center space-y-4">
                                    <p className="text-3xl">👨‍🍳</p>
                                    <h3 className="text-2xl font-bold text-pink-100">Ready to Cook?</h3>
                                    <p className="text-pink-200">
                                        Add your ingredients to discover amazing recipes
                                    </p>
                                    <div className="flex gap-4 justify-center">
                                        <button
                                            onClick={() => setActiveTab('input')}
                                            className="px-6 py-3 bg-gradient-to-r from-pink-500 to-pink-400 rounded-lg text-white font-semibold hover:shadow-lg hover:shadow-pink-500/50 transition-all"
                                        >
                                            Get Started
                                        </button>
                                    </div>
                                </div>
                            )}
                        </div>
                    )}

                    {/* Metrics Tab */}
                    {activeTab === 'metrics' && (
                        <div className="animate-fadeIn">
                            <MetricsDashboard />
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
