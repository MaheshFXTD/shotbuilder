from PySide2 import QtWidgets, QtCore
import hou


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Signal-Slot Debugging")
        self.counter = 0

        # Main layout
        layout = QtWidgets.QVBoxLayout()

        # Label
        self.label = QtWidgets.QLabel("Press the build button")
        layout.addWidget(self.label)

        # Build button
        build_button = QtWidgets.QPushButton("Build")
        build_button.clicked.connect(self.build)
        layout.addWidget(build_button)

        # Close button
        close_button = QtWidgets.QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        # Set central widget
        container = QtWidgets.QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def build(self):
        self.counter += 1
        self.label.setText(f"Build pressed {self.counter} times.")
        collected_files = [
            "File1 (Version: 1)",
            "File2 (Version: 2)",
            "File3 (Version: 3)",
            "File4 (Version: 4)"
        ]
        self.show_collected_files_window(collected_files)

    def show_collected_files_window(self, collected_files):
        # Create a new dialog
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Collected Files")
        dialog.resize(800, 600)

        # Layout for the dialog
        layout = QtWidgets.QVBoxLayout(dialog)

        # Main splitter for version, file name, and department
        main_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal, dialog)

        # First splitter: Version (QListWidget)
        version_layout = QtWidgets.QVBoxLayout()
        version_label = QtWidgets.QLabel("Version")
        version_list = QtWidgets.QListWidget()

        # Populate the version list with unique versions from collected files
        versions = {file.split(" (Version: ")[1][:-1] for file in collected_files}
        version_list.addItems(sorted(versions))

        version_layout.addWidget(version_label)
        version_layout.addWidget(version_list)

        version_widget = QtWidgets.QWidget()
        version_widget.setLayout(version_layout)
        main_splitter.addWidget(version_widget)

        # Second splitter: File names
        file_layout = QtWidgets.QVBoxLayout()
        file_label = QtWidgets.QLabel("Files")
        file_list = QtWidgets.QListWidget()
        file_names = [file.split(" (Version: ")[0] for file in collected_files]
        file_list.addItems(file_names)
        file_layout.addWidget(file_label)
        file_layout.addWidget(file_list)

        file_widget = QtWidgets.QWidget()
        file_widget.setLayout(file_layout)
        main_splitter.addWidget(file_widget)

        # Third splitter: Department layout using QListWidget
        department_layout = QtWidgets.QVBoxLayout()
        department_label = QtWidgets.QLabel("Department")
        department_list = QtWidgets.QListWidget()

        categories = ["Asset", "Texture", "Lookdev", "FX", "Lighting"]

        checkboxes = []

        def update_checkboxes():
            """Enable only one checkbox at a time."""
            for cb in checkboxes:
                if cb.isChecked():
                    for other_cb in checkboxes:
                        if other_cb != cb:
                            other_cb.setEnabled(False)
                    return
            for cb in checkboxes:
                cb.setEnabled(True)

        for category in categories:
            row_widget = QtWidgets.QWidget()
            row_layout = QtWidgets.QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)

            checkbox = QtWidgets.QCheckBox()
            checkboxes.append(checkbox)
            checkbox.stateChanged.connect(update_checkboxes)

            row_layout.addWidget(checkbox)
            row_layout.addWidget(QtWidgets.QLabel(category))
            row_layout.addStretch()

            list_item = QtWidgets.QListWidgetItem(department_list)
            department_list.addItem(list_item)
            department_list.setItemWidget(list_item, row_widget)

        department_layout.addWidget(department_label)
        department_layout.addWidget(department_list)

        department_widget = QtWidgets.QWidget()
        department_widget.setLayout(department_layout)
        main_splitter.addWidget(department_widget)

        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 2)
        main_splitter.setStretchFactor(2, 1)

        layout.addWidget(main_splitter)

        # Buttons at the bottom
        button_layout = QtWidgets.QHBoxLayout()
        build_button = QtWidgets.QPushButton("Build")
        build_button.clicked.connect(lambda: print("Debugging collected files."))  # Placeholder for debugging
        button_layout.addWidget(build_button)

        close_button = QtWidgets.QPushButton("Close")
        close_button.clicked.connect(dialog.reject)  # Use reject to close the dialog
        button_layout.addWidget(close_button)

        layout.addLayout(button_layout)

        dialog.setLayout(layout)
        dialog.exec()


# Create a parent window for Houdini's main window
def get_houdini_main_window():
    """Get the Houdini main window as a parent."""
    for widget in QtWidgets.QApplication.instance().topLevelWidgets():
        if widget.objectName() == "MainWindow":
            return widget
    return None


# Run the window
parent = get_houdini_main_window()
window = MainWindow(parent)
window.show()
