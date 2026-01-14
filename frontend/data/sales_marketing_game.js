// Game state
let revenue = 10000;
let retention = 80; // Overall retention
let userSegments = {
    'New Players': 1000,
    'Grinders': 2000,
    'Minnows': 500,
    'Dolphins': 100,
    'Whales': 10,
    'Lapsed Players': 500
};
let totalUsers = 0;
let currentTurn = 1;

// DOM elements
const revenueEl = document.getElementById('revenue');
const usersEl = document.getElementById('users');
const retentionEl = document.getElementById('retention');
const outputEl = document.getElementById('output');
const runCampaignBtn = document.getElementById('run-campaign-btn');
const offerDiscountBtn = document.getElementById('offer-discount-btn');
const subscriptionDriveBtn = document.getElementById('subscription-drive-btn');

// DOM elements for segments
const segmentNewPlayersEl = document.getElementById('segment-new-players');
const segmentGrindersEl = document.getElementById('segment-grinders');
const segmentMinnowsEl = document.getElementById('segment-minnows');
const segmentDolphinsEl = document.getElementById('segment-dolphins');
const segmentWhalesEl = document.getElementById('segment-whales');
const segmentLapsedPlayersEl = document.getElementById('segment-lapsed-players');


function updateTotalUsers() {
    totalUsers = Object.values(userSegments).reduce((a, b) => a + b, 0);
}

// AI Simulation
function getAIRecommendation(actionType) {
    // This is a simplified simulation of the AI algorithms
    switch (actionType) {
        case 'marketing':
            // The AI suggests targeting grinders to convert them to spenders
            return "AI Suggestion: Target 'Grinders' with a marketing campaign to convert them to 'Minnows'.";
        case 'discounts':
            // The AI suggests offering discounts to Dolphins to encourage repeat purchases
            return "AI Suggestion: Offer special bundles to 'Dolphins' to increase their spending.";
        case 'subscription':
            // The AI suggests targeting Loyalists (let's assume Whales are loyalists) for high-tier subscriptions
            return "AI Suggestion: Promote the 'Elite' subscription tier to 'Whales' to maximize their value.";
        default:
            return "No AI suggestion available.";
    }
}

// Player actions
function runMarketingCampaign() {
    log('Running a marketing campaign...');
    // For simplicity, let's assume the player follows the AI's advice and targets Grinders
    const conversionRate = 0.1; // 10% of grinders become minnows
    const convertedUsers = Math.floor(userSegments['Grinders'] * conversionRate);
    userSegments['Grinders'] -= convertedUsers;
    userSegments['Minnows'] += convertedUsers;
    revenue -= 5000; // Cost of the campaign
    log(`Converted ${convertedUsers} Grinders to Minnows.`);
    advanceTurn();
}

function offerDiscounts() {
    log('Offering discounts to Dolphins...');
    const purchaseRate = 0.5; // 50% of dolphins make a purchase
    const purchases = Math.floor(userSegments['Dolphins'] * purchaseRate);
    const revenueFromDiscounts = purchases * 25; // average purchase value
    revenue += revenueFromDiscounts;
    log(`Dolphins made ${purchases} purchases, generating $${revenueFromDiscounts}.`);
    advanceTurn();
}

function subscriptionDrive() {
    log('Starting a subscription drive for Whales...');
    const subscriptionRate = 0.8; // 80% of whales subscribe
    const newSubscribers = Math.floor(userSegments['Whales'] * subscriptionRate);
    const revenueFromSubscriptions = newSubscribers * 15; // monthly subscription
    revenue += revenueFromSubscriptions;
    retention += 1;
    log(`${newSubscribers} Whales subscribed to the Elite tier, generating $${revenueFromSubscriptions} monthly.`);
    advanceTurn();
}

// Helper functions
function log(message) {
    const p = document.createElement('p');
    p.textContent = message;
    outputEl.insertBefore(p, outputEl.firstChild);
}

function disableActions() {
    runCampaignBtn.disabled = true;
    offerDiscountBtn.disabled = true;
    subscriptionDriveBtn.disabled = true;
}

function updateDashboard() {
    updateTotalUsers();
    revenueEl.textContent = `$${Math.round(revenue)}`;
    usersEl.textContent = totalUsers;
    retentionEl.textContent = `${retention}%`;

    if(segmentNewPlayersEl) {
        // Update user segments display
        segmentNewPlayersEl.textContent = userSegments['New Players'];
        segmentGrindersEl.textContent = userSegments['Grinders'];
        segmentMinnowsEl.textContent = userSegments['Minnows'];
        segmentDolphinsEl.textContent = userSegments['Dolphins'];
        segmentWhalesEl.textContent = userSegments['Whales'];
        segmentLapsedPlayersEl.textContent = userSegments['Lapsed Players'];
    }
}

function advanceTurn() {
    log(`--- End of Turn ${currentTurn} ---`);

    // Simulate user churn
    const churnRate = (100 - retention) / 2000; // Simplified churn
    for (const segment in userSegments) {
        if (segment !== 'Lapsed Players') {
            const churnedUsers = Math.floor(userSegments[segment] * churnRate);
            userSegments[segment] -= churnedUsers;
            userSegments['Lapsed Players'] += churnedUsers;
        }
    }
    log('Simulated user churn.');

    // Simulate organic growth (new players)
    const organicGrowth = Math.floor(Math.random() * 200) + 50;
    userSegments['New Players'] += organicGrowth;
    log(`Gained ${organicGrowth} new players organically.`);

    currentTurn++;
    log(`--- Start of Turn ${currentTurn} ---`);
    // AI provides suggestions for the turn
    log(getAIRecommendation('marketing'));
    log(getAIRecommendation('discounts'));
    log(getAIRecommendation('subscription'));


    updateDashboard();

    if (revenue >= 1000000) {
        log('Congratulations! You reached $1,000,000 in revenue and won the game!');
        disableActions();
    } else if (totalUsers <= 100 && revenue < 0) {
        log('You have less than 100 users and negative revenue. You lost the game.');
        disableActions();
    }
}

// Event listeners
runCampaignBtn.addEventListener('click', runMarketingCampaign);
offerDiscountBtn.addEventListener('click', offerDiscounts);
subscriptionDriveBtn.addEventListener('click', subscriptionDrive);

// Initial game state
updateDashboard();
log(`--- Start of Turn ${currentTurn} ---`);
log('Welcome to the Sales & Marketing Simulation! Your goal is to reach $1,000,000 in revenue.');
log('The AI will provide suggestions each turn. Choose your actions wisely.');
log(getAIRecommendation('marketing'));
log(getAIRecommendation('discounts'));
log(getAIRecommendation('subscription'));