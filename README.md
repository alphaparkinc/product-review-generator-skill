# genpark-product-review-generator-skill

> **GenPark AI Agent Skill** — Generate authentic, diverse product reviews for e-commerce listings.

## Overview

Generates realistic product reviews with tone variation, reviewer personas, star ratings, and feature-driven content. No LLM API required — works fully offline with template-based NLG.

## Features

- 4 tone styles: `enthusiastic`, `balanced`, `critical`, `analytical`
- Star ratings 1–5 with sentiment-matched language
- 8 reviewer personas with locations and badges
- Configurable word count range
- Batch processing for multiple products

## Quick Start

```python
from client import ProductReviewGenerator

gen = ProductReviewGenerator()
result = gen.generate(
    product_name="HydraBoost Moisturizer",
    product_features=["lightweight", "SPF 30", "24-hour hydration"],
    rating=5,
    tone="enthusiastic",
    num_reviews=3,
)
for review in result["reviews"]:
    print(f"[{review['rating']}*] {review['title']}")
    print(review["body"])
```

## Installation

```bash
python example_usage.py  # No external dependencies
```

---
Built by [GenPark](https://genpark.ai) | [alphaparkinc](https://github.com/alphaparkinc)
