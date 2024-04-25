from P1.DLT import DLT
from P1.BilinInterp import bilin_interp
from P2.DollyEffect import dolly_effect


def main():
    H = DLT()
    bilin_interp("P1/basketball-court.ppm", H,
                 "../Output/P1/basketball-court-warped-500x940.ppm")
    dolly_effect()


if __name__ == "__main__":
    main()
