import questionary
from prompt_toolkit.styles import Style

from thinkup_cli.utils.configs import custom_style


def get_text_review_menu_form():
    try:
        type_choices = [
            'Get current version in Remote Config', 'Review Figma file', 'Update Remote Config', 'Generate Local Android Strings'
        ]

        result = questionary.unsafe_prompt(
            {
                'type': 'select',
                'name': 'value',
                'message': 'What do you want to do?',
                'choices': type_choices,
                'style': custom_style
            }
        )

        if result['value'] == type_choices[0]:
            return "GET"
        elif result['value'] == type_choices[1]:
            return "REVIEW"
        elif result['value'] == type_choices[2]:
            return "UPDATE"
        else:
            return "LOCAL_ANDROID"
    except KeyboardInterrupt:
        return -1
