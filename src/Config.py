import yaml


class Config:

    data_folder: str

    def __init__(self, file_path: str):
        with open(file_path) as file:
            config = yaml.full_load(file.read())
            data_folder = config.get("data_folder", None)
            assert data_folder is not None, "Missing data folder"
            self.data_folder = data_folder
