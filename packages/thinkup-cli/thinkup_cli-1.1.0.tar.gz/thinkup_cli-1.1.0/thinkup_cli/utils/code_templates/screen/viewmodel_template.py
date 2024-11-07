def create_viewmodel(name, package):
    file_name = name + "ViewModel.kt"
    file_content = f'''package {package}

import androidx.compose.runtime.Immutable
import com.thinkup.core.base.state.BaseAction
import com.thinkup.core.base.state.BaseEvent
import com.thinkup.core.base.state.BaseState
import com.thinkup.core.base.state.BaseViewModel
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject

@HiltViewModel
class {name}ViewModel @Inject constructor(

) : BaseViewModel<{name}ViewModel.State, {name}ViewModel.UIEvent, {name}ViewModel.Action>(State()) {{

    override fun onEvent(event: UIEvent) {{
        when (event) {{
            UIEvent.ClearDestination -> sendAction(Action.DestinationChange(null))
        }}
    }}

    override fun reduce(action: Action): State {{
        return when (action) {{
            is Action.DestinationChange -> State(action.destination)
        }}
    }}

    @Immutable
    sealed class UIEvent : BaseEvent {{
        object ClearDestination : UIEvent()
    }}

    @Immutable
    sealed class Action : BaseAction {{
        data class DestinationChange(val destination: State.Destination?) : Action()
    }}

    @Immutable
    data class State(
        val destination: Destination? = null
    ) : BaseState {{
        sealed class Destination {{
            data class DeepLink(val value: String) : Destination()
        }}
    }}
}}
'''
    with open(file_name, "w") as file:
        file.write(file_content)
