import os

from pyspark.sql import SparkSession


def copy_file_to_spark(session: SparkSession, path: str):
    filename = os.path.basename(path)
    content = open(path).read()

    session.sparkContext.addFile(path)

    def write_keyfile():
        from pyspark import SparkFiles

        keyfile_path = SparkFiles.get(filename)
        with open(keyfile_path, 'w') as keyfile:
            keyfile.write(content)

    session.sparkContext.parallelize([1], 1).foreach(lambda _: write_keyfile())
