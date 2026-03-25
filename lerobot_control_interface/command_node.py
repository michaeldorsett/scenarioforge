import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger

from lerobot_control_interface.process_manager import LeRobotProcessManager


class LeRobotCommandNode(Node):
    def __init__(self):
        super().__init__("lerobot_command_node")

        self.manager = LeRobotProcessManager()

        # Hardcoded for now
        self.follower_port = "/dev/ttyACM1"
        self.follower_id = "my_follower_arm"
        self.leader_port = "/dev/ttyACM0"
        self.leader_id = "my_leader_arm"

        self.start_srv = self.create_service(
            Trigger,
            "start_teleop",
            self.handle_start_teleop
        )

        self.stop_srv = self.create_service(
            Trigger,
            "stop_teleop",
            self.handle_stop_teleop
        )

        self.status_srv = self.create_service(
            Trigger,
            "teleop_status",
            self.handle_teleop_status
        )

        self.get_logger().info("LeRobot command node is up.")
        self.get_logger().info("Services available: /start_teleop, /stop_teleop, /teleop_status")

    def handle_start_teleop(self, request, response):
        success, message = self.manager.start_teleop(
            follower_port=self.follower_port,
            follower_id=self.follower_id,
            leader_port=self.leader_port,
            leader_id=self.leader_id,
        )
        response.success = success
        response.message = message
        self.get_logger().info(f"start_teleop: {message}")
        return response

    def handle_stop_teleop(self, request, response):
        success, message = self.manager.stop_teleop()
        response.success = success
        response.message = message
        self.get_logger().info(f"stop_teleop: {message}")
        return response

    def handle_teleop_status(self, request, response):
        success, message = self.manager.get_teleop_status()
        response.success = success
        response.message = message
        self.get_logger().info(f"teleop_status: {message}")
        return response


def main(args=None):
    rclpy.init(args=args)
    node = LeRobotCommandNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.manager.stop_teleop()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()