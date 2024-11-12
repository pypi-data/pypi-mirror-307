# PX4/ArduPilot Autopilot tools [![](https://badge.fury.io/py/autopilot-tools.svg)](https://pypi.org/project/autopilot-tools/) ![](https://github.com/PonomarevDA/autopilot_tools/actions/workflows/build_package.yml/badge.svg) ![](https://github.com/PonomarevDA/autopilot_tools/actions/workflows/pylint.yml/badge.svg) ![](https://github.com/PonomarevDA/autopilot_tools/actions/workflows/tests.yml/badge.svg)

[autopilot_tools](https://pypi.org/project/autopilot-tools/) is a python package intended to be used as part of automated work with PX4 and ArduPilot autopilots. It allows you to:

- [x] 1. Upload firmware to PX4/ArduPilot targets
- [x] 2. Easily write set of parameters,
- [x] 3. Run flight mission and wait for result,
- [x] 4. Download flight logs,
- [x] 5. Upload flight logs to [review.px4.io](https://review.px4.io/),
- [ ] 6. Parse flight logs,
- [ ] 7. Provide a flight log stats and overall stats of multiple log files.

## 1. INSTALLATION

The package is distrubuted via [pypi.org/project/autopilot-tools/](https://pypi.org/project/autopilot-tools/).

```bash
pip install autopilot_tools
```

Alternatively, you can install the package from sources in [Development Mode (a.k.a. “Editable Installs”)](https://setuptools.pypa.io/en/latest/userguide/development_mode.html). Clone the repository, install the package in development mode and use it in virtual environment:

```bash
git clone https://github.com/PonomarevDA/autopilot_tools.git
python3 -m venv venv
./venv/bin/activate
pip install -e .
```

## 2. USE CASES

After the installation the package is accessible as a few executables.

## 2.1. Autopilot configurator

`autopilot-configurator` uploads the given firmware to the autopilot, reset parameters to default, upload the required parameters and perform force sensor calibration.

<img src="https://github.com/PonomarevDA/autopilot_tools/blob/docs/assets/autopilot_configurator.gif?raw=true" width="768">

## 2.2. Test scenario

`test-scenario` uploads the given mission to the autopilot, run it and wait until it is finished, then download the log from the vehicle and upload it to [review.px4.io](https://review.px4.io/). It returns a user the result of the flight and link to the flight report.

<img src="https://github.com/PonomarevDA/autopilot_tools/blob/docs/assets/test_scenario.gif?raw=true" width="768">


### 2.3. Using as a module

The package can be imported as a module. This allows you to implement more customized behaviour and use extended features if you need.

An example is shown below:

```python
from autopilot_tools.vehicle import Vehicle
from autopilot_tools.analyzer import Analyzer

vehicle = Vehicle()
vehicle.connect(device="serial")
vehicle.upload_firmware(firmware_path_or_url)
vehicle.configure(params_path)
vehicle.load_mission(mission_path)

res = vehicle.run_mission(mission_path)
print(res)

log_file = vehicle.load_latest_log(mission_path)

analzyer = Analyzer()
res = analzyer.analyse_log(log_file, analyze_requests=("airspeed", "ice", "esc_status"))
print(res)
```

## 2. DESIGN

The package is primarily based on [ArduPilot/pymavlink](https://github.com/ArduPilot/pymavlink).

<!-- The project structure should be like:

```
src/autopilot-tools/
├── autopilot_tools/
│   ├── firmware.py
│   ├── parameters.py
│   ├── mission.py
│   ├── logs.py
│   ├── stats.py
│   └── cli/
│       ├── __init__.py
│       ├── upload_firmware.py
│       ├── set_parameters.py
│       ├── run_mission.py
│       ├── download_logs.py
│       ├── upload_logs.py
│       ├── parse_logs.py
│       ├── log_stats.py
│       └── overall_stats.py
├── scripts/
│   ├── deploy.sh
│   ├── install.sh
|   └── code_style.py
├── tests/
│   ├── test_firmware.py
│   ├── test_parameters.py
│   ├── test_mission.py
│   ├── test_logs.py
│   └── test_stats.py
├── LICENSE
├── README.md
├── requirements.txt
└── pyproject.toml
``` -->

## 3. Developer guide

A developer should follow the [CONTRIBUTING.md](CONTRIBUTING.md) guide.

**Deployment**.
Please, deploy initially on [test.pypi.org](https://test.pypi.org/project/autopilot-tools/). Only if everything is fine, then deploy on [pypi.org](https://pypi.org/project/autopilot-tools/). Try the script below to get details:

```bash
./deploy.sh --help
```

## 4. LICENSE

The package inherits [ArduPilot/pymavlink](https://github.com/ArduPilot/pymavlink) license and is distributed under GPLv3 license.
