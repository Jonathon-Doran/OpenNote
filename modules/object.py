from models.notebook import *
from models.object import *
from PySide6.QtWidgets import *
import random
import cv2
import os
from datetime import datetime

# When a user creates a new Object (TextBox, ImageObj, etc.)
# 1 Create a Widget of (type)
# 2 Create an Object of (type) and add it to models.Notebook.Page[x].Section[x]
# 3 Add Widget to editor.object list (List of widgets in Page[current], Section[current])
def add_object(editor, event, type):

    # Defaults for object
    x = event.pos().x() + 250
    y = event.pos().y() + 130
    t = '...'

    if type == 'text':

        # Name for undo
        random_number = random.randint(100, 999)
        name = 'textbox-'+str(random_number)

        # Create textbox and add to notebook
        text = TextBox(editor, x, y, 100, 100, t) # w, h needs to come from whats stored on object when they're resizable (same below)
        editor.notebook.page[editor.page].section[editor.section].object.append(Text(name,x, y, 100, 100, t))
        editor.object.append(text)

        # Undo related
        text.setObjectName(name)
        cmd = {'type':'object','name':name, 'action':'create'}
        editor.undo_stack.append(cmd)

    if type == 'image':

        # Get path from user
        path, _ = QFileDialog.getOpenFileName(editor, 'Add Image')
        if path == "": return

        # Name for undo
        random_number = random.randint(100, 999)
        name = 'imagebox-'+str(random_number)

        # Get image size
        image_blob = cv2.imread(path)
        h, w, _ = image_blob.shape

        # Create image and add to notebook
        image = ImageObj(editor, x, y, w, h, path)
        editor.notebook.page[editor.page].section[editor.section].object.append(Image(name,x, y, w, h, path))
        editor.object.append(image)

        # Undo related
        image.setObjectName(name)
        cmd = {'type':'object','name':name, 'action':'create'}
        editor.undo_stack.append(cmd)

    editor.autosaver.onChangeMade()

def add_snip(editor, event_pos, image_blob):
    x = event_pos['x'] + 250
    y = event_pos['y'] + 130

    # Name for undo
    random_number = random.randint(100, 999)
    name = 'imagebox-'+str(random_number)

    # Use datetime to generate ss image filename, save to local directory
    currentDatetime = datetime.now()
    fileName = currentDatetime.strftime("%d-%m-%Y_%H-%M-%S") + ".png"
    if (not os.path.exists(os.getcwd() + "/screenshots")):
        os.makedirs(os.getcwd() + "/screenshots")

    path = os.getcwd() + "/screenshots/" + fileName
    cv2.imwrite(path, image_blob)

    # Create image and add to notebook
    h, w, _ = image_blob.shape
    image = ImageObj(editor, x, y, w, h, path)
    editor.notebook.page[editor.page].section[editor.section].object.append(Image(name, x, y, w, h, path))
    editor.object.append(image)

    editor.autosaver.onChangeMade()

def paste_object(editor, event):
    if isinstance(editor.clipboard_object, ClipboardObject):
        x = event.pos().x() + 250
        y = event.pos().y() + 130
        w = editor.clipboard_object.width
        h = editor.clipboard_object.height
        t = editor.clipboard_object.html
        n = editor.clipboard_object.undo_name

        if editor.clipboard_object.type == 'image':
            image = ImageObj(editor, x, y, w, h, t)
            editor.object.append(image)
            editor.notebook.page[editor.page].section[editor.section].object.append(Image(n, x, y, w, h, t))

        else:
            text = TextBox(editor, x, y, w, h, t)
            editor.object.append(text)
            editor.notebook.page[editor.page].section[editor.section].object.append(Text(n, x, y, w, h, t))

        #cmd = Undo({'type':'clipboard', 'action':'paste'}) # This was throwing errors
        #editor.undo_stack.append(cmd)
        editor.autosaver.onChangeMade()

    elif editor.clipboard_object == None:
        return
    else: # Because anything thats not a QTextEdit prob wont work like this
        print("ERROR: Pasting unsupported object.")

# Create Widget of (type) with (params) from models.Notebook.Page[x].Section[x]
# Case 1: When a Notebook is loaded, function is called for every
#         Object in models.Notebook.Page[0].Section[0]
# Case 2: When a user selects a new Page or Section in the editor
def build_object(editor, params):
    if params.type == 'text':
        text = TextBox(editor, params.x, params.y, params.w, params.h, params.text)
        editor.object.append(text)

    if params.type == "image":
        image = ImageObj(editor, params.x, params.y, params.w, params.h, params.path)
        editor.object.append(image)

    if params.type == 'plugin':
        params.show()
        editor.object.append(params)

def add_plugin_object(editor, event, name, c):

    # Defaults for object
    x = event.pos().x() + 250
    y = event.pos().y() + 130
    w = 100
    h = 100

    inst = c(editor,x,y,w,h)
    editor.notebook.page[editor.page].section[editor.section].object.append(inst)
    editor.object.append(inst)

