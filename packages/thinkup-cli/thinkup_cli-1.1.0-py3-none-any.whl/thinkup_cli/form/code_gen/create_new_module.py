import os
import re
from thinkup_cli.form.code_gen.create_new_screen import _get_directories
from thinkup_cli.utils.code_templates.module.update_app_gradle import update_app_gradle
from thinkup_cli.utils.code_templates.module.update_settings_gradle import update_settings_gradle
from thinkup_cli.utils.code_templates.module.build_gradle_template import create_build_gradle
from thinkup_cli.utils.code_templates.module.consumer_rules_pro_template import create_consumer_rules
from thinkup_cli.utils.code_templates.module.git_ignore_tempate import create_gitignore
from thinkup_cli.utils.code_templates.module.manifest_template import create_manifest
from thinkup_cli.utils.code_templates.module.proguard_rules_pro_template import create_proguard_rules
import questionary
from thinkup_cli.utils.ui import UI

def valid_module_name(value):

    if not value:
        return True

    pattern = r'^[a-zA-Z]+(?:-[a-zA-Z]+)*$'
    return bool(re.match(pattern, value))

def _print_header():
    UI().clear()
    UI().pheader(f"Create new module")
    UI().pline()
    UI().ptext(f"│  Working directory:")
    UI().ptext(f"│  {os.getcwd()}")
    UI().pline()

def _new_module_form(base_namespace):
    new_module = questionary.unsafe_prompt([
                    {
                        'type': 'input',
                        'name': 'name',
                        'message': f'Enter module name',
                        'validate': lambda val: 'Invalid format. Ej. web-view' if not valid_module_name(val) else True,
                    }])["name"]
    src_main_path = os.path.join("feature", new_module, "src", "main")
    
    namespace_name = new_module.replace("-", "_")

    kotlin_path = os.path.join(src_main_path, "java", base_namespace, namespace_name)

    os.makedirs(kotlin_path, exist_ok=True)

    return new_module, namespace_name


def create_new_module():
    initial_path = os.getcwd()
    
    os.chdir("feature")
    next_dir = _get_directories()[-1]
    while next_dir != 'feature':
        os.chdir(next_dir)
        next_dir = _get_directories()[-1]
    os.chdir(next_dir)
    base_namespace = os.getcwd().split("java"+os.sep)[-1]
    os.chdir(initial_path)

    UI().clear()
    _print_header()
    new_module, namespace = _new_module_form(base_namespace)

    os.chdir("app")
    update_app_gradle(new_module)
    os.chdir("..")

    update_settings_gradle(new_module)

    os.chdir(os.path.join("feature", new_module))
    create_gitignore()
    create_build_gradle( base_namespace.replace(os.sep,".") + "." + namespace)
    create_consumer_rules()
    create_proguard_rules()

    os.chdir(os.path.join("src", "main"))
    create_manifest()

    os.chdir(initial_path)

    UI().psuccess()


