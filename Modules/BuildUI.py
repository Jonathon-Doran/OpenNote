from Modules.Save import save, saveAs
from Modules.Load import new, load

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from Views.EditorFrameView import *
from Widgets.Table import *
from Modules.EditorSignals import editorSignalsInstance, ChangedWidgetAttribute

FONT_SIZES = [7, 8, 9, 10, 11, 12, 13, 14, 18, 24, 36, 48, 64, 72, 96, 144, 288]

#builds the application's UI
def build_ui(editor):
    print("Building UI...")

    #editor.statusBar = editor.statusBar()
    build_window(editor)
    build_menubar(editor)
    build_toolbar(editor)

    # Application's main layout (grid)
    gridLayout = QGridLayout()
    gridContainerWidget = QWidget()
    editor.setCentralWidget(gridContainerWidget)
    gridContainerWidget.setLayout(gridLayout)

    gridLayout.setSpacing(3)
    gridLayout.setContentsMargins(6, 6, 0, 0)

    gridLayout.setColumnStretch(0, 1) # The left side (index 0) will take up 1/7? of the space of the right
    gridLayout.setColumnStretch(1, 7)

    # Left side of the app's layout
    leftSideLayout = QVBoxLayout()
    leftSideContainerWidget = QWidget()
    leftSideContainerWidget.setLayout(leftSideLayout)
    leftSideLayout.setContentsMargins(0, 0, 0, 0)
    leftSideLayout.setSpacing(0)


    

    # Right side of the app's layout
    rightSideLayout = QVBoxLayout()
    rightSideContainerWidget = QWidget()
    rightSideContainerWidget.setLayout(rightSideLayout)
    rightSideLayout.setContentsMargins(0, 0, 0, 0)
    rightSideLayout.setSpacing(0)
    rightSideLayout.setStretch(0, 0)
    rightSideLayout.setStretch(1, 1)

    # Add appropriate widgets (ideally just view controllers) to their layouts
    leftSideLayout.addWidget(editor.notebookTitleView, 0)
    leftSideLayout.addWidget(editor.pageView, 1) # Page view has max stretch factor
    rightSideLayout.addWidget(editor.sectionView, 0)
    rightSideLayout.addWidget(editor.frameView, 1) # Frame view has max stretch factor

    # Add L+R container's widgets to the main grid
    gridLayout.addWidget(leftSideContainerWidget, 0, 0)
    gridLayout.addWidget(rightSideContainerWidget, 0, 1)

    addSectionButton = QPushButton("Add Section")
    #add functionality e.g. addSectionButton.clcicked.connect(editor.add_section_function)
    leftSideLayout.addWidget(addSectionButton)

def build_window(editor):
    editor.setWindowTitle("OpenNote")
    editor.setWindowIcon(QIcon('./Assets/OpenNoteLogo.png'))
    editor.setAcceptDrops(True)
    with open('./Styles/styles.qss',"r") as fh:
        editor.setStyleSheet(fh.read())

def build_menubar(editor):
    file = editor.menuBar().addMenu('&File')
    plugins = editor.menuBar().addMenu('&Plugins')

    new_file = build_action(editor, 'assets/icons/svg_file_open', 'New Notebook', 'New Notebook', False)
    new_file.setShortcut(QKeySequence.StandardKey.New)
    new_file.triggered.connect(lambda: new(editor))

    open_file = build_action(editor, 'assets/icons/svg_file_open', 'Open Notebook', 'Open Notebook', False)
    open_file.setShortcut(QKeySequence.StandardKey.Open)
    open_file.triggered.connect(lambda: load(editor))

    save_file = build_action(editor, 'assets/icons/svg_file_save', 'Save Notebook', 'Save Notebook', False)
    save_file.setShortcut(QKeySequence.StandardKey.Save)
    save_file.triggered.connect(lambda: save(editor))

    save_fileAs = build_action(editor, 'assets/icons/svg_file_save', 'Save Notebook As...', 'Save Notebook As', False)
    save_fileAs.setShortcut(QKeySequence.fromString('Ctrl+Shift+S'))
    save_fileAs.triggered.connect(lambda: saveAs(editor))

    file.addActions([new_file, open_file, save_file, save_fileAs])

