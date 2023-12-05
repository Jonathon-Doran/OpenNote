from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from Modules.Enums import WidgetType

import random
import cv2

class ImageWidget(QLabel):
    def __init__(self, x, y, w, h, image_matrix):
        super().__init__()
        self.image_matrix = image_matrix
        self.w = w
        self.h = h

        # Image matrix from cv2 -> QImage -> QPixmap on this label
        matrix_height, matrix_width, _ = image_matrix.shape # Calc dimensions from real image matrix, not the current widget geometry
        bytes_per_line = 3 * matrix_width
        q_image = QImage(image_matrix.data, matrix_width, matrix_height, bytes_per_line, QImage.Format_BGR888)
        self.q_pixmap = QPixmap(q_image)
        self.setPixmap(self.q_pixmap.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation)) # Scale to widget geometry

        self.setGeometry(x, y, w, h) # this should get fixed
        self.persistantGeometry = self.geometry()

    # Handle resize
    def newGeometryEvent(self, newGeometry):
        new_w = newGeometry.width()
        new_h = newGeometry.height()
        if (self.w != new_w) or (self.h != new_h): # Not exactly sure how object's width and height attribute gets updated but this works
            self.setPixmap(self.q_pixmap.scaled(new_w, new_h, Qt.KeepAspectRatio, Qt.SmoothTransformation))

            pixmap_rect = self.pixmap().rect()
            w = pixmap_rect.width()
            h = pixmap_rect.height()
            # parent.resize(w, h) # Set container to the size of the new scaled pixmap

        self.persistantGeometry = newGeometry

    @staticmethod
    def new(clickPos):

        # Get path from user
        path, _ = QFileDialog.getOpenFileName(QWidget(), 'Add Image')
        if path == "": return

        # Get image size
        image_matrix = cv2.imread(path)
        h, w, _ = image_matrix.shape

        # Create image and add to notebook
        h, w, _ = image_matrix.shape
        image = ImageWidget(clickPos.x(), clickPos.y(), w, h, image_matrix) # Note: the editorframe will apply pos based on event

        return image

    @staticmethod # Special staticmethod that screensnip uses
    def newFromMatrix(clickPos, imageMatrix):
        h, w, _ = imageMatrix.shape
        image = ImageWidget(clickPos.x(), clickPos.y(), w, h, imageMatrix)

        return image

    def __getstate__(self):
        state = {}
        state['geometry'] = self.parentWidget().geometry()
        state['image_matrix'] = self.image_matrix
        return state

    def __setstate__(self, state):
        self.__init__(state['geometry'].x(), state['geometry'].y(), state['geometry'].width(), state['geometry'].height(), state['image_matrix'])

    def customMenuItems(self):
        def build_action(parent, icon_path, action_name, set_status_tip, set_checkable):
            action = QAction(QIcon(icon_path), action_name, parent)
            action.setStatusTip(set_status_tip)
            action.setCheckable(set_checkable)
            return action


        toolbarBottom = QToolBar()
        toolbarBottom.setIconSize(QSize(16, 16))
        toolbarBottom.setMovable(False)

        #crop = build_action(toolbarTop, 'assets/icons/svg_crop', "Crop", "Crop", False)
        
        flipHorizontal = build_action(toolbarBottom, 'assets/icons/svg_flip_horizontal', "Horizontal Flip", "Horizontal Flip", False)
        flipHorizontal.triggered.connect(self.flipHorizontal)
        flipVertical = build_action(toolbarBottom, 'assets/icons/svg_flip_vertical', "Vertical Flip", "Vertical Flip", False)
        flipVertical.triggered.connect(self.flipVertical)

        rotateLeftAction = build_action(toolbarBottom, 'assets/icons/svg_rotate_left', "Rotate 90 degrees Left", "Rotate 90 degrees Left", False)
        rotateLeftAction.triggered.connect(self.rotate90Left)
        rotateRightAction = build_action(toolbarBottom, 'assets/icons/svg_rotate_right', "Rotate 90 degrees Right", "Rotate 90 degrees Right", False)
        rotateRightAction.triggered.connect(self.rotate90Right)


        toolbarBottom.addActions([rotateLeftAction, rotateRightAction, flipHorizontal, flipVertical])

        qwaBottom = QWidgetAction(self)
        qwaBottom.setDefaultWidget(toolbarBottom)

        return [qwaBottom] 
        
    def flipVertical(self):
        # Flip the image matrix vertically using OpenCV
        self.image_matrix = cv2.flip(self.image_matrix, 0)
        self.updatePixmap()

    def flipHorizontal(self):
        # Flip the image matrix horizontally using OpenCV
        self.image_matrix = cv2.flip(self.image_matrix, 1)
        self.updatePixmap()

    def rotate90Left(self):
        # Rotate the image matrix 90 degrees to the left using OpenCV
        self.image_matrix = cv2.rotate(self.image_matrix, cv2.ROTATE_90_COUNTERCLOCKWISE)
        self.updatePixmap()
    def rotate90Right(self):
        # Rotate the image matrix 90 degrees to the right using OpenCV
        self.image_matrix = cv2.rotate(self.image_matrix, cv2.ROTATE_90_CLOCKWISE)
        self.updatePixmap()

    def updatePixmap(self):
        # Update the QImage and QPixmap
        matrix_height, matrix_width, _ = self.image_matrix.shape
        bytes_per_line = 3 * matrix_width
        q_image = QImage(self.image_matrix.data, matrix_width, matrix_height, bytes_per_line, QImage.Format_BGR888)
        self.q_pixmap = QPixmap(q_image)

        # Update the displayed pixmap
        self.setPixmap(self.q_pixmap.scaled(self.w, self.h, Qt.KeepAspectRatio, Qt.SmoothTransformation))