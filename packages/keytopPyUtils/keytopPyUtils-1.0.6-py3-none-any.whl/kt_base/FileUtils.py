import os.path

class FileUtils:
    @staticmethod
    def create_paths(path):
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def read_file(path):
        content = ''
        with open(path,'r',encoding='utf-8') as file:
            content = file.read()
        return content
#FileUtils.create_paths("D:/home/data/mdconverter/")