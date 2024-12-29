import sys, Servises.ConfigManager, asyncio
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QProgressBar, QGroupBox, QLabel, QLineEdit, QMessageBox

class ConfigApp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Config Application")
        self.setGeometry(100, 100, 600, 400)

        # main layout
        widgets = QWidget()
        self.setCentralWidget(widgets)

        self.main_layout = QVBoxLayout()
        widgets.setLayout(self.main_layout)

        # nav bar
        self.nav_bar = QHBoxLayout()
        self.main_layout.addLayout(self.nav_bar)

        self.nav_bar_buttons = [QPushButton("Setup"), QPushButton("Connect config")]

        for button in self.nav_bar_buttons:
            self.nav_bar.addWidget(button)
        
        self.nav_bar_buttons[0].clicked.connect(self.show_setup_menu)
        self.nav_bar_buttons[1].clicked.connect(self.show_config_menu)

        # menu boxs
        self.config_box = QGroupBox("Configuration")
        self.config_box_layout = QVBoxLayout()
        self.config_box.setLayout(self.config_box_layout)

        self.setup_box = QGroupBox("Setup")
        self.setup_box_layout = QVBoxLayout()
        self.setup_box.setLayout(self.setup_box_layout)

        self.setup_box_progres = QGroupBox("Install Progress...")
        self.setup_progres_box_layout = QVBoxLayout()
        self.setup_box_progres.setLayout(self.setup_progres_box_layout)

        # Initially hide the config box
        self.config_box.hide()
        self.setup_box_progres.hide()

        # Add group boxes to the main layout
        self.main_layout.addWidget(self.config_box)
        self.main_layout.addWidget(self.setup_box)
        self.main_layout.addWidget(self.setup_box_progres)

        # setup menu
        self.setup_info = QLabel("qqq")
        self.setup_box_layout.addWidget(self.setup_info)

        self.setup_button = QPushButton("Setup DB")
        self.setup_box_layout.addWidget(self.setup_button)
        self.setup_button.clicked.connect(self.setup_db)

        self.reset_button = QPushButton("Reset DB")
        self.setup_box_layout.addWidget(self.reset_button)
        self.reset_button.clicked.connect(self.setup_db)

        self.setup_log_bar = QTextEdit()
        self.setup_log_bar.setReadOnly(True)
        self.setup_progres_box_layout.addWidget(self.setup_log_bar)

        self.setup_progress_bar = QProgressBar()
        self.setup_progress_bar.setRange(0, 100)
        self.setup_progres_box_layout.addWidget(self.setup_progress_bar)

        # config menu
        self.config_ip_info = QLabel("Server ip")
        self.config_box_layout.addWidget(self.config_ip_info)

        self.config_ip_input = QLineEdit()
        self.config_box_layout.addWidget(self.config_ip_input)

        self.config_token_info = QLabel("API token")
        self.config_box_layout.addWidget(self.config_token_info)

        self.config_token_input = QLineEdit()
        self.config_box_layout.addWidget(self.config_token_input)

        self.config_save_button = QPushButton("Save")
        self.config_box_layout.addWidget(self.config_save_button)

    def show_info_window(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Info")
        msg.setText("Finish")

        msg.exec_()
    
    def show_setup_menu(self):
        self.setup_box.show()
        self.config_box.hide()
    
    def show_config_menu(self):
        self.setup_box.hide()
        self.config_box.show()

    def setup_db(self):
        self.setup_box.hide()
        self.setup_box_progres.show()

        self.setup_log_bar.setPlainText("")
        self.setup_progress_bar.setValue(0)

        asyncio.run(Servises.ConfigManager.db_setup_script(self.print_setup_log))  

    def print_setup_log(self, mess: str, progress: int):
        text = self.setup_log_bar.toPlainText()

        text += "\n" + mess

        self.setup_log_bar.setPlainText(text)
        self.setup_progress_bar.setValue(progress)

        if progress == 100:
            self.setup_box_progres.hide()
            self.setup_box.show()
            self.show_info_window()         

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = ConfigApp()
    window.show()

    sys.exit(app.exec_())
