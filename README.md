# NetInspect

A Python script for scanning IPs or domains to gather service information. This script can identify HTTP and HTTPS services, retrieve server information, status codes, content length, and perform CMS fingerprinting.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Usage](#usage)
- [Options](#options)
- [Examples](#examples)
- [License](#license)
- [Credits](#credits)

## Introduction

This script is designed to scan IPs or domains, providing detailed service information such as server details, HTTP status codes, and content length. It also performs CMS fingerprinting to identify common content management systems.

## Features

- Scan single IPs, domains, or entire subnets
- Multi-threaded scanning for efficient performance
- Support for HTTP and HTTPS services
- CMS fingerprinting for popular content management systems

## Requirements

- Python 3.x
- Required Python packages: `requests`, `socket`, `urllib3`, `colorama`

```bash
  pip install -r requirements.txt
```

## Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/secnextechnologies/NetInspect.git
    ```

2. Navigate to the project directory:

    ```bash
    cd NetInspect
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the script with your desired options:

    ```bash
    python netinspect.py [options]
    ```

## Options

- `-i, --ip`: Single IP address to scan
- `-is, --ip_subnet`: Subnet (e.g., 192.168.1.0/24) to scan
- `-il, --ip_list`: File containing a list of IPs to scan
- `-d, --domain`: Single domain to scan
- `-dl, --domain_list`: File containing a list of domains to scan
- `-o, --output`: Output file for results

For more options, use:

```bash
python netinspect.py -h
```

## Examples

Scan a single IP:
```bash
python netinspect.py -i 192.168.1.1
```

Scan a list of domains:
```bash
python netinspect.py -dl domain_list.txt
```

Scan an IP subnet:
```bash
python netinspect.py -is 192.168.1.0/24
```

## License

This project is licensed under the MIT License.

## Credits

Developed by SecneX Technologies.
```
Feel free to modify the content based on your specific needs and add any additional sections or information that you think would be useful for users of your script.
```
