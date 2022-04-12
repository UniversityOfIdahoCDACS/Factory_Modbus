# Mini Factory Controller
This is a python based controller for the University's PLC Mini Factory over Modbus

# Raspberry Pi setup
WIP

# Installation
## Clone repo
Clone repo

```bash
git clone https://github.com/UniversityOfIdahoCDACS/Mini-Factory-Python-Controller.git
```

## venv setup
Setting up a local environment is useful to isolate packages to this project
1. Navigate to repo

    ```bash
    cd Mini-Factory-Python-Controller
    ```

2. Create environment

    ```bash
    python -m venv ./.venv
    ```

3. Source virtual environment

    ```bash
    # Linux
    source ./.venv/Scripts/activate
    # Windows:
    .\.venv\Scripts\Activate.ps1
    ```

## Python dependencies
Install python3 and pip

Then install project libraries

```bash
sudo apt install python3 python3-pip
pip install -r requirements.txt
```

## .env file
1. Make a copy of .env-example

    ```bash
    cp .env-example .env
    ```

2. Update .env file contents

## Install system service file
optional if system service is not needed
This can be rerun safely to reinstall or update the service file

Run setup script

```bash
sudo setup.sh
```

# Running the program
## Directly

```bash
cd pyController
python3 pyController
```

## Service

```bash
sudo service pyController status|start|stop|restart
```
