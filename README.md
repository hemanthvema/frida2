# FRIDA2 — Automated Electrochemical Experimentation

**Python orchestration for liquid handling, robotic sample transfer, and electrochemical measurements.**

FRIDA2 brings several laboratory devices into a coordinated experimental workflow for corrosion-inhibitor research. It connects formulation preparation on an Opentrons OT-2, vessel handling with a UFACTORY xArm, peristaltic fluid transfer, and electrochemical data acquisition.

This repository contains work from my student-assistant and master's thesis research at **BAM — the Federal Institute for Materials Research and Testing, Germany**. It includes orchestration code, device integrations, PyQt6 interfaces, instrument procedures, and recorded measurement outputs.

**Start here:** [`frida2_official.py`](frida2_official.py) is the main orchestration script. Its `RobotMain.run()` method connects the experimental steps.

## Research purpose and my contribution

Corrosion-inhibitor screening requires repeated preparation, transfer, measurement, and analysis. FRIDA2 addresses the practical challenge of coordinating those operations across instruments with different interfaces and timing requirements.

My contribution focused on liquid-handling automation, integration of experimental modules, and automated electrochemical data analysis. The code demonstrates work with Python, laboratory robotics, serial communication, instrument SDKs, graphical interfaces, and scientific data processing.

My broader master's thesis investigated autonomous optimization of corrosion-inhibitor solutions for steel, including machine-learning-based experimental planning. This repository primarily documents the **automation and measurement layer**. The OT-2 backend contains commented-out measurement-feedback and Bayesian-optimization calls; these are placeholders, not an implemented optimization loop in the uploaded workflow.

## Hardware and software integration

| Component | Function | Implementation |
|---|---|---|
| UFACTORY xArm and gripper | Move and reposition the vessel between stations | Robot SDK calls and motion sequences in `frida2_official.py` |
| Opentrons OT-2 | Dispense two inhibitor solutions into a target container | `OT2_Test_duplicate/heyyounogui.py`, backed by Minerva Lite and the OT-2 HTTP integration |
| Reglo ICC peristaltic pump | Transfer liquid using configured channels, flow rates, and durations | Serial command interface in `pump_official.py` |
| Ender-3-based positioning gantry | Position the measurement assembly over selected samples | Serial G-code in `Electrochemistry_Backend_144Sample.py` |
| PalmSens instrument | Execute electrochemical procedures and return measurement data | Local `palmsens/` modules and MethodSCRIPT files in `scripts/` |
| PyQt6 interfaces | Configure pump operations, samples, and measurement settings | Standalone interfaces and screens in `frida_gui_folder/` |

## Experimental sequence

The main script performs a configured sequence for each preparation/handling cycle:

1. **Prepare the formulation:** pass inhibitor identifiers and volumes to the OT-2 backend, which creates chemical additions in microlitres and requests dispensing into the target container.
2. **Move the vessel:** execute robot and gripper motions between the configured stations.
3. **Transfer liquid:** run inlet and outlet pump channels at the selected flow rates and durations.
4. **Request electrochemical measurements:** pass the measurement height, selected sample positions, and method sequence to the positioning/measurement backend.
5. **Return for the next cycle:** execute the remaining vessel-handling motions and return to the preparation area.

Robot state/error callbacks and command return-code checks are included. The sequence uses blocking calls and timed waits, with motion coordinates configured for the original laboratory layout.

### Measurement methods

| Method | Recorded relationship | Python acquisition script | Instrument procedure |
|---|---|---|---|
| Cyclic voltammetry (CV) | Current versus potential | [`plot_cv.py`](plot_cv.py) | [`Script_CV.mscr`](scripts/Script_CV.mscr) |
| Open-circuit potential (OCP) | Potential versus time | [`plot_ocp.py`](plot_ocp.py) | [`Script_OCP.mscr`](scripts/Script_OCP.mscr) |
| Chronoamperometry (CA) | Current versus time | [`plot_chronoamperometry.py`](plot_chronoamperometry.py) | [`Script_Chronoamperometry.mscr`](scripts/Script_Chronoamperometry.mscr) |

The acquisition scripts parse instrument responses and export **CSV data and PNG plots**. The positioning backend defines a **12 × 12 grid of 144 addressable sample positions**; this describes the coordinate layout rather than demonstrated throughput.

## Recorded outputs

The repository includes historical measurement exports in [`output/`](output/) and experiment folders in [`Results/`](Results/). One example folder contains CV, OCP, and chronoamperometry data, plots, and the corresponding instrument scripts:

[Browse example experiment — 24 August 2023, sample position 1](Results/Experiment_24.08.2023-16.29_Sample%20position_1/)

[CV data](Results/Experiment_24.08.2023-16.29_Sample%20position_1/CV_Data.csv) · [OCP data](Results/Experiment_24.08.2023-16.29_Sample%20position_1/OCP_data.csv) · [Chronoamperometry data](Results/Experiment_24.08.2023-16.29_Sample%20position_1/Chronoamperometry_Data.csv)

