# ScenarioForge

**ScenarioForge** is a robotics software project focused on building a **scenario evaluation and validation harness** for a LeRobot **SO-101** robotic arm.

The long-term goal is to create infrastructure that makes robot behavior:

- testable
- measurable
- repeatable
- reportable

This project is inspired by the kind of tooling used in robotics autonomy validation, scenario evaluation, and simulation QA roles.

---

## Current Status

ScenarioForge is currently in its **foundation phase**.

So far, the project includes:

- a working **ROS 2 Jazzy backend** for controlling LeRobot teleoperation
- a **process manager** that launches and stops `lerobot-teleoperate`
- ROS 2 services for:
  - `/start_teleop`
  - `/stop_teleop`
  - `/teleop_status`
- a working **RQt teleoperation panel**
  - Start Teleop
  - Stop Teleop
  - Refresh Status
- confirmed end-to-end control of the **physical SO-101** through:
  - RQt → ROS 2 services → backend node → LeRobot → robot

---

## Project Goal

The long-term vision for ScenarioForge is to evolve beyond basic teleoperation and become a **robotics implementation/validation framework** with support for:

- scenario definitions (YAML/JSON)
- repeatable execution
- telemetry capture
- pass/fail evaluation
- metrics and reporting
- regression packs
- artifact generation
- mock/sim backends later

The current ROS + RQt control layer is the first step toward that developing the larger system.

---

## Current Architecture

### 1. `lerobot_control_interface`
ROS 2 backend package responsible for:

- exposing teleoperation control services
- launching/stopping LeRobot commands
- reporting realtime teleop status

### 2. `scenarioforge_rqt`
RQt operator panel responsible for:

- starting teleoperation
- stopping teleoperation
- refreshing teleop status
- more to come. 

### 3. LeRobot
LeRobot is used as the robot control layer for the SO-101.  
ScenarioForge currently wraps the existing LeRobot teleoperation workflow rather than replacing its lower-level internals.

---

## Stack

- **OS:** Ubuntu 24.04
- **ROS 2:** Jazzy
- **Language:** Python
- **Robot:** LeRobot SO-101
- **Motors:** Feetech STS3215 smart servos
- **UI:** RQt
- **Version Control:** Git + GitHub

---

## Working Features

### ROS 2 backend
- start teleoperation
- stop teleoperation
- report teleoperation status

### RQt operator panel
- Start Teleop button
- Stop Teleop button
- Refresh Status button
- live status label

### Real robot validation
- physical SO-101 teleoperation can be started and stopped from the UI

---

## Roadmap

### Phase 1 — Control Foundation
- [x] ROS 2 package for teleop control
- [x] start/stop/status services
- [x] RQt teleop control panel
- [ ] add setup/calibration services
- [ ] improve backend observability/logging

### Phase 2 — Operator Tooling
- [ ] expand RQt panel
- [ ] add setup/calibration controls
- [ ] add better status feedback
- [ ] add event/log display

### Phase 3 — Scenario Execution
- [ ] define scenario schema
- [ ] create scenario runner/executor structure
- [ ] support repeatable run metadata
- [ ] collect execution artifacts

### Phase 4 — Evaluation & Reporting
- [ ] pass/fail evaluation
- [ ] failure reason tracking
- [ ] duration and timing metrics
- [ ] report generation
- [ ] artifact bundling per run

### Phase 5 — Regression & Testing
- [ ] mock executor backend
- [ ] smoke/regression packs
- [ ] CI validation pipeline

---

## Why This Project Matters to me

ScenarioForge is designed as a portfolio project to help refine my skills in roles like:

- robotics software
- autonomy validation
- scenario evaluation
- simulation QA
- robotics tooling
- operator interfaces
- embodied AI infrastructure

This project is intended to demonstrate not only robot control, but also the engineering systems around robotics:
- orchestration
- validation
- observability
- tooling
- repeatability

---

## Running the Current Backend

### Start the backend node
```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run lerobot_control_interface command_node
