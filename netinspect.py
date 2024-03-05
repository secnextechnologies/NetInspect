import requests
import socket
import urllib3
from colorama import Fore, Style
import argparse
from concurrent.futures import ThreadPoolExecutor
import signal
import ipaddress
import threading
import sys

# ASCII banner
ascii_banner = """
  _   _      _   _____                           _   
 | \ | |    | | |_   _|                         | |  
 |  \| | ___| |_  | |  _ __  ___ _ __   ___  ___| |_ 
 | . ` |/ _ \ __| | | | '_ \/ __| '_ \ / _ \/ __| __|
 | |\  |  __/ |_ _| |_| | | \__ \ |_) |  __/ (__| |_ 
 |_| \_|\___|\__|_____|_| |_|___/ .__/ \___|\___|\__|
                                | |                  
                                |_|                  - By SecneX Technologies
"""

# Print the ASCII banner
print(ascii_banner)

# Suppress InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Global flag to signal threads to exit
exit_flag = threading.Event()

def get_service_info(ip, output=None):
    if exit_flag.is_set():
        return

    try:
        target = socket.gethostbyaddr(ip)[0]
    except socket.herror:
        target = ip

    result = ""

    # Check for HTTP service
    try:
        url = f"http://{target}"
        response = requests.get(url, timeout=5, verify=False)
        result += f"[ {Fore.GREEN}{url}{Style.RESET_ALL} | {Fore.CYAN}{response.headers.get('Server', 'None')}{Style.RESET_ALL} | {Fore.YELLOW}{response.status_code}{Style.RESET_ALL} | {Fore.MAGENTA}{len(response.content)}{Style.RESET_ALL} | {Fore.WHITE}{response.reason}{Style.RESET_ALL} ]"

        # CMS Fingerprinting
        cms = identify_cms(response.text)
        if cms:
            result += f"\n  {Fore.RED}CMS Detected: {cms}{Style.RESET_ALL}"
    except requests.RequestException as e:
        pass

    # Check for HTTPS service
    try:
        url = f"https://{target}"
        response = requests.get(url, timeout=5, verify=False)
        if result:  # Add a newline only if the HTTP result is not empty
            result += "\n"
        result += f"[ {Fore.GREEN}{url}{Style.RESET_ALL} | {Fore.CYAN}{response.headers.get('Server', 'None')}{Style.RESET_ALL} | {Fore.YELLOW}{response.status_code}{Style.RESET_ALL} | {Fore.MAGENTA}{len(response.content)}{Style.RESET_ALL} | {Fore.WHITE}{response.reason}{Style.RESET_ALL} ]"

        # CMS Fingerprinting
        cms = identify_cms(response.text)
        if cms:
            result += f"\n  {Fore.RED}CMS Detected: {cms}{Style.RESET_ALL}"
    except requests.RequestException as e:
        pass

    if output:
        with open(output, 'a') as file:
            file.write(result)
    elif result.strip():  # Check if result is not empty after stripping spaces
        print(result)

def identify_cms(content):
    cms_list = {
        "WordPress": ["wp-content", "wp-includes"],
        "Joomla": ["com_content", "com_users"],
        "Drupal": ["sites/all/modules", "sites/default/files"],
        # Add more CMS fingerprints as needed
    }

    for cms, keywords in cms_list.items():
        if all(keyword in content for keyword in keywords):
            return cms
    return None

def handle_exception(worker):
    exception_type, exception, traceback = worker.exc_info()
    print(f"Exception in worker: {exception_type.__name__}: {exception}")

def interrupt_handler(signal, frame):
    print("\nScript interrupted. Exiting gracefully.")
    exit_flag.set()
    sys.exit()  # Use sys.exit() from the sys module

def get_ips_from_subnet(subnet):
    # Use the ipaddress module to get all IP addresses in the subnet
    return [str(ip) for ip in ipaddress.IPv4Network(subnet, strict=False).hosts()]

if __name__ == "__main__":
    # Register the interrupt_handler for Ctrl+C
    signal.signal(signal.SIGINT, interrupt_handler)

    parser = argparse.ArgumentParser(description="Scan IPs or domains for service information.")
    parser.add_argument("-i", "--ip", help="Single IP address")
    parser.add_argument("-is", "--ip_subnet", help="Subnet (e.g., 192.168.1.0/24)")
    parser.add_argument("-il", "--ip_list", help="File containing a list of IPs")
    parser.add_argument("-d", "--domain", help="Single domain")
    parser.add_argument("-dl", "--domain_list", help="File containing a list of domains")
    parser.add_argument("-o", "--output", help="Output file for results")

    args = parser.parse_args()

    if not (args.ip or args.ip_list or args.domain or args.domain_list or args.ip_subnet):
        print("Please provide either an IP, IP list, domain, domain list, or IP subnet. Use -h for help.")
        sys.exit()

    targets = []
    if args.ip:
        targets.append(args.ip)
    elif args.ip_list:
        with open(args.ip_list, 'r') as file:
            targets.extend(map(str.strip, file.readlines()))
    elif args.ip_subnet:
        targets.extend(get_ips_from_subnet(args.ip_subnet))

    if args.domain:
        targets.append(args.domain)
    elif args.domain_list:
        with open(args.domain_list, 'r') as file:
            targets.extend(map(str.strip, file.readlines()))

    try:
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(get_service_info, target, args.output): target for target in targets}
            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    handle_exception(future)
    except KeyboardInterrupt:
        print("\nScript interrupted. Exiting gracefully.")

    # Explicitly wait for threads to finish before exiting
    exit_flag.set()
    sys.exit()
