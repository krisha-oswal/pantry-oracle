'use client';

import React, { useState } from 'react';
import { X, Plus, Search } from 'lucide-react';

interface PantryInputProps {
    onSearch: (ingredients: string[], maxTime?: number, diet?: string) => void;
}

export const PantryInput: React.FC<PantryInputProps> = ({ onSearch }) => {
    const [ingredients, setIngredients] = useState<string[]>([]);
    const [inputValue, setInputValue] = useState('');
    const [maxTime, setMaxTime] = useState<number>(60);
    const [diet, setDiet] = useState<string>('');
    const [showSuggestions, setShowSuggestions] = useState(false);

    // Common ingredients for autocomplete
    const commonIngredients = [
        'tomato', 'onion', 'garlic', 'ginger', 'potato', 'carrot',
        'chicken', 'beef', 'pork', 'fish', 'egg', 'milk', 'butter',
        'cheese', 'yogurt', 'cream', 'rice', 'pasta', 'bread',
        'spinach', 'broccoli', 'cauliflower', 'bell pepper', 'cucumber',
        'lemon', 'lime', 'cilantro', 'basil', 'oregano', 'cumin',
        'turmeric', 'coriander', 'chili', 'salt', 'pepper', 'oil'
    ];

    const filteredSuggestions = commonIngredients.filter(
        ing => ing.toLowerCase().includes(inputValue.toLowerCase()) &&
            !ingredients.includes(ing)
    );

    const addIngredient = (ingredient: string) => {
        if (ingredient.trim() && !ingredients.includes(ingredient.trim())) {
            setIngredients([...ingredients, ingredient.trim()]);
            setInputValue('');
            setShowSuggestions(false);
        }
    };

    const removeIngredient = (ingredient: string) => {
        setIngredients(ingredients.filter(i => i !== ingredient));
    };

    const handleSearch = () => {
        if (ingredients.length > 0) {
            onSearch(ingredients, maxTime, diet || undefined);
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter') {
            if (filteredSuggestions.length > 0) {
                addIngredient(filteredSuggestions[0]);
            } else {
                addIngredient(inputValue);
            }
        }
    };

    return (
        <div className="w-full max-w-4xl mx-auto space-y-6">
            {/* Header */}
            <div className="text-center space-y-2">
                <h1 className="text-4xl font-bold gradient-text">
                    What's in Your Pantry?
                </h1>
                <p className="text-pink-200">
                    Add your ingredients and we'll find the perfect recipes for you
                </p>
            </div>

            {/* Ingredient Input */}
            <div className="glass rounded-2xl p-6 space-y-4">
                <div className="relative">
                    <div className="flex items-center gap-2 bg-pink-950/30 rounded-xl px-4 py-3 border border-pink-400/20">
                        <Search className="w-5 h-5 text-pink-300" />
                        <input
                            type="text"
                            value={inputValue}
                            onChange={(e) => {
                                setInputValue(e.target.value);
                                setShowSuggestions(true);
                            }}
                            onKeyPress={handleKeyPress}
                            onFocus={() => setShowSuggestions(true)}
                            placeholder="Type an ingredient (e.g., tomato, chicken, rice)..."
                            className="flex-1 bg-transparent text-pink-100 placeholder-pink-300/50 outline-none"
                        />
                        <button
                            onClick={() => addIngredient(inputValue)}
                            className="px-4 py-2 bg-gradient-to-r from-pink-500 to-pink-400 rounded-lg text-white font-semibold hover:shadow-lg hover:shadow-pink-500/50 transition-all"
                        >
                            <Plus className="w-5 h-5" />
                        </button>
                    </div>

                    {/* Autocomplete Suggestions */}
                    {showSuggestions && inputValue && filteredSuggestions.length > 0 && (
                        <div className="absolute top-full left-0 right-0 mt-2 glass rounded-xl overflow-hidden z-10 max-h-60 overflow-y-auto">
                            {filteredSuggestions.slice(0, 8).map((suggestion) => (
                                <button
                                    key={suggestion}
                                    onClick={() => addIngredient(suggestion)}
                                    className="w-full px-4 py-3 text-left text-pink-100 hover:bg-pink-500/20 transition-colors border-b border-pink-400/10 last:border-0"
                                >
                                    {suggestion}
                                </button>
                            ))}
                        </div>
                    )}
                </div>

                {/* Ingredient Tags */}
                {ingredients.length > 0 && (
                    <div className="flex flex-wrap gap-2">
                        {ingredients.map((ingredient) => (
                            <div
                                key={ingredient}
                                className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-pink-500/20 to-pink-400/20 border border-pink-400/30 rounded-full text-pink-100"
                            >
                                <span>{ingredient}</span>
                                <button
                                    onClick={() => removeIngredient(ingredient)}
                                    className="hover:text-pink-300 transition-colors"
                                >
                                    <X className="w-4 h-4" />
                                </button>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {/* Filters */}
            <div className="glass rounded-2xl p-6 space-y-4">
                <h3 className="text-xl font-semibold text-pink-100">Preferences</h3>

                {/* Max Cooking Time */}
                <div className="space-y-2">
                    <label className="flex items-center justify-between text-pink-200">
                        <span>Max Cooking Time</span>
                        <span className="text-pink-300 font-semibold">{maxTime} minutes</span>
                    </label>
                    <input
                        type="range"
                        min="10"
                        max="180"
                        step="10"
                        value={maxTime}
                        onChange={(e) => setMaxTime(Number(e.target.value))}
                        className="w-full h-2 bg-pink-950/30 rounded-lg appearance-none cursor-pointer accent-pink-400"
                    />
                </div>

                {/* Dietary Preferences */}
                <div className="space-y-2">
                    <label className="text-pink-200">Dietary Preference</label>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                        {['', 'vegetarian', 'vegan', 'gluten-free'].map((option) => (
                            <button
                                key={option}
                                onClick={() => setDiet(option)}
                                className={`px-4 py-2 rounded-lg font-semibold transition-all ${diet === option
                                        ? 'bg-gradient-to-r from-pink-500 to-pink-400 text-white shadow-lg shadow-pink-500/50'
                                        : 'bg-pink-950/30 text-pink-200 border border-pink-400/20 hover:border-pink-400/40'
                                    }`}
                            >
                                {option || 'Any'}
                            </button>
                        ))}
                    </div>
                </div>
            </div>

            {/* Search Button */}
            <button
                onClick={handleSearch}
                disabled={ingredients.length === 0}
                className={`w-full py-4 rounded-xl font-bold text-lg transition-all ${ingredients.length > 0
                        ? 'bg-gradient-to-r from-pink-500 to-pink-400 text-white hover:shadow-2xl hover:shadow-pink-500/50 hover:scale-[1.02]'
                        : 'bg-pink-950/30 text-pink-400/50 cursor-not-allowed'
                    }`}
            >
                {ingredients.length > 0
                    ? `Find Recipes with ${ingredients.length} Ingredient${ingredients.length > 1 ? 's' : ''}`
                    : 'Add ingredients to search'}
            </button>
        </div>
    );
};
