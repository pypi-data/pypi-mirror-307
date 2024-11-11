import sys
import cv2
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QSlider, QSizePolicy, QMessageBox
from PyQt5.QtGui import QImage, QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt

class AnnotationTool(QMainWindow):
    def __init__(self):
        super().__init__()

        # Video variables
        self.video_path = None
        self.cap = None
        self.current_frame = 0
        self.total_frames = 0
        self.annotations = []
        self.current_action = None
        self.current_posture = None

        # Pigeons for which we will create timeline bars
        self.pigeons = ['P1', 'P2', 'P3', 'P4']
        self.timeline_bars = {}

        # GUI components
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Pigeon Behavior Annotation Tool')
        self.setFixedSize(1200, 1040)

        # Video display label
        self.video_label = QLabel(self)
        self.video_label.setScaledContents(True)
        self.video_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Frame information label
        self.frame_info_label = QLabel("Frame: 0 / 0", self)

        # Pigeon selection
        self.pigeon_selector = QComboBox(self)
        self.pigeon_selector.addItems(self.pigeons)

        # Behavior selection
        self.behavior_selector = QComboBox(self)
        self.behavior_selector.addItems(['Feeding', 'Drinking', 'Grit', 'Grooming', 'Incubation', 'Feeding young', 'Walking'])
        self.behavior_selector.currentIndexChanged.connect(self.update_behavior_color)

        # Behavior color display
        self.behavior_color_display = QLabel(self)
        self.behavior_color_display.setFixedSize(50, 20)
        self.behavior_color_display.setStyleSheet("background-color: white;")
        self.update_behavior_color()  # Initialize behavior color display

        # Posture selection
        self.posture_selector = QComboBox(self)
        self.posture_selector.addItems(['Standing', 'Motion', 'Squatting', 'Tail up'])
        self.posture_selector.currentIndexChanged.connect(self.update_posture_color)

        # Posture color display
        self.posture_color_display = QLabel(self)
        self.posture_color_display.setFixedSize(50, 20)
        self.posture_color_display.setStyleSheet("background-color: #e3e3e3;")
        self.update_posture_color()  # Initialize posture color display

        # Control buttons
        self.load_button = QPushButton('Load Video', self)
        self.load_button.clicked.connect(self.load_video)

        self.prev_button = QPushButton('Previous Frame', self)
        self.prev_button.clicked.connect(self.prev_frame)

        self.next_button = QPushButton('Next Frame', self)
        self.next_button.clicked.connect(self.next_frame)

        self.start_action_button = QPushButton('Start Action', self)
        self.start_action_button.clicked.connect(self.start_action)

        self.end_action_button = QPushButton('End Action', self)
        self.end_action_button.clicked.connect(self.end_action)

        self.start_posture_button = QPushButton('Start Posture', self)
        self.start_posture_button.clicked.connect(self.start_posture)

        self.end_posture_button = QPushButton('End Posture', self)
        self.end_posture_button.clicked.connect(self.end_posture)

        self.export_button = QPushButton('Export Annotations', self)
        self.export_button.clicked.connect(self.export_annotations)

        self.export_sorted_button = QPushButton('Export Sorted Format', self)
        self.export_sorted_button.clicked.connect(self.export_sorted_annotations)

        # Video progress bar
        self.progress_slider = QSlider(Qt.Horizontal, self)
        self.progress_slider.sliderMoved.connect(self.slider_moved)

        # Timeline layout for each pigeon
        timeline_layout = QVBoxLayout()
        for pigeon in self.pigeons:
            row_layout_behavior = QHBoxLayout()
            label_behavior = QLabel(f"{pigeon}_B", self)
            timeline_bar_behavior = QLabel(self)
            timeline_bar_behavior.setFixedHeight(20)
            timeline_bar_behavior.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            timeline_bar_behavior.setStyleSheet("background-color: white; border: 1px solid black;")
            self.timeline_bars[f"{pigeon}_B"] = timeline_bar_behavior
            
            row_layout_behavior.addWidget(label_behavior)
            row_layout_behavior.addWidget(timeline_bar_behavior)
            timeline_layout.addLayout(row_layout_behavior)

            row_layout_posture = QHBoxLayout()
            label_posture = QLabel(f"{pigeon}_S", self)
            timeline_bar_posture = QLabel(self)
            timeline_bar_posture.setFixedHeight(20)
            timeline_bar_posture.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            timeline_bar_posture.setStyleSheet("background-color: #e3e3e3; border: 1px solid black;")
            self.timeline_bars[f"{pigeon}_S"] = timeline_bar_posture
            
            row_layout_posture.addWidget(label_posture)
            row_layout_posture.addWidget(timeline_bar_posture)
            timeline_layout.addLayout(row_layout_posture)

            # Add a line separator between each pigeon section
            line_separator = QLabel(self)
            line_separator.setFixedHeight(1)
            line_separator.setStyleSheet("background-color: black;")
            timeline_layout.addWidget(line_separator)

        # Layout for controls
        controls_layout1 = QHBoxLayout()
        controls_layout1.addWidget(self.load_button)
        controls_layout1.addWidget(self.pigeon_selector)
        controls_layout1.addWidget(self.prev_button)
        controls_layout1.addWidget(self.next_button)
        controls_layout1.addWidget(self.export_button)
        controls_layout1.addWidget(self.export_sorted_button)

        controls_layout2 = QHBoxLayout()
        controls_layout2.addWidget(self.behavior_selector)
        controls_layout2.addWidget(self.behavior_color_display)
        controls_layout2.addWidget(self.start_action_button)
        controls_layout2.addWidget(self.end_action_button)
        controls_layout2.addWidget(self.posture_selector)
        controls_layout2.addWidget(self.posture_color_display)
        controls_layout2.addWidget(self.start_posture_button)
        controls_layout2.addWidget(self.end_posture_button)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.video_label)
        main_layout.addWidget(self.frame_info_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.progress_slider)
        main_layout.addLayout(timeline_layout)
        main_layout.addLayout(controls_layout1)
        main_layout.addLayout(controls_layout2)

        # Set main layout
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def update_behavior_color(self):
        behavior = self.behavior_selector.currentText()
        color = "white"
        if behavior == 'Feeding':
            color = "red"
        elif behavior == 'Drinking':
            color = "blue"
        elif behavior == 'Grit':
            color = "green"
        elif behavior == 'Grooming':
            color = "cyan"
        elif behavior == 'Incubation':
            color = "magenta"
        elif behavior == 'Feeding young':
            color = "yellow"
        elif behavior == 'Walking':
            color = "orange"
        self.behavior_color_display.setStyleSheet(f"background-color: {color};")

    def update_posture_color(self):
        posture = self.posture_selector.currentText()
        color = "#e3e3e3"
        if posture == 'Standing':
            color = "purple"
        elif posture == 'Motion':
            color = "brown"
        elif posture == 'Squatting':
            color = "orange"
        elif posture == 'Tail up':
            color = "pink"
        self.posture_color_display.setStyleSheet(f"background-color: {color};")

    def load_video(self):
        self.video_path, _ = QFileDialog.getOpenFileName(self, 'Open Video')
        if self.video_path:
            if self.cap:
                self.cap.release()
            self.cap = cv2.VideoCapture(self.video_path)
            if not self.cap.isOpened():
                print("Error: Cannot open video.")
                return

            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.progress_slider.setRange(0, self.total_frames - 1)
            self.current_frame = 0
            self.update_frame_info()
            self.show_frame()

    def show_frame(self):
        if not self.cap or not self.cap.isOpened():
            return
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame)
        ret, frame = self.cap.read()
        if not ret:
            print("Error: Cannot read frame.")
            return
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w = frame.shape[:2]
        qimg = QImage(frame.data, w, h, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qimg))
        self.progress_slider.setValue(self.current_frame)
        self.update_frame_info()
        self.update_timeline()  # Update timeline after showing each frame

    def update_frame_info(self):
        self.frame_info_label.setText(f"Frame: {self.current_frame} / {self.total_frames}")

    def prev_frame(self):
        if self.current_frame > 0:
            self.current_frame -= 1
            self.show_frame()

    def next_frame(self):
        if self.current_frame < self.total_frames - 1:
            self.current_frame += 1
            self.show_frame()

    def slider_moved(self, position):
        self.current_frame = position
        self.show_frame()
        self.update_timeline()

    def start_action(self):
        pigeon = self.pigeon_selector.currentText()
        behavior = self.behavior_selector.currentText()

        self.current_action = {
            'pigeon_id': pigeon,
            'action_label': behavior,
            'start_frame': self.current_frame,
            'end_frame': None
        }

        # Visualize the start of the action
        self.update_timeline()

    def end_action(self):
        if self.current_action:
            self.current_action['end_frame'] = self.current_frame
            self.annotations.append({
                'pigeon_id': self.current_action['pigeon_id'],
                'start_frame': self.current_action['start_frame'],
                'end_frame': self.current_action['end_frame'],
                'action_label': self.current_action['action_label'],
                'posture_label': -1  # Default for posture
            })
            self.current_action = None
            self.update_timeline()

    def start_posture(self):
        pigeon = self.pigeon_selector.currentText()
        posture = self.posture_selector.currentText()

        self.current_posture = {
            'pigeon_id': pigeon,
            'posture_label': posture,
            'start_frame': self.current_frame,
            'end_frame': None
        }

        # Visualize the start of the posture
        self.update_timeline()

    def end_posture(self):
        if self.current_posture:
            self.current_posture['end_frame'] = self.current_frame
            self.annotations.append({
                'pigeon_id': self.current_posture['pigeon_id'],
                'start_frame': self.current_posture['start_frame'],
                'end_frame': self.current_posture['end_frame'],
                'posture_label': self.current_posture['posture_label'],
                'action_label': -1  # Default for action
            })
            self.current_posture = None
            self.update_timeline()

    def update_timeline(self):
        for pigeon in self.pigeons:
            timeline_bar_behavior = self.timeline_bars[f"{pigeon}_B"]
            timeline_bar_posture = self.timeline_bars[f"{pigeon}_S"]

            timeline_image_behavior = QImage(timeline_bar_behavior.width(), timeline_bar_behavior.height(), QImage.Format_RGB32)
            timeline_image_behavior.fill(Qt.white)

            timeline_image_posture = QImage(timeline_bar_posture.width(), timeline_bar_posture.height(), QImage.Format_RGB32)
            timeline_image_posture.fill(QColor(211, 211, 211))

            painter_behavior = QPainter(timeline_image_behavior)
            painter_posture = QPainter(timeline_image_posture)

            # Draw behavior annotations
            for annotation in self.annotations:
                if annotation['pigeon_id'] == pigeon:
                    if annotation.get('action_label', -1) != -1:
                        start_frame = annotation.get('start_frame')
                        end_frame = annotation.get('end_frame')
                        if start_frame is not None and end_frame is not None:
                            start_x = int(start_frame / self.total_frames * timeline_bar_behavior.width())
                            end_x = int(end_frame / self.total_frames * timeline_bar_behavior.width())
                            width = end_x - start_x
                            color = QColor("red") if annotation['action_label'] == 'Feeding' else \
                                    QColor("blue") if annotation['action_label'] == 'Drinking' else \
                                    QColor("green") if annotation['action_label'] == 'Grit' else \
                                    QColor("cyan") if annotation['action_label'] == 'Grooming' else \
                                    QColor("magenta") if annotation['action_label'] == 'Incubation' else \
                                    QColor("yellow") if annotation['action_label'] == 'Feeding young' else \
                                    QColor("orange")  # Walking
                            painter_behavior.fillRect(start_x, 0, width, timeline_bar_behavior.height(), color)

            # Draw posture annotations
            for annotation in self.annotations:
                if annotation['pigeon_id'] == pigeon:
                    if annotation.get('posture_label', -1) != -1:
                        start_frame = annotation.get('start_frame')
                        end_frame = annotation.get('end_frame')
                        if start_frame is not None and end_frame is not None:
                            start_x = int(start_frame / self.total_frames * timeline_bar_posture.width())
                            end_x = int(end_frame / self.total_frames * timeline_bar_posture.width())
                            width = end_x - start_x
                            color = QColor("purple") if annotation['posture_label'] == 'Standing' else \
                                    QColor("brown") if annotation['posture_label'] == 'Motion' else \
                                    QColor("orange") if annotation['posture_label'] == 'Squatting' else \
                                    QColor("pink")  # Tail up
                            painter_posture.fillRect(start_x, 0, width, timeline_bar_posture.height(), color)

            # Draw the black line for the current action
            if self.current_action and self.current_action['pigeon_id'] == pigeon:
                current_action_black_x = int(self.current_action['start_frame'] / self.total_frames * timeline_bar_behavior.width())
                painter_behavior.fillRect(current_action_black_x, 0, 2, timeline_bar_behavior.height(), QColor("black"))

                # Fill the current action color from start to current frame
                current_fill_x = int(self.current_frame / self.total_frames * timeline_bar_behavior.width())
                color = QColor("red") if self.current_action['action_label'] == 'Feeding' else \
                        QColor("blue") if self.current_action['action_label'] == 'Drinking' else \
                        QColor("green") if self.current_action['action_label'] == 'Grit' else \
                        QColor("cyan") if self.current_action['action_label'] == 'Grooming' else \
                        QColor("magenta") if self.current_action['action_label'] == 'Incubation' else \
                        QColor("yellow") if self.current_action['action_label'] == 'Feeding young' else \
                        QColor("orange")  # Walking
                painter_behavior.fillRect(current_action_black_x, 0, current_fill_x - current_action_black_x, timeline_bar_behavior.height(), color)

            # Draw the black line for the current posture
            if self.current_posture and self.current_posture['pigeon_id'] == pigeon:
                current_posture_black_x = int(self.current_posture['start_frame'] / self.total_frames * timeline_bar_posture.width())
                painter_posture.fillRect(current_posture_black_x, 0, 2, timeline_bar_posture.height(), QColor("black"))

                # Fill the current posture color from start to current frame
                current_fill_x = int(self.current_frame / self.total_frames * timeline_bar_posture.width())
                color = QColor("purple") if self.current_posture['posture_label'] == 'Standing' else \
                        QColor("brown") if self.current_posture['posture_label'] == 'Motion' else \
                        QColor("orange") if self.current_posture['posture_label'] == 'Squatting' else \
                        QColor("pink")  # Tail up
                painter_posture.fillRect(current_posture_black_x, 0, current_fill_x - current_posture_black_x, timeline_bar_posture.height(), color)

            painter_behavior.end()
            painter_posture.end()

            # Draw separator line
            if pigeon != self.pigeons[-1]:
                separator = QPainter(timeline_image_behavior)
                separator.fillRect(timeline_bar_behavior.width() - 1, 0, 1, timeline_bar_behavior.height(), QColor("black"))
                separator.end()

            timeline_bar_behavior.setPixmap(QPixmap.fromImage(timeline_image_behavior))
            timeline_bar_posture.setPixmap(QPixmap.fromImage(timeline_image_posture))

    def export_annotations(self):
        save_path, _ = QFileDialog.getSaveFileName(self, 'Save Annotations', '', 'CSV Files (*.csv)')
        if save_path:
            try:
                df = pd.DataFrame(self.annotations)
                df.to_csv(save_path, index=False)
                QMessageBox.information(self, 'Success', 'Annotations saved successfully.')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to save annotations: {str(e)}')

    def export_sorted_annotations(self):
        save_path, _ = QFileDialog.getSaveFileName(self, 'Save Sorted Annotations', '', 'CSV Files (*.csv)')
        if save_path:
            try:
                sorted_annotations = []
                for frame_id in range(self.total_frames):
                    for pigeon in self.pigeons:
                        action_label = -1
                        posture_label = -1
                        for annotation in self.annotations:
                            if annotation['start_frame'] <= frame_id <= annotation['end_frame']:
                                if annotation['pigeon_id'] == pigeon:
                                    action_label = annotation['action_label'] if annotation['action_label'] != -1 else action_label
                                    posture_label = annotation['posture_label'] if annotation['posture_label'] != -1 else posture_label
                        sorted_annotations.append({
                            'frame_id': frame_id,
                            'pigeon_id': pigeon,
                            'action_label': action_label,
                            'posture_label': posture_label
                        })
                df_sorted = pd.DataFrame(sorted_annotations, columns=['frame_id', 'pigeon_id', 'action_label', 'posture_label'])
                df_sorted.to_csv(save_path, index=False)
                QMessageBox.information(self, 'Success', 'Sorted annotations saved successfully.')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to save sorted annotations: {str(e)}')

    def keyPressEvent(self, event):
            """Handle key press events for shortcuts."""
            key = event.key()

            # Navigation shortcuts
            if key == Qt.Key_D:  # Pressing 'D' for Next Frame
                self.next_frame()
            elif key == Qt.Key_S:  # Pressing 'S' for Previous Frame
                self.prev_frame()

            # Pigeon selection shortcuts
            elif key == Qt.Key_1:  # Pressing '1' for P_1
                self.pigeon_selector.setCurrentIndex(0)
            elif key == Qt.Key_2:  # Pressing '2' for P_2
                self.pigeon_selector.setCurrentIndex(1)
            elif key == Qt.Key_3:  # Pressing '3' for P_3
                self.pigeon_selector.setCurrentIndex(2)
            elif key == Qt.Key_4:  # Pressing '4' for P_4
                self.pigeon_selector.setCurrentIndex(3)    
    
def main():
    app = QApplication(sys.argv)
    ex = AnnotationTool()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
