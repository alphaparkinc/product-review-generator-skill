"""
product-review-generator-skill: Client SDK
Generate authentic, diverse product reviews for e-commerce listings.
"""

from __future__ import annotations
import random
import re
from typing import Literal, Optional

Tone = Literal["enthusiastic", "balanced", "critical", "analytical"]

REVIEWER_PERSONAS = [
    {"name": "Sarah M.", "location": "Austin, TX", "badge": "Verified Purchase"},
    {"name": "James K.", "location": "New York, NY", "badge": "Top Contributor"},
    {"name": "Linda R.", "location": "Chicago, IL", "badge": "Verified Purchase"},
    {"name": "David P.", "location": "Seattle, WA", "badge": "Early Reviewer"},
    {"name": "Emily T.", "location": "Miami, FL", "badge": "Verified Purchase"},
    {"name": "Michael B.", "location": "Denver, CO", "badge": "Verified Purchase"},
    {"name": "Priya S.", "location": "San Jose, CA", "badge": "Top Contributor"},
    {"name": "Carlos R.", "location": "Dallas, TX", "badge": "Verified Purchase"},
]

TONE_TEMPLATES = {
    "enthusiastic": {
        "openers": [
            "Absolutely love this product!",
            "This exceeded all my expectations!",
            "Best purchase I have made this year!",
            "Wow, I am genuinely impressed!",
        ],
        "transitions": ["Not only that, but", "What really surprised me was", "On top of that,"],
        "closers": [
            "Highly recommend to anyone looking for quality.",
            "Will definitely buy again. 5 stars all the way!",
            "Cannot imagine going back to my old routine without it.",
        ],
    },
    "balanced": {
        "openers": [
            "Overall, a solid product with some minor caveats.",
            "Good product for the price — here is my honest take.",
            "After using this for a few weeks, I have a fair assessment.",
            "Decent product that delivers on its core promises.",
        ],
        "transitions": ["That said,", "On the other hand,", "One thing to note is that"],
        "closers": [
            "Would recommend for most users, with the above in mind.",
            "Good value overall despite the small drawbacks.",
            "A reliable choice if you manage expectations.",
        ],
    },
    "critical": {
        "openers": [
            "Disappointed with this purchase — here is why.",
            "Not quite what I expected based on the description.",
            "Has potential but falls short in several areas.",
            "Mixed feelings about this one.",
        ],
        "transitions": ["Additionally,", "Another issue I noticed was", "To make matters worse,"],
        "closers": [
            "Would not repurchase at this price point.",
            "Needs improvement before I can recommend it.",
            "Hopefully the manufacturer addresses these issues.",
        ],
    },
    "analytical": {
        "openers": [
            "After systematic testing over 30 days, here are my findings.",
            "I evaluated this product across multiple dimensions — here is the breakdown.",
            "Objective assessment after extensive use:",
            "Conducted a thorough evaluation. Results follow.",
        ],
        "transitions": ["From a performance standpoint,", "Technically speaking,", "Comparatively,"],
        "closers": [
            "Net assessment: strong performer in its category.",
            "Recommended for users who prioritize reliability over aesthetics.",
            "Overall score: 4.2/5 based on measured criteria.",
        ],
    },
}

RATING_SENTIMENT = {
    5: ["outstanding", "exceptional", "flawless", "top-tier", "best-in-class"],
    4: ["solid", "reliable", "well-built", "capable", "worth it"],
    3: ["decent", "adequate", "functional", "acceptable", "average"],
    2: ["disappointing", "underwhelming", "subpar", "lacking", "inconsistent"],
    1: ["poor", "defective", "unacceptable", "frustrating", "avoid"],
}


