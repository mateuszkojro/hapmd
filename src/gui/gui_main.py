from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QMainWindow,
    QDoubleSpinBox,
    QLabel,
)
import sys


class ManualControll(QWidget):
    def __init__(self, rotor_controller):
        super(ManualControll, self).__init__()
        self.rotor_controller = rotor_controller
        self.left_button = QPushButton("Left")
        self.left_button.clicked.connect(self.left_button_clicked)
        self.right_button = QPushButton("Right")
        self.right_button.clicked.connect(self.right_button_clicked)
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_button_clicked)

        layout = QHBoxLayout()
        layout.addWidget(self.left_button)
        layout.addWidget(self.right_button)
        layout.addWidget(self.reset_button)

        self.setLayout(layout)

    def left_button_clicked(self):
        # self.rotor_controller.move_left()
        pass

    def right_button_clicked(self):
        # self.rotor_controller.move_right()
        pass

    def reset_button_clicked(self):
        # self.rotor_controller.reset()
        pass


class AngleSetup(QWidget):
    def __init__(self):
        super(AngleSetup, self).__init__()
        self.min_label = QLabel("Min:")
        self.min_spinbox = QDoubleSpinBox()
        self.max_label = QLabel("Max:")
        self.max_spinbox = QDoubleSpinBox()

        layout = QHBoxLayout()
        layout.addWidget(self.min_label)
        layout.addWidget(self.min_spinbox)
        layout.addWidget(self.max_label)
        layout.addWidget(self.max_spinbox)

        self.setLayout(layout)

    @property
    def min_angle(self):
        return self.min_spinbox.value()

    @property
    def max_angle(self):
        return self.max_spinbox.value()


class FrequencySetup(QWidget):
    def __init__(self):
        super(FrequencySetup, self).__init__()
        layout = QHBoxLayout()
        # TODO: Add unit selector
        self.generated_spinbox = QDoubleSpinBox()
        self.received_spinbox = QDoubleSpinBox()

        layout.addWidget(QLabel("Generated:"))
        layout.addWidget(self.generated_spinbox)
        layout.addWidget(QLabel("Received:"))
        layout.addWidget(self.received_spinbox)

        self.setLayout(layout)

    @property
    def receive_freq(self):
        return self.received_spinbox.value()

    @property
    def generate_freq(self):
        return self.generated_spinbox.value()


class MainWindow(QMainWindow):
    def __init__(self, rotor_controller, measurement_controller):
        super(MainWindow, self).__init__()

        # Inject deps
        self.rotor_controller = rotor_controller
        self.measurement_controller = measurement_controller

        self.setWindowTitle("HAPMD - controller")

        # Create sub menus
        # NOTE: Manual controll acccesses rhe rotor controller directly - should that be changed?
        self.manual_controll = ManualControll(rotor_controller=self.rotor_controller)
        self.angle_setup = AngleSetup()
        self.freq_setup = FrequencySetup()

        # Add action buttons
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_button_clicked)
        self.start_button = QPushButton("Start")
        self.start_button.setCheckable(True)
        self.start_button.toggled.connect(self.start_button_toggled)

        # Organize toolbar
        toolbar_layout = QVBoxLayout()
        toolbar_layout.addWidget(QLabel("Angle:"))
        toolbar_layout.addWidget(self.angle_setup)
        toolbar_layout.addWidget(QLabel("Frequency:"))
        toolbar_layout.addWidget(self.freq_setup)
        toolbar_layout.addWidget(self.manual_controll)
        toolbar_layout.addWidget(self.save_button)
        toolbar_layout.addWidget(self.start_button)

        # Organize plot area
        plot_layout = QVBoxLayout()
        plot_layout.addWidget(QLabel("Plot"))

        # Put everything together
        main_layout = QHBoxLayout()
        main_layout.addLayout(toolbar_layout)
        main_layout.addLayout(plot_layout)

        # Qt boilerplate
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def widgets_enabled(self, enabled):
        """
        Enable or disable all widgets other than the `Start` button
        This is used to prevent the user from changing settings while the measurement is running
        TODO: This could be done dynamically looping through all widgets
        """
        self.save_button.setEnabled(enabled)
        self.angle_setup.setEnabled(enabled)
        self.freq_setup.setEnabled(enabled)
        self.manual_controll.setEnabled(enabled)

    def start_button_toggled(self, checked):
        self.widgets_enabled(not checked)
        if checked:
            self.start_button.setText("Stop")
            # TODO Run measurement
        else:
            self.start_button.setText("Start")
            # TODO Stop measurement

    def save_button_clicked(self):
        # Save results
        pass


def main():
    app = QApplication(sys.argv)
    window = MainWindow(rotor_controller=None, measurement_controller=None)
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
