import SAD_Stereo
import RankTransform
import GroundTruthError
import Image
import numpy as np

def main():
    GroundTruth = Image.get_image("../teddy/disp2.pgm")
    L = Image.get_image("../teddy/teddyL.pgm")
    R = Image.get_image("../teddy/teddyR.pgm")
    RankTL = RankTransform.rank_transform(L)
    RankTR = RankTransform.rank_transform(R)
    DispMap3, PKRN3 = SAD_Stereo.SAD(RankTL, RankTR, 3)
    DispMap15, PKRN15 = SAD_Stereo.SAD(RankTL, RankTR, 15)
    Image.save_image(SAD_Stereo.normalize_SAD(DispMap3), "../Output/P1/DispMap3.pgm")
    print(f"Error 3x3 Window: {GroundTruthError.GroundTruthErr(GroundTruth, DispMap3)}")
    print(f"Error 15x15 Window: {GroundTruthError.GroundTruthErr(GroundTruth, DispMap15)}")
    PKRN3Err, PKRNKept = GroundTruthError.GroundTruthErrPKRN(GroundTruth, DispMap3, PKRN3)
    print(f"PKRN Error 3x3 Window: {PKRN3Err}, Kept Pixels = {PKRNKept}")
if __name__ == "__main__":
    main()