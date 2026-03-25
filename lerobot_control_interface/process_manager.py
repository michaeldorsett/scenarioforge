import os
import signal
import subprocess


class LeRobotProcessManager:
    def __init__(self):
        self.teleop_process = None

    def start_teleop(self, follower_port: str, follower_id: str, leader_port: str, leader_id: str) -> tuple[bool, str]:
        if self.teleop_process is not None and self.teleop_process.poll() is None:
            return False, "Teleop is already running."

        cmd = [
            "/home/mdorsett/anaconda3/bin/conda",
            "run",
            "--no-capture-output",
            "-n",
            "lerobot",
            "lerobot-teleoperate",
            "--robot.type=so101_follower",
            f"--robot.port={follower_port}",
            f"--robot.id={follower_id}",
            "--teleop.type=so101_leader",
            f"--teleop.port={leader_port}",
            f"--teleop.id={leader_id}",
        ]

        try:
            self.teleop_process = subprocess.Popen(
                cmd,
                start_new_session=True,   # important: create a new process group
            )
            return True, f"Teleop started. PID: {self.teleop_process.pid}"
        except Exception as e:
            return False, f"Failed to start teleop: {e}"

    def stop_teleop(self) -> tuple[bool, str]:
        if self.teleop_process is None or self.teleop_process.poll() is not None:
            self.teleop_process = None
            return False, "Teleop is not running."

        try:
            pgid = os.getpgid(self.teleop_process.pid)

            # First try a graceful Ctrl+C style stop
            os.killpg(pgid, signal.SIGINT)

            try:
                self.teleop_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # If still alive, force termination of the whole group
                os.killpg(pgid, signal.SIGTERM)
                self.teleop_process.wait(timeout=5)

            self.teleop_process = None
            return True, "Teleop stopped successfully."
        except Exception as e:
            return False, f"Failed to stop teleop cleanly: {e}"

    def get_teleop_status(self) -> tuple[bool, str]:
        if self.teleop_process is None:
            return True, "Teleop is stopped."

        return_code = self.teleop_process.poll()

        if return_code is None:
            return True, "Teleop is running."

        self.teleop_process = None
        return False, f"Teleop exited unexpectedly with code {return_code}"