from PySide6.QtWidgets import QPlainTextEdit
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPainter, QLinearGradient, QColor


class ShimmerPlainTextEdit(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.shimmer_pos = -100
        self.shimmer_active = False
        self.shimmer_width = 120
        self.shimmer_speed = 8
        self.shimmer_intensity = 120
        
        self.shimmer_timer = QTimer(self)
        self.shimmer_timer.timeout.connect(self._update_shimmer)
    
    def start_shimmer(self):
        self.shimmer_active = True
        self.shimmer_pos = -self.shimmer_width
        self.shimmer_timer.start(30)
    
    def stop_shimmer(self):
        self.shimmer_active = False
        self.shimmer_timer.stop()
        self.viewport().update()
    
    def _update_shimmer(self):
        self.shimmer_pos += self.shimmer_speed
        if self.shimmer_pos > self.viewport().width():
            self.shimmer_pos = -self.shimmer_width
        self.viewport().update()
    
    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.shimmer_active:
            return
        painter = QPainter(self.viewport())
        gradient = QLinearGradient(self.shimmer_pos, 0, self.shimmer_pos + self.shimmer_width, 0)
        gradient.setColorAt(0.0, QColor(255, 255, 255, 0))
        gradient.setColorAt(0.5, QColor(255, 255, 255, self.shimmer_intensity))
        gradient.setColorAt(1.0, QColor(255, 255, 255, 0))
        painter.fillRect(self.viewport().rect(), gradient)
        painter.end()