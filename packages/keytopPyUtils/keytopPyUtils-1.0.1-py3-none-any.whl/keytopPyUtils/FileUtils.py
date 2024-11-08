import os.path

class FileUtils:
    @staticmethod
    def create_paths(path):
        if not os.path.exists(path):
            os.makedirs(path)

FileUtils.create_paths("D:/home/data/mdconverter/")