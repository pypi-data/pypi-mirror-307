import os
import json

from thinkup_cli.utils.singleton import singleton

DIR_NAME = '.thinkupcli'
DEFAULT_FILE_NAME = 'thinkup-cli-config.json'
DEFAULT_SETTING = {
    "gemini_api_key": ""
}


@singleton
class Settings:
    directory = os.path.join(os.path.expanduser('~'), DIR_NAME)
    file_path = os.path.join(directory, DEFAULT_FILE_NAME)
    use_custom = False
    config = None

    def init(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as config_file:
                json.dump(DEFAULT_SETTING, config_file, indent=4)

        self.load()

    def load(self):
        with open(self.file_path, "r") as config_file:
            self.config = json.load(config_file)
        return self.config

    def save(self):
        with open(self.file_path, "w") as config_file:
            json.dump(self.config, config_file, indent=4)
        return self.config