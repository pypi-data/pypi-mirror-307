import base64
import os

from thinkup_cli.form.code_gen.code_gen_form import get_code_gen_menu_form
from thinkup_cli.form.code_gen.create_new_screen import create_new_screen
from thinkup_cli.form.code_gen.create_new_module import create_new_module
from thinkup_cli.entities.app import App
from thinkup_cli.form.text_review.get_from_remote_config import get_from_remote_config
from thinkup_cli.form.text_review.local_strings_template import create_local_strings
from thinkup_cli.form.text_review.review_figma import review_figma
from thinkup_cli.form.text_review.text_review_form import get_text_review_menu_form
from thinkup_cli.form.text_review.update_remote_config import update_remote_config
from thinkup_cli.utils.ui_menu import UIMenu, UIMenuOptions
from thinkup_cli.utils.singleton import singleton
from thinkup_cli.utils.ui import UI


@singleton
class Menu:

    @staticmethod
    def code_gen_menu():
        working_directory = os.getcwd()
        UI().clear()
        UI().pheader(f"ANDROID CODE GENERATION")
        UI().pline()
        UI().ptext(f"│  Working directory:")
        UI().ptext(f"│  {working_directory}")
        if (not os.path.exists("settings.gradle.kts")):
            UI().ptext('│  <y>WARNING:</y> This doesn\'t seem to be the right directory.')
        UI().pline()
        UI().ptext('<g>Options</g>')

        result = get_code_gen_menu_form()
        if result == -1:
            return

        if result == "SCREEN":
            create_new_screen()
        else:
            create_new_module()
    
    @staticmethod
    def text_review_menu():
        UI().clear()
        UI().pheader(f"TEXT REVIEW")
        UI().pline()
        UI().ptext(f"│  Working directory:")
        UI().ptext(f"│  {os.getcwd()}")
        UI().pline()
        UI().ptext('<g>Options</g>')

        result = get_text_review_menu_form()
        if result == -1:
            return
        if result == "GET":
            get_from_remote_config()
        elif result == "REVIEW":
            review_figma()
        elif result == "UPDATE":
            update_remote_config()
        else:
            create_local_strings()


    # MAIN MENU ------------------------------------
    def main_menu(self):
        options = [
            ("1", f"Android Code Generation", self.code_gen_menu),
            ("2", f"Text Review", self.text_review_menu),
        ]

        menu = UIMenuOptions(
            type="main_menu",
            top=f"<y>ThinkUp CLI</y> │ <gray>{App().version}</gray>",
            options=options
        )

        UIMenu().print_menu(menu)
