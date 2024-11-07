import re

def create_screen(name, package):
    file_name = name + "Screen.kt"
    file_content = f'''package {package}

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.hilt.navigation.compose.hiltViewModel
import com.thinkup.core.base.state.ContentState
import com.thinkup.core.design_system.DefaultPreview
import com.thinkup.core.design_system.text.Body1
import com.thinkup.core.design_system.theme.ThinkUpTheme

@Composable
internal fun {name}Screen(
    viewModel: {name}ViewModel = hiltViewModel(),
    navigate: (String) -> Unit
) {{
    val state by viewModel.stateFlow.collectAsState()

    LaunchedEffect(state.destination) {{
        state.destination?.let {{ destination ->
            when (destination) {{
                is {name}ViewModel.State.Destination.DeepLink -> {{
                    navigate(destination.value)
                }}
            }}
        }}
        viewModel.onEvent({name}ViewModel.UIEvent.ClearDestination)
    }}

    val serviceState by viewModel.serviceStateFlow.collectAsState()
    ContentState(
        serviceState = serviceState,
        onDismissAlert = {{ viewModel.hideAlert() }}
    ) {{
        {name}Content(
            state = state,
            onUIEvent = viewModel::onEvent
        )
    }}
}}

@Composable
private fun {name}Content(
    state: {name}ViewModel.State,
    onUIEvent: ({name}ViewModel.UIEvent) -> Unit = {{}}
) {{
    Box(
        modifier = Modifier
            .fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {{
        Body1("{name}")
    }}
}}

@Composable
@DefaultPreview
private fun ScreenPreview() {{
    ThinkUpTheme {{
        {name}Content(
            state = {name}ViewModel.State()
        )
    }}
}}
'''
    with open(file_name, "w") as file:
        file.write(file_content)