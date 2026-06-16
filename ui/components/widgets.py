from PyQt6.QtWidgets import QPushButton, QLabel, QFrame, QVBoxLayout, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor, QPainter, QPainterPath, QPixmap, QColor, QLinearGradient, QBrush, QFont
from config.settings import PALETTE, STATUS_COLORS

def pill_button(text, color=None, text_color="white", hover_color=None):
    c = color or PALETTE['accent']
    hc = hover_color or PALETTE['accent2']
    btn = QPushButton(text)
    btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    btn.setStyleSheet(f"""
        QPushButton {{
            background: {c};
            color: {text_color};
            border: none;
            border-radius: 10px;
            padding: 9px 20px;
            font-size: 13px;
            font-weight: 600;
            letter-spacing: 0.3px;
        }}
        QPushButton:hover {{
            background: {hc};
        }}
        QPushButton:pressed {{
            background: {c};
            opacity: 0.8;
        }}
    """)
    return btn


def ghost_button(text, color=None):
    c = color or PALETTE['accent']
    btn = QPushButton(text)
    btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    btn.setStyleSheet(f"""
        QPushButton {{
            background: transparent;
            color: {c};
            border: 1.5px solid {c};
            border-radius: 10px;
            padding: 8px 18px;
            font-size: 13px;
            font-weight: 600;
        }}
        QPushButton:hover {{
            background: {c}22;
        }}
    """)
    return btn


class RoundedImageLabel(QLabel):
    def __init__(self, size=120, radius=18, parent=None):
        super().__init__(parent)
        self._size = size
        self._radius = radius
        self._pixmap = None
        self.setFixedSize(size, size)

    def setRoundedPixmap(self, pixmap):
        self._pixmap = pixmap
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(0, 0, self._size, self._size, self._radius, self._radius)
        painter.setClipPath(path)
        if self._pixmap and not self._pixmap.isNull():
            scaled = self._pixmap.scaled(self._size, self._size,
                                          Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                          Qt.TransformationMode.SmoothTransformation)
            x = (self._size - scaled.width()) // 2
            y = (self._size - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)
        else:
            # Draw placeholder gradient
            grad = QLinearGradient(0, 0, self._size, self._size)
            grad.setColorAt(0, QColor(PALETTE['surface2']))
            grad.setColorAt(1, QColor(PALETTE['border']))
            painter.fillPath(path, QBrush(grad))
            painter.setPen(QColor(PALETTE['text_dim']))
            painter.setFont(QFont("Segoe UI", 28))
            painter.drawText(0, 0, self._size, self._size,
                             Qt.AlignmentFlag.AlignCenter, "🐾")


class AnimalCard(QFrame):
    edit_requested   = pyqtSignal(int)
    delete_requested = pyqtSignal(int)

    def __init__(self, animal_data, parent=None):
        super().__init__(parent)
        (self.animal_id, name, species, habitat, diet,
         status, age, weight, origin, notes, image_blob) = animal_data

        self.setFixedWidth(260)
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.setStyleSheet(f"""
            QFrame {{
                background: {PALETTE['surface']};
                border: 1.5px solid {PALETTE['border']};
                border-radius: 18px;
            }}
            QFrame:hover {{
                border-color: {PALETTE['accent']};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 16)
        layout.setSpacing(10)

        # ── Image ──
        img_label = RoundedImageLabel(size=220, radius=12)
        img_label.setFixedWidth(220)
        if image_blob:
            px = QPixmap()
            px.loadFromData(image_blob)
            img_label.setRoundedPixmap(px)
        else:
            img_label.setRoundedPixmap(None)
        layout.addWidget(img_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        # ── Status badge ──
        sc = STATUS_COLORS.get(status, PALETTE['text_dim'])
        status_lbl = QLabel(status)
        status_lbl.setStyleSheet(f"""
            background: {sc}22;
            color: {sc};
            border: 1px solid {sc}55;
            border-radius: 8px;
            padding: 2px 10px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.5px;
        """)
        status_lbl.setFixedHeight(22)
        status_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ── Name & Species ──
        name_lbl = QLabel(name)
        name_lbl.setStyleSheet(f"color:{PALETTE['text']}; font-size:16px; font-weight:700;")
        name_lbl.setWordWrap(True)

        species_lbl = QLabel(f"<i>{species}</i>")
        species_lbl.setStyleSheet(f"color:{PALETTE['text_dim']}; font-size:12px;")
        species_lbl.setWordWrap(True)

        # ── Meta chips ──
        meta_row = QHBoxLayout()
        meta_row.setSpacing(6)
        for icon, val in [("🌿", habitat or "—"), ("🥩", diet or "—")]:
            chip = QLabel(f"{icon} {val}")
            chip.setStyleSheet(f"""
                background:{PALETTE['surface2']};
                color:{PALETTE['text_dim']};
                border-radius:7px;
                padding:3px 8px;
                font-size:11px;
            """)
            meta_row.addWidget(chip)
        meta_row.addStretch()

        # ── Stats row ──
        stats_row = QHBoxLayout()
        stats_row.setSpacing(8)
        for val, lbl in [(f"{age} thn", "Umur"), (f"{weight} kg", "Berat")]:
            stat_w = QWidget()
            stat_w.setStyleSheet(f"background:{PALETTE['surface2']}; border-radius:10px;")
            sv = QVBoxLayout(stat_w)
            sv.setContentsMargins(8, 6, 8, 6)
            sv.setSpacing(0)
            v = QLabel(val)
            v.setStyleSheet(f"color:{PALETTE['accent2']}; font-size:14px; font-weight:700;")
            v.setAlignment(Qt.AlignmentFlag.AlignCenter)
            l2 = QLabel(lbl)
            l2.setStyleSheet(f"color:{PALETTE['text_dim']}; font-size:10px;")
            l2.setAlignment(Qt.AlignmentFlag.AlignCenter)
            sv.addWidget(v); sv.addWidget(l2)
            stats_row.addWidget(stat_w)

        origin_lbl = QLabel(f"📍 {origin or '—'}")
        origin_lbl.setStyleSheet(f"color:{PALETTE['text_dim']}; font-size:11px;")

        # ── Action buttons ──
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        edit_btn = ghost_button("✏ Edit", PALETTE['accent'])
        del_btn  = ghost_button("🗑 Hapus", PALETTE['red'])
        edit_btn.setFixedHeight(34)
        del_btn.setFixedHeight(34)
        edit_btn.clicked.connect(lambda: self.edit_requested.emit(self.animal_id))
        del_btn.clicked.connect(lambda: self.delete_requested.emit(self.animal_id))
        btn_row.addWidget(edit_btn)
        btn_row.addWidget(del_btn)

        layout.addWidget(status_lbl)
        layout.addWidget(name_lbl)
        layout.addWidget(species_lbl)
        layout.addLayout(meta_row)
        layout.addLayout(stats_row)
        layout.addWidget(origin_lbl)
        layout.addSpacing(4)
        layout.addLayout(btn_row)