def build_toolbar(editor):
    toolbar = QToolBar()
    toolbar.setIconSize(QSize(16, 16))
    toolbar.setMovable(False)
    editor.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

    spacer = QWidget()
    spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    undo = build_action(toolbar, 'assets/icons/svg_undo', "undo", "undo", False)
    redo = build_action(toolbar, 'assets/icons/svg_redo', "redo", "redo", False)
    


    font = QFontComboBox()
    font.currentFontChanged.connect(lambda x: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.Font, font.currentFont()))

    size = QComboBox()
    size.addItems([str(fs) for fs in FONT_SIZES])
    size.currentIndexChanged.connect(lambda x: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.FontSize, int(size.currentText())))

    bgColor = build_action(toolbar, 'assets/icons/svg_font_bucket', "Text Box Color", "Text Box Color", False)
    bgColor.triggered.connect(lambda: openGetColorDialog(purpose = "background"))


    
    fontColor = build_action(toolbar, 'assets/icons/svg_font_color', "Font Color", "Font Color", False)
    fontColor.triggered.connect(lambda: openGetColorDialog(purpose = "font"))

    bold = build_action(toolbar, 'assets/icons/bold', "Bold", "Bold", True)
    bold.triggered.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.FontBold, None))
    

    italic = build_action(toolbar, 'assets/icons/italic.svg', "Italic", "Italic", True)
    #italic.triggered.connect(lambda: editorSignalsInstance.widgetAttributeChanged.emit(setFontItalicCustom), None)

    underline = build_action(toolbar, 'assets/icons/underline.svg', "Underline", "Underline", True)
    #underline.toggled.connect(lambda x: editor.childWidget. setFontUnderlineCustom(True if x else False))
    table = build_action(toolbar, 'assets/icons/svg_table', "Create Table", "Create Table", False)
    table.triggered.connect(show_table_popup)

    hyperlink = build_action(toolbar, 'assets/icons/svg_hyperlink', "Hyperlink", "Hyperlink", True)

    toolbar.addActions([undo, redo])
    toolbar.addSeparator()
    toolbar.addWidget(font)
    toolbar.addWidget(size)
    toolbar.addSeparator()
    toolbar.addActions([bgColor, fontColor, bold, italic, underline])
    toolbar.addSeparator()
    toolbar.addActions([table, hyperlink])


def openGetColorDialog(purpose):
    color = QColorDialog.getColor()
    if color.isValid():
        if purpose == "font":
            editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.FontColor, color)
        elif purpose == "background":
            editorSignalsInstance.widgetAttributeChanged.emit(ChangedWidgetAttribute.BackgroundColor, color)

def build_action(parent, icon_path, action_name, set_status_tip, set_checkable):
    action = QAction(QIcon(icon_path), action_name, parent)
    action.setStatusTip(set_status_tip)
    action.setCheckable(set_checkable)
    return action

def show_table_popup(self):
    popup = TablePopupWindow()
    popup.exec_() 
    #def undo_triggered(self):
    # Call the EditorFrameView's triggerUndo method
    #self.EditorFrameView.triggerUndo()

class TablePopupWindow(QDialog):
    def __init__(self):
        super().__init__()
        '''self.setWindowTitle("Popup Window")
        layout = QVBoxLayout()
        label = QLabel("This is a popup window.")
        layout.addWidget(label)
        self.setLayout(layout)'''
        self.setWindowTitle("Table Configuration")
        self.layout = QVBoxLayout()

        self.rows_input = QLineEdit(self)
        self.rows_input.setPlaceholderText("Enter number of rows:")
        self.layout.addWidget(self.rows_input)

        self.cols_input = QLineEdit(self)
        colNum = self.cols_input.setPlaceholderText("Enter number of columns:")
        self.layout.addWidget(self.cols_input)

        create_table_button = QPushButton("Create Table")
        self.layout.addWidget(create_table_button)
        create_table_button.clicked.connect(self.accept)
        #create error message if no data is entered or if number of rows or columns are < 1
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        self.setLayout(self.layout)
    
    def get_table_data(self):
        rows_input = self.rows_input.text()
        cols_input = self.cols_input.text()
        return rows_input, cols_input

    def create_table(self):
        print("table")
        #row_num = int(self.rows_input.text())
        #col_num = int(self.cols_input.text())
        #self.EditorFrameView.add_table_action(row_num, col_num)

