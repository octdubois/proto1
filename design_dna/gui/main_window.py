import sys
import random
import json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton, QSlider,
                             QSpinBox, QComboBox, QCheckBox, QTextEdit,
                             QGroupBox, QFormLayout, QMessageBox, QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt

from core.ground_truth import GroundTruth
from core.compatibility import CompatibilityEngine
from core.novelty import NoveltyEngine
from core.validator import Validator
from core.generator import DesignGenerator
from core.storage import StorageEngine
from core.config import AppConfig

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Design DNA Generator")
        self.resize(1000, 700)

        # Core Components
        self.gt = GroundTruth()
        self.compat = CompatibilityEngine()
        self.novelty = NoveltyEngine()
        self.validator = Validator(self.gt, self.compat)
        self.generator = DesignGenerator(self.gt, self.compat, self.novelty, self.validator)
        self.storage = StorageEngine()
        self.config = AppConfig()

        self.current_dna = None
        self.setup_ui()
        self.load_history()

    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # Left Panel - Controls
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)

        # Settings Group
        settings_group = QGroupBox("Generation Settings")
        settings_layout = QFormLayout()

        self.seed_input = QSpinBox()
        self.seed_input.setRange(0, 999999999)
        self.seed_input.setValue(random.randint(0, 999999999))

        random_seed_btn = QPushButton("Randomize Seed")
        random_seed_btn.clicked.connect(lambda: self.seed_input.setValue(random.randint(0, 999999999)))

        seed_layout = QHBoxLayout()
        seed_layout.addWidget(self.seed_input)
        seed_layout.addWidget(random_seed_btn)

        self.temp_slider = QSlider(Qt.Orientation.Horizontal)
        self.temp_slider.setRange(0, 100)
        self.temp_slider.setValue(self.config.default_temperature)
        self.temp_label = QLabel(str(self.config.default_temperature))
        self.temp_slider.valueChanged.connect(lambda v: self.temp_label.setText(str(v)))

        temp_layout = QHBoxLayout()
        temp_layout.addWidget(self.temp_slider)
        temp_layout.addWidget(self.temp_label)

        settings_layout.addRow("Seed:", seed_layout)
        settings_layout.addRow("Temperature:", temp_layout)

        # Duplicates
        self.avoid_exact_chk = QCheckBox("Avoid Exact Duplicates")
        self.avoid_exact_chk.setChecked(self.config.duplicate_detection.get("avoid_exact", True))

        self.avoid_near_chk = QCheckBox("Avoid Near Duplicates")
        self.avoid_near_chk.setChecked(self.config.duplicate_detection.get("avoid_near", False))

        settings_layout.addRow(self.avoid_exact_chk)
        settings_layout.addRow(self.avoid_near_chk)

        settings_group.setLayout(settings_layout)
        left_layout.addWidget(settings_group)

        # Locks Group
        locks_group = QGroupBox("Field Locks (Unchecked = Random)")
        self.locks_layout = QFormLayout()

        self.lock_combos = {}
        self.lock_checks = {}

        categories = {
            "occasion": "occasions",
            "theme": "themes",
            "subject": "subjects",
            "art_style": "art_styles"
        }

        for field, category in categories.items():
            check = QCheckBox(field.replace("_", " ").title())
            combo = QComboBox()
            combo.addItem("-- Select --", None)
            for entity in self.gt.get_entities(category):
                combo.addItem(entity.display_name, entity.id)
            combo.setEnabled(False)

            check.toggled.connect(combo.setEnabled)

            self.lock_checks[field] = check
            self.lock_combos[field] = combo

            row_layout = QHBoxLayout()
            row_layout.addWidget(check)
            row_layout.addWidget(combo)
            self.locks_layout.addRow(row_layout)

        locks_group.setLayout(self.locks_layout)
        left_layout.addWidget(locks_group)

        # Action Buttons
        generate_btn = QPushButton("Generate Design DNA")
        generate_btn.setStyleSheet("font-weight: bold; padding: 10px; background-color: #4CAF50; color: white;")
        generate_btn.clicked.connect(self.generate_dna)
        left_layout.addWidget(generate_btn)

        repro_regen_layout = QHBoxLayout()
        reproduce_btn = QPushButton("Reproduce Current")
        reproduce_btn.clicked.connect(self.reproduce_dna)
        regenerate_btn = QPushButton("Regenerate")
        regenerate_btn.clicked.connect(self.regenerate_dna)

        repro_regen_layout.addWidget(reproduce_btn)
        repro_regen_layout.addWidget(regenerate_btn)
        left_layout.addLayout(repro_regen_layout)

        left_layout.addStretch()
        main_layout.addWidget(left_panel, 1)

        # Right Panel - Tabs
        self.tabs = QTabWidget()

        # JSON Tab
        json_tab = QWidget()
        json_layout = QVBoxLayout(json_tab)

        self.json_viewer = QTextEdit()
        self.json_viewer.setStyleSheet("font-family: monospace;")
        json_layout.addWidget(self.json_viewer)

        json_btn_layout = QHBoxLayout()
        validate_json_btn = QPushButton("Validate JSON")
        validate_json_btn.clicked.connect(self.validate_manual_json)

        save_json_btn = QPushButton("Save Edited JSON")
        save_json_btn.clicked.connect(self.save_manual_json)

        copy_json_btn = QPushButton("Copy to Clipboard")
        copy_json_btn.clicked.connect(self.copy_json)

        json_btn_layout.addWidget(validate_json_btn)
        json_btn_layout.addWidget(save_json_btn)
        json_btn_layout.addWidget(copy_json_btn)
        json_layout.addLayout(json_btn_layout)

        self.tabs.addTab(json_tab, "JSON Output")

        # History Tab
        hist_tab = QWidget()
        hist_layout = QVBoxLayout(hist_tab)
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["ID", "Date", "Subject", "Style", "Novelty"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.history_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.history_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.history_table.itemDoubleClicked.connect(self.load_history_item)

        hist_layout.addWidget(self.history_table)

        hist_btn_layout = QHBoxLayout()
        load_hist_btn = QPushButton("Load Selected")
        load_hist_btn.clicked.connect(self.load_history_item_btn)
        hist_btn_layout.addWidget(load_hist_btn)
        hist_layout.addLayout(hist_btn_layout)

        self.tabs.addTab(hist_tab, "History")

        main_layout.addWidget(self.tabs, 2)

    def generate_dna(self):
        seed = self.seed_input.value()
        temp = self.temp_slider.value()

        locked_fields = {}
        for field, check in self.lock_checks.items():
            if check.isChecked():
                val = self.lock_combos[field].currentData()
                if val:
                    locked_fields[field] = val

        dna = self.generator.generate(seed, temp, locked_fields)
        self.current_dna = dna

        errors = self.validator.validate_dna(dna)
        if errors:
            QMessageBox.warning(self, "Validation Warnings", "\n".join(errors))

        avoid_exact = self.avoid_exact_chk.isChecked()
        avoid_near = self.avoid_near_chk.isChecked()
        thresh = self.config.duplicate_detection.get("near_duplicate_threshold", 0.85)

        if (avoid_exact and dna.validation.novelty_score == 0.0) or \
           (avoid_near and dna.validation.novelty_score < (1.0 - thresh)):

            msg = "Exact Duplicate Detected!" if dna.validation.novelty_score == 0.0 else "Near Duplicate Detected!"
            reply = QMessageBox.question(self, msg,
                                        f"{msg}\nNovelty: {dna.validation.novelty_score:.2f}. Accept anyway?",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.No:
                self.json_viewer.setPlainText("Generation rejected due to duplicate detection.")
                return

        # Output and Log
        filename = self.storage.save_dna(dna)
        self.storage.log_creation(dna, filename)

        # Update novelties memory
        self.novelty.add_to_history({
            "occasion": dna.context.occasion,
            "theme": dna.context.theme,
            "subject": dna.design.subject,
            "art_style": dna.design.art_style,
            "mood": dna.design.mood[0] if dna.design.mood else None,
            "palette": dna.design.palette,
            "composition": dna.design.composition
        })

        self.json_viewer.setPlainText(dna.model_dump_json(indent=4))
        self.load_history()

    def regenerate_dna(self):
        self.seed_input.setValue(random.randint(0, 999999999))
        self.generate_dna()

    def reproduce_dna(self):
        if self.current_dna:
            self.seed_input.setValue(self.current_dna.generation.seed)
            self.temp_slider.setValue(self.current_dna.generation.temperature)
            self.generate_dna()

    def validate_manual_json(self):
        try:
            txt = self.json_viewer.toPlainText()
            json.loads(txt)
            QMessageBox.information(self, "Valid JSON", "The JSON is valid.")
        except json.JSONDecodeError as e:
            QMessageBox.critical(self, "Invalid JSON", f"JSON is malformed:\n{str(e)}")

    def save_manual_json(self):
        try:
            txt = self.json_viewer.toPlainText()
            data = json.loads(txt)
            # Check if it has a generation ID
            if "generation" in data and "id" in data["generation"]:
                file_name = self.storage.json_dir / f"{data['generation']['id']}_edited.json"
                with open(file_name, "w") as f:
                    json.dump(data, f, indent=4)
                QMessageBox.information(self, "Saved", f"Saved successfully to {file_name}")
            else:
                QMessageBox.warning(self, "Error", "JSON missing 'generation.id'")
        except json.JSONDecodeError:
            QMessageBox.critical(self, "Error", "Cannot save invalid JSON.")

    def copy_json(self):
        QApplication.clipboard().setText(self.json_viewer.toPlainText())

    def load_history_item_btn(self):
        ranges = self.history_table.selectedRanges()
        if not ranges: return
        row = ranges[0].topRow()
        self.load_history_row(row)

    def load_history_item(self, item):
        self.load_history_row(item.row())

    def load_history_row(self, row):
        design_id = self.history_table.item(row, 0).text()
        # Find in log to get the file
        for entry in self.novelty.history:
            if entry.get("design_id") == design_id:
                filename = entry.get("filename")
                if filename:
                    file_path = self.storage.json_dir / filename
                    if file_path.exists():
                        with open(file_path, "r") as f:
                            self.json_viewer.setPlainText(f.read())
                        self.tabs.setCurrentIndex(0)

                        # Load seed and temp to UI for easy reproduction
                        self.seed_input.setValue(entry.get("seed", 0))
                        self.temp_slider.setValue(entry.get("temperature", 50))
                        return
        QMessageBox.warning(self, "Not Found", "Could not locate the saved JSON file.")

    def load_history(self):
        self.history_table.setRowCount(0)
        history = self.novelty.history

        for entry in reversed(history[-50:]): # Show last 50
            if "design_id" not in entry: continue # Skip novelty-only intermediate updates if any

            row = self.history_table.rowCount()
            self.history_table.insertRow(row)

            self.history_table.setItem(row, 0, QTableWidgetItem(str(entry.get("design_id", ""))))

            ts = entry.get("timestamp", "")[:19].replace("T", " ")
            self.history_table.setItem(row, 1, QTableWidgetItem(ts))

            self.history_table.setItem(row, 2, QTableWidgetItem(str(entry.get("subject", ""))))
            self.history_table.setItem(row, 3, QTableWidgetItem(str(entry.get("art_style", ""))))
            self.history_table.setItem(row, 4, QTableWidgetItem(f"{entry.get('novelty_score', 0):.2f}"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
