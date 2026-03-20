"""
Image Similarity Module using OpenCV
Compares two images using multiple techniques:
  1. Color Histogram Comparison — compares overall color distribution
  2. ORB Feature Matching — compares structural features/keypoints
  3. Structural Similarity (SSIM-like) — compares resized grayscale structure

Returns a combined similarity score between 0.0 and 1.0
"""

import cv2
import numpy as np
import urllib.request
import os
import tempfile


def download_image(url):
    """Download an image from a URL and return it as an OpenCV image (numpy array)."""
    try:
        # Create a temporary file
        tmp_file = os.path.join(tempfile.gettempdir(), f"campus_img_{hash(url)}.jpg")
        
        # Download the image
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            img_data = response.read()
        
        # Write to temp file and read with OpenCV
        with open(tmp_file, 'wb') as f:
            f.write(img_data)
        
        img = cv2.imread(tmp_file)
        
        # Cleanup temp file
        try:
            os.remove(tmp_file)
        except OSError:
            pass
        
        return img
    except Exception as e:
        print(f"[ImageSimilarity] Error downloading image from {url}: {e}")
        return None


def resize_image(img, size=(256, 256)):
    """Resize image to a standard size for comparison."""
    return cv2.resize(img, size, interpolation=cv2.INTER_AREA)


def histogram_similarity(img1, img2):
    """
    Compare two images using color histogram correlation.
    Uses HSV color space for better color matching.
    Returns a score between 0.0 and 1.0
    """
    try:
        # Convert to HSV
        hsv1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
        hsv2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
        
        # Calculate histograms for H and S channels
        h_bins = 50
        s_bins = 60
        hist_size = [h_bins, s_bins]
        h_ranges = [0, 180]
        s_ranges = [0, 256]
        ranges = h_ranges + s_ranges
        channels = [0, 1]
        
        hist1 = cv2.calcHist([hsv1], channels, None, hist_size, ranges)
        cv2.normalize(hist1, hist1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
        
        hist2 = cv2.calcHist([hsv2], channels, None, hist_size, ranges)
        cv2.normalize(hist2, hist2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
        
        # Compare using correlation method (returns -1 to 1, we normalize to 0-1)
        score = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        return max(0.0, score)  # Clamp to [0, 1]
    except Exception as e:
        print(f"[ImageSimilarity] Histogram comparison error: {e}")
        return 0.0


def orb_feature_similarity(img1, img2):
    """
    Compare two images using ORB (Oriented FAST and Rotated BRIEF) feature matching.
    Good for detecting similar objects even with different angles/sizes.
    Returns a score between 0.0 and 1.0
    """
    try:
        # Convert to grayscale
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        
        # Create ORB detector
        orb = cv2.ORB_create(nfeatures=500)
        
        # Find keypoints and descriptors
        kp1, des1 = orb.detectAndCompute(gray1, None)
        kp2, des2 = orb.detectAndCompute(gray2, None)
        
        if des1 is None or des2 is None or len(des1) == 0 or len(des2) == 0:
            return 0.0
        
        # Create BFMatcher (Brute Force Matcher)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
        
        # Find matches using KNN
        matches = bf.knnMatch(des1, des2, k=2)
        
        # Apply Lowe's ratio test to filter good matches
        good_matches = []
        for match_pair in matches:
            if len(match_pair) == 2:
                m, n = match_pair
                if m.distance < 0.75 * n.distance:
                    good_matches.append(m)
        
        # Calculate similarity score
        if len(matches) == 0:
            return 0.0
        
        score = len(good_matches) / max(len(kp1), len(kp2))
        return min(1.0, score)  # Clamp to [0, 1]
    except Exception as e:
        print(f"[ImageSimilarity] ORB feature matching error: {e}")
        return 0.0


def structural_similarity(img1, img2):
    """
    Compare two resized grayscale images pixel-by-pixel.
    A simplified SSIM-like comparison.
    Returns a score between 0.0 and 1.0
    """
    try:
        # Resize both to same small size
        size = (128, 128)
        gray1 = cv2.cvtColor(cv2.resize(img1, size), cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(cv2.resize(img2, size), cv2.COLOR_BGR2GRAY)
        
        # Compute absolute difference
        diff = cv2.absdiff(gray1, gray2)
        
        # Normalize: 0 difference = 1.0 similarity, 255 avg diff = 0.0 similarity
        mean_diff = np.mean(diff)
        score = 1.0 - (mean_diff / 255.0)
        
        return max(0.0, score)
    except Exception as e:
        print(f"[ImageSimilarity] Structural comparison error: {e}")
        return 0.0


def compute_image_similarity(url1, url2):
    """
    Main function: Compare two images from URLs using multiple OpenCV techniques.
    
    Returns:
        dict with:
            - combined_score (float): Weighted average of all methods (0.0 - 1.0)
            - histogram_score (float): Color histogram similarity
            - feature_score (float): ORB feature matching score
            - structural_score (float): Structural pixel similarity
            - is_similar (bool): True if combined_score > threshold
    """
    if not url1 or not url2:
        return {
            "combined_score": 0.0,
            "histogram_score": 0.0,
            "feature_score": 0.0,
            "structural_score": 0.0,
            "is_similar": False
        }
    
    # Download both images
    img1 = download_image(url1)
    img2 = download_image(url2)
    
    if img1 is None or img2 is None:
        return {
            "combined_score": 0.0,
            "histogram_score": 0.0,
            "feature_score": 0.0,
            "structural_score": 0.0,
            "is_similar": False
        }
    
    # Resize for consistent comparison
    img1 = resize_image(img1)
    img2 = resize_image(img2)
    
    # Run all three comparison methods
    hist_score = histogram_similarity(img1, img2)
    feat_score = orb_feature_similarity(img1, img2)
    struct_score = structural_similarity(img1, img2)
    
    # Weighted combination:
    # - Histogram (40%): Good for color-based matching
    # - ORB Features (35%): Good for shape/object matching
    # - Structural (25%): Good for overall appearance
    combined = (hist_score * 0.40) + (feat_score * 0.35) + (struct_score * 0.25)
    
    SIMILARITY_THRESHOLD = 0.35
    
    result = {
        "combined_score": round(combined, 4),
        "histogram_score": round(hist_score, 4),
        "feature_score": round(feat_score, 4),
        "structural_score": round(struct_score, 4),
        "is_similar": combined > SIMILARITY_THRESHOLD
    }
    
    print(f"[ImageSimilarity] Comparison result: {result}")
    return result
