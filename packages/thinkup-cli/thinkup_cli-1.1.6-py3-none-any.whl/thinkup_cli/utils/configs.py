from enum import Enum

from prompt_toolkit.styles import Style

custom_style = Style([
    ('qmark', 'fg:#673ab7 bold'),  # Color y estilo para el símbolo de la pregunta
    ('question', 'bold'),  # Estilo para la pregunta
    ('selected', 'fg:#cc5454 bold'),  # Color para la opción seleccionada
    ('pointer', 'fg:#673ab7 bold'),  # Color y estilo para el puntero
    ('highlighted', 'fg:#2ecc71 bold'),  # Color y estilo para la opción destacada
    # ('answer', 'fg:#f44336 bold'),  # Color y estilo para la respuesta
    ('text', ''),  # Estilo para el texto normal
])
