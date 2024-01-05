import time
import requests
from requests.exceptions import RequestException
import yaml
import argparse
from urllib.parse import urlparse
from typing import Dict, List
import logging
from helper.constants import LOG_FORMAT, LOG_FILE_PATH, LOG_DATE_FORMAT
import os


def test_endpoints_health(endpoint_list: List[Dict], endpoint_status: Dict) -> None:
    '''
    This function is called every 15 seconds to check the health of all the endpoints in the YAML file.

    Parameters:
        endpoint_list (List[Dict]): List of all the endpoints.
        endpoint_status (Dict): With keys as domain names and value is a list of two integers. First, indicating the number of times it is UP and second, indicating the number of times it is DOWN.

    Return:
        None
    '''

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

    # Calculate availability
    for domain, [up, down] in endpoint_status.items():
        sum = up + down

        avail_perc = (up / sum) * 100 if sum != 0 else 0
        print(f'{domain} has {avail_perc:.0f}% availability percentage')
        logging.info(
            f"{domain} has {avail_perc:.0f}% availability percentage")

    logging.info("Completed the Health Check for the endpoints")


if __name__ == '__main__':
    # To parse command line argument for the Config file
    p = argparse.ArgumentParser()
    p.add_argument('--f', dest='file_path',
                   help='Enter the Configuration YAML file path.', required=True)
    p.add_argument('--log', dest="loglevel",
                   help="Enter the Log level if needed. [optional]")
    args = p.parse_args()

    # Setup logging for this application
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
    if args.loglevel:
        numeric_level = getattr(logging, args.loglevel.upper(), None)
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
        with open(args.file_path) as f:
            logging.info(f"Reading the config file: {args.file_path}")
            endpoint_list = yaml.safe_load(f)

        # The yaml.safe_load can return a Dict so convert it List for further processing
        if type(endpoint_list) == "Dict":
            endpoint_list = list(endpoint_list.values())

        logging.debug(f"Number of endpoints found: {len(endpoint_list)}")

        endpoint_status = {}

        script_start_time = time.time()
        while True:
            # Check the Health of the endpoints
            test_endpoints_health(endpoint_list, endpoint_status)

            # Sleep for 15 seconds
            time.sleep(15.0 - ((time.time() - script_start_time) % 15.0))

    except Exception as e:
        logging.error(f"{e}")
        print(f'{e}')

    logging.info(f"Exiting the script...")
