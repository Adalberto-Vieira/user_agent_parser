# User Agent Augmentor

The User Agent Augmentor is a tool designed to process and augment datasets containing user agent strings. It focuses on extracting information such as the device type, browser version, and browser family.

## How to install 

### Virtualenv

To get started with the tool, set up a virtual environment with Python 3.10 and activate it.

#### Linux and Mac

```sh
python -m venv <env_name>
source ./<env_name>/bin/activate
```

#### Windows

```sh
python -m venv <env_name>
./<env_name>/Scripts/activate
```

### Dependencies

#### Required 

Install the necessary dependencies for running the solution.
From the project's root folder, run:

```sh
pip install -r requirements.txt
```

#### Required for development

This step is optional and only required for development purposes.

 - Install dependencies

From the project's root folder, run:

```sh
pip install -r requirements-dev.txt
```

 - Install pre-commit

Pre-commit is a Python tool that facilitates leveraging Git hooks more efficiently. In this repository, it is employed to maintain code standards using flake8 and black.

Inside the project`s root folder, run:

```sh
pre-commit install
```

### Run 

Inside the `input` folder, add the dataset.

From the `src` folder, run:

```sh
python main.py
```

The output will be generated in the `output` folder. 

### Run tests

From the root folder, run:

```sh
pytest tests/
```

This command will execute the test suite and ensure the proper functioning of the User Agent Augmentor.

### Data quality issues

A few data quality issues were identified during the processing of the input data. Firstly, 
the input file did not adhere to a proper JSON format, necessitating special handling during the file 
loading process.

Furthermore, there were instances where elements had None values and empty double quotation marks in the 
USER_AGENT field. To address this, during the user agent parsing phase, a failure column was introduced to 
indicate if the element had succeed or failed to convert. In the event of such failures, the values in the 
augmented columns(Browser type, Browser Version, Device Type) were set to None as well. 

This approach facilitates identification of root causes of the failure of specific elements in subsequent 
steps of the processing pipeline.
