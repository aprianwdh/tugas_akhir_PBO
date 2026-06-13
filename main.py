import sys
import os
import sqlite3
import base64
from datetime import date
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QPushButton, QLineEdit, QTextEdit,
    QComboBox, QScrollArea, QFrame, QFileDialog, QMessageBox,
    QDialog, QSizePolicy, QStackedWidget, QSpinBox
)
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, pyqtSignal
from PyQt6.QtGui import (
    QPixmap, QFont, QIcon, QColor, QPainter, QPainterPath,
    QLinearGradient, QBrush, QPen, QFontDatabase, QCursor
)


# ─────────────────────────── DATABASE ────────────────────────────
DB_PATH = "database/zoo.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS animals (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT NOT NULL,
            species  TEXT NOT NULL,
            habitat  TEXT,
            diet     TEXT,
            status   TEXT DEFAULT 'Stabil',
            age      INTEGER DEFAULT 0,
            weight   REAL DEFAULT 0.0,
            origin   TEXT,
            notes    TEXT,
            image    BLOB
        )
    """)
    # Seed with sample data if empty
    c.execute("SELECT COUNT(*) FROM animals")
    if c.fetchone()[0] == 0:
        samples = [
            ("Singa Afrika", "Panthera leo", "Sabana", "Karnivora", "Baik", 5, 190.0, "Afrika", "Raja hutan yang gagah", None),
            ("Gajah Sumatera", "Elephas maximus sumatranus", "Hutan Tropis", "Herbivora", "Kritis", 12, 2700.0, "Sumatera", "Spesies terancam punah", None),
            ("Komodo", "Varanus komodoensis", "Pulau Kering", "Karnivora", "Rentan", 8, 70.0, "NTT", "Kadal terbesar di dunia", None),
            ("Harimau Benggala", "Panthera tigris tigris", "Hutan Hujan", "Karnivora", "Terancam", 6, 220.0, "India", "Kucing besar yang majestic", None),
            ("Jerapah", "Giraffa camelopardalis", "Sabana", "Herbivora", "Baik", 9, 800.0, "Afrika", "Hewan darat tertinggi", None),
            ("Orang Utan", "Pongo pygmaeus", "Hutan Hujan", "Omnivora", "Kritis", 15, 85.0, "Kalimantan", "Primata cerdas dari Borneo", None),
        ]
        c.executemany("""
            INSERT INTO animals (name,species,habitat,diet,status,age,weight,origin,notes,image)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """, samples)
    conn.commit()
    conn.close()

def fetch_all():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id,name,species,habitat,diet,status,age,weight,origin,notes,image FROM animals ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def fetch_one(animal_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM animals WHERE id=?", (animal_id,))
    row = c.fetchone()
    conn.close()
    return row

def insert_animal(data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO animals (name,species,habitat,diet,status,age,weight,origin,notes,image)
        VALUES (?,?,?,?,?,?,?,?,?,?)
    """, data)
    conn.commit()
    conn.close()

