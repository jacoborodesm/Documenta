from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence, QShortcut
from keybindings_dialog import KeybindingsDialog

class KeybindingsManager:
    def __init__(self, window):
        self.window = window
        self.shortcuts = {}
        self.setup_shortcuts()
        
    def setup_shortcuts(self):
        # Clear any existing shortcuts to avoid conflicts
        for shortcut in self.shortcuts.values():
            shortcut.setEnabled(False)
        self.shortcuts.clear()
        
        # Define shortcuts that don't conflict with menu actions
        # Screenshot shortcut - use Alt+S instead of Ctrl+Shift+S
        self.shortcuts['screenshot'] = QShortcut(
            QKeySequence("Alt+S"),
            self.window
        )
        self.shortcuts['screenshot'].activated.connect(
            self.window.screenshot_tool.start_capture
        )
        
        # Text shortcut - use Alt+T instead of Ctrl+T
        self.shortcuts['text'] = QShortcut(
            QKeySequence("Alt+T"),
            self.window
        )
        self.shortcuts['text'].activated.connect(
            self.window.canvas.add_text
        )
        
        # Code shortcut - use Alt+K instead of Ctrl+K
        self.shortcuts['code'] = QShortcut(
            QKeySequence("Alt+K"),
            self.window
        )
        self.shortcuts['code'].activated.connect(
            self.window.canvas.add_code
        )
        
        # Add new shortcuts
        self.shortcuts['save'] = QShortcut(
            QKeySequence("Ctrl+S"),
            self.window
        )
        self.shortcuts['save'].activated.connect(self.window.save_project)
        
        self.shortcuts['open'] = QShortcut(
            QKeySequence("Ctrl+O"),
            self.window
        )
        self.shortcuts['open'].activated.connect(self.window.load_project)
        
        self.shortcuts['copy'] = QShortcut(
            QKeySequence("Ctrl+C"),
            self.window
        )
        self.shortcuts['copy'].activated.connect(self.window.copy_to_clipboard)
    
    def configure_shortcuts(self):
        dialog = KeybindingsDialog(self.window)
        if dialog.exec():
            # Update shortcuts with new values
            self.shortcuts['screenshot'].setKey(QKeySequence(dialog.screenshot_input.text()))
            self.shortcuts['text'].setKey(QKeySequence(dialog.text_input.text()))
            self.shortcuts['code'].setKey(QKeySequence(dialog.code_input.text()))