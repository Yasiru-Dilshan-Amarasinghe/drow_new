"""
Professional UI for Driver Drowsiness Detection System using PyQt6
Industry-level interface with video display, controls, and analytics
"""

import sys
import cv2
import numpy as np
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSlider, QGroupBox, QGridLayout, QTabWidget,
    QTableWidget, QTableWidgetItem, QComboBox, QSpinBox, QDoubleSpinBox,
    QCheckBox, QStatusBar, QProgressBar, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QImage, QPixmap, QFont, QColor, QPalette
from PyQt6.QtChart import QChart, QChartView, QLineSeries
from PyQt6.QtCore import QPointF

from src.eye_detector import EyeDetector
from src.drowsiness_detector import DrowsinessDetector
from src.utils import setup_logging, draw_detections, display_stats


class VideoCapture(QThread):
    """Thread for capturing video frames without blocking UI"""
    
    frame_captured = pyqtSignal(np.ndarray)
    error_occurred = pyqtSignal(str)
    fps_updated = pyqtSignal(float)
    
    def __init__(self, camera_index=0):
        super().__init__()
        self.camera_index = camera_index
        self.running = False
        self.cap = None
        self.fps = 0
        self.frame_count = 0
        
    def run(self):
        """Capture video frames"""
        self.cap = cv2.VideoCapture(self.camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        if not self.cap.isOpened():
            self.error_occurred.emit("Failed to open camera")
            return
        
        self.running = True
        last_time = datetime.now()
        
        while self.running:
            ret, frame = self.cap.read()
            
            if ret:
                self.frame_captured.emit(frame)
                self.frame_count += 1
                
                # Update FPS every second
                current_time = datetime.now()
                elapsed = (current_time - last_time).total_seconds()
                if elapsed >= 1:
                    self.fps = self.frame_count / elapsed
                    self.fps_updated.emit(self.fps)
                    self.frame_count = 0
                    last_time = current_time
            else:
                self.error_occurred.emit("Failed to read frame from camera")
                break
        
        self.cap.release()
    
    def stop(self):
        """Stop video capture"""
        self.running = False
        self.wait()


class DrowsinessDetectionUI(QMainWindow):
    """Professional PyQt6 UI for Drowsiness Detection System"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Professional Driver Drowsiness Detection System")
        self.setGeometry(100, 100, 1400, 900)
        
        # Initialize components
        self.logger = setup_logging("drowsiness_detection.log")
        self.eye_detector = EyeDetector()
        self.drowsiness_detector = DrowsinessDetector()
        
        # Video capture thread
        self.video_thread = None
        
        # Statistics
        self.events = []
        self.ear_history = []
        
        # Setup UI
        self.setup_ui()
        self.apply_theme()
        
        # Timer for updating UI
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_statistics)
        self.update_timer.start(500)
    
    def setup_ui(self):
        """Setup the main UI layout"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout()
        
        # Left side - Video display
        left_panel = self.create_video_panel()
        main_layout.addWidget(left_panel, 3)
        
        # Right side - Controls and info
        right_panel = self.create_control_panel()
        main_layout.addWidget(right_panel, 1)
        
        central_widget.setLayout(main_layout)
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def create_video_panel(self):
        """Create video display panel"""
        panel = QGroupBox("Live Video Feed")
        layout = QVBoxLayout()
        
        # Video label
        self.video_label = QLabel()
        self.video_label.setMinimumSize(QSize(640, 480))
        self.video_label.setStyleSheet("background-color: black; border: 2px solid #2c3e50;")
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.video_label)
        
        panel.setLayout(layout)
        return panel
    
    def create_control_panel(self):
        """Create control panel with tabs"""
        # Tab widget
        tabs = QTabWidget()
        
        # Control tab
        control_tab = self.create_controls_tab()
        tabs.addTab(control_tab, "Controls")
        
        # Settings tab
        settings_tab = self.create_settings_tab()
        tabs.addTab(settings_tab, "Settings")
        
        # Statistics tab
        statistics_tab = self.create_statistics_tab()
        tabs.addTab(statistics_tab, "Statistics")
        
        # System Info tab
        info_tab = self.create_info_tab()
        tabs.addTab(info_tab, "System Info")
        
        return tabs
    
    def create_controls_tab(self):
        """Create controls tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Start/Stop buttons
        button_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("▶ START")
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        self.start_btn.clicked.connect(self.start_detection)
        button_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹ STOP")
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """)
        self.stop_btn.clicked.connect(self.stop_detection)
        self.stop_btn.setEnabled(False)
        button_layout.addWidget(self.stop_btn)
        
        layout.addLayout(button_layout)
        
        # Status indicator
        status_box = QGroupBox("Status")
        status_layout = QVBoxLayout()
        
        self.status_label = QLabel("● STOPPED")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #e74c3c;")
        status_layout.addWidget(self.status_label)
        
        self.fps_label = QLabel("FPS: 0.0")
        self.fps_label.setStyleSheet("font-size: 12px;")
        status_layout.addWidget(self.fps_label)
        
        status_box.setLayout(status_layout)
        layout.addWidget(status_box)
        
        # Alert status
        alert_box = QGroupBox("Alert Status")
        alert_layout = QVBoxLayout()
        
        self.alert_label = QLabel("✓ No Drowsiness Detected")
        self.alert_label.setStyleSheet("font-size: 12px; color: #27ae60; font-weight: bold;")
        alert_layout.addWidget(self.alert_label)
        
        alert_box.setLayout(alert_layout)
        layout.addWidget(alert_box)
        
        # Key metrics
        metrics_box = QGroupBox("Key Metrics")
        metrics_layout = QGridLayout()
        
        metrics_layout.addWidget(QLabel("EAR:"), 0, 0)
        self.ear_label = QLabel("0.00")
        self.ear_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        metrics_layout.addWidget(self.ear_label, 0, 1)
        
        metrics_layout.addWidget(QLabel("Events:"), 1, 0)
        self.events_label = QLabel("0")
        self.events_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        metrics_layout.addWidget(self.events_label, 1, 1)
        
        metrics_layout.addWidget(QLabel("Time:"), 2, 0)
        self.time_label = QLabel("00:00:00")
        self.time_label.setStyleSheet("font-size: 12px;")
        metrics_layout.addWidget(self.time_label, 2, 1)
        
        metrics_box.setLayout(metrics_layout)
        layout.addWidget(metrics_box)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_settings_tab(self):
        """Create settings tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Camera settings
        camera_box = QGroupBox("Camera Settings")
        camera_layout = QGridLayout()
        
        camera_layout.addWidget(QLabel("Camera:"), 0, 0)
        self.camera_combo = QComboBox()
        self.camera_combo.addItems(["USB Webcam", "CSI Camera", "Custom"])
        camera_layout.addWidget(self.camera_combo, 0, 1)
        
        camera_box.setLayout(camera_layout)
        layout.addWidget(camera_box)
        
        # Detection settings
        detection_box = QGroupBox("Detection Settings")
        detection_layout = QGridLayout()
        
        detection_layout.addWidget(QLabel("EAR Threshold:"), 0, 0)
        self.ear_threshold_spin = QDoubleSpinBox()
        self.ear_threshold_spin.setRange(0.1, 1.0)
        self.ear_threshold_spin.setValue(0.3)
        self.ear_threshold_spin.setSingleStep(0.05)
        detection_layout.addWidget(self.ear_threshold_spin, 0, 1)
        
        detection_layout.addWidget(QLabel("Consecutive Frames:"), 1, 0)
        self.consec_frames_spin = QSpinBox()
        self.consec_frames_spin.setRange(5, 100)
        self.consec_frames_spin.setValue(30)
        detection_layout.addWidget(self.consec_frames_spin, 1, 1)
        
        detection_box.setLayout(detection_layout)
        layout.addWidget(detection_box)
        
        # Alert settings
        alert_box = QGroupBox("Alert Settings")
        alert_layout = QVBoxLayout()
        
        self.audio_alert_check = QCheckBox("Enable Audio Alert")
        self.audio_alert_check.setChecked(True)
        alert_layout.addWidget(self.audio_alert_check)
        
        self.visual_alert_check = QCheckBox("Enable Visual Alert")
        self.visual_alert_check.setChecked(True)
        alert_layout.addWidget(self.visual_alert_check)
        
        alert_box.setLayout(alert_layout)
        layout.addWidget(alert_box)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_statistics_tab(self):
        """Create statistics tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Statistics summary
        summary_box = QGroupBox("Session Statistics")
        summary_layout = QGridLayout()
        
        summary_layout.addWidget(QLabel("Total Events:"), 0, 0)
        self.total_events_label = QLabel("0")
        self.total_events_label.setStyleSheet("font-weight: bold;")
        summary_layout.addWidget(self.total_events_label, 0, 1)
        
        summary_layout.addWidget(QLabel("Average EAR:"), 1, 0)
        self.avg_ear_label = QLabel("0.00")
        self.avg_ear_label.setStyleSheet("font-weight: bold;")
        summary_layout.addWidget(self.avg_ear_label, 1, 1)
        
        summary_layout.addWidget(QLabel("Eyes Closed %:"), 2, 0)
        self.closed_pct_label = QLabel("0.0%")
        self.closed_pct_label.setStyleSheet("font-weight: bold;")
        summary_layout.addWidget(self.closed_pct_label, 2, 1)
        
        summary_layout.addWidget(QLabel("Session Duration:"), 3, 0)
        self.duration_label = QLabel("00:00:00")
        self.duration_label.setStyleSheet("font-weight: bold;")
        summary_layout.addWidget(self.duration_label, 3, 1)
        
        summary_box.setLayout(summary_layout)
        layout.addWidget(summary_box)
        
        # Progress indicator
        progress_box = QGroupBox("Drowsiness Level")
        progress_layout = QVBoxLayout()
        
        self.drowsiness_progress = QProgressBar()
        self.drowsiness_progress.setRange(0, 100)
        self.drowsiness_progress.setValue(0)
        progress_layout.addWidget(self.drowsiness_progress)
        
        progress_box.setLayout(progress_layout)
        layout.addWidget(progress_box)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_info_tab(self):
        """Create system info tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # System info
        info_box = QGroupBox("System Information")
        info_layout = QGridLayout()
        
        info_layout.addWidget(QLabel("Application:"), 0, 0)
        info_layout.addWidget(QLabel("Drowsiness Detection v1.0"), 0, 1)
        
        info_layout.addWidget(QLabel("Status:"), 1, 0)
        self.app_status = QLabel("Idle")
        info_layout.addWidget(self.app_status, 1, 1)
        
        info_layout.addWidget(QLabel("Last Update:"), 2, 0)
        self.last_update = QLabel(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        info_layout.addWidget(self.last_update, 2, 1)
        
        info_box.setLayout(info_layout)
        layout.addWidget(info_box)
        
        # About
        about_box = QGroupBox("About")
        about_layout = QVBoxLayout()
        
        about_text = QLabel(
            "Driver Drowsiness Detection System\n\n"
            "A real-time computer vision system for detecting\n"
            "driver fatigue and alerting when drowsiness is detected.\n\n"
            "Technology: OpenCV, PyQt6, Python"
        )
        about_text.setStyleSheet("color: #34495e; line-height: 1.5;")
        about_layout.addWidget(about_text)
        
        about_box.setLayout(about_layout)
        layout.addWidget(about_box)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def apply_theme(self):
        """Apply professional dark theme"""
        theme = """
        QMainWindow {
            background-color: #ecf0f1;
        }
        QGroupBox {
            color: #2c3e50;
            border: 2px solid #bdc3c7;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
            font-weight: bold;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px 0 3px;
        }
        QLabel {
            color: #2c3e50;
        }
        QTabWidget::pane {
            border: 1px solid #bdc3c7;
        }
        QTabBar::tab {
            background-color: #95a5a6;
            color: white;
            padding: 8px 20px;
            border: 1px solid #7f8c8d;
        }
        QTabBar::tab:selected {
            background-color: #3498db;
        }
        """
        self.setStyleSheet(theme)
    
    def start_detection(self):
        """Start drowsiness detection"""
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_label.setText("● RUNNING")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #27ae60;")
        self.app_status.setText("Running")
        
        # Start video capture thread
        if self.video_thread is None or not self.video_thread.isRunning():
            self.video_thread = VideoCapture()
            self.video_thread.frame_captured.connect(self.process_frame)
            self.video_thread.error_occurred.connect(self.handle_error)
            self.video_thread.fps_updated.connect(self.update_fps)
            self.video_thread.start()
        
        self.logger.info("Detection started")
    
    def stop_detection(self):
        """Stop drowsiness detection"""
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText("● STOPPED")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #e74c3c;")
        self.app_status.setText("Stopped")
        
        if self.video_thread:
            self.video_thread.stop()
        
        self.logger.info("Detection stopped")
    
    def process_frame(self, frame):
        """Process frame and update display"""
        # Detect faces and eyes
        faces = self.eye_detector.detect_faces(frame)
        
        current_ear = 0
        if len(faces) > 0:
            face = faces[0]
            eyes = self.eye_detector.detect_eyes(frame, face)
            current_ear = len(eyes) / 2 if len(eyes) > 0 else 0.2
            
            # Update drowsiness detector
            is_drowsy, counter, alarm_on = self.drowsiness_detector.update(current_ear)
            
            # Draw detections
            frame = draw_detections(frame, faces, eyes, is_drowsy, current_ear)
            
            # Update alert status
            if is_drowsy:
                self.alert_label.setText("⚠ DROWSINESS DETECTED!")
                self.alert_label.setStyleSheet("font-size: 12px; color: #e74c3c; font-weight: bold;")
            else:
                self.alert_label.setText("✓ No Drowsiness Detected")
                self.alert_label.setStyleSheet("font-size: 12px; color: #27ae60; font-weight: bold;")
        
        # Update EAR label
        self.ear_label.setText(f"{current_ear:.2f}")
        self.ear_history.append(current_ear)
        
        # Convert frame to QImage and display
        self.display_frame(frame)
    
    def display_frame(self, frame):
        """Convert and display frame in label"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        scaled_pixmap = pixmap.scaledToWidth(640, Qt.TransformationMode.SmoothTransformation)
        self.video_label.setPixmap(scaled_pixmap)
    
    def update_fps(self, fps):
        """Update FPS display"""
        self.fps_label.setText(f"FPS: {fps:.1f}")
    
    def update_statistics(self):
        """Update statistics display"""
        metrics = self.drowsiness_detector.get_drowsiness_metrics()
        self.total_events_label.setText(str(metrics['total_events']))
        self.avg_ear_label.setText(f"{metrics['avg_ear']:.3f}")
        self.closed_pct_label.setText(f"{metrics['closed_percentage']:.1f}%")
        
        # Update drowsiness progress
        drowsiness_level = min(int(metrics['closed_percentage']), 100)
        self.drowsiness_progress.setValue(drowsiness_level)
        
        # Update time
        self.time_label.setText(datetime.now().strftime("%H:%M:%S"))
        self.last_update.setText(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    def handle_error(self, error_msg):
        """Handle errors from video thread"""
        self.statusBar().showMessage(f"Error: {error_msg}")
        self.stop_detection()
    
    def closeEvent(self, event):
        """Handle application close"""
        if self.video_thread and self.video_thread.isRunning():
            self.stop_detection()
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = DrowsinessDetectionUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