class ProductReviewGenerator:
    """
    SDK for generating authentic, diverse product reviews.

    Supports tone variation, reviewer persona simulation,
    feature-driven review body construction, and word count control.
    """

    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    def generate(
        self,
        product_name: str,
        product_features: list[str],
        rating: int = 5,
        tone: Tone = "balanced",
        num_reviews: int = 3,
        min_words: int = 40,
        max_words: int = 120,
    ) -> dict:
        """
        Generate product review variants.

        Args:
            product_name:     Name of the product.
            product_features: Key features/selling points.
            rating:           Star rating 1-5.
            tone:             Review tone style.
            num_reviews:      Number of variants to generate.
            min_words:        Minimum word count per review.
            max_words:        Maximum word count per review.

        Returns:
            dict with keys: product, rating, tone, reviews, avg_word_count
        """
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5.")
        if tone not in TONE_TEMPLATES:
            raise ValueError(f"Tone must be one of: {list(TONE_TEMPLATES.keys())}")

        reviews = []
        personas = random.sample(REVIEWER_PERSONAS, min(num_reviews, len(REVIEWER_PERSONAS)))

        for i in range(num_reviews):
            persona = personas[i % len(personas)]
            review = self._build_review(
                product_name, product_features, rating, tone, persona, min_words, max_words
            )
            reviews.append(review)

        total_words = sum(len(r["body"].split()) for r in reviews)
        avg_word_count = round(total_words / len(reviews), 1) if reviews else 0

        return {
            "product": product_name,
            "rating": rating,
            "tone": tone,
            "reviews": reviews,
            "avg_word_count": avg_word_count,
        }

    def generate_batch(self, products: list[dict]) -> list[dict]:
        """
        Generate reviews for multiple products.

        Args:
            products: List of dicts with keys matching generate() params.

        Returns:
            List of result dicts.
        """
        return [self.generate(**p) for p in products]

    def _build_review(
        self,
        product_name: str,
        features: list[str],
        rating: int,
        tone: Tone,
        persona: dict,
        min_words: int,
        max_words: int,
    ) -> dict:
        """Construct a single review object."""
        tmpl = TONE_TEMPLATES[tone]
        sentiment_words = RATING_SENTIMENT.get(rating, RATING_SENTIMENT[3])

        opener = random.choice(tmpl["openers"])
        transition = random.choice(tmpl["transitions"])
        closer = random.choice(tmpl["closers"])
        sentiment = random.choice(sentiment_words)

        # Feature sentences
        selected_features = random.sample(features, min(3, len(features)))
        feature_sentences = []
        for feat in selected_features:
            templates = [
                f"The {feat.lower()} is genuinely {sentiment}.",
                f"I was particularly impressed by the {feat.lower()}.",
                f"{feat} works exactly as advertised.",
                f"The {feat.lower()} alone makes this worth buying.",
            ]
            feature_sentences.append(random.choice(templates))

        body_parts = [
            opener,
            f"I have been using the {product_name} for a few weeks now.",
            f"{transition} {feature_sentences[0]}",
        ]
        if len(feature_sentences) > 1:
            body_parts.append(feature_sentences[1])
        if len(feature_sentences) > 2:
            body_parts.append(feature_sentences[2])
        body_parts.append(closer)

        body = " ".join(body_parts)

        # Trim to word count
        words = body.split()
        if len(words) > max_words:
            body = " ".join(words[:max_words]) + "."
        elif len(words) < min_words:
            padding = f" For anyone considering {product_name}, I would say it delivers solid results in daily use."
            body += padding

        title = self._generate_title(product_name, rating, tone)

        return {
            "title": title,
            "body": body,
            "rating": rating,
            "reviewer": persona["name"],
            "location": persona["location"],
            "badge": persona["badge"],
            "word_count": len(body.split()),
        }

    @staticmethod
    def _generate_title(product_name: str, rating: int, tone: Tone) -> str:
        """Generate a compelling review title."""
        title_templates = {
            5: [f"Best {product_name} I have owned", f"Exceptional quality — highly recommend", f"Exceeded expectations!"],
            4: [f"Great {product_name} overall", f"Solid performer, minor quibbles", f"Happy with my purchase"],
            3: [f"Decent, but room for improvement", f"Meets basic expectations", f"Okay for the price"],
            2: [f"Not quite there yet", f"Some issues to be aware of", f"Disappointing for the cost"],
            1: [f"Would not recommend", f"Major quality issues", f"Returned after one week"],
        }
        return random.choice(title_templates.get(rating, title_templates[3]))
