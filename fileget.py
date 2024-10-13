import os
import requests
import argparse
import sys
import time
from ftplib import FTP
from pathlib import Path
from requests.auth import HTTPBasicAuth

def parse_headers(headers_str):
    headers = {}
    for header in headers_str.split(','):
        key, value = header.split(':')
        headers[key.strip()] = value.strip()
    return headers

def download_file_http(url, save_path, method='GET', data=None, headers=None, auth=None, proxy=None, timeout=10, max_retries=3, force_https=False, no_check_certificate=False, cert=None):
    if force_https and not url.startswith('https'):
        url = url.replace('http://', 'https://')

    session = requests.Session()

    # Setup proxy if provided
    proxies = None
    if proxy:
        proxies = {
            "http": proxy,
            "https": proxy
        }

    for attempt in range(max_retries):
        try:
            if method == 'POST':
                response = session.post(url, data=data, headers=headers, auth=auth, proxies=proxies, timeout=timeout, verify=not no_check_certificate, cert=cert)
            else:
                response = session.get(url, headers=headers, auth=auth, proxies=proxies, timeout=timeout, verify=not no_check_certificate, cert=cert)

            response.raise_for_status()  # Raise an error for bad responses
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {save_path}")
            return
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait before retrying

    print(f"Failed to download {url} after {max_retries} attempts.")

def download_file_ftp(ftp_url, save_path, username, password, anonymous=False):
    try:
        # Parse the FTP URL and extract hostname and file path
        ftp_url = ftp_url.replace('ftp://', '')
        host, path = ftp_url.split('/', 1)

        ftp = FTP(host)
        if anonymous:
            ftp.login()  # Anonymous login
        else:
            ftp.login(username, password)

        with open(save_path, 'wb') as f:
            ftp.retrbinary(f"RETR /{path}", f.write)

        ftp.quit()
        print(f"Downloaded: {save_path}")
    except Exception as e:
        print(f"FTP download failed: {e}")

def main():
    parser = argparse.ArgumentParser(description="File Downloader with FTP, HTTP/HTTPS, Custom Headers, User-Agent, and Proxy Support")
    parser.add_argument("url", help="URL of the file to download (supports HTTP, HTTPS, FTP).")
    parser.add_argument("-d", "--directory", type=str, help="Directory to save the downloaded file.")
    parser.add_argument("-m", "--method", choices=['GET', 'POST'], default='GET', help="HTTP method to use.")
    parser.add_argument("--data", type=str, help="Data to send with POST request.")
    parser.add_argument("--timeout", type=int, default=10, help="Timeout for the request in seconds.")
    parser.add_argument("--retries", type=int, default=3, help="Maximum number of retries.")
    parser.add_argument("--force-https", action='store_true', help="Force HTTPS if using HTTP.")
    parser.add_argument("--no-check-certificate", action='store_true', help="Disable SSL certificate validation.")
    parser.add_argument("--cert", type=str, help="Path to SSL certificate (PEM or CRT) file.")
    parser.add_argument("--headers", type=str, help="Custom headers (format: 'Header1: value1, Header2: value2').")
    parser.add_argument("--user-agent", type=str, help="Custom User-Agent string.")
    parser.add_argument("-u", "--username", type=str, help="Username for FTP/HTTP authentication.")
    parser.add_argument("-p", "--password", type=str, help="Password for FTP/HTTP authentication.")
    parser.add_argument("--ftp-anonymous", action='store_true', help="Use anonymous FTP login.")
    parser.add_argument("--proxy", type=str, help="Proxy URL (format: 'http://user:pass@proxyserver:port').")
    parser.add_argument("-6", "--ipv6", action='store_true', help="Use IPv6.")

    args = parser.parse_args()

    # Set up authentication if provided
    auth = None
    if args.username and args.password:
        auth = HTTPBasicAuth(args.username, args.password)

    # Ensure the directory exists
    if args.directory:
        Path(args.directory).mkdir(parents=True, exist_ok=True)

    # Determine save path
    filename = os.path.basename(args.url)
    save_path = os.path.join(args.directory, filename) if args.directory else filename

    # Prepare data for POST request
    post_data = None
    if args.method == 'POST' and args.data:
        post_data = {k: v for k, v in (item.split('=') for item in args.data.split('&'))}

    # Parse custom headers
    headers = parse_headers(args.headers) if args.headers else {}

    # Add custom user-agent if provided
    if args.user_agent:
        headers['User-Agent'] = args.user_agent

    # Check if a certificate file is specified
    cert = None
    if args.cert:
        cert = args.cert

    # Determine whether to use FTP or HTTP/HTTPS
    if args.url.startswith('ftp://'):
        download_file_ftp(args.url, save_path, username=args.username, password=args.password, anonymous=args.ftp_anonymous)
    else:
        # HTTP/HTTPS download
        download_file_http(args.url, save_path, method=args.method, data=post_data, headers=headers, auth=auth, proxy=args.proxy, timeout=args.timeout, max_retries=args.retries, force_https=args.force_https, no_check_certificate=args.no_check_certificate, cert=cert)

if __name__ == "__main__":
    main()
