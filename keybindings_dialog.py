from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QLabel, QLineEdit)
from PyQt6.QtGui import QKeySequence

class KeybindingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configure Keybindings")
        self.setModal(True)
        layout = QVBoxLayout(self)
        
        # Screenshot shortcut
        screenshot_layout = QHBoxLayout()
        screenshot_layout.addWidget(QLabel("Screenshot:"))
        self.screenshot_input = QLineEdit(self)
        self.screenshot_input.setText("Ctrl+Shift+S")
        screenshot_layout.addWidget(self.screenshot_input)
        layout.addLayout(screenshot_layout)
        
        # Text shortcut
        text_layout = QHBoxLayout()
        text_layout.addWidget(QLabel("Text Box:"))
        self.text_input = QLineEdit(self)
        self.text_input.setText("Ctrl+T")
        text_layout.addWidget(self.text_input)
        layout.addLayout(text_layout)
        
        # Code shortcut
        code_layout = QHBoxLayout()
        code_layout.addWidget(QLabel("Code Box:"))
        self.code_input = QLineEdit(self)
        self.code_input.setText("Ctrl+K")
        code_layout.addWidget(self.code_input)
        layout.addLayout(code_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)