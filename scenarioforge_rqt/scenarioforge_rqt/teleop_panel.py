import sys

import rclpy
from python_qt_binding.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from qt_gui.plugin import Plugin
from std_srvs.srv import Trigger


class TeleopPanel(Plugin):
    def __init__(self, context):
        super().__init__(context)
        self.setObjectName("TeleopPanel")

        if not rclpy.ok():
            rclpy.init(args=None)

        self.node = rclpy.create_node("scenarioforge_rqt_panel")

        self._widget = QWidget()
        self._widget.setWindowTitle("ScenarioForge Teleop Panel")

        layout = QVBoxLayout()

        self.status_label = QLabel("Status: Unknown")
        layout.addWidget(self.status_label)

        self.start_button = QPushButton("Start Teleop")
        self.stop_button = QPushButton("Stop Teleop")
        self.refresh_button = QPushButton("Refresh Status")

        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.refresh_button)

        self._widget.setLayout(layout)
        context.add_widget(self._widget)

        self.start_button.clicked.connect(self.start_teleop)
        self.stop_button.clicked.connect(self.stop_teleop)
        self.refresh_button.clicked.connect(self.refresh_status)

    def _call_trigger_service(self, service_name: str):
        client = self.node.create_client(Trigger, service_name)

        if not client.wait_for_service(timeout_sec=2.0):
            self.status_label.setText(f"Status: Service {service_name} unavailable")
            return None

        request = Trigger.Request()
        future = client.call_async(request)

        rclpy.spin_until_future_complete(self.node, future, timeout_sec=5.0)

        if future.result() is None:
            self.status_label.setText(f"Status: No response from {service_name}")
            return None

        return future.result()

    def start_teleop(self):
        result = self._call_trigger_service("/start_teleop")
        if result:
            self.status_label.setText(f"Status: {result.message}")

    def stop_teleop(self):
        result = self._call_trigger_service("/stop_teleop")
        if result:
            self.status_label.setText(f"Status: {result.message}")

    def refresh_status(self):
        result = self._call_trigger_service("/teleop_status")
        if result:
            self.status_label.setText(f"Status: {result.message}")

    def shutdown_plugin(self):
        self.node.destroy_node()

    def save_settings(self, plugin_settings, instance_settings):
        pass

    def restore_settings(self, plugin_settings, instance_settings):
        pass