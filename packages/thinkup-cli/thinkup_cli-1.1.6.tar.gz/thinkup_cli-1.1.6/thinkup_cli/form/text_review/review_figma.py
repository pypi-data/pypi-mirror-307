import io
import questionary
import requests
import google.generativeai as genai
from thinkup_cli.entities.setting import Settings
from thinkup_cli.utils.file import get_json_from_figma_file, update_figma_file_locally
from thinkup_cli.utils.firebase import REMOTE_CONFIG_URL, get_access_token
from thinkup_cli.utils.ui import UI

def review_figma():
    genai.configure(api_key=Settings().config['gemini_api_key'])
    strings_json = get_json_from_figma_file()
    print(strings_json.replace(',', ',\n').replace('{', '{\n').replace('}', '\n}'))
    print()
    model = genai.GenerativeModel(
        model_name= "gemini-1.5-flash",
        system_instruction="You are a intelligent translator and grammar expert. You are trained to receive json and fix all issues and make suggestions to improve the texts in any way you deem fit. Since this will be used directly with code, please make sure to keep the format correct. Given a json file, you will first respond with the suggestions you would make and why you would make them (be specific, the user has to know exactly which key will change and what will be the end result), then the user may confirm all or do some modifications, after that return the json file (and only the json file) with the changes. Your responses will be printed to a console so do not use any markup, for formatting use new lines and commas.",
        )
    chat = model.start_chat()
    response = chat.send_message(strings_json)
    print(response.text)
    input = questionary.unsafe_prompt([
        {
            'type': 'input',
            'name': 'changes',
            'message': f'Do you want to confirm this changes?',
        }])
    response = chat.send_message(input['changes'])
    update_figma_file_locally(response.text)
    UI().psuccess(f'Figma file updated locally')


