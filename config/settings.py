PALETTE = {
    "bg":         "#0F1117",
    "surface":    "#1A1D2E",
    "surface2":   "#232640",
    "accent":     "#6C63FF",
    "accent2":    "#A78BFA",
    "green":      "#34D399",
    "yellow":     "#FBBF24",
    "red":        "#F87171",
    "text":       "#F1F5F9",
    "text_dim":   "#94A3B8",
    "border":     "#2D3154",
}

STATUS_COLORS = {
    "Baik":      "#34D399",
    "Stabil":    "#60A5FA",
    "Rentan":    "#FBBF24",
    "Terancam":  "#FB923C",
    "Kritis":    "#F87171",
}

GLOBAL_STYLE = f"""
QMainWindow, QWidget {{
    background-color: {PALETTE['bg']};
    color: {PALETTE['text']};
    font-family: 'Segoe UI', 'SF Pro Display', Arial, sans-serif;
}}
QScrollArea {{
    border: none;
    background: transparent;
}}
QScrollBar:vertical {{
    background: {PALETTE['surface']};
    width: 6px;
    border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: {PALETTE['border']};
    border-radius: 3px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background: {PALETTE['accent']};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}
QLineEdit, QTextEdit, QComboBox, QSpinBox {{
    background: {PALETTE['surface2']};
    color: {PALETTE['text']};
    border: 1.5px solid {PALETTE['border']};
    border-radius: 10px;
    padding: 8px 12px;
    font-size: 13px;
    selection-background-color: {PALETTE['accent']};
}}
QLineEdit:focus, QTextEdit:focus, QSpinBox:focus {{
    border-color: {PALETTE['accent']};
}}
QComboBox::drop-down {{
    border: none;
    width: 24px;
}}
QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid {PALETTE['text_dim']};
    margin-right: 8px;
}}
QComboBox QAbstractItemView {{
    background: {PALETTE['surface2']};
    color: {PALETTE['text']};
    border: 1.5px solid {PALETTE['border']};
    border-radius: 8px;
    selection-background-color: {PALETTE['accent']};
    padding: 4px;
}}
QLabel {{
    background: transparent;
}}
QMessageBox {{
    background: {PALETTE['surface']};
    color: {PALETTE['text']};
}}
QMessageBox QPushButton {{
    background: {PALETTE['accent']};
    color: white;
    border: none;
    border-radius: 8px;
    padding: 6px 18px;
    font-weight: 600;
}}
"""
