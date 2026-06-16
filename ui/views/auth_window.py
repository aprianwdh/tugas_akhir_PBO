from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QStackedWidget, QLineEdit, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal
from config.settings import PALETTE, GLOBAL_STYLE
from ui.components.widgets import pill_button, ghost_button
from database.manager import authenticate_user, register_user

class AuthWindow(QMainWindow):
    login_successful = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🦁 Login — ZooBase")
        self.setFixedSize(400, 520)
        self.setStyleSheet(GLOBAL_STYLE)
        
        root = QWidget()
        self.setCentralWidget(root)
        self.layout = QVBoxLayout(root)
        self.layout.setContentsMargins(40, 40, 40, 40)
        
        # Logo
        logo = QLabel("🦁")
        logo.setStyleSheet("font-size:60px;")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(logo)
        
        # Title
        self.title_lbl = QLabel("Masuk ke ZooBase")
        self.title_lbl.setStyleSheet(f"color:{PALETTE['text']}; font-size:24px; font-weight:800; letter-spacing:-0.5px;")
        self.title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_lbl)
        
        self.layout.addSpacing(30)
        
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)
        
        self._build_login_page()
        self._build_register_page()
        
        self.stack.setCurrentIndex(0)
        
    def _build_login_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        self.login_user = QLineEdit()
        self.login_user.setPlaceholderText("Username")
        self.login_pass = QLineEdit()
        self.login_pass.setPlaceholderText("Password")
        self.login_pass.setEchoMode(QLineEdit.EchoMode.Password)
        
        layout.addWidget(self.login_user)
        layout.addWidget(self.login_pass)
        
        layout.addSpacing(10)
        
        btn = pill_button("Sign In", PALETTE['accent'])
        btn.clicked.connect(self.handle_login)
        layout.addWidget(btn)
        
        switch_btn = ghost_button("Belum punya akun? Sign Up", PALETTE['text_dim'])
        switch_btn.setStyleSheet(switch_btn.styleSheet().replace("border: 1.5px solid", "border: none;"))
        switch_btn.clicked.connect(lambda: self.switch_mode(1))
        layout.addWidget(switch_btn)
        
        layout.addStretch()
        self.stack.addWidget(page)
        
    def _build_register_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        self.reg_user = QLineEdit()
        self.reg_user.setPlaceholderText("Username Baru")
        self.reg_pass = QLineEdit()
        self.reg_pass.setPlaceholderText("Password")
        self.reg_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.reg_pass2 = QLineEdit()
        self.reg_pass2.setPlaceholderText("Konfirmasi Password")
        self.reg_pass2.setEchoMode(QLineEdit.EchoMode.Password)
        
        layout.addWidget(self.reg_user)
        layout.addWidget(self.reg_pass)
        layout.addWidget(self.reg_pass2)
        
        layout.addSpacing(10)
        
        btn = pill_button("Sign Up", PALETTE['green'])
        btn.clicked.connect(self.handle_register)
        layout.addWidget(btn)
        
        switch_btn = ghost_button("Sudah punya akun? Sign In", PALETTE['text_dim'])
        switch_btn.setStyleSheet(switch_btn.styleSheet().replace("border: 1.5px solid", "border: none;"))
        switch_btn.clicked.connect(lambda: self.switch_mode(0))
        layout.addWidget(switch_btn)
        
        layout.addStretch()
        self.stack.addWidget(page)
        
    def switch_mode(self, index):
        self.stack.setCurrentIndex(index)
        if index == 0:
            self.title_lbl.setText("Masuk ke ZooBase")
            self.login_user.clear()
            self.login_pass.clear()
        else:
            self.title_lbl.setText("Daftar Akun Baru")
            self.reg_user.clear()
            self.reg_pass.clear()
            self.reg_pass2.clear()

    def handle_login(self):
        user = self.login_user.text().strip()
        pwd = self.login_pass.text().strip()
        if not user or not pwd:
            QMessageBox.warning(self, "Error", "Username dan Password harus diisi!")
            return
            
        if authenticate_user(user, pwd):
            self.login_successful.emit()
        else:
            QMessageBox.warning(self, "Error", "Username atau Password salah!")
            
    def handle_register(self):
        user = self.reg_user.text().strip()
        pwd = self.reg_pass.text().strip()
        pwd2 = self.reg_pass2.text().strip()
        
        if not user or not pwd or not pwd2:
            QMessageBox.warning(self, "Error", "Semua field harus diisi!")
            return
            
        if pwd != pwd2:
            QMessageBox.warning(self, "Error", "Password tidak cocok!")
            return
            
        if register_user(user, pwd):
            QMessageBox.information(self, "Sukses", "Akun berhasil dibuat! Silakan login.")
            self.switch_mode(0)
            self.login_user.setText(user)
        else:
            QMessageBox.warning(self, "Error", "Username sudah terdaftar!")
