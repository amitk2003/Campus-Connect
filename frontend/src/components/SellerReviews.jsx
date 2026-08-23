import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { X, Star, MessageSquare, Send, User, AlertCircle } from 'lucide-react';

const backendUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000';

/* ── Helper: render 5 stars ─────────────────────────────────────────── */
function StarDisplay({ rating, size = 'sm' }) {
  const sizeClass = size === 'lg' ? 'w-6 h-6' : 'w-4 h-4';
  return (
    <span className="flex items-center gap-0.5">
      {[1, 2, 3, 4, 5].map((star) => (
        <Star
          key={star}
          className={`${sizeClass} ${
            star <= Math.round(rating)
              ? 'text-amber-400 fill-amber-400'
              : 'text-slate-300 dark:text-slate-600'
          }`}
        />
      ))}
    </span>
  );
}

/* ── Interactive star picker ─────────────────────────────────────────── */
function StarPicker({ value, onChange }) {
  const [hovered, setHovered] = useState(0);
  return (
    <div className="flex gap-1">
      {[1, 2, 3, 4, 5].map((star) => (
        <button
          key={star}
          type="button"
          onMouseEnter={() => setHovered(star)}
          onMouseLeave={() => setHovered(0)}
          onClick={() => onChange(star)}
          className="focus:outline-none transition-transform hover:scale-110"
          aria-label={`${star} star${star > 1 ? 's' : ''}`}
        >
          <Star
            className={`w-8 h-8 transition-colors ${
              star <= (hovered || value)
                ? 'text-amber-400 fill-amber-400'
                : 'text-slate-300 dark:text-slate-600'
            }`}
          />
        </button>
      ))}
    </div>
  );
}

function formatDate(dateStr) {
  if (!dateStr) return '';
  try {
    return new Date(dateStr).toLocaleDateString('en-IN', {
      year: 'numeric', month: 'short', day: 'numeric',
    });
  } catch {
    return '';
  }
}

