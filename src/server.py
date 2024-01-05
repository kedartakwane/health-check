from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every
import uvicorn
import time
import requests
from requests.exceptions import RequestException
import yaml
import argparse
from urllib.parse import urlparse
from typing import Dict, List
import logging
from helper.constants import LOG_FORMAT, LOG_FILE_PATH, LOG_DATE_FORMAT
import prometheus_client
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

available_perc_first_domain = prometheus_client.Gauge(
    "available_perc_first_domain",
    "Available Percentage of Fetch Rewards"
)

total_requests_count = prometheus_client.Counter(
    "total_requests_count",
    "Number of endpoints requested"
)


@app.get("/metrics")
async def fetch_metrics():
    return Response(
        media_type="text/plain",
        content=prometheus_client.generate_latest()
    )


@app.on_event("startup")
@repeat_every(seconds=15)
def test_endpoints_health() -> None:
    '''
    This function is called every 15 seconds to check the health of all the endpoints in the YAML file.

    Parameters:
        None

    Return:
        None
    '''
    try:
        logging.info("Starting the Health Check for the endpoints")
        for endpoint in endpoint_list:
            domain = urlparse(endpoint['url']).netloc

            logging.debug(f"Check for the endpoint: {endpoint['name']}")
            logging.debug(f"Domain extracted: {domain}")

            # If the domain is not valid skip it
            if not domain:
                continue

            # Add the domain in endpoint status if not present
            if not endpoint_status.get(domain):
                endpoint_status[domain] = [0, 0]

            # Extract the endpoint attributes
            name = endpoint.get("name")
            url = endpoint.get("url")
            method = endpoint.get("method", "GET")  # The default method is GET
            headers = endpoint.get("headers", {})
            body = endpoint.get("body", {})

            logging.debug(f"Endpoint attributes:")
            logging.debug(f"name: {name}")
            logging.debug(f"url: {url}")
            logging.debug(f"method: {method}")
            logging.debug(f"headers: {headers}")
            logging.debug(f"body: {body}")

            try:
                request_start_time = time.time()
                response = requests.request(
                    method=method, headers=headers, url=url, data=body)
                latency_in_ms = (time.time() - request_start_time) * 1000
                logging.debug(
                    f"Latency in milliseconds for current request: {latency_in_ms}")

                # Check if UP
                if 200 <= response.status_code <= 299 and latency_in_ms < 500:
                    endpoint_status[domain][0] += 1

                else:
                    endpoint_status[domain][1] += 1

            except RequestException:
                endpoint_status[domain][1] += 1
                logging.error(
                    f"Current endpoint threw RequestException and is DOWN")

            total_requests_count.inc(1)

        # Calculate availability
        i = 0
        for domain, [up, down] in endpoint_status.items():
            sum = up + down

            avail_perc = up / sum * 100 if sum != 0 else 0
            print(f'{domain} has {avail_perc:.0f}% availability percentage')
            logging.info(
                f"{domain} has {avail_perc:.0f}% availability percentage")

            # Set the availibility percentage for the first domain
            if i == 0:
                available_perc_first_domain.set(avail_perc)
            i += 1

        logging.info("Completed the Health Check for the endpoints")

    except Exception:
        logging.error(e)
        print(e)


@app.get("/")
async def home():
    return "Hello! The script has began execution and the endpoints will be triggered every 15 seconds. Go to http://localhost:9090/metrics to view the metrics. To view the metric graph go to http://localhost:9090/graph and enter 'available_perc_first_domain' hit enter and select the 'Graph' tab."

if __name__ == "__main__":
    # Check if the env var CONFIG_FILE is set or not
    if not os.environ['CONFIG_FILE']:
        raise Exception(
            "Please set the CONFIG_FILE env var to point to a valid YAML file.")

    config_file = os.environ['CONFIG_FILE']

    # Setup logging for this application
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

   # Get log level from env var
    log_level = os.environ['LOG_LEVEL']

    print(f'CONFIG_FILE: {config_file}, LOG_LEVEL: {log_level}')

    if log_level:
        numeric_level = getattr(logging, log_level.upper(), None)
        if numeric_level:
            logging.basicConfig(
                filename=LOG_FILE_PATH, level=numeric_level, format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
        else:
            logging.basicConfig(
                filename=LOG_FILE_PATH, level=logging.INFO, format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    else:
        logging.basicConfig(
            filename=LOG_FILE_PATH, level=logging.INFO, format=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

    logging.info(f"Starting the script...")

    # Open the Config YAML file
    try:
        with open(config_file) as f:
            logging.info(f"Reading the config file: {config_file}")
            endpoint_list = yaml.safe_load(f)

        # The yaml.safe_load can return a Dict so convert it List for further processing
        if type(endpoint_list) == "Dict":
            endpoint_list = list(endpoint_list.values())

        logging.debug(f"Number of endpoints found: {len(endpoint_list)}")

        endpoint_status = {}

    except Exception as e:
        logging.error(f"{e}")
        print(f'{e}')

    logging.info(f"Exiting the script...")

    # Start server
    uvicorn.run(app, host="0.0.0.0", port=5000)
