'use client';

import { Button } from '@/components/ui/Button';
import { RecipeCard } from '@/components/features/RecipeCard';
import { Sparkles, Search, Camera, Utensils, TrendingUp, Heart } from 'lucide-react';

// Mock recipe data
const mockRecipes = [
  {
    id: 137739,
    name: "Arriba Baked Winter Squash",
    pantry_coverage: 0.85,
    missing_ingredients: ["squash"],
    nutrition: { calories: 51.5, protein: 2.0, carbs: 13.0, fat: 0.0 },
    time_minutes: 55,
    servings: 4,
  },
  {
    id: 31490,
    name: "Breakfast Pizza",
    pantry_coverage: 0.67,
    missing_ingredients: ["pizza crust", "sausage"],
    nutrition: { calories: 173.4, protein: 22.0, carbs: 17.0, fat: 18.0 },
    time_minutes: 30,
    servings: 6,
  },
];

export default function Home() {
  return (
    <div className="min-h-screen py-12 px-4 relative overflow-hidden">
      {/* Floating Gradient Orbs - Pink Theme */}
      <div className="gradient-orb w-96 h-96 bg-gradient-to-r from-neon-pink to-pink-300 top-20 -left-48" style={{ animationDelay: '0s' }}></div>
      <div className="gradient-orb w-80 h-80 bg-gradient-to-r from-pink-400 to-neon-pink top-1/3 -right-40" style={{ animationDelay: '5s' }}></div>
      <div className="gradient-orb w-72 h-72 bg-gradient-to-r from-neon-pink to-pink-200 bottom-20 left-1/4" style={{ animationDelay: '10s' }}></div>

      {/* Content */}
      <div className="relative z-10">
        {/* Hero Section */}
        <div className="max-w-4xl mx-auto text-center mb-20">
          <div className="inline-block mb-6">
            <div className="text-8xl animate-float">🧙‍♂️</div>
          </div>
          <h1 className="text-7xl font-bold mb-6">
            <span className="gradient-text">Pantry Oracle</span>
          </h1>
          <p className="text-xl text-pink-200 mb-10 max-w-2xl mx-auto leading-relaxed">
            AI-powered bio-nutrient delivery for <span className="text-neon-pink font-semibold">enhanced</span> culinary health
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-wrap justify-center gap-4">
            <button className="px-8 py-4 rounded-full bg-gradient-to-r from-neon-pink to-pink-400 text-white font-semibold hover:scale-105 transition-all shadow-lg">
              Get Started
            </button>
            <button className="px-8 py-4 rounded-full border-2 border-neon-pink text-neon-pink font-semibold hover:bg-neon-pink/10 transition-all">
              View Architecture
            </button>
          </div>
        </div>

        {/* Features */}
        <div className="max-w-6xl mx-auto mb-20">
          <div className="grid md:grid-cols-3 gap-6">
            <FeatureCard
              icon={<Camera className="w-12 h-12" />}
              title="OCR Magic"
              description="Scan your pantry with AI-powered image recognition"
              accent="pink"
            />
            <FeatureCard
              icon={<Utensils className="w-12 h-12" />}
              title="Indianization Engine"
              description="Transform recipes with regional variations"
              accent="blue"
            />
            <FeatureCard
              icon={<TrendingUp className="w-12 h-12" />}
              title="Macro Tracking"
              description="Real-time nutrition and calorie monitoring"
              accent="purple"
            />
          </div>
        </div>

        {/* Sample Recipes */}
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold mb-8 flex items-center gap-3">
            <Sparkles className="text-neon-yellow" size={32} />
            <span className="gradient-text">Trending Recipes</span>
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {mockRecipes.map((recipe) => (
              <RecipeCard key={recipe.id} recipe={recipe} onIndianize={() => alert('Indianization coming soon!')} />
            ))}
          </div>
        </div>

        {/* Footer */}
        <div className="max-w-6xl mx-auto mt-20 text-center">
          <p className="text-gray-500 text-sm">
            © 2036 PANTRY ORACLE LABS. BUILT FOR <span className="gradient-text font-semibold">THE BOLD & BEAUTIFUL</span>
          </p>
        </div>
      </div>
    </div>
  );
}

const FeatureCard: React.FC<{
  icon: React.ReactNode;
  title: string;
  description: string;
  accent: 'pink' | 'blue' | 'purple';
}> = ({ icon, title, description, accent }) => {
  const accentColors = {
    pink: 'text-neon-pink',
    blue: 'text-pink-300',
    purple: 'text-pink-400',
  };

  return (
    <div className="feature-card text-center group">
      <div className={`${accentColors[accent]} mb-4 inline-block group-hover:scale-110 transition-transform`}>
        {icon}
      </div>
      <h3 className="text-xl font-bold mb-3 text-pink-100">{title}</h3>
      <p className="text-pink-200 leading-relaxed">{description}</p>
    </div>
  );
};
