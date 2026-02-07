'use client';

import React, { useState, useCallback } from 'react';
import { Upload, X, Camera, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import API_URL from '@/lib/api-config';

interface OCRUploadProps {
    onIngredientsExtracted: (ingredients: string[]) => void;
}

interface OCRResult {
    ingredients: string[];
    raw_text: string;
    confidence: number;
    language_detected: string;
}

export const OCRUpload: React.FC<OCRUploadProps> = ({ onIngredientsExtracted }) => {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [preview, setPreview] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<OCRResult | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [dragActive, setDragActive] = useState(false);

    const handleDrag = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    }, []);

    const handleDrop = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0]);
        }
    }, []);

    const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            handleFile(e.target.files[0]);
        }
    };

    const handleFile = (file: File) => {
        // Validate file type
        const validTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/bmp', 'image/webp'];
        if (!validTypes.includes(file.type)) {
            setError('Please upload a valid image file (PNG, JPG, GIF, BMP, or WebP)');
            return;
        }

        // Validate file size (max 10MB)
        if (file.size > 10 * 1024 * 1024) {
            setError('File size must be less than 10MB');
            return;
        }

        setSelectedFile(file);
        setError(null);
        setResult(null);

        // Create preview
        const reader = new FileReader();
        reader.onloadend = () => {
            setPreview(reader.result as string);
        };
        reader.readAsDataURL(file);
    };

    const handleUpload = async () => {
        if (!selectedFile) return;

        setLoading(true);
        setError(null);

        try {
            const formData = new FormData();
            formData.append('image', selectedFile);

            const response = await fetch(`${API_URL}/api/ocr/scan`, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error('Failed to process image');
            }

            const data: OCRResult = await response.json();
            setResult(data);

            // Pass ingredients to parent component
            if (data.ingredients && data.ingredients.length > 0) {
                onIngredientsExtracted(data.ingredients);
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An error occurred');
        } finally {
            setLoading(false);
        }
    };

    const handleReset = () => {
        setSelectedFile(null);
        setPreview(null);
        setResult(null);
        setError(null);
    };

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="text-center space-y-2">
                <h2 className="text-3xl font-bold gradient-text flex items-center justify-center gap-2">
                    <Camera className="w-8 h-8" />
                    OCR Pantry Scanner
                </h2>
                <p className="text-pink-200">
                    Upload an image of your pantry or ingredient list
                </p>
            </div>

            {/* Upload Area */}
            {!selectedFile ? (
                <div
                    className={`glass rounded-2xl p-12 border-2 border-dashed transition-all ${dragActive
                        ? 'border-pink-400 bg-pink-500/10'
                        : 'border-pink-400/30 hover:border-pink-400/50'
                        }`}
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                >
                    <div className="text-center space-y-4">
                        <div className="inline-block p-6 bg-pink-500/20 rounded-full">
                            <Upload className="w-12 h-12 text-pink-300" />
                        </div>
                        <div>
                            <p className="text-xl text-pink-100 font-semibold mb-2">
                                Drag & drop your image here
                            </p>
                            <p className="text-pink-300 mb-4">or</p>
                            <label className="inline-block px-6 py-3 bg-gradient-to-r from-pink-500 to-pink-400 rounded-lg text-white font-semibold cursor-pointer hover:shadow-lg hover:shadow-pink-500/50 transition-all">
                                Browse Files
                                <input
                                    type="file"
                                    className="hidden"
                                    accept="image/*"
                                    onChange={handleFileInput}
                                />
                            </label>
                        </div>
                        <p className="text-pink-300 text-sm">
                            Supports: PNG, JPG, GIF, BMP, WebP (Max 10MB)
                        </p>
                    </div>
                </div>
            ) : (
                <div className="glass rounded-2xl p-6 space-y-4">
                    {/* Preview */}
                    <div className="relative">
                        <img
                            src={preview || ''}
                            alt="Preview"
                            className="w-full max-h-96 object-contain rounded-xl"
                        />
                        <button
                            onClick={handleReset}
                            className="absolute top-2 right-2 p-2 bg-pink-950/80 rounded-full hover:bg-pink-900 transition-colors"
                        >
                            <X className="w-5 h-5 text-pink-100" />
                        </button>
                    </div>

                    {/* File Info */}
                    <div className="flex items-center justify-between text-pink-200">
                        <span className="truncate">{selectedFile.name}</span>
                        <span className="text-pink-300 text-sm">
                            {(selectedFile.size / 1024).toFixed(1)} KB
                        </span>
                    </div>

                    {/* Upload Button */}
                    <button
                        onClick={handleUpload}
                        disabled={loading}
                        className={`w-full py-3 rounded-xl font-semibold transition-all ${loading
                            ? 'bg-pink-950/30 text-pink-400/50 cursor-not-allowed'
                            : 'bg-gradient-to-r from-pink-500 to-pink-400 text-white hover:shadow-lg hover:shadow-pink-500/50'
                            }`}
                    >
                        {loading ? (
                            <span className="flex items-center justify-center gap-2">
                                <Loader2 className="w-5 h-5 animate-spin" />
                                Processing...
                            </span>
                        ) : (
                            'Extract Ingredients'
                        )}
                    </button>
                </div>
            )}

            {/* Error Message */}
            {error && (
                <div className="glass rounded-xl p-4 border border-red-400/30 bg-red-500/10">
                    <div className="flex items-center gap-2 text-red-300">
                        <AlertCircle className="w-5 h-5" />
                        <p>{error}</p>
                    </div>
                </div>
            )}

            {/* Results */}
            {result && (
                <div className="glass rounded-2xl p-6 space-y-4">
                    <div className="flex items-center gap-2 text-green-400">
                        <CheckCircle className="w-6 h-6" />
                        <h3 className="text-xl font-semibold">Extraction Complete!</h3>
                    </div>

                    {/* Confidence Score */}
                    <div className="space-y-2">
                        <div className="flex items-center justify-between text-sm">
                            <span className="text-pink-300">Confidence</span>
                            <span className="text-pink-100 font-semibold">
                                {(result.confidence * 100).toFixed(1)}%
                            </span>
                        </div>
                        <div className="h-2 bg-pink-950/30 rounded-full overflow-hidden">
                            <div
                                className="h-full bg-gradient-to-r from-pink-500 to-pink-400"
                                style={{ width: `${result.confidence * 100}%` }}
                            />
                        </div>
                    </div>

                    {/* Extracted Ingredients */}
                    {result.ingredients.length > 0 ? (
                        <div className="space-y-2">
                            <h4 className="text-pink-200 font-semibold">
                                Extracted Ingredients ({result.ingredients.length})
                            </h4>
                            <div className="flex flex-wrap gap-2">
                                {result.ingredients.map((ingredient, index) => (
                                    <div
                                        key={index}
                                        className="px-4 py-2 bg-gradient-to-r from-pink-500/20 to-pink-400/20 border border-pink-400/30 rounded-full text-pink-100"
                                    >
                                        {ingredient}
                                    </div>
                                ))}
                            </div>
                        </div>
                    ) : (
                        <div className="text-center py-4 text-pink-300">
                            No ingredients detected. Try a clearer image or add ingredients manually.
                        </div>
                    )}

                    {/* Raw Text (Collapsible) */}
                    {result.raw_text && (
                        <details className="space-y-2">
                            <summary className="text-pink-300 cursor-pointer hover:text-pink-200">
                                View Raw OCR Text
                            </summary>
                            <div className="mt-2 p-4 bg-pink-950/30 rounded-lg text-pink-200 text-sm font-mono whitespace-pre-wrap max-h-40 overflow-y-auto">
                                {result.raw_text}
                            </div>
                        </details>
                    )}
                </div>
            )}
        </div>
    );
};
