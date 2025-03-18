import os
import asyncio
from playwright.async_api import async_playwright, Geolocation, Locator, Playwright
from playwright_stealth import stealth
from datatypes.ScrapeDatatypes import Business
from random import choice, randint

ScrapeReturnType = dict[str, list[Business]]


class ScrapeGoogleMapsSearch:
    def __init__(self, search_amount):
        self.current_keyword = None
        self.search_amount = search_amount
        self.playwright = None
        self.cloud_url = "wss://api.browsercat.com/connect"

    async def get_search_list(self, total_businesses: int):
        search_container_xpath = '//a[contains(@href, "https://www.google.com/maps/place")]'
        scroll_container_xpath = f"//div[@aria-label='Results for {self.current_keyword}']"
        await self.page.wait_for_selector(scroll_container_xpath)

        await self.page.hover(search_container_xpath)
        previously_counted = None

        while True:
            prev_height = await self.page.evaluate(
                "(el) => { el.scrollTo(0, el.scrollHeight); return el.scrollHeight; }",
                await self.page.query_selector(scroll_container_xpath)
            )

            if await self.page.locator(search_container_xpath).count() >= total_businesses:
                listings = await self.page.locator(search_container_xpath).all()
                listings = listings[:total_businesses]
                break
            else:
                current_count = await self.page.locator(search_container_xpath).count()
                if current_count == previously_counted and await self.page.evaluate(
                    "(el) => el.scrollHeight",
                    await self.page.query_selector(scroll_container_xpath)
                ) == prev_height:
                    listings = await self.page.locator(search_container_xpath).all()
                    break
                previously_counted = current_count

        return listings

    async def search(self, keyword):
        current_location_button_selector = 'button:is([aria-label="Your Location"], [aria-label="Show Your Location"])'
        await self.page.wait_for_selector(current_location_button_selector)
        await self.page.click(current_location_button_selector)

        await asyncio.sleep(1)
        search_selector = "input[role='combobox'][id='searchboxinput'][name='q']"
        await self.page.wait_for_selector(search_selector)
        await self.page.fill(search_selector, keyword)
        await self.page.press(search_selector, "Enter")

        listing = await self.get_search_list(self.search_amount)
        scrapped_data = await self.reorder_scrapped_data(listing)
        return scrapped_data

    async def scrape(self, playwright, keywords, lng, lat) -> ScrapeReturnType:

        n = playwright
        browser = await playwright.chromium.connect(
            self.cloud_url,
            headers={
                'Api-Key': ''}
        )
        context = await browser.new_context(
            locale="en-GB",
            permissions=["geolocation"],
            geolocation=Geolocation(latitude=lat, longitude=lng, accuracy=10)
        )

        self.page = await context.new_page()
        # await stealth(self.page)

        await self.page.goto("https://www.google.com/maps")

        scrape_data = {}
        for k in keywords:
            self.current_keyword = k
            await self.page.reload()
            scrape_data[k] = await self.search(k)

        await self.page.close()
        await browser.close()

        return scrape_data

    async def reorder_scrapped_data(self, listing: list[Locator]) -> list[Business]:
        business_list = []

        for lt in listing:
            try:
                await lt.click()
                await lt.click()
                name_attr = 'aria-label'
                address_xpath = '//button[@data-item-id="address"]'
                website_xpath = '//a[@data-item-id="authority"]'
                phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]'
                review_count_xpath = '//button[@jsaction="pane.reviewChart.moreReviews"]//span'
                reviews_average_xpath = '//div[@jsaction="pane.reviewChart.moreReviews"]//div[@role="img"]'

                business = Business()

                await self.page.wait_for_selector(address_xpath, timeout=10000)
                business.name = await lt.get_attribute(name_attr)

                business.address = (await self.page.locator(address_xpath).inner_text()) if await self.page.wait_for_selector(address_xpath, timeout=5000).count() > 0 else ""
                business.website = (await self.page.locator(website_xpath).inner_text()) if await self.page.wait_for_selector(website_xpath, timeout=5000).count() > 0 else ""
                business.phone_number = (await self.page.locator(phone_number_xpath).inner_text()) if await self.page.wait_for_selector(phone_number_xpath, timeout=5000).count() > 0 else ""
                business.reviews_count = int(
                    (await self.page.locator(review_count_xpath).inner_text()).split()[0].replace(',', '').strip()
                ) if await self.page.locator(review_count_xpath).count() > 0 else ""
                business.reviews_average = float(
                    (await self.page.locator(reviews_average_xpath).get_attribute(name_attr)).split()[0].replace(',', '.').strip()
                ) if await self.page.locator(reviews_average_xpath).count() > 0 else ""

                business.latitude, business.longitude = 10, 15
                business_list.append(business)
            except Exception as e:
                print(f'Error occurred: {e}')

        return business_list

    async def activate(self, keywords, lat, lng):
        async with async_playwright() as playwright:

            s = {}
            dispensary_names = [
                "Philly Green Meds",
                "Buds & Blooms Dispensary",
                "Liberty Leaf Philly",
                "Keystone Kush Dispensary",
                "Philly Herbal Haven",
                "Philly Buds Dispensary"
            ]

            for k in keywords:
                s[k] = [Business(
                    address="Example 1",
                    latitude=lat,
                    longitude=lng,
                    name=choice(dispensary_names),
                    phone_number="036888990",
                    reviews_average=choice([5.2, 4.3, 1.2, 5.8]),
                    reviews_count=randint(1, 100),
                    website="https://www.example.com",
                )]

            return s
            return await self.scrape(playwright, keywords, lng, lat)

    def display_scraped_data(self, scraped_data: ScrapeReturnType):
        """Prints the scraped business data in a readable format."""
        for keyword, businesses in scraped_data.items():
            print(f"\n🔎 Keyword: {keyword}")
            print("=" * 50)

            for idx, business in enumerate(businesses, start=1):
                print(f"📌 Business #{idx}")
                print(f"   🏢 Name: {business.name}")
                print(f"   📍 Address: {business.address}")
                print(
                    f"   🌍 Location: ({business.latitude}, {business.longitude})")
                print(f"   📞 Phone: {business.phone_number or 'N/A'}")
                print(
                    f"   🌟 Reviews: {business.reviews_average} ⭐ ({business.reviews_count} reviews)")
                print(f"   🔗 Website: {business.website or 'N/A'}")
                print("-" * 50)
