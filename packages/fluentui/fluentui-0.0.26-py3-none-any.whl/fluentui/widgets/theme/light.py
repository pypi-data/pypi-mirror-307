from .theme import Light

Widget = {
    'background': Light.Background
}

Button = {
    'color': Light.Text,
    'background': Light.Background,
    'padding': '6 12 5',
    'border': f'1 solid {Light.Border}',
    'border-radius': 4,
    'font-weight': 600,
    ':hover': {'background': '#f5f5f5', 'border-color': '#c7c7c7'},
    ':pressed': {'background': '#e0e0e0', 'border-color': '#b3b3b3'},
    ':disabled': {'color': '#bdbdbd', 'background': '#f0f0f0', 'border-color': '#e0e0e0'}
}

RadioButton = {
    'spacing': '11',
    'background': 'yellow',
    'padding': '7 8 6',
    '::indicator': {
        'width': '16',
        'height': '16',
        'image': 'url(:/icons/radio-uncheck-16.svg)'
    },
    '::indicator:hover': {
        'image': 'url(:/icons/radio-uncheck-hover-16.svg)'
    },
    '::indicator:pressed': {
        'image': 'url(:/icons/radio-uncheck-pressed-16.svg)'
    },
    '::indicator:checked': {
        'image': 'url(:/icons/radio-checked-16.svg)'
    },
    '::indicator:checked:hover': {
        'image': 'url(:/icons/radio-checked-hover-16.svg)'
    },
    '::indicator:checked:pressed': {
        'image': 'url(:/icons/radio-checked-pressed-16.svg)'
    }
}

PrimaryButton = Button | {
    'color': Light.Background,
    'background': Light.Primary,
    'border-color': 'transparent',
    ':hover': {'background': Light.PrimaryHover},
    ':pressed': {'background': Light.PrimaryPressed},
}

DangerButton = PrimaryButton | {
    'color': Light.Background,
    'background': Light.DangerBackground,
    ':hover': {'background': Light.DangerBackgroundHover},
    ':pressed': {'background': Light.DangerBackgroundPressed},
}

SubtleButton = Button | {
    'background': 'transparent',
    'border-color': 'transparent',
    ':hover': {'background': '#f5f5f5'},
    ':pressed': {'background': '#e0e0e0'},
}

InvisButton = SubtleButton | {
    ':hover': {'color': Light.Primary, 'background': 'transparent'},
    ':pressed': {'color': Light.PrimaryHover, 'background': 'transparent'},
}

Input = {
    'color': Light.Text,
    'padding': '4 8',
    'border': f'1 solid {Light.Border}',
    'border-radius': 4,
    'disable': {
        'color': '#bdbdbd',
        'background': '#fafafa',
        'border-color': '#e0e0e0'
    }
}

Slider = {
    'padding': '0 10',
    'QSlider::groove:horizontal': {
        'height': 4,
        'background': '#616161',
        'border-radius': 2
    },
    'QSlider::handle:horizontal': {
        'width': '20;',
        'height': '20;',
        'margin': '-8 -10;',
        'image': 'url(:/icons/slider-20.svg)'
    },
    'QSlider::handle:horizontal:hover': {
        'image': 'url(:/icons/slider-hover-20.svg)'
    },
    'QSlider::sub-page:horizontal': {
        'background': '#0f6cbd'
    }
}
