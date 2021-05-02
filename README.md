# python-screeps-spybot

An experimental spy utility for Screeps

### Credits

- [screepers/python-screeps](https://github.com/screepers/python-screeps)

### Requirements

- Python v3.8 (only version tested)

### Install

Download or clone this repository and then install python packages in a virtual environment with the following steps:

```bash
python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install pyyaml jsonschema rich envyaml
pip install git+https://github.com/admon84/python-screeps.git@v0.5.2#egg=screepsapi
deactivate
```

### Configure

Save your config settings to `config.yaml` before running the script

Each config option is described in the [Config Settings Wiki page](https://github.com/admon84/python-screeps-spybot/wiki/Config-Settings)

### Usage

Once everything is configured, you can run the `spybot.py` script

```bash
source env/bin/activate
python3 spybot.py
deactivate # to stop the app and exit virtual environment
```