def update_animal(animal_id, data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        UPDATE animals SET name=?,species=?,habitat=?,diet=?,status=?,age=?,weight=?,origin=?,notes=?,image=?
        WHERE id=?
    """, (*data, animal_id))
    conn.commit()
    conn.close()

def delete_animal(animal_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM animals WHERE id=?", (animal_id,))
    conn.commit()
    conn.close()

def search_animals(query):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    like = f"%{query}%"
    c.execute("""
        SELECT id,name,species,habitat,diet,status,age,weight,origin,notes,image
        FROM animals
        WHERE name LIKE ? OR species LIKE ? OR habitat LIKE ? OR origin LIKE ?
        ORDER BY id DESC
    """, (like, like, like, like))
    rows = c.fetchall()
    conn.close()
    return rows


# ─────────────────────────── STYLE ───────────────────────────────
PALETTE = {
    "bg":         "#0F1117",
    "surface":    "#1A1D2E",
    "surface2":   "#232640",
    "accent":     "#6C63FF",
    "accent2":    "#A78BFA",
    "green":      "#34D399",
    "yellow":     "#FBBF24",
    "red":        "#F87171",
    "text":       "#F1F5F9",
    "text_dim":   "#94A3B8",
    "border":     "#2D3154",
}

STATUS_COLORS = {
    "Baik":      "#34D399",
    "Stabil":    "#60A5FA",
    "Rentan":    "#FBBF24",
    "Terancam":  "#FB923C",
    "Kritis":    "#F87171",
}

GLOBAL_STYLE = f"""
QMainWindow, QWidget {{
    background-color: {PALETTE['bg']};
    color: {PALETTE['text']};
    font-family: 'Segoe UI', 'SF Pro Display', Arial, sans-serif;
}}
QScrollArea {{
    border: none;
    background: transparent;
}}
QScrollBar:vertical {{
    background: {PALETTE['surface']};
    width: 6px;
    border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: {PALETTE['border']};
    border-radius: 3px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background: {PALETTE['accent']};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}
QLineEdit, QTextEdit, QComboBox, QSpinBox {{
    background: {PALETTE['surface2']};
    color: {PALETTE['text']};
    border: 1.5px solid {PALETTE['border']};
    border-radius: 10px;
    padding: 8px 12px;
    font-size: 13px;
    selection-background-color: {PALETTE['accent']};
}}
QLineEdit:focus, QTextEdit:focus, QSpinBox:focus {{
    border-color: {PALETTE['accent']};
}}
QComboBox::drop-down {{
    border: none;
    width: 24px;
}}
QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid {PALETTE['text_dim']};
    margin-right: 8px;
}}
QComboBox QAbstractItemView {{
    background: {PALETTE['surface2']};
    color: {PALETTE['text']};
    border: 1.5px solid {PALETTE['border']};
    border-radius: 8px;
    selection-background-color: {PALETTE['accent']};
    padding: 4px;
}}
QLabel {{
    background: transparent;
}}
QMessageBox {{
    background: {PALETTE['surface']};
    color: {PALETTE['text']};
}}
QMessageBox QPushButton {{
    background: {PALETTE['accent']};
    color: white;
    border: none;
    border-radius: 8px;
    padding: 6px 18px;
    font-weight: 600;
}}
"""


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


# ─────────────────────── ROUNDED IMAGE LABEL ─────────────────────
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


# ─────────────────────────── ANIMAL CARD ─────────────────────────
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


# ────────────────────────── FORM DIALOG ──────────────────────────
class AnimalFormDialog(QDialog):
    def __init__(self, parent=None, animal_data=None):
        super().__init__(parent)
        self.animal_data = animal_data
        self.image_bytes = None
        self.setWindowTitle("Tambah Hewan" if not animal_data else "Edit Hewan")
        self.setMinimumWidth(520)
        self.setStyleSheet(f"""
            QDialog {{
                background: {PALETTE['bg']};
                color: {PALETTE['text']};
            }}
        """)
        self._build_ui()
        if animal_data:
            self._populate(animal_data)

    def _build_ui(self):
        main = QVBoxLayout(self)
        main.setContentsMargins(28, 24, 28, 24)
        main.setSpacing(14)

        # Title
        title_text = "Tambah Hewan Baru" if not self.animal_data else "Edit Data Hewan"
        title = QLabel(title_text)
        title.setStyleSheet(f"color:{PALETTE['text']}; font-size:20px; font-weight:700;")
        main.addWidget(title)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color:{PALETTE['border']};")
        main.addWidget(sep)

        # Image section
        img_row = QHBoxLayout()
        self.img_preview = RoundedImageLabel(size=110, radius=14)
        img_row.addWidget(self.img_preview)
        img_col = QVBoxLayout()
        img_col.setSpacing(6)
        img_lbl = QLabel("Foto Hewan")
        img_lbl.setStyleSheet(f"color:{PALETTE['text']}; font-size:13px; font-weight:600;")
        img_hint = QLabel("Format: JPG, PNG, WEBP (max 5 MB)")
        img_hint.setStyleSheet(f"color:{PALETTE['text_dim']}; font-size:11px;")
        self.upload_btn = ghost_button("📁  Pilih Gambar", PALETTE['accent'])
        self.upload_btn.setFixedWidth(160)
        self.upload_btn.clicked.connect(self._pick_image)
        img_col.addWidget(img_lbl)
        img_col.addWidget(img_hint)
        img_col.addWidget(self.upload_btn)
        img_col.addStretch()
        img_row.addSpacing(14)
        img_row.addLayout(img_col)
        img_row.addStretch()
        main.addLayout(img_row)

        # Fields grid
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.setColumnStretch(1, 1)

        def lbl(t):
            l = QLabel(t)
            l.setStyleSheet(f"color:{PALETTE['text_dim']}; font-size:12px; font-weight:600;")
            return l

        self.f_name    = QLineEdit(); self.f_name.setPlaceholderText("cth: Singa Afrika")
        self.f_species = QLineEdit(); self.f_species.setPlaceholderText("cth: Panthera leo")
        self.f_habitat = QLineEdit(); self.f_habitat.setPlaceholderText("cth: Sabana, Hutan Hujan")
        self.f_origin  = QLineEdit(); self.f_origin.setPlaceholderText("cth: Afrika, Sumatera")
        self.f_age     = QSpinBox(); self.f_age.setRange(0, 200); self.f_age.setSuffix(" tahun")
        self.f_weight  = QLineEdit(); self.f_weight.setPlaceholderText("cth: 190.5")

        self.f_diet = QComboBox()
        self.f_diet.addItems(["Herbivora", "Karnivora", "Omnivora", "Insektivora"])

        self.f_status = QComboBox()
        self.f_status.addItems(["Baik", "Stabil", "Rentan", "Terancam", "Kritis"])

        fields = [
            ("Nama Hewan *",  self.f_name),
            ("Spesies *",     self.f_species),
            ("Habitat",       self.f_habitat),
            ("Asal Daerah",   self.f_origin),
            ("Umur",          self.f_age),
            ("Berat (kg)",    self.f_weight),
            ("Jenis Makanan", self.f_diet),
            ("Status",        self.f_status),
        ]
        for i, (label, widget) in enumerate(fields):
            r, c = divmod(i, 2)
            grid.addWidget(lbl(label), r * 2, c * 2)
            grid.addWidget(widget,     r * 2 + 1, c * 2)
        grid.setColumnMinimumWidth(1, 10)  # gap

        main.addLayout(grid)

        # Notes
        notes_lbl = QLabel("Catatan")
        notes_lbl.setStyleSheet(f"color:{PALETTE['text_dim']}; font-size:12px; font-weight:600;")
        self.f_notes = QTextEdit()
        self.f_notes.setPlaceholderText("Informasi tambahan tentang hewan...")
        self.f_notes.setMaximumHeight(80)
        main.addWidget(notes_lbl)
        main.addWidget(self.f_notes)

        # Buttons
        btn_row = QHBoxLayout()
        cancel_btn = ghost_button("Batal", PALETTE['text_dim'])
        save_btn   = pill_button("💾  Simpan", PALETTE['accent'])
        cancel_btn.clicked.connect(self.reject)
        save_btn.clicked.connect(self._save)
        btn_row.addStretch()
        btn_row.addWidget(cancel_btn)
        btn_row.addSpacing(8)
        btn_row.addWidget(save_btn)
        main.addLayout(btn_row)

    def _pick_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Pilih Gambar Hewan", "",
            "Images (*.png *.jpg *.jpeg *.webp *.bmp)"
        )
        if path:
            with open(path, "rb") as f:
                self.image_bytes = f.read()
            px = QPixmap(path)
            self.img_preview.setRoundedPixmap(px)

    def _populate(self, data):
        # data: (id, name, species, habitat, diet, status, age, weight, origin, notes, image)
        _, name, species, habitat, diet, status, age, weight, origin, notes, image_blob = data
        self.f_name.setText(name or "")
        self.f_species.setText(species or "")
        self.f_habitat.setText(habitat or "")
        self.f_origin.setText(origin or "")
        self.f_age.setValue(age or 0)
        self.f_weight.setText(str(weight) if weight else "")
        idx = self.f_diet.findText(diet or ""); self.f_diet.setCurrentIndex(max(idx,0))
        idx2 = self.f_status.findText(status or ""); self.f_status.setCurrentIndex(max(idx2,0))
        self.f_notes.setPlainText(notes or "")
        if image_blob:
            self.image_bytes = image_blob
            px = QPixmap(); px.loadFromData(image_blob)
            self.img_preview.setRoundedPixmap(px)

    def _save(self):
        name = self.f_name.text().strip()
        species = self.f_species.text().strip()
        if not name or not species:
            QMessageBox.warning(self, "Validasi", "Nama Hewan dan Spesies wajib diisi!")
            return
        try:
            weight = float(self.f_weight.text().replace(",", ".")) if self.f_weight.text().strip() else 0.0
        except ValueError:
            QMessageBox.warning(self, "Validasi", "Berat harus berupa angka!")
            return
        self.result_data = (
            name,
            species,
            self.f_habitat.text().strip(),
            self.f_diet.currentText(),
            self.f_status.currentText(),
            self.f_age.value(),
            weight,
            self.f_origin.text().strip(),
            self.f_notes.toPlainText().strip(),
            self.image_bytes,
        )
        self.accept()


# ──────────────────────────── MAIN WINDOW ────────────────────────
class ZooApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🦁  Zoo Database — Kebun Binatang")
        self.setMinimumSize(1080, 720)
        self.resize(1280, 800)
        self.setStyleSheet(GLOBAL_STYLE)
        self._build_ui()
        self.refresh_grid()

    def _build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ── Sidebar ──
        sidebar = QWidget()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet(f"background:{PALETTE['surface']}; border-right:1px solid {PALETTE['border']};")
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(18, 28, 18, 28)
        sb_layout.setSpacing(6)

        logo = QLabel("🦁")
        logo.setStyleSheet("font-size:40px;")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_main = QLabel("ZooBase")
        title_main.setStyleSheet(f"color:{PALETTE['text']}; font-size:22px; font-weight:800; letter-spacing:-0.5px;")
        title_main.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tagline = QLabel("Manajemen Hewan")
        tagline.setStyleSheet(f"color:{PALETTE['text_dim']}; font-size:11px;")
        tagline.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sb_layout.addWidget(logo)
        sb_layout.addWidget(title_main)
        sb_layout.addWidget(tagline)
        sb_layout.addSpacing(24)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color:{PALETTE['border']};")
        sb_layout.addWidget(sep)
        sb_layout.addSpacing(12)

        nav_label = QLabel("NAVIGASI")
        nav_label.setStyleSheet(f"color:{PALETTE['text_dim']}; font-size:10px; font-weight:700; letter-spacing:1.5px;")
        sb_layout.addWidget(nav_label)

        for icon, text in [("🐾", "Semua Hewan"), ("📊", "Statistik")]:
            btn = QPushButton(f"  {icon}  {text}")
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    color: {PALETTE['text_dim']};
                    border: none;
                    border-radius: 10px;
                    padding: 10px 14px;
                    text-align: left;
                    font-size: 13px;
                    font-weight: 500;
                }}
                QPushButton:hover {{
                    background: {PALETTE['surface2']};
                    color: {PALETTE['text']};
                }}
            """)
            sb_layout.addWidget(btn)

        sb_layout.addStretch()

        self.count_lbl = QLabel("0 Hewan")
        self.count_lbl.setStyleSheet(f"""
            background:{PALETTE['surface2']};
            color:{PALETTE['accent2']};
            border-radius:10px;
            padding:10px;
            font-size:13px;
            font-weight:700;
        """)
        self.count_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sb_layout.addWidget(self.count_lbl)

        root_layout.addWidget(sidebar)

        # ── Main content ──
        content = QWidget()
        content.setStyleSheet(f"background:{PALETTE['bg']};")
        c_layout = QVBoxLayout(content)
        c_layout.setContentsMargins(28, 24, 28, 24)
        c_layout.setSpacing(0)

        # Header
        header = QHBoxLayout()
        header.setSpacing(12)

        h_col = QVBoxLayout()
        page_title = QLabel("Database Hewan Kebun Binatang")
        page_title.setStyleSheet(f"color:{PALETTE['text']}; font-size:26px; font-weight:800; letter-spacing:-0.5px;")
        page_sub = QLabel("Kelola dan pantau semua hewan di kebun binatang Anda")
        page_sub.setStyleSheet(f"color:{PALETTE['text_dim']}; font-size:13px;")
        h_col.addWidget(page_title)
        h_col.addWidget(page_sub)

        add_btn = pill_button("＋  Tambah Hewan", PALETTE['accent'])
        add_btn.setFixedSize(160, 42)
        add_btn.clicked.connect(self.add_animal)

        header.addLayout(h_col)
        header.addStretch()
        header.addWidget(add_btn, alignment=Qt.AlignmentFlag.AlignBottom)
        c_layout.addLayout(header)
        c_layout.addSpacing(20)

        # Search bar
        search_row = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍  Cari hewan, spesies, habitat, atau asal daerah...")
        self.search_box.setFixedHeight(42)
        self.search_box.textChanged.connect(self.on_search)
        self.search_box.setStyleSheet(f"""
            QLineEdit {{
                background:{PALETTE['surface']};
                color:{PALETTE['text']};
                border:1.5px solid {PALETTE['border']};
                border-radius:12px;
                padding:8px 16px;
                font-size:13px;
            }}
            QLineEdit:focus {{
                border-color:{PALETTE['accent']};
            }}
        """)

        filter_combo = QComboBox()
        filter_combo.addItems(["Semua Status", "Baik", "Stabil", "Rentan", "Terancam", "Kritis"])
        filter_combo.setFixedSize(150, 42)
        filter_combo.currentTextChanged.connect(self.on_filter)
        filter_combo.setStyleSheet(filter_combo.styleSheet())

        self._filter_status = ""
        search_row.addWidget(self.search_box)
        search_row.addSpacing(8)
        search_row.addWidget(filter_combo)
        c_layout.addLayout(search_row)
        c_layout.addSpacing(20)

        # Cards scroll area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.grid_container = QWidget()
        self.grid_container.setStyleSheet("background:transparent;")
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(16)
        self.grid_layout.setContentsMargins(0, 0, 12, 12)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.scroll.setWidget(self.grid_container)
        c_layout.addWidget(self.scroll)

        root_layout.addWidget(content)
        self._filter_status = ""

    def _clear_grid(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def refresh_grid(self, rows=None):
        if rows is None:
            rows = fetch_all()
        self._clear_grid()
        if not rows:
            empty = QLabel("Belum ada hewan.\nKlik '＋ Tambah Hewan' untuk mulai.")
            empty.setStyleSheet(f"color:{PALETTE['text_dim']}; font-size:16px;")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid_layout.addWidget(empty, 0, 0)
        else:
            cols = max(1, (self.scroll.width() - 40) // (260 + 16))
            for i, row in enumerate(rows):
                card = AnimalCard(row)
                card.edit_requested.connect(self.edit_animal)
                card.delete_requested.connect(self.delete_animal)
                self.grid_layout.addWidget(card, i // cols, i % cols)
        self.count_lbl.setText(f"{len(rows)} Hewan")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.refresh_grid()

    def on_search(self, text):
        if text.strip():
            rows = search_animals(text.strip())
        else:
            rows = fetch_all()
        if self._filter_status and self._filter_status != "Semua Status":
            rows = [r for r in rows if r[5] == self._filter_status]
        self.refresh_grid(rows)

    def on_filter(self, status):
        self._filter_status = status
        self.on_search(self.search_box.text())

    def add_animal(self):
        dlg = AnimalFormDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            insert_animal(dlg.result_data)
            self.refresh_grid()

    def edit_animal(self, animal_id):
        data = fetch_one(animal_id)
        if not data:
            return
        # fetch_one returns full row: (id, name, species, habitat, diet, status, age, weight, origin, notes, image)
        # AnimalFormDialog expects same format
        dlg = AnimalFormDialog(self, animal_data=data)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            update_animal(animal_id, dlg.result_data)
            self.refresh_grid()

    def delete_animal(self, animal_id):
        data = fetch_one(animal_id)
        name = data[1] if data else "hewan ini"
        reply = QMessageBox.question(
            self, "Hapus Hewan",
            f"Apakah Anda yakin ingin menghapus <b>{name}</b>?<br>Data tidak dapat dikembalikan.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel
        )
        if reply == QMessageBox.StandardButton.Yes:
            delete_animal(animal_id)
            self.refresh_grid()


# ─────────────────────────── ENTRY POINT ─────────────────────────
def main():
    init_db()
    app = QApplication(sys.argv)
    app.setApplicationName("ZooBase")

    # Try to set a nice font
    for family in ["Segoe UI", "SF Pro Display", "Helvetica Neue", "Arial"]:
        font = QFont(family, 10)
        app.setFont(font)
        break

    window = ZooApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
