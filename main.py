from lib.radius_grid.GridGenerator import GridGenerator
from lib.utilities.Spinner import Spinner
from lib.utilities.Json import Json
import asyncio


async def main():
    grid_generator = GridGenerator()

    address = "Bammel S.M.O.K.E Shop | CBD| Kratom| Vape Shop| Hookah| Delta 8| THC-O| THC Vape | THC Flower"
    spinner = Spinner()

    spinner.start()
    analysis = await grid_generator.run(
        address=address,
        cid="6311414705666154752",
        keywords=[
            "Tobacco shop",
            "Cigar shop",
            "Hookah Shop",
            "Vaporiser Shop",
            "Tobacco supplier"
        ],
        radius_km=50,
        step_km=5
    )

    spinner.stop()


if __name__ == "__main__":
    asyncio.run(main())
