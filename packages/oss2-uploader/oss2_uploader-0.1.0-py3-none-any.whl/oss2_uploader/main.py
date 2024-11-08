from multiprocessing import Process
import os
import sys
import pathlib
from typing import List

import tqdm
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider


def split_array(array, n):
    """Splits an array into n pieces as evenly as possible.

    Args:
        array: The array to split.
        n: The number of pieces to split the array into.

    Returns:
        A list of lists, where each sublist is a piece of the original array.
    """
    chunk_size = len(array) // n  # Integer division for even floor
    remainder = len(array) % n

    pieces = []
    start = 0
    for i in range(n):
        end = start + chunk_size + (1 if i < remainder else 0)
        pieces.append(array[start:end])
        start = end

    return pieces


class UploadTask(Process):

    def __init__(
        self, file_list, bucket_name, oss_endpoint, oss_path="", process_idx=""
    ) -> None:

        # execute the base constructor
        Process.__init__(self)

        self.file_list = file_list
        self.oss_path = oss_path
        self.process_idx = process_idx

        # if oss_path is empty, take the last folder name of the first file
        if not oss_path:
            self.oss_path = os.path.basename(os.path.dirname(file_list[0])) + "/"

        # 使用环境变量中获取的RAM用户的访问密钥配置访问凭证。
        auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())

        # yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
        # 填写Bucket名称，并设置连接超时时间为30秒。
        self.bucket = oss2.Bucket(auth, oss_endpoint, bucket_name, connect_timeout=30)

    def run(self) -> None:
        """
        list all files in the upload_dir and upload them to oss, not checking sub directories
        """

        for filepath in tqdm.tqdm(
            self.file_list,
            position=self.process_idx,
            desc=f"Process {self.process_idx}",
        ):
            if not os.path.isfile(filepath):
                continue

            filename = os.path.basename(filepath)

            target_path = f"{self.oss_path}{filename}"

            # check if the file already exists in oss
            if self.bucket.object_exists(target_path):
                # print(f"{self.process_idx}: {target_path} already exists in oss")
                continue

            self.bucket.put_object_from_file(
                f"{target_path}",
                filepath,
            )

            # print(f"{self.process_idx}: uploaded {filepath} to {target_path}")


def folder_uploader(folder_path, bucket_name, oss_endpoint, oss_path=None):

    folder_path = os.path.abspath(folder_path)

    if not os.path.exists(folder_path):
        print(f"{folder_path} does not exist")
        sys.exit(1)

    # get all files in the folder
    all_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path)]

    # get cpu count
    cpu_count = os.cpu_count()

    # split the files into cpu_count parts
    file_chunks = split_array(all_files, cpu_count)

    # create a process for each chunk
    processes = [
        UploadTask(
            file_list=chunk,
            bucket_name=bucket_name,
            oss_path=oss_path,
            oss_endpoint=oss_endpoint,
            process_idx=i,
        )
        for i, chunk in enumerate(file_chunks)
    ]

    print(
        f"Uploading {len(all_files)} files to {bucket_name} using {cpu_count} processes"
    )

    # run the process,
    for process in processes:
        process.start()

    for process in processes:
        process.join()


class DopwnloadTask(Process):

    def __init__(self, bucket, osskey_list, target_dir, process_idx="") -> None:

        # execute the base constructor
        Process.__init__(self)

        self.osskey_list = osskey_list
        self.target_dir = target_dir
        self.process_idx = process_idx

        self.bucket = bucket

    def run(self) -> None:
        """
        list all files in the upload_dir and upload them to oss, not checking sub directories
        """

        for osskey in tqdm.tqdm(
            self.osskey_list,
            position=self.process_idx,
            desc=f"Process {self.process_idx}",
        ):
            # split `osskey` into `path` and `filename`
            filename = osskey.split("/")[-1]

            target_path = os.path.join(self.target_dir, filename)

            if os.path.isfile(target_path):
                continue

            self.bucket.get_object_to_file(osskey, target_path)


def folder_downloader(bucket_name, oss_endpoint, oss_prefix, target_dir):

    # 使用环境变量中获取的RAM用户的访问密钥配置访问凭证。
    auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())

    # yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
    # 填写Bucket名称，并设置连接超时时间为30秒。
    bucket = oss2.Bucket(auth, oss_endpoint, bucket_name, connect_timeout=30)

    # list all files in the oss_prefix
    osskey_list = [obj.key for obj in oss2.ObjectIterator(bucket, prefix=oss_prefix)]

    # get cpu count
    cpu_count = os.cpu_count()

    print(
        f"Downloading {len(osskey_list)} files from {bucket_name} using {cpu_count} processes"
    )

    # split the files into cpu_count parts
    file_chunks = split_array(osskey_list, cpu_count)

    os.makedirs(target_dir, exist_ok=True)

    # create a process for each chunk
    processes = [
        DopwnloadTask(
            bucket=bucket,
            osskey_list=chunk,
            target_dir=target_dir,
            process_idx=i,
        )
        for i, chunk in enumerate(file_chunks)
    ]

    # run the process,
    for process in processes:
        process.start()

    for process in processes:
        process.join()


def folder_uploader_sync(folder_path, bucket_name, oss_endpoint):

    folder_path = os.path.abspath(folder_path)

    if not os.path.exists(folder_path):
        print(f"{folder_path} does not exist")
        sys.exit(1)

    path_delimiter = os.path.sep
    all_oos_path = []

    # get all files in the folder recursively
    all_files: List[str] = [
        str(f) for f in pathlib.Path(folder_path).rglob("*") if f.is_file()
    ]

    for filepath in all_files:

        # remove the prefix `folder_path` from the file path
        sub_path = filepath[len(folder_path) + 1 :]

        all_oos_path.append("/".join(sub_path.split(path_delimiter)))

    # create a bucket
    auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
    bucket = oss2.Bucket(auth, oss_endpoint, bucket_name, connect_timeout=30)

    print(f"Total files to upload: {len(all_files)}")

    # upload all files
    for i, filepath in enumerate(tqdm.tqdm(all_files, desc="Uploading files")):
        if not os.path.isfile(filepath):
            continue

        target_path = all_oos_path[i]

        # check if the file already exists in oss
        if bucket.object_exists(target_path):
            # print(f"{self.process_idx}: {target_path} already exists in oss")
            continue

        bucket.put_object_from_file(
            target_path,
            filepath,
        )


if __name__ == "__main__":

    def load_env_from_file(file_path: str = None):
        """
        Loads environment variables from a local file.

        Args:
            file_path (str): Path to the environment variable file.

        Returns:
            dict: Dictionary containing the loaded environment variables.
        """

        if file_path is None:
            file_path = os.path.join(os.path.dirname(__file__), ".env")

        if not os.path.exists(file_path):
            raise ValueError(f"Environment variable file not found: {file_path}")

        # Open the file and read its lines
        with open(file_path, "r") as file:
            lines = file.readlines()

        # Load variables into a dictionary
        for line in lines:
            line = line.strip()  # Remove leading/trailing whitespace
            if not line or line.startswith("#"):  # Skip empty lines and comments
                continue
            key, value = line.split("=", 1)  # Split line by `=`
            # Remove leading/trailing quotes from key and value
            os.environ[key.strip()] = value.strip()

    load_env_from_file(
        file_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env")
    )

    folder_uploader_sync(
        os.path.join(os.path.expanduser("~"), "Documents", "test111"),
        "video2motion-pretrain",
        "oss-ap-southeast-1.aliyuncs.com",
    )
