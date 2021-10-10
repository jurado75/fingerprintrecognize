import os
import sys
import threading

from math import ceil
from core.compressed_images import compress_image
from core.searcher_images import compare_images

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DIR_DATASET_COMPRESSED = 'images-dataset-compressed'
R_VALUE = 500
NUMBER_THREADS = 7
result_found = False, False, False


class QueryImageThreading(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name,
                         daemon=daemon)
        self.sub_directories = args[0]
        self.query_image = args[1]
        self.sub_directories_name = args[2]

    def run(self):
        len_sub_directories = len(self.sub_directories)
        counter = 0
        while (counter < len_sub_directories) and not result_found[0]:
            query_image_file(self.sub_directories[counter], self.query_image, self.sub_directories_name[counter])
            counter += 1


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


def query_image_file(path_dir, image_to_query, file_j) -> object:
    if os.path.isdir(path_dir):
        for file_i in os.listdir(path_dir):
            path_i_subdir_file = os.path.join(path_dir, file_i)
            if compare_images(image_to_query, path_i_subdir_file):
                print('Find match with one image in dir %s and file name %s' % (file_j, file_i))
                globals()['result_found'] = True, file_j, file_i
                if os.path.exists('image-search-compressed.jpg'):
                    os.remove('image-search-compressed.jpg')
                return file_i
    return None


def query_image(image_to_query):
    directories_database = []
    directories_database_name = []
    path_subdir_compressed = ROOT_DIR + '\\' + DIR_DATASET_COMPRESSED + '\\'
    for file_j in os.listdir(path_subdir_compressed):
        path_j_subdir = os.path.join(path_subdir_compressed, file_j)
        directories_database_name.append(file_j)
        directories_database.append(path_j_subdir)

    lower_limit = 0
    upper_limit = 0
    len_directories = len(directories_database)
    if len_directories % NUMBER_THREADS == 0:
        upper_limit = int(len_directories / NUMBER_THREADS)
    else:
        upper_limit = int(ceil((len_directories + 1) / NUMBER_THREADS))

    for i_thread in range(NUMBER_THREADS):
        finder_sub_directories = directories_database[i_thread * upper_limit: (i_thread + 1) * upper_limit]
        finder_sub_directories_names = directories_database_name[i_thread * upper_limit: (i_thread + 1) * upper_limit]
        thread_image = QueryImageThreading(
            args=(finder_sub_directories, image_to_query, finder_sub_directories_names),
            daemon=False)
        thread_image.start()


if __name__ == '__main__':
    compressed_dataset('./images-dataset')
    path_image_query = ''
    if len(sys.argv) > 1:
        path_image_query = sys.argv[1]
    else:
        path_image_query = input('Type path of image you want to search matches in dataset: ')

    # if os.path.exists('image-search-compressed.jpg'):
    #     os.remove('image-search-compressed.jpg')
    # compress_image(path_image_query, 'image-search-compressed.jpg', R_VALUE)
    query_image(path_image_query)
