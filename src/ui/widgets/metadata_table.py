from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt
from core.models import VideoMetadata

class MetadataTableWidget(QTableWidget):
    """
    Виджет для отображения и редактирования метаданных видео.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["Поле", "Значение"])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setVisible(False)
        self.metadata = None

    def set_metadata(self, metadata: VideoMetadata):
        """
        Заполняет таблицу значениями из объекта VideoMetadata.
        """
        self.metadata = metadata
        fields = ["title", "artist", "comment", "codec", "duration", "filepath"]
        self.setRowCount(len(fields))

        for row, field in enumerate(fields):
            item_key = QTableWidgetItem(field.capitalize())
            item_key.setFlags(item_key.flags() & ~Qt.ItemIsEditable)
            self.setItem(row, 0, item_key)

            value = getattr(metadata, field, "")
            item_value = QTableWidgetItem(str(value) if value is not None else "")
            self.setItem(row, 1, item_value)

    def get_updated_metadata(self) -> VideoMetadata:
        """
        Возвращает объект VideoMetadata с обновлёнными значениями из таблицы.
        """
        if not self.metadata:
            return None

        updated = VideoMetadata(filepath=self.metadata.filepath)
        for row in range(self.rowCount()):
            field = self.item(row, 0).text().lower()
            value = self.item(row, 1).text()
            if hasattr(updated, field):
                if field == "duration":
                    try:
                        setattr(updated, field, float(value))
                    except ValueError:
                        setattr(updated, field, None)
                else:
                    setattr(updated, field, value if value else None)
        return updated
