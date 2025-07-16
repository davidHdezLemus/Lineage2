from PyQt5 import QtWidgets, QtGui, QtCore
from utils.locale import LANGS

def resource_path(relative_path):
    """Helper to get absolute path to resource, works for dev and for PyInstaller"""
    import os
    import sys
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    return os.path.join(base_path, relative_path)

class LauncherUI:
    def setup_ui(self, main_window):
        """
        Sets up the user interface for the main launcher window.
        :param main_window: The main QWidget instance to build the UI on.
        """
        main_window.setStyleSheet('background-color: #181818;')
        
        # Banner
        main_window.banner = QtWidgets.QLabel(main_window)
        main_window.banner.setPixmap(QtGui.QPixmap(resource_path('assets/banner.png')).scaled(640, 80, QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation))
        main_window.banner.setGeometry(0, 0, 640, 80)
        main_window.banner.setAlignment(QtCore.Qt.AlignCenter)

        # Background
        main_window.bg = QtWidgets.QLabel(main_window)
        main_window.bg.setPixmap(QtGui.QPixmap(resource_path('assets/bg.png')).scaled(640, 340))
        main_window.bg.setGeometry(0, 80, 640, 340)
        main_window.bg.lower()

        # Language Button
        main_window.lang_btn = QtWidgets.QPushButton(main_window)
        main_window.lang_btn.setIcon(QtGui.QIcon(resource_path('assets/flag.png')))
        main_window.lang_btn.setIconSize(QtCore.QSize(32, 32))
        main_window.lang_btn.setGeometry(590, 10, 32, 32)
        main_window.lang_btn.setStyleSheet('''
            QPushButton { background: transparent; border: none; }
            QPushButton:hover { background: rgba(255, 204, 102, 0.18); border-radius: 8px; border: 1px solid #ffcc66; }
        ''')
        main_window.lang_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        main_window.lang_btn.clicked.connect(main_window.switch_language)

        # Start Button
        main_window.start_btn = QtWidgets.QPushButton(LANGS[main_window.lang]['start'], main_window)
        main_window.start_btn.setGeometry(470, 340, 150, 50)
        main_window.start_btn.setEnabled(False)
        main_window.start_btn.clicked.connect(main_window.start_game)
        self.set_start_btn_style(main_window.start_btn, enabled=False, glow=False)

        # News Widget
        main_window.news_widget = QtWidgets.QWidget(main_window)
        main_window.news_widget.setGeometry(50, 90, 550, 240)
        main_window.news_widget.setStyleSheet('background-color: rgba(0,0,0,0.65); border-radius: 12px;')
        news_layout = QtWidgets.QVBoxLayout(main_window.news_widget)
        news_layout.setContentsMargins(16, 16, 16, 16)
        news_layout.setSpacing(8)
        
        news_header = QtWidgets.QLabel(main_window.config['LauncherTitle'], main_window.news_widget)
        news_header.setStyleSheet('color: #ffcc66; font-size: 20px; font-weight: bold;')
        news_layout.addWidget(news_header)
        
        main_window.news_area = QtWidgets.QTextEdit(main_window.news_widget)
        main_window.news_area.setReadOnly(True)
        main_window.news_area.setStyleSheet('background: transparent; color: #fff; font-size: 15px; border: none;')
        news_layout.addWidget(main_window.news_area, stretch=1)

        # Status Label
        main_window.status = QtWidgets.QLabel(LANGS[main_window.lang]['checking'], main_window)
        main_window.status.setGeometry(30, 350, 400, 30)
        main_window.status.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        main_window.status.setStyleSheet('color: #fff; font-size: 16px; background: rgba(0,0,0,0.5); font-weight: bold; border-radius: 6px; padding-left: 8px;')

    def set_start_btn_style(self, button, enabled, glow):
        shadow_effect = QtWidgets.QGraphicsDropShadowEffect(button)
        
        if not enabled:
            style = '''
                QPushButton {
                    background-color: #444; color: #888; font-size: 22px;
                    border-radius: 8px; border: 2px solid #ffcc66;
                }'''
            shadow_effect.setEnabled(False)
        elif glow:
            style = '''
                QPushButton {
                    background-color: #222; color: #fff; font-size: 22px;
                    border-radius: 8px; border: 2px solid #ffcc66; outline: 0;
                }
                QPushButton:hover {
                    background-color: #2a2a00; color: #fffbe0; border: 2px solid #ffe066;
                }'''
            shadow_effect.setBlurRadius(32)
            shadow_effect.setColor(QtGui.QColor(255, 204, 102, 180))
            shadow_effect.setOffset(0, 0)
            shadow_effect.setEnabled(True)
        else:
            style = '''
                QPushButton {
                    background-color: #222; color: #fff; font-size: 22px;
                    border-radius: 8px; border: 2px solid #ffcc66;
                }
                QPushButton:hover { background-color: #333; color: #fff; }'''
            shadow_effect.setEnabled(False)
            
        button.setStyleSheet(style)
        button.setGraphicsEffect(shadow_effect)