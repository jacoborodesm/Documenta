from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTextEdit, 
                           QScrollArea, QFrame, QApplication)
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QPixmap, QDrag, QImage
import io
from PyQt6.QtCore import QBuffer

class DraggableWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        # Make the widget visually indicate it's draggable
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_position = event.pos()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setCursor(Qt.CursorShape.OpenHandCursor)
            
    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
            
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText('move')
        drag.setMimeData(mime_data)
        
        # Add visual feedback during drag
        pixmap = self.grab()
        drag.setPixmap(pixmap.scaled(pixmap.width()//2, pixmap.height()//2, Qt.AspectRatioMode.KeepAspectRatio))
        drag.setHotSpot(event.pos())
        
        # Execute the drag operation
        result = drag.exec(Qt.DropAction.MoveAction)

class CanvasPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setAcceptDrops(True)
        self.items = []
        
    def add_screenshot(self, pixmap):
        container = DraggableWidget(self)
        label = QLabel()
        label.setPixmap(pixmap)
        container.layout.addWidget(label)
        self.layout.addWidget(container)
        self.items.append(('image', container, pixmap))
        
    def add_text(self):
        container = DraggableWidget(self)
        text_edit = QTextEdit()
        text_edit.setMinimumHeight(100)
        text_edit.setPlaceholderText("Enter text here...")
        container.layout.addWidget(text_edit)
        self.layout.addWidget(container)
        self.items.append(('text', container, text_edit))
        
    def add_code(self):
        container = DraggableWidget(self)
        code_edit = QTextEdit()
        code_edit.setMinimumHeight(100)
        code_edit.setPlaceholderText("Enter code here...")
        code_edit.setStyleSheet("font-family: 'Courier New'; background-color: #f0f0f0;")
        container.layout.addWidget(code_edit)
        self.layout.addWidget(container)
        self.items.append(('code', container, code_edit))
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasText() and event.mimeData().text() == 'move':
            event.acceptProposedAction()
            
    def dragMoveEvent(self, event):
        if event.mimeData().hasText() and event.mimeData().text() == 'move':
            event.acceptProposedAction()
            
    def dropEvent(self, event):
        widget = event.source()
        if not widget:
            return
            
        # Get the drop position
        drop_pos = event.position().y()
        drop_index = self.get_drop_index(drop_pos)
        
        # Find the widget in our items list
        source_index = -1
        for i, (_, container, _) in enumerate(self.items):
            if container == widget:
                source_index = i
                break
                
        if source_index != -1:
            # Move the item in our items list
            item = self.items.pop(source_index)
            if drop_index > source_index:
                drop_index -= 1
            self.items.insert(drop_index, item)
            self.update_layout()
            
        event.acceptProposedAction()
                
    def get_drop_index(self, y):
        # Find the index where to insert the dragged widget
        for i, (_, container, _) in enumerate(self.items):
            widget_center = container.y() + container.height() / 2
            if y < widget_center:
                return i
        return len(self.items)
        
    def update_layout(self):
        # Remove all widgets from layout
        for i in reversed(range(self.layout.count())): 
            widget = self.layout.itemAt(i).widget()
            if widget:
                self.layout.removeWidget(widget)
                
        # Add them back in the new order
        for _, container, _ in self.items:
            self.layout.addWidget(container)
            
    def get_content_as_text(self):
        mime_data = QMimeData()
        text_parts = []
        html_parts = []
        
        for type_, _, content in self.items:
            if type_ == 'image':
                # For images, we need to handle them differently
                buffer = QBuffer()
                buffer.open(QBuffer.OpenModeFlag.WriteOnly)
                content.save(buffer, 'PNG')  # Save pixmap directly
                buffer_data = buffer.data()
                base64_data = buffer_data.toBase64().data().decode()
                html_parts.append(f'<img src="data:image/png;base64,{base64_data}">')
                text_parts.append('[Image]')
                buffer.close()
                
                # Also set the image in the mime data
                mime_data.setImageData(content)
            else:
                text = content.toPlainText()
                text_parts.append(text)
                if type_ == 'code':
                    html_parts.append(f'<pre style="background-color: #f0f0f0; font-family: \'Courier New\'">{text}</pre>')
                else:
                    html_parts.append(f'<p>{text}</p>')
        
        text_content = '\n\n'.join(text_parts)
        html_content = ''.join(html_parts)
        mime_data.setText(text_content)
        mime_data.setHtml(html_content)
        QApplication.clipboard().setMimeData(mime_data)
        return text_content
    
    def save_as_html(self, filename):
        """Save the canvas content as an HTML file"""
        text_parts = []
        html_parts = []
        
        for type_, _, content in self.items:
            if type_ == 'image':
                buffer = QBuffer()
                buffer.open(QBuffer.OpenModeFlag.WriteOnly)
                content.save(buffer, 'PNG')
                buffer_data = buffer.data()
                base64_data = buffer_data.toBase64().data().decode()
                html_parts.append(f'<img src="data:image/png;base64,{base64_data}">')
                buffer.close()
            else:
                text = content.toPlainText()
                if type_ == 'code':
                    html_parts.append(f'<pre style="background-color: #f0f0f0; font-family: \'Courier New\'">{text}</pre>')
                else:
                    html_parts.append(f'<p>{text}</p>')
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Documenta Export</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        pre {{ background-color: #f0f0f0; padding: 10px; border-radius: 5px; }}
        img {{ max-width: 100%; }}
    </style>
</head>
<body>
    {''.join(html_parts)}
</body>
</html>"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return html_content

    def remove_selected_item(self):
        """Remove the currently selected item"""
        # This would require implementing selection first
        # For now, let's add a right-click context menu to each widget
        
    def contextMenuEvent(self, event):
        """Show context menu for canvas items"""
        menu = QMenu(self)
        delete_action = menu.addAction("Delete Item")
        action = menu.exec(self.mapToGlobal(event.pos()))
        
        if action == delete_action:
            # Find the item under the cursor and remove it
            for i, (_, container, _) in enumerate(self.items):
                if container.geometry().contains(event.pos()):
                    self.items.pop(i)
                    self.update_layout()
                    break