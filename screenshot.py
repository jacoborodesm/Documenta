from PyQt6.QtWidgets import QWidget, QRubberBand, QLabel
from PyQt6.QtCore import Qt, QRect, QPoint, QTimer
from PyQt6.QtGui import QScreen, QGuiApplication, QColor
import sys

class ScreenshotTool(QWidget):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        self.rubberband = None
        self.origin = QPoint()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        # Make completely transparent by default
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background-color: transparent;")
        
    def start_capture(self):
        # Add a small delay to allow the user to prepare
        QTimer.singleShot(500, self._perform_capture)
        
    def _perform_capture(self):
        # Take a full screenshot of the entire screen
        screen = QGuiApplication.primaryScreen()
        
        # Capture the entire screen (0 is the ID for the entire desktop)
        screenshot = screen.grabWindow(0)
        
        # Add the screenshot to the canvas
        self.canvas.add_screenshot(screenshot)
        
        # Debug info
        print(f"Captured full screen screenshot: {screenshot.width()}x{screenshot.height()}")