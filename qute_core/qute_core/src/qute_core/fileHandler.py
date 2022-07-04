import os


class FileHandler(object):

    def __init__(self, path, name):
        self.path = path
        self.name = name

    def check_file(self):
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file == self.name:
                    return True
            else:
                return False
