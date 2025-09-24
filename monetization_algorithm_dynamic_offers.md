# Monetization Algorithm: Dynamic Offers for In-Game Content

This document outlines the design of a data-driven algorithm to provide dynamic, personalized offers for in-game content and DLC on the Games Universe Platform.

## The 5-Step Design

The algorithm is designed in five main parts, from understanding the user to testing and optimizing the results.

### 1. User Segmentation

The foundation of the algorithm is to group users based on their behavior. This allows for tailored messaging.

*   **Key Data Points:** `total_playtime`, `total_spent`, `purchase_count`, `recency`, `account_age`, `in_game_progress`.
*   **Core Segments:**
    *   **Whales:** High-value spenders. Goal: Retention with premium content.
    *   **Dolphins:** Consistent mid-value spenders. Goal: Encourage repeat purchases with bundles.
    *   **Minnows:** Occasional/first-time spenders. Goal: Convert to Dolphins with high-value starter packs.
    *   **Grinders:** Engaged non-spenders. Goal: First-time conversion with time-savers or exclusive cosmetics.
    *   **New Players:** Users with new accounts. Goal: Positive onboarding with a single, high-value welcome pack.
    *   **Lapsed Players:** Inactive users. Goal: Win back with generous "welcome back" offers.

### 2. Offer Triggers

These are the specific, context-aware moments when an offer should be presented.

*   **Progression-Based:** On Level Up, After Defeating a Boss, On Failing a Challenge.
*   **Session-Based:** On Login (for daily deals).
*   **Behavioral:** Near-Miss on In-Game Currency purchase, Repeatedly Viewing an Item in the store.
*   **Cooldown:** A mandatory "offer cooldown" period (e.g., 24 hours) must be enforced to prevent spam.

### 3. Offer-Matching Logic

A scoring system determines the best offer to show when a trigger is fired.

1.  **Prerequisite:** An Offer Catalog where every offer is tagged with metadata (e.g., `price_point`, `target_segment`, `target_trigger`, `content_category`).
2.  **Filtering:** The system first creates a short list of eligible offers based on the `target_trigger`.
3.  **Scoring:** Each eligible offer is given a score based on how well it matches the user's `Segment`, `Content Affinity`, and `Price Point` history.
4.  **Selection:** The offer with the highest score is chosen, provided it meets a minimum quality threshold.

### 4. Full Algorithm Outline

The system operates in two parts:

*   **Daily Batch Process:** Once a day, it updates every user's `Segment` based on their latest activity.
*   **Real-Time Trigger Process:**
    1.  An in-game action fires a `Trigger`.
    2.  The system checks the user's `Cooldown` status.
    3.  It fetches the user's pre-calculated `Segment`.
    4.  It filters and scores all eligible offers using the `Offer-Matching Logic`.
    5.  The highest-scoring offer is selected and displayed to the user.

### 5. A/B Testing Framework

To ensure continuous improvement, a testing framework is essential.

*   **Control Group:** A small group of users who receive no offers, acting as a baseline.
*   **Champion (Group A):** The majority of users who receive the current best version of the algorithm.
*   **Challenger (Group B):** A smaller group that receives a modified offer to test a new hypothesis (e.g., different pricing, content, or timing).
*   **Key Metrics:**
    *   **Primary:** Conversion Rate, Average Revenue Per User (ARPU).
    *   **Guardrail:** Retention Rate, Playtime (to ensure user experience isn't harmed).
*   **Process:** Test new ideas as Challengers. If a Challenger proves to be statistically better than the Champion without harming guardrail metrics, it becomes the new Champion. Repeat.
