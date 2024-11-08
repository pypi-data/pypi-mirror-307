# EMP - Utilities Service (UTL-S)

This repository is focusing on shared functions, code(-snippets) and generic functionalities. The goal is to reduce redundancy and to increase productivity in the usage of shared modules / functions. To maximize the advantage of this repository, the selected type of sharing is python packaging for python modules. Although github submodules and docker do offer a professional solution - It is specifically for this usecase not applicable.

## Logging Module

The setup_logger function in the Logging Module simplifies consistent logging across services, creating structured, environment-aware log files. The JSON-formatted output is ideal for integration with monitoring tools like AWS CloudWatch, Splunk, and New Relic.

### Key Features

- Environment-based Logging: Generates separate log files based on the specified environment (dev, int, stg, prd), automatically creating a logs directory.
- Formatted JSON Logs: Logs are formatted in JSON, making them easily readable and compatible with modern monitoring tools.
- Dynamic Log Levels: Automatically switches to overwrite mode in non-production environments and append mode in production, facilitating easy log management.

### Usage

1. Installing the package

    `pip3 install emp-utils-logger`

2. Setting up the logger

    ```python
    from emp_utils_logger import setup_logger

    logger = setup_logger(ENVIRONMENT = '<ENVIRONMENT>', SERVICE = '<SERVICE>', module = '<module> | default = Serverless')
    logger.info('Logger setup successfully')
    ```

### Additional Notes

- __Environment Detection__: If ENVIRONMENT is not specified, the logger defaults to dev.
- __Custom File Naming__: Log files are generated with a name format of EMP-<SERVICE>-<module>_<ENVIRONMENT>.log, aiding easy identification.
- __Directory Creation__: The module will automatically create a logs folder if it does not already exist.

*This logger module is built to seamlessly integrate into various environments, supporting straightforward and organized logging across applications.*