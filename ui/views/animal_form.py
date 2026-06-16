from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QFrame, QLineEdit, QSpinBox, QComboBox, QTextEdit, QMessageBox, QFileDialog
from PyQt6.QtGui import QPixmap
from config.settings import PALETTE
from ui.components.widgets import RoundedImageLabel, ghost_button, pill_button

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
