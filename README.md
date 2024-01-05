# HTTP Endpoint Health Checker

## Overview

This project implements a program to monitor the health of a set of HTTP endpoints. The program reads an input argument to a file path containing a list of HTTP endpoints in YAML format. It tests the health of these endpoints every 15 seconds and keeps track of the availability percentage of the HTTP domain names being monitored.

## Salient Features

- **Logging interactions and persistence**:

  - Tracks and stores interactions within log files for future debugging and analysis purposes.

- **Continuous Monitoring via Prometheus**:

  - Implemented Prometheus for consistent monitoring, observing, and analyzing health metrics, ensuring sustained application reliability.

- **Visualizing Availability Metrics**:

  - Utilizes Prometheus UI to visualize availability metrics, facilitating quick insights into domain health statuses over time.

- **Dockerized Application**:

  - Deployed as a Dockerized application, ensuring consistent behavior across various environments and simplifying deployment processes.

- **FastAPI Framework Integration**:

  - Enhanced the implementation using the FastAPI web framework, leveraging its capabilities for efficient API development.

- **Reliable Execution with Standard Libraries**:
  - Leverages standard Python libraries such as PyYAML, requests, and urllib for robust and reliable application execution.

## Directory structure

```
.
├── Dockerfile                  ...[Blueprint of the enhanced implementation to be assembled]
├── README.md                   ...[Repo README file]
├── docker-compose.yml          ...[Define and configure health-check and prometheus services of enhanced implementation]
├── env.local                   ...[Env file that contains the YAML endpoints file path and Logger level]
├── images                              ...[Images directory]
│   ├── avail-first-domain-graph.png    ...[Graph showing how the Availibility changes over time]
│   ├── basic-impl-log-file.png         ...[Basic Implementation Log file]
│   ├── constants.png                   ...[Image of constants.py]
│   ├── docker-containers.png           ...[Image of the running Docker containers]
│   ├── enhanced-impl-log-file.png      ...[Enchanced Implementation Log file]
│   ├── env.local.png                   ...[Image of env.local file]
│   ├── metrics.png                     ...[Image showing health-check metrics exposed to Prometheus]
│   ├── post-stopping.png               ...[Image of Docker containers after shut down]
│   └── prometheus-dashboard.png        ...[Prometheus Dashboard]
├── inputs                      ...[Inputs directory]
│   ├── input.yml               ...[Sample YAML file with Endpoints]
│   └── input2.yml              ...[Another sample YAML file with Endpoints]
├── logs                        ...[Logs directory]
│   └── health-check.log        ...[Logs Generated After Running the Script]
├── prometheus.yml              ...[Setup prometheus to monitor the health-check application]
├── requirements.txt            ...[List of Required Libraries]
└── src                         ...[Source directory]
    ├── helper                  ...[Helper directory]
    │   └── constants.py        ...[Logger Constants]
    ├── main.py                 ...[Script for Health Check Execution]
    └── server.py               ...[FastAPI server to test endpoints and expose metrics needed by Prometheus for monitoring]
6 directories, 22 files
```

## Pre-requisities and Installation steps

```
Note: This setup has been tested on macOS. If testing on a Windows environment, ensure to change any `/` in the paths to `\`.
```

1. Make sure you have `python`(Version 3.9+) and `pip` installed.

2. Clone the repository:

