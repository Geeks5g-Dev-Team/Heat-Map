from lib.radius_grid.GridGenerator import GridGenerator
from lib.utilities.Spinner import Spinner


def main():
    grid_generator = GridGenerator()

    address = "3014 W Palmira Ave STE 302, Tampa, FL 33629, United States"
    spinner = Spinner()
    spinner.start()
    analysis = grid_generator.run(
        address=address,
        cid="17185809657243164573",
        keywords=[
            "GarageDoorRepair",
            "SlidingGateRepair",
            "RollUpRepair ",
            "GateRepair",
            "GarageDoorBrokenSpring ",
            "OverheadGate",
            "GateMotorRepair ",
            "LiftmasterRepair",
            "RamsetGateMotorRepair"
        ],
        radius_km=200
    )

    print(analysis)
    spinner.stop()


if __name__ == "__main__":
    main()
