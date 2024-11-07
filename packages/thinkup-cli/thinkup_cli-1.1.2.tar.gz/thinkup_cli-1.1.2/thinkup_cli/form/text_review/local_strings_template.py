from thinkup_cli.utils.file import get_json_from_rc_file
from thinkup_cli.utils.ui import UI
import json


def create_local_strings():
    file_name = "AppString.kt"
    json_rc = get_json_from_rc_file()
    with open("local_backup.json", "w") as file:
        file.write(json.dumps(json_rc))
    strings = ""
    for key in json_rc:
        strings += f"    {key.upper()}(\"{key}\"),\n"
    
    file_content = f'''package com.thinkup.stringmanager.strings

import androidx.compose.runtime.Composable

/*@Composable
fun AppString.getStringComposable(): String = StringResources.getStringComposable(this.key)*/

fun AppString.getString(): String = StringResources.getString(this.key)

enum class AppString(val key: String) {{
{strings}
}}

    '''
    with open(file_name, "w") as file:
        file.write(file_content)
    UI().psuccess(f'Strings object created')
    