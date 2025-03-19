from lib.radius_grid.GridGenerator import GridGenerator
from lib.utilities.Spinner import Spinner
from lib.utilities.Json import Json
import asyncio
from services.scraping.main import ScrapeGoogleMapsSearch


async def main():
    grid_generator = GridGenerator()

    address = "Bammel S.M.O.K.E Shop | CBD| Kratom| Vape Shop| Hookah| Delta 8| THC-O| THC Vape | THC Flower"
    spinner = Spinner()

    spinner.start()
    analysis = await grid_generator.run(
        address=address,
        cid="Bammel S.M.O.K.E Shop | CBD| Kratom| Vape Shop| Hookah| Delta 8| THC-O| THC Vape | THC Flower",
        keywords=[
            "Vape shop",
            "Restaurant"
        ],
        radius_km=2,
        step_km=1
    )

    spinner.stop()


async def test_scrapped_data():

    scrape_data = ScrapeGoogleMapsSearch(10)
    d = [
        await scrape_data.activate(
            keywords=["restaurant"],
            lat=29.93605980242429,
            lng=-95.49824496675434
        ),
        await scrape_data.activate(
            keywords=["bar"],
            lat=52.51603613511733,
            lng=13.394612597346114
        )
    ]

    scrape_data.display_scraped_data(d[0])
    scrape_data.display_scraped_data(d[1])

if __name__ == "__main__":

    test = False

    if test:

        asyncio.run(test_scrapped_data())

    else:
        asyncio.run(main())
