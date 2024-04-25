import Image
import KMeans
import SLIC
import Classification
import numpy as np
def main():
    whitetower = Image.get_image("white-tower.png")
    KMeansTower = KMeans.kmeans_rgb(whitetower, 10)
    Image.save_image(KMeansTower, "white-tower-kmeans.png")
    wtslic = Image.get_image("wt_slic.png")
    slicwhitetower = SLIC.do_SLIC(whitetower)
    slicwtslic = SLIC.do_SLIC(wtslic)
    Image.save_image(np.floor(slicwhitetower).astype(np.uint8), "white-tower-slic.png")
    Image.save_image(np.floor(slicwtslic).astype(np.uint8), "wt_slic-slic.png")
    train_unlabeled = Image.get_image("sky/sky_train.jpg")
    train_labeled = Image.get_image("sky/sky_train_labeled.jpg")
    input_images = []
    for i in range(1,5):
         input_images.append(Image.get_image(f"sky/sky_test{i}.jpg"))
    output_images = Classification.do_classification(train_labeled, train_unlabeled, input_images)
    for i in range(4):
        Image.save_image(np.floor(output_images[i]).astype(np.uint8), f"sky/sky_output{i+1}.jpg")
if __name__ == "__main__":
    main()