import Image
from Camera import Camera
from VoxelGrid import VoxelGrid
from tqdm import trange, tqdm
import numpy as np
import xml.etree.ElementTree as ET


# Load a projection matrix from an xml file in the calibration folder.
def load_P_from_xml(file):
    tree = ET.parse(file)
    root = tree.getroot()
    Ptext = root.text
    Psplit = Ptext.split(" ")
    Pvals = []
    for elem in Psplit:
        if elem == "":
            pass
        else:
            Pvals.append(float(elem))
    P = np.matrix(np.array(Pvals).reshape((3, 4)))
    return P


# For every voxel in the provided grid, determine
# whether it is occupied or free, and whether it
# is a boundary voxel. Returns a list of boundary
# voxels.
def process_voxels(V, cameras):
    boundary_voxels = set()
    occupied_indices = np.zeros(V.grid.shape[:3], np.bool8)
    for i in trange(V.grid.shape[0], desc="Processing..."):
        for j in trange(V.grid.shape[1], leave=False):
            for k in range(V.grid.shape[2]):
                free = False
                X, Y, Z = V.index_to_coords(i, j, k)
                for c in cameras:
                    # If voxel is not in the silhouette of a camera, it
                    # is free. No need to check rest of cameras.
                    if not c.get_silhouette_presence(X, Y, Z):
                        free = True
                        break
                # If all cameras have this voxel in their silhouette, it
                # is occupied.
                if not free:
                    V.set_voxel(X, Y, Z, [255, 255, 255])
                    occupied_indices[i, j, k] = True
                # Check for difference between this voxel and priors,
                # in order to set boundary voxels. Only check:
                #   i - i, j ,k
                #   i, j - 1, k
                #   i, j, k - 1
                # Since these have already been checked for free/occupied.
                # If any of these 3 are of a different state than this voxel
                # then set all of the different ones, as well as this voxel,
                # to a boundary. Explained further in PDF
                r1, g1, b1 = V.grid[i, j, k]

                if free != (not occupied_indices[i - 1, j, k]) and i > 0:
                    r2, g2, b2 = V.grid[i - 1, j, k]
                    boundary_voxels.add((i, j, k, r1, g1, b1))
                    boundary_voxels.add((i - 1, j, k, r2, g2, b2))
                if free != (not occupied_indices[i, j - 1, k]) and j > 0:
                    r2, g2, b2 = V.grid[i, j - 1, k]
                    boundary_voxels.add((i, j, k, r1, g1, b1))
                    boundary_voxels.add((i, j - 1, k, r2, g2, b2))
                if free != (not occupied_indices[i, j, k - 1]) and k > 0:
                    r2, g2, b2 = V.grid[i, j, k - 1]
                    boundary_voxels.add((i, j, k, r1, g1, b1))
                    boundary_voxels.add((i, j, k - 1, r2, g2, b2))
    return boundary_voxels


# Creates the PLY file for the boundary voxel array provided
def create_ply(V, boundary, cameras):
    b = list(boundary)
    # Discard free boundary voxels
    b = list(filter(lambda elem: not (elem[3] == 0 and elem[4] == 0
                    and elem[5] == 0), b))
    b_colored = []
    print("Determining point colors.")
    for voxel in tqdm(b):
        i, j, k = voxel[0], voxel[1], voxel[2]
        X, Y, Z = V.index_to_coords(i, j, k)
        r, g, bl = V.calc_color(X, Y, Z, cameras)
        b_colored.append((i, j, k, r, g, bl))
    print("Creating PLY file.")
    with open("../Output/output.ply", "w+") as plyf:
        plyf.write("ply\n")
        plyf.write("format ascii 1.0\n")
        plyf.write(f"element vertex {len(b_colored)}\n")
        plyf.write("property float x\n")
        plyf.write("property float y\n")
        plyf.write("property float z\n")
        plyf.write("property uchar red\n")
        plyf.write("property uchar green\n")
        plyf.write("property uchar blue\n")
        plyf.write("element face 0\n")
        plyf.write("end_header\n")
        for voxel in b_colored:
            X, Y, Z = V.index_to_coords(voxel[0], voxel[1], voxel[2])
            r, g, b = voxel[3], voxel[4], voxel[5]
            plyf.write("{0} {1} {2} {3} {4} {5}\n".format(float(X), float(Y),
                                                          float(Z), int(r),
                                                          int(g), int(b)))
        plyf.write("\n")


def main():
    # Define images
    Ps = []
    images = []
    silhouettes = []
    cameras = []
    print("Loading projection matrices.")
    for i in range(8):
        P = load_P_from_xml(f"../calibration/cam0{i}.xml")
        Ps.append(P)
    print("Loading images.")
    for i in range(8):
        image = Image.get_image(f"../cam0{i}_00023_0000008550.png")
        images.append(image)
    print("Loading silhouettes.")
    for i in range(8):
        silhouette = Image.get_image(f"../silh_cam0{i}_00023_0000008550.pbm")
        silhouettes.append(silhouette)
    print("Creating camera objects.")
    for i in range(8):
        camera = Camera(Ps[i], images[i], silhouettes[i])
        cameras.append(camera)
    print("Creating voxel grid.")
    V = VoxelGrid()
    print("Processing voxels.")
    boundary = process_voxels(V, cameras)
    create_ply(V, boundary, cameras)
    print("Done.")


if __name__ == "__main__":
    main()
