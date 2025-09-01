# How to Launch a Game on Facebook Gaming (Instant Games)

This guide provides a step-by-step overview of the process for launching an HTML5 game on the Facebook Instant Games platform.

## 1. Prerequisites

Before you begin, you will need:
- A **Facebook Account** to create a developer account.
- An **HTML5 Game**: Your game must be built using web technologies (HTML, JavaScript, CSS).
- A **ZIP file** of your game, with an `index.html` file in the root directory.

## 2. Create a Facebook Developer Account and App

1.  **Go to the Facebook for Developers website:** [https://developers.facebook.com/](https://developers.facebook.com/)
2.  **Create a Developer Account:** If you don't already have one, you will be prompted to create one.
3.  **Create a New App:**
    - From the "My Apps" menu, select "Create App".
    - Choose "Gaming" as the app type.
    - Fill in your game's name and your contact email.
4.  **Configure App Settings:**
    - In your app's dashboard, go to **Settings > Basic**.
    - Fill in the required details, such as App Icon, Privacy Policy URL, etc.
    - Choose "Games" as the category and select an appropriate sub-category.

## 3. Enable the Instant Games Product

1.  In the app dashboard, click the **"+"** button next to "Products" in the left-hand menu.
2.  Find "Instant Games" and click **"Set Up"**.
3.  This will add the Instant Games settings to your app.

## 4. Integrate the Instant Games SDK

Your game needs to include the Facebook Instant Games SDK to work on the platform.

1.  **Add the SDK script to your `index.html` file:**
    ```html
    <script src="https://connect.facebook.net/en_US/fbinstant.6.3.js"></script>
    ```
    **Important:** Do not download the SDK and bundle it with your game. Always load it from this URL.

2.  **Initialize the SDK:** Your game must call `FBInstant.initializeAsync()` before using any other SDK functions.
    ```javascript
    FBInstant.initializeAsync().then(function() {
      // SDK is ready to use
      // Start loading your game assets here
    });
    ```

3.  **Report Loading Progress:** You must use the SDK to report the loading progress of your game assets.
    ```javascript
    FBInstant.setLoadingProgress(50); // e.g., 50% loaded
    ```

For more details on the SDK, refer to the [official documentation](https://developers.facebook.com/docs/games/build/instant-games/get-started/quick-start/).

## 5. Upload Your Game to Facebook Web Hosting

Facebook provides a hosting service for your game's assets.

1.  **Go to the Web Hosting Tab:** In your app dashboard, under "Instant Games", go to **Web Hosting**.
2.  **Upload Your Build:**
    - Click **"Upload Version"**.
    - Select the ZIP file containing your game.
3.  **Processing:** Facebook will process your build. This may take a few minutes.

## 6. Test Your Game

1.  **Mark a Build for Production:** After a build is successfully uploaded and processed, you must mark it as the "Production" version by clicking the star icon next to it. **You must do this to be able to test your game.**
2.  **Add Testers:**
    - In the left-hand menu, go to **Roles > Testers**.
    - Add the Facebook accounts of anyone you want to test the game.
3.  **Play the Game:** Testers can now find and play the game directly on Facebook. You can also get a shareable link to send to your testers.

For more details on testing, refer to the [Testing, Publishing, and Sharing an Instant Game](https://developers.facebook.com/docs/games/build/instant-games/get-started/test-publish-share/) guide.

## 7. Launch Your Game

Once you are satisfied with your game, you can submit it for review.

1.  **Go to the "Review" Tab:** In your app dashboard, there will be a section for submitting your app for review.
2.  **Submit for Review:** Follow the instructions to submit your app. The Facebook team will review your game to ensure it meets their platform policies and quality guidelines.
3.  **Launch:** Once your game is approved, you can make it live for all Facebook users to play.

This guide provides a high-level overview. For more detailed information, always refer to the official [Facebook Games Documentation](https://developers.facebook.com/docs/games/).