/* ─────────────────────────────────────────────────────────────────────── */
/*  SellerReviewsModal                                                    */
/* ─────────────────────────────────────────────────────────────────────── */
export function SellerReviewsModal({ sellerId, sellerName, onClose }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!sellerId) return;
    setLoading(true);
    axios
      .get(`${backendUrl}/api/reviews/seller/${sellerId}`)
      .then((res) => setData(res.data))
      .catch(() => setError('Could not load reviews.'))
      .finally(() => setLoading(false));
  }, [sellerId]);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 animate-in fade-in">
      <div className="bg-white dark:bg-slate-900 rounded-3xl w-full max-w-lg max-h-[85vh] flex flex-col shadow-2xl relative overflow-hidden">

        {/* Header */}
        <div className="bg-gradient-to-r from-amber-500 to-orange-500 p-6 text-white flex-shrink-0">
          <button
            onClick={onClose}
            className="absolute top-4 right-4 p-2 text-white/70 hover:text-white hover:bg-white/20 rounded-full transition-all"
          >
            <X className="w-5 h-5" />
          </button>
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 bg-white/20 rounded-xl flex items-center justify-center">
              <Star className="w-6 h-6" />
            </div>
            <div>
              <h2 className="font-bold text-lg">Seller Reviews</h2>
              {sellerName && <p className="text-amber-100 text-sm">{sellerName}</p>}
            </div>
          </div>
          {data && (
            <div className="flex items-center gap-3 mt-1">
              <StarDisplay rating={data.average_rating} size="lg" />
              <span className="text-2xl font-black">{data.average_rating.toFixed(1)}</span>
              <span className="text-amber-200 text-sm">
                ({data.total_reviews} review{data.total_reviews !== 1 ? 's' : ''})
              </span>
            </div>
          )}
        </div>

        {/* Body */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {loading && (
            <div className="flex justify-center py-12">
              <div className="animate-spin rounded-full h-10 w-10 border-b-4 border-amber-500" />
            </div>
          )}
          {error && (
            <div className="flex items-center gap-3 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl text-red-600 dark:text-red-400">
              <AlertCircle className="w-5 h-5 flex-shrink-0" />
              {error}
            </div>
          )}
          {!loading && !error && data?.reviews?.length === 0 && (
            <div className="text-center py-16 text-slate-400">
              <MessageSquare className="w-12 h-12 mx-auto mb-3 opacity-40" />
              <p className="font-medium">No reviews yet</p>
              <p className="text-sm mt-1">Be the first to review this seller!</p>
            </div>
          )}
          {!loading && data?.reviews?.map((review) => (
            <div
              key={review._id}
              className="bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl p-4 space-y-2"
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-8 h-8 rounded-full bg-amber-100 dark:bg-amber-900/30 flex items-center justify-center">
                    <User className="w-4 h-4 text-amber-600" />
                  </div>
                  <span className="font-semibold text-slate-800 dark:text-white text-sm">
                    {review.reviewer_name}
                  </span>
                </div>
                <span className="text-xs text-slate-400">{formatDate(review.created_at)}</span>
              </div>
              <StarDisplay rating={review.rating} />
              {review.comment && (
                <p className="text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
                  {review.comment}
                </p>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

/* ─────────────────────────────────────────────────────────────────────── */
/*  WriteReviewModal                                                      */
/* ─────────────────────────────────────────────────────────────────────── */
export function WriteReviewModal({ transactionId, itemTitle, onClose, onSuccess }) {
  const [rating, setRating] = useState(0);
  const [comment, setComment] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (rating === 0) { setError('Please select a star rating.'); return; }
    const token = localStorage.getItem('token');
    if (!token) { setError('You must be logged in to leave a review.'); return; }

    setSubmitting(true);
    setError('');
    try {
      await axios.post(
        `${backendUrl}/api/reviews/add`,
        { transaction_id: transactionId, rating, comment },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      onSuccess?.();
      onClose();
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to submit review. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 animate-in fade-in">
      <div className="bg-white dark:bg-slate-900 rounded-3xl w-full max-w-md shadow-2xl relative overflow-hidden">

        {/* Header */}
        <div className="bg-gradient-to-r from-purple-600 to-indigo-600 p-6 text-white">
          <button
            onClick={onClose}
            className="absolute top-4 right-4 p-2 text-white/70 hover:text-white hover:bg-white/20 rounded-full transition-all"
          >
            <X className="w-5 h-5" />
          </button>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-white/20 rounded-xl flex items-center justify-center">
              <Star className="w-6 h-6" />
            </div>
            <div>
              <h2 className="font-bold text-lg">Leave a Review</h2>
              {itemTitle && (
                <p className="text-purple-200 text-sm truncate max-w-xs">{itemTitle}</p>
              )}
            </div>
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-5">
          <div>
            <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">
              Your Rating *
            </label>
            <StarPicker value={rating} onChange={setRating} />
            {rating > 0 && (
              <p className="text-sm text-amber-600 dark:text-amber-400 mt-2 font-medium">
                {['', 'Poor', 'Fair', 'Good', 'Very Good', 'Excellent'][rating]}
              </p>
            )}
          </div>

          <div>
            <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">
              Comment <span className="font-normal text-slate-400">(optional)</span>
            </label>
            <textarea
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              rows={4}
              maxLength={500}
              className="w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-transparent focus:ring-2 focus:ring-purple-500 outline-none transition-all dark:text-white text-sm resize-none"
              placeholder="How was your experience with this seller?"
            />
            <p className="text-xs text-slate-400 text-right mt-1">{comment.length}/500</p>
          </div>

          {error && (
            <div className="flex items-center gap-2 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl text-red-600 dark:text-red-400 text-sm">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              {error}
            </div>
          )}

          <div className="flex gap-3">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 py-3 border border-slate-300 dark:border-slate-600 rounded-xl font-semibold text-slate-700 dark:text-white hover:bg-slate-50 dark:hover:bg-slate-800 transition-all"
            >
              Skip
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="flex-1 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-bold rounded-xl shadow-lg shadow-purple-500/30 transition-all active:scale-95 flex items-center justify-center gap-2 disabled:opacity-60 disabled:cursor-not-allowed"
            >
              {submitting ? (
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              ) : (
                <>
                  <Send className="w-4 h-4" />
                  Submit Review
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

/* ─────────────────────────────────────────────────────────────────────── */
/*  SellerRatingBadge — compact inline badge on item cards               */
/* ─────────────────────────────────────────────────────────────────────── */
export function SellerRatingBadge({ sellerId, onClick }) {
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    if (!sellerId) return;
    axios
      .get(`${backendUrl}/api/reviews/seller/${sellerId}`)
      .then((res) => setSummary(res.data))
      .catch(() => {});
  }, [sellerId]);

  if (!summary) return null;

  return (
    <button
      onClick={onClick}
      title="View seller reviews"
      className="flex items-center gap-1.5 text-xs font-semibold text-amber-600 dark:text-amber-400 hover:text-amber-700 dark:hover:text-amber-300 transition-colors group"
    >
      <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-400 group-hover:scale-110 transition-transform" />
      {summary.total_reviews > 0 ? (
        <>
          <span>{summary.average_rating.toFixed(1)}</span>
          <span className="text-slate-400 dark:text-slate-500">({summary.total_reviews})</span>
        </>
      ) : (
        <span className="text-slate-400 dark:text-slate-500">No reviews yet</span>
      )}
    </button>
  );
}
