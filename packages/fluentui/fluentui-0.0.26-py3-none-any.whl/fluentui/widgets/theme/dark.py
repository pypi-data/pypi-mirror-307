from .theme import Dark

Widget = {
    'background': Dark.Background
}

Button = {
    'color': Dark.Text,
    'background': Dark.Background,
    'padding': '5 10',
    'border': f'1 solid {Dark.Border}',
    'border-radius': 4,
    'font-weight': 600,
    ':hover': {'background': '#3d3d3d', 'border-color': '#757575'},
    ':pressed': {'background': '#1f1f1f', 'border-color': '#6b6b6b'},
    ':disabled': {'color': '#5c5c5c', 'background': '#141414', 'border-color': '#424242'}
}

PrimaryButton = Button | {
    'color': Dark.Text,
    'background': Dark.Primary,
    'border-color': 'transparent',
    ':hover': {'background': '#0f6cbd'},
    ':pressed': {'background': '#0c3b5e'},
}
