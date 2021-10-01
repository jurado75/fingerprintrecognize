import os
from core.compressed_images import compress_image
from core.searcher_images import compare_images

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DIR_DATASET_COMPRESSED = 'images-dataset-compressed'
R_VALUE = 500


def compressed_dataset(dataset_path):
    if not os.path.isdir(dataset_path):
        return Exception('The directory dataset does not exist or is not available directory')
    for file_j in os.listdir(dataset_path):
        path_j_subdir = os.path.join(dataset_path, file_j)
        if os.path.isdir(path_j_subdir):
            path_subdir_compressed = ROOT_DIR + '\\' + DIR_DATASET_COMPRESSED + '\\' + file_j + '\\'
            os.makedirs(path_subdir_compressed, exist_ok=True)
            for file_i in os.listdir(path_j_subdir):
                path_i_subdir_file = os.path.join(path_j_subdir, file_i)
                path_i_subdir_file_compressed = path_subdir_compressed + file_i
                if os.path.isfile(path_i_subdir_file) and not os.path.isfile(path_i_subdir_file_compressed):
                    compress_image(path_i_subdir_file, path_i_subdir_file_compressed, R_VALUE)


def query_image(image_to_query):
    path_subdir_compressed = ROOT_DIR + '\\' + DIR_DATASET_COMPRESSED + '\\'
    for file_j in os.listdir(path_subdir_compressed):
        path_j_subdir = os.path.join(path_subdir_compressed, file_j)
        if os.path.isdir(path_j_subdir):
            for file_i in os.listdir(path_j_subdir):
                path_i_subdir_file = os.path.join(path_j_subdir, file_i)
                if compare_images(image_to_query, path_i_subdir_file):
                    return file_j, file_i
    return False


if __name__ == '__main__':
    print('Compressed images dataset with r 500')
    compressed_dataset('./images-dataset')
    path_image_query = input('Type path of image you want to search matches in dataset: ')
    result = query_image(path_image_query)
    if not result:
        print('There isn\'t image that can math with your image query in dataset')
    else:
        print('Find match with one image in dir %s and name %s' % (result[0], result[1]))
