# FEAS-1

**Fire Evacuation Automation System (FEAS)** for warehouses, developed in Python using Tkinter for the GUI, MySQL for data management, and advanced voice and data interaction capabilities.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [License](#license)

---

## Overview

FEAS is a Python-based application designed to automate the fire evacuation process in warehouse environments. It provides live reporting and emergency alerts, integrates with fire, heat, and smoke sensors, and utilizes an interactive UI. The system is highly customizable, allowing for safe and efficient warehouse evacuation.

## Features

- **Live Sensor Integration**: Connects to fire, heat, and smoke sensors for real-time data.
- **Automatic Evacuation Alerts**: Generates alerts based on detected hazards.
- **Dynamic UI**: Designed using Tkinter, adhering to Microsoft professional design standards.
- **Voice Commands**: Accepts voice commands for hands-free operation.
- **Data Management**: Integrates with MySQL to store sensor data and logs.
- **Customizable Exits**: Guides safe evacuation routes for a multi-floor warehouse setup.

## Installation

To install FEAS-1, ensure that you have Python 3.12 or higher and MySQL installed.

1. Clone the repository or download it to `D:\feas`:
   ```bash
   git clone https://github.com/tahiriqbal70/FEAS.git
2. Import database 
   ```bash
   mysql -u root -p feas < FEAS_Database.sql
3. Usage
   python /feas/feas.py

## Project Structure
FEAS/
FEAS/FEAS.PY
├── src/
│   └── feas/
│       ├── __init__.py          # Initializes the FEAS package
│       └── feas.py              # Main application file
├── README.md                    # Project description and usage
├── pyproject.toml               # Project configuration for PyPI
├── LICENSE                      # License file
└── requirements.txt             # List of dependencies

