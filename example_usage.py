"""
example_usage.py -- Demonstrates the ProductReviewGenerator SDK.
"""
from client import ProductReviewGenerator

def main():
    gen = ProductReviewGenerator(seed=42)

    # 1. Single product, enthusiastic 5-star
    print("\n[1] 5-Star Enthusiastic Reviews for a Moisturizer")
    result = gen.generate(
        product_name="HydraBoost Daily Moisturizer",
        product_features=["lightweight formula", "SPF 30 protection", "24-hour hydration", "non-greasy finish"],
        rating=5,
        tone="enthusiastic",
        num_reviews=3,
    )
    print(f"Product: {result['product']} | Rating: {result['rating']}★ | Tone: {result['tone']}")
    print(f"Avg Word Count: {result['avg_word_count']}")
    for i, r in enumerate(result["reviews"], 1):
        print(f"\n  Review {i}: [{r['rating']}★] {r['title']}")
        print(f"  By {r['reviewer']} ({r['location']}) — {r['badge']}")
        print(f"  {r['body']}")

    # 2. Balanced 4-star
    print("\n\n[2] 4-Star Balanced Reviews for a Wireless Keyboard")
    result = gen.generate(
        product_name="ProType Wireless Keyboard",
        product_features=["bluetooth 5.0", "backlit keys", "6-month battery life", "compact layout"],
        rating=4,
        tone="balanced",
        num_reviews=2,
    )
    for r in result["reviews"]:
        print(f"\n  [{r['rating']}★] {r['title']} — {r['reviewer']}")
        print(f"  {r['body']}")

    # 3. Batch generation
    print("\n\n[3] Batch Review Generation")
    batch_results = gen.generate_batch([
        {"product_name": "UltraFit Running Shoes", "product_features": ["cushioned sole", "breathable mesh", "lightweight"], "rating": 5, "tone": "enthusiastic", "num_reviews": 1},
        {"product_name": "BudgetBlend Blender", "product_features": ["700W motor", "3 speed settings", "easy cleaning"], "rating": 3, "tone": "balanced", "num_reviews": 1},
        {"product_name": "SleepWell Pillow", "product_features": ["memory foam", "cooling cover", "adjustable loft"], "rating": 4, "tone": "analytical", "num_reviews": 1},
    ])
    for batch in batch_results:
        r = batch["reviews"][0]
        print(f"  [{r['rating']}★] {batch['product']}: {r['title']} — {r['reviewer']}")

if __name__ == "__main__":
    main()
