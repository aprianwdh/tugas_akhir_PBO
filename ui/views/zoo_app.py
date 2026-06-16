from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QComboBox, QScrollArea, QFrame, QStackedWidget, QLineEdit, QMessageBox, QDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from config.settings import PALETTE, GLOBAL_STYLE, STATUS_COLORS
from ui.components.widgets import AnimalCard, pill_button
from ui.views.animal_form import AnimalFormDialog
from database.manager import fetch_all, fetch_status_stats, search_animals, fetch_one, insert_animal, update_animal, delete_animal

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

        self.nav_buttons = []
        nav_items = [("🐾", "Semua Hewan", 0), ("📊", "Statistik", 1)]
        for icon, text, page_idx in nav_items:
            btn = QPushButton(f"  {icon}  {text}")
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.clicked.connect(lambda checked, idx=page_idx: self._switch_page(idx))
            sb_layout.addWidget(btn)
            self.nav_buttons.append(btn)
        self._update_nav_style(0)

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

        # ── Main content (stacked pages) ──
        self.stack = QStackedWidget()
        self.stack.setStyleSheet(f"background:{PALETTE['bg']};")

        # Page 0: Semua Hewan
        animals_page = QWidget()
        animals_page.setStyleSheet(f"background:{PALETTE['bg']};")
        c_layout = QVBoxLayout(animals_page)
        c_layout.setContentsMargins(28, 24, 28, 24)
        c_layout.setSpacing(0)

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
        self.stack.addWidget(animals_page)

        # Page 1: Statistik
        stats_page = QWidget()
        stats_page.setStyleSheet(f"background:{PALETTE['bg']};")
        stats_layout = QVBoxLayout(stats_page)
        stats_layout.setContentsMargins(28, 24, 28, 24)
        stats_layout.setSpacing(0)

        stats_header = QVBoxLayout()
        stats_title = QLabel("Statistik Status Hewan")
        stats_title.setStyleSheet(f"color:{PALETTE['text']}; font-size:26px; font-weight:800; letter-spacing:-0.5px;")
        stats_sub = QLabel("Persentase distribusi status konservasi seluruh hewan")
        stats_sub.setStyleSheet(f"color:{PALETTE['text_dim']}; font-size:13px;")
        stats_header.addWidget(stats_title)
        stats_header.addWidget(stats_sub)
        stats_layout.addLayout(stats_header)
        stats_layout.addSpacing(24)

        self.stats_scroll = QScrollArea()
        self.stats_scroll.setWidgetResizable(True)
        self.stats_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.stats_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.stats_container = QWidget()
        self.stats_container.setStyleSheet("background:transparent;")
        self.stats_layout = QVBoxLayout(self.stats_container)
        self.stats_layout.setSpacing(16)
        self.stats_layout.setContentsMargins(0, 0, 12, 12)
        self.stats_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.stats_scroll.setWidget(self.stats_container)
        stats_layout.addWidget(self.stats_scroll)
        self.stack.addWidget(stats_page)

        root_layout.addWidget(self.stack)
        self._filter_status = ""
        self._current_page = 0

    def _nav_style(self, active=False):
        if active:
            return f"""
                QPushButton {{
                    background: {PALETTE['surface2']};
                    color: {PALETTE['text']};
                    border: none;
                    border-left: 3px solid {PALETTE['accent']};
                    border-radius: 10px;
                    padding: 10px 14px;
                    text-align: left;
                    font-size: 13px;
                    font-weight: 600;
                }}
            """
        return f"""
            QPushButton {{
                background: transparent;
                color: {PALETTE['text_dim']};
                border: none;
                border-left: 3px solid transparent;
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
        """

    def _update_nav_style(self, active_idx):
        for i, btn in enumerate(self.nav_buttons):
            btn.setStyleSheet(self._nav_style(i == active_idx))

    def _switch_page(self, page_idx):
        self._current_page = page_idx
        self.stack.setCurrentIndex(page_idx)
        self._update_nav_style(page_idx)
        if page_idx == 0:
            self.refresh_grid()
        else:
            self.refresh_stats()

    def _clear_grid(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _clear_stats(self):
        while self.stats_layout.count():
            item = self.stats_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def refresh_stats(self):
        self._clear_stats()
        stats = fetch_status_stats()
        total = sum(stats.values())

        summary = QFrame()
        summary.setStyleSheet(f"""
            QFrame {{
                background: {PALETTE['surface']};
                border: 1.5px solid {PALETTE['border']};
                border-radius: 18px;
            }}
        """)
        summary_layout = QHBoxLayout(summary)
        summary_layout.setContentsMargins(24, 20, 24, 20)

        total_lbl = QLabel(str(total))
        total_lbl.setStyleSheet(f"color:{PALETTE['accent2']}; font-size:36px; font-weight:800;")
        total_desc = QLabel("Total Hewan\nTerdaftar")
        total_desc.setStyleSheet(f"color:{PALETTE['text_dim']}; font-size:13px;")
        total_col = QVBoxLayout()
        total_col.addWidget(total_lbl)
        total_col.addWidget(total_desc)
        summary_layout.addLayout(total_col)
        summary_layout.addStretch()

        status_count = len([s for s in STATUS_COLORS if stats.get(s, 0) > 0])
        info_lbl = QLabel(f"{status_count} status berbeda")
        info_lbl.setStyleSheet(f"color:{PALETTE['text_dim']}; font-size:13px;")
        summary_layout.addWidget(info_lbl, alignment=Qt.AlignmentFlag.AlignVCenter)
        self.stats_layout.addWidget(summary)

        if total == 0:
            empty = QLabel("Belum ada data hewan.\nTambahkan hewan terlebih dahulu.")
            empty.setStyleSheet(f"color:{PALETTE['text_dim']}; font-size:16px;")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.stats_layout.addWidget(empty)
            self.count_lbl.setText("0 Hewan")
            return

        for status in STATUS_COLORS:
            count = stats.get(status, 0)
            pct = (count / total) * 100 if total else 0
            sc = STATUS_COLORS[status]

            card = QFrame()
            card.setStyleSheet(f"""
                QFrame {{
                    background: {PALETTE['surface']};
                    border: 1.5px solid {PALETTE['border']};
                    border-radius: 14px;
                }}
            """)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(20, 16, 20, 16)
            card_layout.setSpacing(10)

            top_row = QHBoxLayout()
            status_lbl = QLabel(status)
            status_lbl.setStyleSheet(f"""
                background: {sc}22;
                color: {sc};
                border: 1px solid {sc}55;
                border-radius: 8px;
                padding: 4px 12px;
                font-size: 13px;
                font-weight: 700;
            """)
            pct_lbl = QLabel(f"{pct:.1f}%")
            pct_lbl.setStyleSheet(f"color:{sc}; font-size:22px; font-weight:800;")
            count_lbl = QLabel(f"{count} hewan")
            count_lbl.setStyleSheet(f"color:{PALETTE['text_dim']}; font-size:12px;")
            top_row.addWidget(status_lbl)
            top_row.addStretch()
            top_row.addWidget(count_lbl)
            top_row.addSpacing(12)
            top_row.addWidget(pct_lbl)

            bar_bg = QFrame()
            bar_bg.setFixedHeight(10)
            bar_bg.setStyleSheet(f"background: {PALETTE['surface2']}; border-radius: 5px;")
            bar_row = QHBoxLayout(bar_bg)
            bar_row.setContentsMargins(0, 0, 0, 0)
            bar_row.setSpacing(0)
            bar_fill = QFrame()
            bar_fill.setStyleSheet(f"background: {sc}; border-radius: 5px;")
            bar_empty = QFrame()
            bar_empty.setStyleSheet("background: transparent;")
            fill_stretch = max(1, int(pct * 10)) if pct > 0 else 0
            empty_stretch = max(1, int((100 - pct) * 10)) if pct < 100 else 0
            if fill_stretch:
                bar_row.addWidget(bar_fill, fill_stretch)
            if empty_stretch:
                bar_row.addWidget(bar_empty, empty_stretch)

            card_layout.addLayout(top_row)
            card_layout.addWidget(bar_bg)
            self.stats_layout.addWidget(card)

        self.count_lbl.setText(f"{total} Hewan")

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
        if self._current_page == 0:
            self.refresh_grid()
        else:
            self.refresh_stats()

    def _refresh_current_view(self):
        if self._current_page == 0:
            self.refresh_grid()
        else:
            self.refresh_stats()

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
            self._refresh_current_view()

    def edit_animal(self, animal_id):
        data = fetch_one(animal_id)
        if not data:
            return
        dlg = AnimalFormDialog(self, animal_data=data)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            update_animal(animal_id, dlg.result_data)
            self._refresh_current_view()

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
            self._refresh_current_view()
