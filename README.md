# Documenta

Documenta is a document composition tool that allows you to easily create documentation with screenshots, text, and code snippets. It's built with PyQt6 and provides a simple, intuitive interface for creating technical documentation.

## Features

- **Full-screen Screenshots**: Capture your entire screen with a single keyboard shortcut
- **Text Boxes**: Add formatted text explanations to your document
- **Code Blocks**: Include code snippets with proper formatting
- **Drag and Drop Interface**: Easily reorder elements in your document
- **Export Options**: Save your document as HTML
- **Clipboard Support**: Copy your document content to the clipboard
- **Customizable Keyboard Shortcuts**: Configure shortcuts to match your workflow

## Installation

1. Ensure you have Python 3.6+ installed
2. Install the required dependencies:

```bash
pip install PyQt6 python-docx pyperclip
````
## Usage
### Basic Controls
- Alt+S : Take a full-screen screenshot
- Alt+T : Add a text box
- Alt+K : Add a code box
- Ctrl+S : Save your project
- Ctrl+O : Open an existing project
- Ctrl+C : Copy content to clipboard
### Creating Documentation
1. Use the keyboard shortcuts or menu options to add content to your document
2. Drag and drop elements to reorder them
3. Edit text and code directly in the boxes
4. Export your document to HTML when finished
### Customizing Shortcuts
1. Click the "Configure Shortcuts" button
2. Enter your preferred key combinations
3. Click "Save" to apply the changes
## Project Structure
- main.py : Application entry point
- main_window.py : Main application window and UI
- canvas_panel.py : Document canvas where content is displayed and edited
- screenshot.py : Screenshot capture functionality
- keybindings.py : Keyboard shortcut management
- keybindings_dialog.py : Dialog for configuring shortcuts
- docx_exporter.py : Document export functionality
## Future Enhancements
- Save/load project functionality
- Export to additional formats (PDF, Markdown)
- Image editing capabilities
- Undo/redo functionality
- Themes and styling options
## License
This project is open source and available under the MIT License.
