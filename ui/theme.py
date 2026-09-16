COLORS = {
    "bg_primary":    "#0f172a",
    "bg_secondary":  "#1e293b",
    "bg_card":       "#1e293b",
    "bg_input":      "#0f172a",
    "accent":        "#6366f1",
    "accent_hover":  "#4f46e5",
    "success":       "#22c55e",
    "danger":        "#ef4444",
    "warning":       "#f59e0b",
    "text_primary":  "#f1f5f9",
    "text_secondary":"#94a3b8",
    "border":        "#334155",
    "sidebar_bg":    "#0f172a",
    "topbar_bg":     "#0f172a",
}

FONTS = {
    "family":   "Inter",
    "fallback": "Segoe UI",
    "size_xs":  10,
    "size_sm":  12,
    "size_md":  14,
    "size_lg":  16,
    "size_xl":  20,
    "size_2xl": 24,
}

STYLESHEET = f"""
QMainWindow, QWidget {{
    background-color: {COLORS['bg_primary']};
    color:            {COLORS['text_primary']};
    font-family:      {FONTS['family']}, {FONTS['fallback']};
    font-size:        {FONTS['size_md']}px;
}}

QPushButton {{
    background-color: {COLORS['accent']};
    color:            white;
    border:           none;
    border-radius:    8px;
    padding:          10px 20px;
    font-size:        {FONTS['size_sm']}px;
    font-weight:      600;
}}

QPushButton:hover {{
    background-color: {COLORS['accent_hover']};
}}

QPushButton:disabled {{
    background-color: {COLORS['border']};
    color:            {COLORS['text_secondary']};
}}

QPushButton#danger {{
    background-color: {COLORS['danger']};
}}

QPushButton#success {{
    background-color: {COLORS['success']};
}}

QPushButton#ghost {{
    background-color: transparent;
    color:            {COLORS['text_secondary']};
    border:           1px solid {COLORS['border']};
}}

QPushButton#ghost:hover {{
    background-color: {COLORS['bg_secondary']};
    color:            {COLORS['text_primary']};
}}

QLineEdit, QTextEdit, QPlainTextEdit {{
    background-color: {COLORS['bg_input']};
    color:            {COLORS['text_primary']};
    border:           1px solid {COLORS['border']};
    border-radius:    8px;
    padding:          8px 12px;
    font-size:        {FONTS['size_sm']}px;
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border-color:     {COLORS['accent']};
}}

QComboBox {{
    background-color: {COLORS['bg_input']};
    color:            {COLORS['text_primary']};
    border:           1px solid {COLORS['border']};
    border-radius:    8px;
    padding:          8px 12px;
}}

QComboBox::drop-down {{
    border: none;
}}

QTableWidget {{
    background-color: {COLORS['bg_secondary']};
    color:            {COLORS['text_primary']};
    border:           1px solid {COLORS['border']};
    border-radius:    8px;
    gridline-color:   {COLORS['border']};
}}

QTableWidget::item:selected {{
    background-color: {COLORS['accent']};
}}

QHeaderView::section {{
    background-color: {COLORS['bg_primary']};
    color:            {COLORS['text_secondary']};
    border:           none;
    padding:          8px;
    font-size:        {FONTS['size_xs']}px;
    font-weight:      600;
}}

QScrollBar:vertical {{
    background:   {COLORS['bg_primary']};
    width:        6px;
    border-radius:3px;
}}

QScrollBar::handle:vertical {{
    background:   {COLORS['border']};
    border-radius:3px;
}}

QProgressBar {{
    background-color: {COLORS['bg_secondary']};
    border:           none;
    border-radius:    4px;
    height:           6px;
    text-align:       center;
}}

QProgressBar::chunk {{
    background-color: {COLORS['accent']};
    border-radius:    4px;
}}

QLabel#heading {{
    font-size:   {FONTS['size_xl']}px;
    font-weight: 700;
    color:       {COLORS['text_primary']};
}}

QLabel#subheading {{
    font-size: {FONTS['size_sm']}px;
    color:     {COLORS['text_secondary']};
}}

QFrame#card {{
    background-color: {COLORS['bg_card']};
    border:           1px solid {COLORS['border']};
    border-radius:    12px;
    padding:          16px;
}}

QTabWidget::pane {{
    border:           1px solid {COLORS['border']};
    background-color: {COLORS['bg_secondary']};
    border-radius:    8px;
}}

QTabBar::tab {{
    background-color: transparent;
    color:            {COLORS['text_secondary']};
    padding:          8px 16px;
    border:           none;
}}

QTabBar::tab:selected {{
    color:            {COLORS['text_primary']};
    border-bottom:    2px solid {COLORS['accent']};
}}

QSplitter::handle {{
    background-color: {COLORS['border']};
}}
"""
