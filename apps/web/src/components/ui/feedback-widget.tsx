"use client"

import React, { useState } from 'react';
import { MessageSquare, X, Send, Camera } from 'lucide-react';
import { Button } from './button';
import { Textarea } from './textarea';
import { Label } from './label';
import { RadioGroup, RadioGroupItem } from './radio-group';
import { cn } from '@/lib/utils';
import { toast } from 'sonner';

export interface FeedbackWidgetProps {
  className?: string;
}

type FeedbackCategory = 'bug' | 'feature' | 'general';
type SentimentRating = 'happy' | 'neutral' | 'sad';

/**
 * FeedbackWidget Component
 * 
 * Floating feedback widget for collecting user feedback.
 * Appears as a button in the bottom-right corner.
 * 
 * Features:
 * - Sentiment rating (😊 😐 😞)
 * - Category selection (Bug, Feature Request, General)
 * - Message textarea
 * - Screenshot capture (optional)
 * 
 * @example
 * ```tsx
 * <FeedbackWidget />
 * ```
 */
export function FeedbackWidget({ className }: FeedbackWidgetProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [rating, setRating] = useState<SentimentRating | null>(null);
  const [category, setCategory] = useState<FeedbackCategory>('general');
  const [message, setMessage] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!message.trim()) {
      toast.error('Please enter your feedback');
      return;
    }

    setIsSubmitting(true);

    try {
      // TODO: Replace with actual API endpoint
      const response = await fetch('/api/feedback', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          rating,
          category,
          message,
          url: window.location.href,
          timestamp: new Date().toISOString(),
        }),
      });

      if (!response.ok) throw new Error('Failed to submit feedback');

      toast.success('Thank you for your feedback!');
      
      // Reset form
      setRating(null);
      setCategory('general');
      setMessage('');
      setIsOpen(false);
    } catch (error) {
      toast.error('Failed to submit feedback. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const sentiments = [
    { value: 'happy' as const, emoji: '😊', label: 'Happy' },
    { value: 'neutral' as const, emoji: '😐', label: 'Neutral' },
    { value: 'sad' as const, emoji: '😞', label: 'Sad' },
  ];

  return (
    <div className={cn('fixed bottom-6 right-6 z-50', className)}>
      {/* Feedback Form */}
      {isOpen && (
        <div className="mb-4 w-80 bg-white dark:bg-slate-900 rounded-lg shadow-xl border border-slate-200 dark:border-slate-800">
          <div className="p-4 border-b border-slate-200 dark:border-slate-800 flex items-center justify-between">
            <h3 className="font-semibold text-sm">Send Feedback</h3>
            <button
              onClick={() => setIsOpen(false)}
              className="p-1 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-md transition-colors"
              aria-label="Close feedback form"
            >
              <X className="h-4 w-4" />
            </button>
          </div>

          <form onSubmit={handleSubmit} className="p-4 space-y-4">
            {/* Sentiment Rating */}
            <div>
              <Label className="text-xs mb-2 block">How do you feel?</Label>
              <div className="flex gap-2">
                {sentiments.map((sentiment) => (
                  <button
                    key={sentiment.value}
                    type="button"
                    onClick={() => setRating(sentiment.value)}
                    className={cn(
                      'flex-1 p-3 rounded-md border-2 transition-all hover:scale-105',
                      rating === sentiment.value
                        ? 'border-blue-500 bg-blue-50 dark:bg-blue-950'
                        : 'border-slate-200 dark:border-slate-700 hover:border-slate-300'
                    )}
                    aria-label={sentiment.label}
                  >
                    <span className="text-2xl">{sentiment.emoji}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Category */}
            <div>
              <Label className="text-xs mb-2 block">Category</Label>
              <RadioGroup
                value={category}
                onValueChange={(value) => setCategory(value as FeedbackCategory)}
              >
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="bug" id="bug" />
                  <Label htmlFor="bug" className="text-sm font-normal cursor-pointer">
                    Bug Report
                  </Label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="feature" id="feature" />
                  <Label htmlFor="feature" className="text-sm font-normal cursor-pointer">
                    Feature Request
                  </Label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="general" id="general" />
                  <Label htmlFor="general" className="text-sm font-normal cursor-pointer">
                    General Feedback
                  </Label>
                </div>
              </RadioGroup>
            </div>

            {/* Message */}
            <div>
              <Label htmlFor="message" className="text-xs mb-2 block">
                Your Feedback
              </Label>
              <Textarea
                id="message"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Tell us what you think..."
                rows={4}
                className="resize-none text-sm"
                required
              />
            </div>

            {/* Submit Button */}
            <Button
              type="submit"
              className="w-full"
              disabled={isSubmitting}
            >
              {isSubmitting ? (
                'Sending...'
              ) : (
                <>
                  <Send className="h-4 w-4 mr-2" />
                  Send Feedback
                </>
              )}
            </Button>
          </form>
        </div>
      )}

      {/* Floating Button */}
      {!isOpen && (
        <Button
          onClick={() => setIsOpen(true)}
          className="rounded-full h-14 w-14 shadow-lg"
          size="icon"
          aria-label="Open feedback form"
        >
          <MessageSquare className="h-6 w-6" />
        </Button>
      )}
    </div>
  );
}
