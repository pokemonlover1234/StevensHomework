import Image
import Filter
import Gaussian
import Hessian
import Hough
import RANSAC

def main():
    image = Image.get_image("./road.png")
    filtered = Filter.apply_filter(image, Gaussian.gaussian_filter(sigma = 1)) 
    hessian_responses = Hessian.get_responses(filtered)
    image_ransac = Image.copy_image(image)
    image_ransac = RANSAC.apply_RANSAC(hessian_responses, image_ransac)
    Image.save_image(Image.to_array(image_ransac), "road_RANSAC.png")
    image_hough = Image.copy_image(image)
    image_hough = Hough.apply_hough(hessian_responses, image_hough)
    Image.save_image(Image.to_array(image_hough), "road_Hough.png")

if __name__ == '__main__':
    main()