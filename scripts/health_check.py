#!/usr/bin/env python3
"""
Health Check Module for DevOps Project.
Checks the availability of a web service and logs the result.
"""

import requests
import time
import logging
from datetime import datetime
import sys

def setup_logging(log_file='health_check.log'):
    """Configure logging to write to a file and console."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def check_service_health(url, timeout=5):
    """
    Check if a web service is responding with a successful status.
    
    Args:
        url (str): The URL to check
        timeout (int): Request timeout in seconds
    
    Returns:
        tuple: (is_healthy: bool, response_time: float, status_code: int)
    """
    start_time = time.time()
    try:
        response = requests.get(url, timeout=timeout)
        response_time = time.time() - start_time
        is_healthy = response.status_code < 400  # 2xx or 3xx codes are considered healthy
        return is_healthy, response_time, response.status_code
    except requests.exceptions.RequestException as e:
        response_time = time.time() - start_time
        return False, response_time, None

def main():
    """Main function to run the health check."""
    logger = setup_logging()
    
    # Configuration
    SERVICE_URL = "http://localhost:5000/health"  # Our Flask app's health endpoint
    CHECK_INTERVAL = 30  # seconds
    
    logger.info(f"Starting health check for {SERVICE_URL}")
    
    try:
        while True:
            is_healthy, response_time, status_code = check_service_health(SERVICE_URL)
            
            if is_healthy:
                logger.info(f"Service HEALTHY - Status: {status_code}, Response time: {response_time:.3f}s")
            else:
                logger.error(f"Service UNHEALTHY - Status: {status_code}, Response time: {response_time:.3f}s")
            
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        logger.info("Health check stopped by user")

if __name__ == "__main__":
    main()
