import asyncio
from services.scraping.main import ScrapeGoogleMapsSearch


async def test_scrapped_data():

    scrape_data = ScrapeGoogleMapsSearch(10)
    d = [
        await scrape_data.activate(
            keywords=["Vape shop"],
            lat=29.882100506069165,
            lng=-95.56051171538272
        ),
        await scrape_data.activate(
            keywords=["bar"],
            lat=52.51603613511733,
            lng=13.394612597346114
        )
    ]

    scrape_data.display_scraped_data(d[0])
    scrape_data.display_scraped_data(d[1])
    # scrape_data.display_scraped_data(d[1])

if __name__ == "__main__":

    asyncio.run(test_scrapped_data())
