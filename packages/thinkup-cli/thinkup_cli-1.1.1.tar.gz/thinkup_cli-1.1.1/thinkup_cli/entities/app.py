import os

import questionary
from thinkup_cli.entities.setting import Settings
from thinkup_cli.utils.singleton import singleton


@singleton
class App:
    version: str = "1.1.1"

    def init(self):
        os.system('printf "\033c"')
        os.system('cls' if os.name == 'nt' else 'clear')
        Settings().init()
        self.init_install()

    @staticmethod
    def close():
        os.system('printf "\033c"')
        os.system('cls' if os.name == 'nt' else 'clear')
        exit()
    
    def init_install(self):
        gemini_api_key = Settings().config['gemini_api_key']
        if not gemini_api_key or gemini_api_key == "":
            try:
                input = questionary.unsafe_prompt([
                        {
                            'type': 'input',
                            'name': 'gemini_api_key',
                            'message': f'Enter your Gemini API key or empty to skip (https://aistudio.google.com/app/apikey)',
                        }])
                Settings().config['gemini_api_key'] = input['gemini_api_key']
                Settings().save()
            except KeyboardInterrupt:
                self.close()