```bash
git clone https://github.com/kedartakwane/health-check.git
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Implementation

<details>
<summary>Basic Implementation</summary>

### Running the script

```bash
python main.py --f=<Path to YAML configuration file> [--log]
```

**Note: The script takes two arguments: `--f` and `--log`.**

Arguments:

- `--f`: This is argument to a file path with a list of HTTP endpoints in YAML format. This is a **required** arugment.

- `--log`: Optional argument to set the log level. Accepts `INFO`, `DEBUG`, `WARN`, or `ERROR`. **Default** is `INFO`.

## Need a walkthrough?

1. Open terminal, make sure you are at the root of the repository.

```bash
pwd
```

Output:

```bash
/Users/kedarsmac/Developer/Full-time-tests/Fetch/SRE/health-check-repo/health-check
```

2. Run the `main.py` script.
   - `--f=inputs/input.yml`: Here, I am using a the sample input YAML file from the Take home test pdf.
   - Not using `--log` as it is optional. Default value taken is `INFO`.
   - The location of the log file is `logs/health-check.log` as mentioned in the `constants.py` file.
     ![constants.py file](/images/constants.png)

```bash
python src/main.py --f=inputs/input.yml
```

3. The script starts executing and you will see something like this on the terminal:

```bash
fetch.com has 67% availability percentage
www.fetchrewards.com has 100% availability percentage
fetch.com has 67% availability percentage
www.fetchrewards.com has 100% availability percentage
fetch.com has 67% availability percentage
www.fetchrewards.com has 100% availability percentage
fetch.com has 67% availability percentage
www.fetchrewards.com has 100% availability percentage
fetch.com has 67% availability percentage
www.fetchrewards.com has 100% availability percentage
```

4. To exit, press `Ctrl+C` or `control+Z` on Mac.
5. Log file at location `logs/health-check.log` will look like this:
![Log File Output](/images/basic-impl-log-file.png)
</details>

<details>
<summary>Enhanced Implementation (Dockerized Implementation with Prometheus Monitoring)</summary>

### Running the script

Use the following command to build and start the Docker containers defined in the `docker-compose.yml` file:

```bash
docker-compose up -d --build
```

Once executed, this command initiates the health-check and prometheus services within Docker containers.

Upon completion of container creation, the script will begin execution.

### Accessing Service URLs

- **Health Check Metrics**: Visit http://localhost:5000/metrics to access the metrics generated by the health-check service.

- **Prometheus Dashboard**: Access the Prometheus dashboard via http://localhost:9090.

### Monitoring Availability via Prometheus Graph

As the script runs health checks every 15 seconds, monitor the availability changes of the first domain specified in the input YAML configuration file by following these steps:

- Go to http://localhost:9090/graph.
- Input available_perc_first_domain in the provided box and click the Execute button.
- Under the input box, select the Graph tab to view the availability changes graphically.

### Modifying the Input YAML Configuration File

To modify the input YAML configuration file: Update the `input.yml` file in `inputs` directory with the new file content.

To change the log level:
Locate the `env.local` file containing two configuration parameters:

- `LOG_LEVEL`: (Optional) Modify this value to `INFO`, `DEBUG` or `ERROR` to set the log level. The default value is `INFO`.

### Changing the Log File Path

- The log file path is specified in the `constants.py` file.
- To alter it, update the value of `LOG_FILE_PATH`.
  **Note: Even if the log directory doesn't exist the script will create it.**

## Walkthrough

1. First let's set the input YAML configuration file location and log level by opening the `env.local` file.

- Currently, I am setting the path to `inputs/input.yml`.
- Keeping the log level as `DEBUG`.
  ![env.local File](/images/env.local.png)

2. Next, let's set the log file location in `constants.py` file to `logs/health-check.log`.
   ![constants.py file](/images/constants.png)

3. Now we can build and run the docker container. Check these two things before executing the command:

- Make sure you are the root of the repository.
- Make sure Docker is running.
- Make sure that the ports `5000` and `9090` are available.

```bash
docker-compose up -d --build
```

- After the command is executed, the terminal output will look something like this:

```bash
Building health-check
[+] Building 9.6s (13/13) FINISHED
 => [internal] load build definition from Dockerfile                                                                                                                                 0.0s
 => => transferring dockerfile: 37B                                                                                                                                                  0.0s
 => [internal] load .dockerignore                                                                                                                                                    0.0s
 => => transferring context: 2B                                                                                                                                                      0.0s
 => [internal] load metadata for docker.io/library/python:3.10.2-slim-buster                                                                                                         1.2s
 => [1/8] FROM docker.io/library/python:3.10.2-slim-buster@sha256:32190393b82d91e98ae65b1071273e5fa32e737c855b589488d90d257a022503                                                   0.0s
 => [internal] load build context                                                                                                                                                    0.0s
 => => transferring context: 12.63kB                                                                                                                                                 0.0s
 => CACHED [2/8] WORKDIR /app                                                                                                                                                        0.0s
 => CACHED [3/8] RUN apt-get update                                                                                                                                                  0.0s
 => CACHED [4/8] RUN pip install --upgrade pip                                                                                                                                       0.0s
 => [5/8] COPY . .                                                                                                                                                                   0.0s
 => [6/8] RUN chmod 777 docker-entrypoint.sh                                                                                                                                         0.2s
 => [7/8] RUN pip3 install -r requirements.txt                                                                                                                                       7.6s
 => [8/8] RUN mkdir -p logs                                                                                                                                                          0.3s
 => exporting to image                                                                                                                                                               0.2s
 => => exporting layers                                                                                                                                                              0.2s
 => => writing image sha256:796062dbdb76c91192b171f5c2120e7b73684ee10be00c7a858e0b2696c83a68                                                                                         0.0s
 => => naming to docker.io/library/health-check_health-check                                                                                                                         0.0s
