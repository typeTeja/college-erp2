'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { odcService } from '@/utils/odc-service';

interface FeedbackFormProps {
    applicationId: number;
    onSuccess?: () => void;
}

export default function FeedbackForm({ applicationId, onSuccess }: FeedbackFormProps) {
    const [rating, setRating] = useState(0);
    const [feedback, setFeedback] = useState('');
    const [submitting, setSubmitting] = useState(false);
    const [hoveredRating, setHoveredRating] = useState(0);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (rating === 0) {
            alert('Please select a rating');
            return;
        }

        if (!feedback.trim()) {
            alert('Please provide feedback');
            return;
        }

        setSubmitting(true);
        try {
            await odcService.submitStudentFeedback(applicationId, {
                student_rating: rating,
                student_feedback: feedback
            });

            alert('Feedback submitted successfully!');
            setRating(0);
            setFeedback('');
            if (onSuccess) onSuccess();
        } catch (error: any) {
            console.error('Error submitting feedback:', error);
            alert(error.response?.data?.detail || 'Failed to submit feedback');
        } finally {
            setSubmitting(false);
        }
    };

    const renderStars = () => {
        return (
            <div className="flex gap-2">
                {[1, 2, 3, 4, 5].map((star) => (
                    <button
                        key={star}
                        type="button"
                        onClick={() => setRating(star)}
                        onMouseEnter={() => setHoveredRating(star)}
                        onMouseLeave={() => setHoveredRating(0)}
                        className="text-3xl focus:outline-none transition-transform hover:scale-110"
                    >
                        {star <= (hoveredRating || rating) ? (
                            <span className="text-yellow-400">★</span>
                        ) : (
                            <span className="text-gray-300">★</span>
                        )}
                    </button>
                ))}
            </div>
        );
    };

    return (
        <Card>
            <CardHeader>
                <h3 className="text-lg font-medium">Submit Your Feedback</h3>
            </CardHeader>
            <CardContent>
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Rating
                        </label>
                        {renderStars()}
                        {rating > 0 && (
                            <p className="text-sm text-gray-500 mt-1">
                                You rated: {rating} star{rating !== 1 ? 's' : ''}
                            </p>
                        )}
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Your Feedback
                        </label>
                        <textarea
                            value={feedback}
                            onChange={(e) => setFeedback(e.target.value)}
                            rows={4}
                            className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="Share your experience with this ODC event..."
                            required
                        />
                    </div>

                    <Button type="submit" disabled={submitting} className="w-full">
                        {submitting ? 'Submitting...' : 'Submit Feedback'}
                    </Button>
                </form>
            </CardContent>
        </Card>
    );
}
