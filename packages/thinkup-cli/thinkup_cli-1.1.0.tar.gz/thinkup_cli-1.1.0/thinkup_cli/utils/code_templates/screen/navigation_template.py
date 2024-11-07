def firstLowerCase(string):
    return string[0].lower() + string[1:]

def create_navigation(name,package):
    filename = name + "ScreenNavigation.kt"
    file_content = f'''package {package}

import androidx.navigation.NavController
import androidx.navigation.NavGraphBuilder
import androidx.navigation.NavOptionsBuilder
import androidx.navigation.compose.composable
import com.thinkup.core.base.navigation.BaseScreenNavigation

private const val screenRoute = \"{firstLowerCase(name)}\"

internal object {name}ScreenNavigation : BaseScreenNavigation(
    baseRoute = screenRoute,
)

fun NavGraphBuilder.{firstLowerCase(name)}Screen(
    navigate: (String) -> Unit,
) {{
    composable(
        route = {name}ScreenNavigation.fullRoute,
    ) {{
        {name}Screen(
            navigate = navigate
        )
    }}
}}

fun NavController.navigateTo{name}Screen(navOptionsBuilder: NavOptionsBuilder.() -> Unit = {{}}) {{
    this.navigate({name}ScreenNavigation.fullRoute, navOptionsBuilder)
}}
'''
    with open(filename, "w") as file:
        file.write(file_content)