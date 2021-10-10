import cv2
import os


def compare_images(image_search, image_compare):
    # if os.path.exists('image-search-compressed.jpg'):
    images_equals = False
    image_query = cv2.imread(image_search)
    image_analyze = cv2.imread(image_compare)
    if image_query.shape == image_analyze.shape:
        difference = cv2.subtract(image_query, image_analyze)
        b, g, r = cv2.split(difference)
        images_equals = cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0

    shift = cv2.SIFT_create()
    kp_1, desc_1 = shift.detectAndCompute(image_query, None)
    kp_2, desc_2 = shift.detectAndCompute(image_analyze, None)

    index_params = dict(algorithm=0, trees=5)
    search_params = dict()

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(desc_1, desc_2, k=2)

    good_points = []
    for m, n in matches:
        if m.distance < 0.6 * n.distance:
            good_points.append(m)

    if len(kp_1) <= len(kp_2):
        number_keypoints = len(kp_1)
    else:
        number_keypoints = len(kp_2)

    percentage_to_match = len(good_points) / number_keypoints * 100

    if images_equals or percentage_to_match > 65:
        return True
    return False


if __name__ == '__main__':
    image_to_search = "./images-dataset/sub1/11.jpg"
    image_to_compare = "./images-dataset/sub1/11.jpg"
    result = compare_images(image_to_search, image_to_compare)
    print(result)
