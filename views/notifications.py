from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QColor, QPainter, QPainterPath, QBrush
from user_files.user_config import color_system

class NotifWindow(QWidget):
    def __init__(self):
        super().__init__()
        screen = QApplication.primaryScreen().availableGeometry()
        self.w, self.h = 300, 52
        self.screen = screen
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(self.w, self.h)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.setGraphicsEffect(shadow)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(18, 0, 18, 0)
        layout.setSpacing(10)

        self.icon_label = QLabel("⬤")
        self.icon_label.setStyleSheet("color: #4cff91; font-size: 8px; background: transparent;")
        self.icon_label.setFixedWidth(10)

        self.label = QLabel("")
        self.label.setStyleSheet(f"""
            color: {color_system.value[0]};
            font-size: 13px;
            font-family: 'Segoe UI', sans-serif;
            font-weight: 400;
            background: transparent;
            letter-spacing: 0.3px;
        """)

        layout.addWidget(self.icon_label)
        layout.addWidget(self.label)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(0, 0, self.w, self.h, 14, 14)
        painter.fillPath(path, QBrush(QColor(color_system.value[1])))

    def set_notif(self, text, duration=3000):
        self.label.setText(text)
        self._animate_in()
        QTimer.singleShot(duration, self._animate_out)

    def _animate_in(self):
        self.show()
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(350)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.setStartValue(self.pos().__class__(self.screen.width() - self.w - 20, self.screen.height()))
        self.anim.setEndValue(self.pos().__class__(self.screen.width() - self.w - 20, self.screen.height() - self.h - 20))
        self.anim.start()

    def _animate_out(self):
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(280)
        self.anim.setEasingCurve(QEasingCurve.InCubic)
        self.anim.setStartValue(self.pos())
        self.anim.setEndValue(self.pos().__class__(self.screen.width() - self.w - 20, self.screen.height()))
        self.anim.finished.connect(self.hide)
        self.anim.start()