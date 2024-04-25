# Output the ply file

def ply_write(transformed_colored_pts, filename):
    total = len(transformed_colored_pts[0]) + \
            len(transformed_colored_pts[1]) + \
            len(transformed_colored_pts[2])
    with open(filename, "w+") as plyf:
        plyf.write("ply\n")
        plyf.write("format ascii 1.0\n")
        plyf.write(f"element vertex {total}\n")
        plyf.write("property float x\n")
        plyf.write("property float y\n")
        plyf.write("property float z\n")
        plyf.write("property uchar red\n")
        plyf.write("property uchar green\n")
        plyf.write("property uchar blue\n")
        plyf.write("element face 0\n")
        plyf.write("end_header\n")
        for i in range(3):
            for j in range(len(transformed_colored_pts[i])):
                pt, color = transformed_colored_pts[i][j]
                _, _, X, Y, Z = pt
                r, g, b = color
                plyf.write("{0} {1} {2} {3} {4} {5}\n".format(float(X), float(Y),
                                                              float(Z), int(r),
                                                              int(g), int(b)))
        plyf.write("\n")