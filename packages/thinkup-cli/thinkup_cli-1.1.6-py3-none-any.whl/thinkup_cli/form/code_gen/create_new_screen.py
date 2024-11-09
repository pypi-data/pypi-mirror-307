import os
from thinkup_cli.utils.code_templates.screen.screen_template import create_screen
from thinkup_cli.utils.code_templates.screen.navigation_template import create_navigation
from thinkup_cli.utils.code_templates.screen.viewmodel_template import create_viewmodel
import questionary
from thinkup_cli.utils.ui import UI
from thinkup_cli.utils.configs import custom_style

def _get_directories():
    list = os.listdir(".")
    filtered = []
    for item in list:
        if os.path.isdir(item):
            filtered.append(item)
    filtered.sort()
    return filtered

def _print_header():
    UI().clear()
    UI().pheader(f"Create new screen")
    UI().pline()
    UI().ptext(f"│  Working directory:")
    UI().ptext(f"│  {os.getcwd()}")
    UI().pline()

def _module_form():
    list = _get_directories()

    UI().ptext('<g>Picking directory</g>')
    result = questionary.unsafe_prompt(
            {
                'type': 'select',
                'name': 'module',
                'message': 'Module?',
                'choices': list,
                'style': custom_style
            }
        )
    os.chdir(result['module'])
    os.chdir("src")
    os.chdir("main")

    feature_name = result['module'].replace("-", "_")
    next_dir = _get_directories()[0]
    while next_dir != feature_name:
        os.chdir(next_dir)
        next_dir = _get_directories()[0]
    os.chdir(next_dir)


def _package_form():
    list = _get_directories()
    list.insert(0, "[CREATE HERE]")

    UI().ptext('<g>Picking directory</g>')
    result = questionary.unsafe_prompt(
            {
                'type': 'select',
                'name': 'package',
                'message': 'Package?',
                'choices': list,
                'style': custom_style
            }
        )
    if result['package'] == "[CREATE HERE]":
        return ""
    else:
        return result['package']

def _new_package_form():
    UI().ptext('<g>Creating new package</g>')
    new_package = questionary.unsafe_prompt([
                    {
                        'type': 'input',
                        'name': 'name',
                        'message': f'Enter name (empty if no package)'
                    }])["name"]
    if(new_package != ""):
        os.mkdir(new_package)
        os.chdir(new_package)

def _new_screen_form():
    UI().ptext('<g>Creating files</g>')
    return questionary.unsafe_prompt([
                    {
                        'type': 'input',
                        'name': 'name',
                        'message': f'Enter screen name',
                        'validate': lambda val: 'Title cannot be empty' if not val else True
                    }])["name"]

def create_new_screen():
    initial_path = os.getcwd()
    os.chdir("feature")

    UI().clear()
    _print_header()
    _module_form()

    package = "-"
    while(package != ""):
        UI().clear()
        _print_header()
        package = _package_form()
        if package != "":
            os.chdir(package)
    
    UI().clear()
    _print_header()
    _new_package_form()

    UI().clear()
    _print_header()
    screen_name = _new_screen_form()

    adjusted_path = os.path.join("src", "main", "java")
    package_to_import = os.getcwd().split(adjusted_path + os.sep)[1].replace(os.sep,".")
    create_screen(screen_name, package_to_import)
    create_viewmodel(screen_name, package_to_import)
    create_navigation(screen_name, package_to_import)

    os.chdir(initial_path)

    UI().psuccess()

