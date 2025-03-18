from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QPushButton, QFileDialog, QScrollArea, QApplication,
                           QMessageBox)
from PyQt6.QtCore import Qt, QBuffer
from PyQt6.QtGui import QAction
from canvas_panel import CanvasPanel
from keybindings import KeybindingsManager
from screenshot import ScreenshotTool
from docx_exporter import DocxExporter
import pyperclip

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Document Composer")
        self.setGeometry(100, 100, 800, 600)
        
        # Create status bar
        self.statusBar().showMessage("Ready")
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Create scroll area for canvas
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
        # Canvas panel for content
        self.canvas = CanvasPanel()
        scroll_area.setWidget(self.canvas)
        
        # Initialize screenshot tool first
        self.screenshot_tool = ScreenshotTool(self.canvas)
        
        # Create menu bar (after screenshot_tool is initialized)
        self.create_menu_bar()
        
        # Buttons layout
        button_layout = QHBoxLayout()
        
        # Export button - changed from Word to HTML
        export_button = QPushButton("Export to HTML")
        export_button.clicked.connect(self.export_to_html)
        button_layout.addWidget(export_button)
        
        # Copy button
        copy_button = QPushButton("Copy to Clipboard")
        copy_button.clicked.connect(self.copy_to_clipboard)
        button_layout.addWidget(copy_button)
        
        # Configure button
        config_button = QPushButton("Configure Shortcuts")
        config_button.clicked.connect(self.configure_shortcuts)
        button_layout.addWidget(config_button)
        
        # Add button layout to main layout
        layout.addLayout(button_layout)
        
        # Initialize keybindings after screenshot tool
        self.keybindings = KeybindingsManager(self)
    
    def configure_shortcuts(self):
        self.keybindings.configure_shortcuts()

    def export_to_html(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Document", "", "HTML files (*.html)"
        )
        if file_path:
            try:
                self.canvas.save_as_html(file_path)
                # Show success message
                QMessageBox.information(self, "Export Successful", f"Document exported to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Failed", f"Failed to export document: {str(e)}")
    
    def copy_to_clipboard(self):
        try:
            content = self.canvas.get_content_as_text()
            pyperclip.copy(content)
            # Optional: Show a small notification
            self.statusBar().showMessage("Content copied to clipboard", 2000)
        except Exception as e:
            QMessageBox.warning(self, "Copy Failed", f"Failed to copy to clipboard: {str(e)}")
    
    # Add these methods to MainWindow
    
    def save_project(self):
        """Save the current project to a file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Project", "", "Documenta Project (*.docproj)"
        )
        if file_path:
            try:
                # Implement project saving logic
                # This would require serializing the canvas items
                self.statusBar().showMessage(f"Project saved to {file_path}", 2000)
            except Exception as e:
                QMessageBox.critical(self, "Save Failed", f"Failed to save project: {str(e)}")
    
    def load_project(self):
        """Load a project from a file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Project", "", "Documenta Project (*.docproj)"
        )
        if file_path:
            try:
                # Implement project loading logic
                self.statusBar().showMessage(f"Project loaded from {file_path}", 2000)
            except Exception as e:
                QMessageBox.critical(self, "Load Failed", f"Failed to load project: {str(e)}")

    def create_menu_bar(self):
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("File")
        
        new_action = QAction("New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)
        
        open_action = QAction("Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.load_project)
        file_menu.addAction(open_action)
        
        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        export_html_action = QAction("Export to HTML", self)
        export_html_action.triggered.connect(self.export_to_html)
        file_menu.addAction(export_html_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Alt+F4")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menu_bar.addMenu("Edit")
        
        copy_action = QAction("Copy to Clipboard", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy_to_clipboard)
        edit_menu.addAction(copy_action)
        
        # Tools menu
        tools_menu = menu_bar.addMenu("Tools")
        
        screenshot_action = QAction("Take Screenshot", self)
        screenshot_action.setShortcut("Ctrl+Shift+S")
        screenshot_action.triggered.connect(self.screenshot_tool.start_capture)
        tools_menu.addAction(screenshot_action)
        
        add_text_action = QAction("Add Text Box", self)
        add_text_action.setShortcut("Ctrl+T")
        add_text_action.triggered.connect(self.canvas.add_text)
        tools_menu.addAction(add_text_action)
        
        add_code_action = QAction("Add Code Box", self)
        add_code_action.setShortcut("Ctrl+K")
        add_code_action.triggered.connect(self.canvas.add_code)
        tools_menu.addAction(add_code_action)

    def new_project(self):
        """Create a new empty project"""
        # Ask for confirmation if there's content
        if self.canvas.items:
            reply = QMessageBox.question(self, "New Project", 
                                        "Are you sure you want to create a new project? Any unsaved changes will be lost.",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.No:
                return
                
        # Clear the canvas
        self.canvas.items.clear()
        self.canvas.update_layout()
        self.statusBar().showMessage("New project created", 2000)