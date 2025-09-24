# Monetization Algorithm: Targeted Game Promotions

This document outlines the design of an algorithm to deliver targeted promotions for full games to users on the Games Universe Platform. The goal is to promote games that users are highly likely to purchase.

## The 5-Step Design

The algorithm is designed in five main parts, from scoring potential games to testing and optimizing the promotion strategy.

### 1. "Propensity to Buy" Score

This score estimates the likelihood a user will purchase a specific game. It is a weighted sum of four components:

*   **Taste Match:** How well the game matches the user's preferences (derived from the core recommendation algorithm).
*   **Social Proof:** The influence of the user's friends (e.g., how many friends own or have wishlisted the game).
*   **User Intent:** Explicit signals from the user, such as having the game on their wishlist or viewing its store page.
*   **Global Factors:** The game's overall popularity and a modifier based on the user's monetization segment (e.g., `Whales` get a boost, `Grinders` get a penalty).

### 2. Promotion Triggers

These are the specific moments and locations for showing a promotion.

*   **Store-Based:** On the main store homepage, on genre-specific pages, or on the page of a similar game.
*   **Event-Driven:** Via a weekly personalized email/notification, or when a game on a user's wishlist goes on sale.
*   **Frequency Capping:** A mandatory cooldown period must be enforced to avoid showing game promotions too frequently.

### 3. Promotion Logic

This logic decides **which** game to promote and **how**.

1.  **Selection:** The system calculates the `PropensityScore` for a pool of candidate games and selects the one with the highest score. The pool is context-dependent (e.g., for a contextual trigger, it only scores similar games).
2.  **Offer:** The type of offer is tailored to the user's monetization segment:
    *   **Whales:** Receive a simple "Recommended For You" notification with no discount.
    *   **Dolphins:** Receive a small, personalized discount (e.g., 10-15%) or a bundle offer.
    *   **Minnows/Grinders:** Receive a more significant discount (e.g., 20-35%) to encourage conversion.

### 4. Full Algorithm Outline

The system operates in two main parts:

*   **Recurring Batch Process:** Periodically (e.g., daily), the system pre-calculates the `PropensityScore` for every user/game combination and caches the top results for each user.
*   **Real-Time Trigger Process:** When a trigger fires, the system:
    1.  Checks the user's frequency cap.
    2.  Selects the best candidate game (either from the cache or via a quick real-time calculation for contextual triggers).
    3.  Applies the promotion logic to determine the offer type.
    4.  Returns the final promotion to be displayed.

### 5. A/B Testing Framework

Continuous optimization is performed via A/B testing.

*   **Setup:** Users are split into a Control Group (no promotions), a Champion group (current best strategy), and a Challenger group (new hypothesis).
*   **What to Test:** The weights of the `PropensityScore`, different discount strategies for different segments, and the effectiveness of different promotional channels (e.g., email vs. in-platform pop-up).
*   **Key Metrics:**
    *   **Primary:** Conversion Rate, Average Revenue Per User (ARPU).
    *   **Guardrail:** Retention Rate, Playtime, to ensure a positive user experience.
