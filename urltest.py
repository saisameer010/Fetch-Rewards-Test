import yaml
import requests
import time
from collections import defaultdict

def load_endpoints(file_path):
    """
    Function to load a file path
    """ 
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def check_health(endpoint):
    """
    Function to check health of an endpoint 
    - status is 200 and time < 500 ms : UP
    - not up : DOWN
    """
    method = endpoint.get('method', 'GET')
    url = endpoint['url']
    headers = endpoint.get('headers', {})
    body = endpoint.get('body', None)

    try:
        response = requests.request(method, url, headers=headers, data=body, timeout=5)
        latency = response.elapsed.total_seconds() * 1000  
        if 200 <= response.status_code < 300 and latency < 500:
            return 'UP'
        else:
            return 'DOWN'
    except requests.RequestException:
        return 'DOWN'

def log_availability(domain_availability, total_checks):
    """
    Printing log data to console
    """
    for domain, up_count in domain_availability.items():
        availability_percentage = (up_count / total_checks[domain]) * 100
        print(f"{domain} has {round(availability_percentage)}% availability percentage")

def main(file_path):
    endpoints = load_endpoints(file_path)
    domain_availability = defaultdict(int)
    total_checks = defaultdict(int)

    try:
        # Infinite loop till interupt
        while True:
            for endpoint in endpoints:
                url = endpoint['url']
                domain = url.split('/')[2]  
                status = check_health(endpoint)
                total_checks[domain] += 1
                if status == 'UP':
                    domain_availability[domain] += 1
            log_availability(domain_availability, total_checks)
            # Sleeping 15 seconds 
            time.sleep(15)
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception:
        print(f"\nError with parsing Yaml FILE")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python health_check.py <path_to_yaml>")
    else:
        main(sys.argv[1])
