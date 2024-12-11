from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QToolBar, QAction, QMainWindow, QLabel, QVBoxLayout, QFileDialog, QApplication, QWidget
from PyQt5.QtGui import QIcon, QPixmap, QTransform
import sys

class NoContextMenuToolBar(QToolBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def contextMenuEvent(self, event):
        # Prevent the right-click context menu from appearing
        pass

class PhotoViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LiteViewer")
        self.setGeometry(100, 100, 800, 600)

        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # QLabel to display the image
        self.image_label = QLabel("No Image Loaded", self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid black;")
        self.layout.addWidget(self.image_label)

        # Toolbar setup
        self.toolbar = NoContextMenuToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)

        # Open Image action
        open_action = QAction(QIcon(None), "Open", self)
        open_action.setStatusTip("Open an image file")
        open_action.triggered.connect(self.open_image)
        self.toolbar.addAction(open_action)

        # Rotate action
        rotate_action = QAction(QIcon(None), "Rotate", self)
        rotate_action.setStatusTip("Rotate the image")
        rotate_action.triggered.connect(self.rotate_image)
        self.toolbar.addAction(rotate_action)

        # Zoom in action
        zoom_in_action = QAction(QIcon(None), "Zoom In", self)
        zoom_in_action.setStatusTip("Zoom in on the image")
        zoom_in_action.triggered.connect(self.zoom_in)
        self.toolbar.addAction(zoom_in_action)

        # Zoom out action
        zoom_out_action = QAction(QIcon(None), "Zoom Out", self)
        zoom_out_action.setStatusTip("Zoom out of the image")
        zoom_out_action.triggered.connect(self.zoom_out)
        self.toolbar.addAction(zoom_out_action)

        # State variables
        self.pixmap = None
        self.rotation_angle = 0
        self.zoom_factor = 1.0
        self.min_zoom = 0.5
        self.max_zoom = 5.0

    def open_image(self):
        # Open a file dialog to select an image
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp);;All Files (*)", options=options)

        if file_path:
            # Load and display the image
            self.pixmap = QPixmap(file_path)
            self.rotation_angle = 0
            self.zoom_factor = 1.0
            self.update_image()

    def rotate_image(self):
        if self.pixmap:
            # Increment rotation angle
            self.rotation_angle += 90
            self.rotation_angle %= 360
            self.update_image()

    def zoom_in(self):
        if self.pixmap:
            # Increase zoom factor, respecting max zoom
            self.zoom_factor = min(self.max_zoom, self.zoom_factor * 1.2)
            self.update_image()

    def zoom_out(self):
        if self.pixmap:
            # Decrease zoom factor, respecting min zoom
            self.zoom_factor = max(self.min_zoom, self.zoom_factor / 1.2)
            self.update_image()

    def update_image(self):
        if self.pixmap:
            # Apply rotation and zoom
            transform = QTransform().rotate(self.rotation_angle)
            rotated_pixmap = self.pixmap.transformed(transform, Qt.SmoothTransformation)

            # Calculate crop dimensions for zoom effect
            width = self.image_label.width()
            height = self.image_label.height()
            scaled_width = int(rotated_pixmap.width() / self.zoom_factor)
            scaled_height = int(rotated_pixmap.height() / self.zoom_factor)

            # Ensure dimensions stay within the pixmap bounds
            scaled_width = max(1, min(rotated_pixmap.width(), scaled_width))
            scaled_height = max(1, min(rotated_pixmap.height(), scaled_height))

            cropped_pixmap = rotated_pixmap.copy(
                (rotated_pixmap.width() - scaled_width) // 2,
                (rotated_pixmap.height() - scaled_height) // 2,
                scaled_width,
                scaled_height
            )

            # Scale cropped pixmap to fit the label while keeping the aspect ratio
            final_pixmap = cropped_pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # Set the pixmap to the label
            self.image_label.setPixmap(final_pixmap)

            # Optionally: Set the label's alignment to keep the image centered
            self.image_label.setAlignment(Qt.AlignCenter)

            # Update the window size if necessary but do not let it grow
            self.setFixedSize(self.width(), self.height())  # Keep window size fixed

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = PhotoViewer()
    viewer.show()
    sys.exit(app.exec_())
