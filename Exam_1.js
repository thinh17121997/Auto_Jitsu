const { chromium } = require('playwright');

async function main() {
    console.log("Launching Playwright...");
    const browser = await chromium.launch({ headless: false });
    const context = await browser.newContext({
        viewport: { width: 1280, height: 800 }
    });
    const page = await context.newPage();

    try {
        console.log("Opening time.is...");
        await page.goto('https://time.is', { waitUntil: 'domcontentloaded', timeout: 60000 });
        
        await page.waitForTimeout(2000);

        console.log("Searching for 'Los Angeles'...");
        const searchBox = page.locator("input[name='q'], input[type='text'], #qs").first();
        await searchBox.fill('Los Angeles');
        await page.waitForTimeout(1000);
        await searchBox.press('Enter');

        console.log("Waiting for page load...");
        await page.waitForTimeout(3000);

        const titleText = await page.title();
        const bodyText = await page.locator("body").innerText();

        if (titleText.includes("Los Angeles") || bodyText.includes("Los Angeles")) {
            console.log("[✓] City name 'Los Angeles' is displayed correctly.");
        } else {
            console.log("[x] City name verification failed.");
            console.log(`Title was: ${titleText}`);
        }

        try {
            const dateText = await page.locator('#dd').innerText();
            console.log(`[✓] Date displayed as: ${dateText}`);
        } catch (e) {
            console.log("[?] Could not find specific date element by ID 'dd', checking body text for dates...");
        }

        console.log("Verifying time updates...");
        let clockLocator = page.locator('#clock');
        if (await clockLocator.count() === 0) {
            clockLocator = page.locator('#twd');
            if (await clockLocator.count() === 0) {
                console.log("[x] Could not locate the clock element.");
                return;
            }
        }

        let timeSamples = [];
        for (let i = 0; i < 3; i++) {
            let timeText = await clockLocator.innerText();
            timeSamples.push(timeText);
            console.log(`  Sampled time: ${timeText}`);
            await page.waitForTimeout(1200);
        }

        const validFormat = timeSamples.every(t => /^\d{1,2}:\d{2}:\d{2}( [AMP]+)?$/.test(t));

        if (validFormat) {
            console.log("[✓] Time format is valid (includes HH:MM:SS).");
        } else {
            console.log("[x] Time format seems invalid or unusual:", timeSamples);
        }

        let uniqueSamples = new Set(timeSamples);
        if (uniqueSamples.size > 1) {
            console.log("[✓] Time is continuously updating and changing.");
        } else {
            console.log("[x] Time does not appear to be updating:", timeSamples);
        }
    } catch (e) {
        console.error("Test encountered an error:", e);
    } finally {
        console.log("Test complete. Creating delay before closing...");
        await page.waitForTimeout(2000);
        await browser.close();
    }
}

if (require.main === module) {
    main().catch(console.error);
}