Starting health-check_prometheus_1 ... done
Creating health-check_health-check_1 ... done
```

4. You can check the `health-check` and `prometheus` services in Docker.
   ![Docker Containers](/images/docker-containers.png)

5. To check the console open the `health-check_health-check_1` container.

```bash
2024-01-05 08:59:47 >>> Log Level taken from the env file: 'DEBUG'
2024-01-05 08:59:47 >>> Input file taken from env file: 'inputs/input.yml'
2024-01-05 08:59:47 >>> Running with '--log' argument
2024-01-05 08:59:48 fetch.com has 67% availability percentage
2024-01-05 08:59:48 www.fetchrewards.com has 100% availability percentage
2024-01-05 08:59:54 INFO:     192.168.96.2:59940 - "GET /metrics HTTP/1.1" 200 OK
2024-01-05 08:59:47 INFO:     Started server process [7]
2024-01-05 08:59:47 INFO:     Waiting for application startup.
2024-01-05 08:59:47 INFO:     Application startup complete.
2024-01-05 08:59:47 INFO:     Uvicorn running on http://0.0.0.0:5000 (Press CTRL+C to quit)
2024-01-05 09:03:54 INFO:     192.168.96.2:59154 - "GET /metrics HTTP/1.1" 200 OK
2024-01-05 09:03:58 fetch.com has 67% availability percentage
2024-01-05 09:03:58 www.fetchrewards.com has 100% availability percentage
2024-01-05 09:04:09 INFO:     192.168.96.2:51550 - "GET /metrics HTTP/1.1" 200 OK
2024-01-05 09:04:13 fetch.com has 67% availability percentage
2024-01-05 09:04:13 www.fetchrewards.com has 100% availability percentage
2024-01-05 09:04:24 INFO:     192.168.96.2:59998 - "GET /metrics HTTP/1.1" 200 OK
2024-01-05 09:04:29 fetch.com has 67% availability percentage
2024-01-05 09:04:29 www.fetchrewards.com has 100% availability percentage
2024-01-05 09:04:39 INFO:     192.168.96.2:34374 - "GET /metrics HTTP/1.1" 200 OK
2024-01-05 09:04:44 fetch.com has 67% availability percentage
2024-01-05 09:04:44 www.fetchrewards.com has 100% availability percentage
```

We can see the availablility being printed. So let's check the `/metrics` at http://localhost:5000/metrics.
![Metrics](/images/metrics.png)

- Also, the logs will be generated in the `logs/health-check.log` directory.
- To see the logs, you will need to `nano` or `vim`.
- To do so, open the terminal tab in the `health-check_health-check_1` container and type the command `apt-get install nano`.
- After opening the logs it will look something like this:
  ![Logs generated](/images/enhanced-impl-log-file.png)

6. Let's take a look at the Prometheus Dashboard by navigating to http://localhost:9090/
   ![Prometheus Dashboard](/images/prometheus-dashboard.png)

7. Now let's check the availability for the first domain mentioned in the YAML configuration file:

- On the prometheus dashboard, enter `available_perc_first_domain` in the input box and then hit the Execute button.
- Select the `Graph` tab.
  ![Availability graph](/images/avail-first-domain-graph.png)

8. To stop the container, open terminal, navigate to the root of repository and enter this command:

```bash
docker-compose down
```

The containers will be deleted.

![After stopping](/images/post-stopping.png)

</details>

## Project Highlights

- **Endpoint Health Monitoring**: Conducts health checks every 15 seconds, evaluating HTTP response codes and response latency.
- **Logging**:
  - Employs a dedicated logger to record information in LOG_FILE_PATH (refer to constants.py).
  - Provides logs at different levels: INFO, DEBUG, and ERROR.
  - Displays availability percentages for each URL domain in the console throughout the program's lifespan.
- **Prometheus Monitoring**:
  - Integrated Prometheus monitoring to visualize changes in the availability of the first domain over time.
  - Implemented a Gauge, available_perc_first_domain, to track availability.
  - Observing the graph on the Prometheus dashboard to monitor changes in the availability of the first domain as time progresses.
- **Dockerized application**:
  - The application has been containerized using Docker for streamlined deployment and scalability.
  - Utilizes Docker to encapsulate the application environment, ensuring consistent behavior across different systems and environments.
- **PyYAML Library**: Safely reads the contents of the YAML file containing endpoint details.
- **Availability Tracking**: Utilizes a Dict to monitor domain availability.
- **urllib Library**: Extracts domains from endpoint URLs for tracking purposes.
- This program will continuously test the endpoints every 15 seconds and print the availability % of each domain.
- Program terminates after hitting `Ctrl + C` or `control + Z` on Mac.

## Future Improvements

- Presently, focusing on visualizing the availability solely for the first domain listed in the input YAML configuration file. Consideration is given to expand this visualization to encompass availabilities across all domains.
- Exploring the integration of Graphana to enhance visualization capabilities, aiming for a more comprehensive and insightful representation of availability metrics.
- Implementing alert mechanisms triggered when the availability of monitored domains falls below a specified threshold. Utilizing Prometheus, these rules can be configured to send alerts via diverse channels such as email, Slack notifications, among others.

## About Me

I am Kedar Takwane and I have recently graduated from University of Illinois at Urbana-Champaign with a Master in Computer Science degree. I have over 3 years of experience working as a Software Engineer and almost 1 year working as a Research Assistant.  
Throughout my career, I've developed a strong passion for Site Reliability Engineering (SRE). It's where my knack for Software Engineering (SWE) meets the pursuit of creating systems that are robust and scalable. There's something incredibly satisfying about making sure systems run smoothly, improving their performance, and making them more resilient against hiccups and glitches.

### Contact

Email: kedar.takwane@gmail.com
