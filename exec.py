import asyncio
from services.scraping.main import ScrapeGoogleMapsSearch


async def test_scrapped_data():

    scrape_data = ScrapeGoogleMapsSearch(10)
    # d = [
    #     await scrape_data.activate(
    #         keywords=["restaurant"],
    #         lat=29.93605980242429,
    #         lng=-95.49824496675434
    #     ),
    #     await scrape_data.activate(
    #         keywords=["bar"],
    #         lat=52.51603613511733,
    #         lng=13.394612597346114
    #     )
    # ]

    r = await scrape_data.handle_bulk_contexts(
        [
            {
                "keywords": ["restaurant"],
                "lat": 29.93605980242429,
                "lng": -95.49824496675434
            },
            {
                "keywords": ["bar"],
                "lat": 52.51603613511733,
                "lng": 13.394612597346114
            }
        ]
    )

    scrape_data.display_scraped_data(r[0])
    scrape_data.display_scraped_data(r[1])
    # scrape_data.display_scraped_data(d[1])

if __name__ == "__main__":

    asyncio.run(test_scrapped_data())
