from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PySide6.QtCore import Qt
from adapters.exiftool_adapter import read_metadata
from core.commands import write_metadata_exiftool
from ui.widgets.metadata_table import MetadataTableWidget
from utils.constants import SUPPORTED_EXTENSIONS


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VidMetaEdit")
        self.current_file = None
        self.metadata = None

        self.setAcceptDrops(True)

        central_widget = QWidget()
        layout = QVBoxLayout()

        self.label_file = QLabel("Файл не выбран")
        layout.addWidget(self.label_file)

        self.metadata_table = MetadataTableWidget()
        layout.addWidget(self.metadata_table)


        open_button = QPushButton("Открыть видео")
        open_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(open_button)

        save_button = QPushButton("Сохранить изменения")
        save_button.clicked.connect(self.save_changes)
        layout.addWidget(save_button)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if any(url.toLocalFile().split('.')[-1].lower() in SUPPORTED_EXTENSIONS for url in urls):
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.open_video(file_path)

    def open_video(self, file_path: str):
        ext = file_path.lower().split('.')[-1]
        if ext not in SUPPORTED_EXTENSIONS:
            self.label_file.setText(f"Неподдерживаемый формат: .{ext}")
            return

        self.current_file = file_path
        self.label_file.setText(f"Файл: {file_path}")
        self.metadata = read_metadata(file_path)

        if self.metadata:
            self.metadata_table.set_metadata(self.metadata)
        else:
            self.label_file.setText("Ошибка чтения метаданных")

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите видео",
            "",
            "Video Files (*.mp4 *.mkv *.avi *.mov);;All Files (*)"
        )
        if file_path:
            self.open_video(file_path)
        else:
            self.label_file.setText("Файл не выбран")

    def save_changes(self):
        if not self.current_file or not self.metadata:
            self.label_file.setText("Сначала выберите файл!")
            return

        updated_metadata = self.metadata_table.get_updated_metadata()
        success = write_metadata_exiftool(self.current_file, updated_metadata, keep_backup=True)
        if success:
            self.label_file.setText(f"Изменения сохранены: {self.current_file}")
        else:
            self.label_file.setText(f"Ошибка при сохранении: {self.current_file}")
