"""Test script for quote provider functionality."""

import logging

from src.providers.quote import get_quote

logging.basicConfig(level=logging.INFO)


def test_quote_fetching():
    """Test quote fetching from all sources."""
    print("\n" + "=" * 60)
    print("Testing Quote Provider")
    print("=" * 60 + "\n")

    # Test 1: Get a quote
    print("Test 1: Fetching quote...")
    quote = get_quote()
    print("✅ Quote fetched successfully!")
    print(f"   Type: {quote['type']}")
    print(f"   Content: {quote['content'][:50]}...")
    print(f"   Author: {quote['author']}")
    print(f"   Source: {quote['source']}")

    # Test 2: Check caching
    print("\nTest 2: Testing cache...")
    quote2 = get_quote()
    if quote == quote2:
        print("✅ Cache working! Same quote returned.")
    else:
        print("⚠️  Different quote returned (cache may have expired)")

    # Test 3: Display formatted quote
    print("\n" + "=" * 60)
    print("Formatted Quote Display:")
    print("=" * 60)
    print(f"\n{quote['content']}\n")
    attribution = f"—— {quote['author']}"
    if quote["source"]:
        attribution += f"《{quote['source']}》"
    print(attribution)
    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_quote_fetching()