These files illustrate the recorded output formats. They are not a curated benchmark, and their presence does not establish that the current code snapshot reproduces each archived run without changes.

## Repository guide

| File or directory | Purpose |
|---|---|
| [`frida2_official.py`](frida2_official.py) | Main workflow: robot initialization, motion, dosing calls, pump transfers, and measurement dispatch |
| [`OT2_Test_duplicate/`](OT2_Test_duplicate/) | OT-2 backend, Minerva Lite components, saved configuration, and labware definitions |
| [`pump_official.py`](pump_official.py) | Reglo ICC serial driver and pump-control methods |
| [`Electrochemistry_Backend_144Sample.py`](Electrochemistry_Backend_144Sample.py) | Sample positioning and measurement dispatch used by the main script |
| [`Electrochemistry_Backend_hemanthversion.py`](Electrochemistry_Backend_hemanthversion.py) | Alternative backend with additional pump-related operations |
| [`palmsens/`](palmsens/) and [`scripts/`](scripts/) | Instrument communication, response parsing, and measurement procedures |
| [`frida_gui_folder/`](frida_gui_folder/) | FRIDA configuration and component screens; GUI entry point is `main_gui.py` |
| [`Electrochemistry_GUI_144Sample.py`](Electrochemistry_GUI_144Sample.py) | Electrochemistry interface for sample and method selection |
| [`pump_gui_qtdesign_version3.py`](pump_gui_qtdesign_version3.py) | Pump-control interface |
| [`Xarm_python_version2_personal_pc_version2_withguihemanth/`](Xarm_python_version2_personal_pc_version2_withguihemanth/) | Bundled xArm SDK and robot-development scripts |
| [`requirements.txt`](requirements.txt) | Historical Python dependency pins |

For a focused review, read `RobotMain.run()`, then `BackendExperiment.add_volumes()` in `OT2_Test_duplicate/heyyounogui.py`, the pump driver, and the measurement backend. The GUI files include development screens; a complete GUI-to-orchestration execution path is not established by this snapshot.

## Setup and configuration

This is a **hardware-dependent research snapshot**. Running it requires a compatible laboratory setup and adaptation of the original workstation configuration.

### Python environment

Create a fresh environment from the repository root. For Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install matplotlib
```

The pinned dependencies record the development environment, not a validated portable installation. Check Python/package compatibility for the target workstation. The archived `test_venv/` and `xarmenv/` directories are machine-specific environments and should not be used as installation instructions.

### Configuration checklist

| Setting | Where to configure it |
|---|---|
| Robot connection and motion coordinates | `frida2_official.py` |
| Preparation-cycle count, inhibitor identifiers, volumes in µL | Arguments to `RobotMain.run()` |
| Pump flow rates, durations, and channels | `RobotMain.run()` and the connection in `pump_official.py` |
| Gantry serial connection, sample geometry, and measurement height | `Electrochemistry_Backend_144Sample.py` |
| OT-2 hardware/container configuration | `OT2_Test_duplicate/Configuration/last_config.json` |
| OT-2 configuration, logging, and temporary-protocol paths | `PathNames` in `OT2_Test_duplicate/HelperClassDefinitions.py` |
| Electrochemical parameters | MethodSCRIPT files in `scripts/` |
| Export destinations | Acquisition scripts and electrochemistry backend |

`num_samples` controls preparation/handling cycles; `samples_list` selects positions on the measurement grid. These are separate settings.

### Integration notes before execution

The main supporting modules are included, but several details still require attention:

- The electrochemistry backend passes a result-folder argument to acquisition functions whose current definitions accept no arguments.
- The standalone electrochemistry GUI passes more arguments to `Measurement()` than the imported backend accepts.
- The backend creates folders under `Results/`, while acquisition scripts use separate destinations under `output/`. Align result routing and ensure destination directories exist.
- OT-2 path definitions contain absolute paths from the original Windows workstation. Update these before loading the saved configuration.
- The electrochemistry GUI imports `gui_resources`, but the archive includes only cached bytecode for that module, not its source. Restore or regenerate the resource module for a portable GUI setup.

**Imports can initialize hardware:** the pump module opens a serial connection, the OT-2 backend loads its configuration, and the electrochemistry backend initializes the gantry and issues a movement command. Review initialization behavior and calibrate device positions before running on connected equipment.

After resolving the integration points and configuring the laboratory setup, the main entry point is:

```powershell
python frida2_official.py
```

The included example values belong to the original setup. Hardware execution has not been revalidated for this repository snapshot; the development/test scripts do not constitute an automated integration-test suite.

## Author and acknowledgements

**Hemanth Kumar Vema** — laboratory automation, experimental integration, and electrochemical data-analysis work at BAM.

The project incorporates collaborative and third-party components. Minerva Lite and the OT-2 integration files credit **Bastian Ruehle, BAM**. Robot-control code builds on **UFACTORY/xArm** software, and electrochemical acquisition uses **PalmSens** components and examples. Some interfaces were generated with Qt Designer.

Retain the copyright and license notices supplied with those components. The repository has no top-level license covering the complete project; component-specific notices apply to their respective files.
