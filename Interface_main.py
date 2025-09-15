import sys
import floor_full
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QListWidget, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QVBoxLayout, QSplitter, QLabel, QHeaderView, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


FLOORS = floor_full.FLOORS

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prototype — Distribution de médicaments")
        self.resize(1100, 600)

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(8, 8, 8, 8)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter)

        # ---- Colonne gauche ----
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addWidget(QLabel("<b>Étages</b>"))
        self.floor_list = QListWidget()
        for floor in FLOORS.keys():
            self.floor_list.addItem(floor)
        self.floor_list.currentTextChanged.connect(self.on_floor_changed)
        left_layout.addWidget(self.floor_list)
        splitter.addWidget(left_widget)
        left_widget.setMinimumWidth(180)

        # Droite : recherche + tableau avec éatges 
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)

        # Barre de recherche
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Rechercher (nom ou numéro de chambre)...")
        self.search_bar.textChanged.connect(self.apply_search_filter)
        right_layout.addWidget(self.search_bar)

        # Tableau de distribution
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            "No. chambre", "Nom, Prénom", "Distribution #1", "Distribution #2",
            "Distribution #3", "Distribution #4"
        ])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        
        self.table.setSortingEnabled(True)

        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        right_layout.addWidget(self.table)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(1, 1)

        
        self.current_rows = []

      
        if self.floor_list.count() > 0:
            self.floor_list.setCurrentRow(0)

    def on_floor_changed(self, floor_name: str):
        #Permet de montrer les patients à chaque étages
        self.current_rows = FLOORS.get(floor_name, [])
        self.populate_table(self.current_rows)

    def populate_table(self, rows):
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        
        now = datetime.now()
        now_minutes = now.hour * 60 + now.minute  # Temps actuel (pour simuler une flotte de pilulier)

        for row_data in rows:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                if col >= 2:  # Colonne de distribution(s)
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    if value == "":
                        item.setBackground(QColor("#d1cbc5"))
                    else:
                        try:
                            h, m = map(int, value.split(":"))
                            t_minutes = h * 60 + m
                            delta = t_minutes - now_minutes  # difference in minutes
                            if -30 <= delta <= 30:
                                color = QColor("#ed9e53") # orange: within ±30 min
                            elif delta < -30:
                                color = QColor("#0b8d0b")  # green: past
                            else:
                                color = QColor("#d1cbc5")  # gray: future
                            item.setBackground(color)
                        except ValueError:
                            item.setBackground(QColor("#d1cbc5"))
                self.table.setItem(row, col, item)
        self.table.setSortingEnabled(True)  


    def apply_search_filter(self, text: str):
        #permet de faire la recherche parmis les patients d'un étage
        text = text.strip().lower()
        if not text:
            self.populate_table(self.current_rows)
            return
        filtered = [
            row for row in self.current_rows
            if text in row[0].lower() or text in row[1].lower()
        ]
        self.populate_table(filtered)

    def confirm_distribution(self):
        #Permet à l'infirmière de changer le status d'une prise de médicament
        sum = 2+1



def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()