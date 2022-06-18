import time
import numpy as np
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from alaas.server.util import S3Downloader, load_image_data_as_np


def download_func(data_url):
    home_path = str(Path.home())
    alaas_home = home_path + "/.alaas/"
    data_save_path = alaas_home + data_url
    S3Downloader("", "", "alaas") \
        .download(data_save_path, data_url)
    return data_save_path


def download_data(data_urls, asynchronous=False):
    path_list = []
    proc_threads = []
    home_path = str(Path.home())
    alaas_home = home_path + "/.alaas/"
    executor = ThreadPoolExecutor(10)
    for url in data_urls:
        if asynchronous:
            proc_threads.append(executor.submit(download_func, data_url=url))
        else:
            data_save_path = alaas_home + url
            S3Downloader("AKIATRAD26AYIF25OYX3", "YsLd4F7kK+gd/kbP6u3692Sv5i5rkEJsdIXhrs1/", "alaas") \
                .download(data_save_path, url)
            path_list.append(data_save_path)
    for thread in proc_threads:
        path_list.append(thread.result())
    return path_list


def prepare_data(path_list):
    image_list = []
    for pth in path_list:
        image_list.append(load_image_data_as_np(pth))
    return np.array(image_list, dtype=np.float32)


if __name__ == '__main__':
    start_time = time.time()
    pool_size = 50000
    with open(f"cifar_s3_{pool_size}.txt") as file:
        url_list = [line.rstrip() for line in file.readlines()]
        data_path = download_data(url_list)
    download_time = time.time()
    # TODO: MODAL
    al_end_time = time.time()