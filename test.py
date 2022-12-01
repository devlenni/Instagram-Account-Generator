import json
from os import system
import random
import threading
import requests
import uuid
import time
import colorama
from colorama import Fore, Style
from threading import Lock
from datetime import datetime
from faker import Faker
from fivesim import FiveSim
from random import randint
import string


def base36(x: int, base: int) -> str:
        base_36 = string.digits + string.ascii_letters

        if x < 0:
            sign = -1
        elif x == 0:
            return base_36[0]
        else:
            sign = 1
        x *= sign
        digits = []
        while x:
            digits.append(base_36[x % base])
            x = x // base
        if sign < 0:
            digits.append("-")
        digits.reverse()
        return "".join(digits)

def x_mid() -> str:
        return "".join([base36(randint(2**29, 2**32), 36) for _ in range(8)])


s = requests.Session()

webhook = "https://discord.com/api/webhooks/..."

print_lock = Lock()
colorama.init(autoreset=True)

def error(text, task_id):
    spaces = 3 - len(task_id)
    MESSAGE = '[{}] [{}{}] {}'.format(Fore.MAGENTA + datetime.now().strftime('%H:%M:%S.%f') + Style.RESET_ALL,
                                        ' ' * spaces, Fore.RED + task_id + Style.RESET_ALL, Fore.RED + text)
    print_lock.acquire()
    print(MESSAGE, Style.RESET_ALL)
    print_lock.release()


def success(text, task_id):
    spaces = 3 - len(task_id)
    MESSAGE = '[{}] [{}{}] {}'.format(Fore.MAGENTA + datetime.now().strftime('%H:%M:%S.%f') + Style.RESET_ALL,
                                        ' ' * spaces, Fore.GREEN + task_id + Style.RESET_ALL, Fore.GREEN + text)
    print_lock.acquire()
    print(MESSAGE, Style.RESET_ALL)
    print_lock.release()

def status(text, task_id):
    spaces = 3 - len(task_id)
    MESSAGE = '[{}] [{}{}] {}'.format(Fore.MAGENTA + datetime.now().strftime('%H:%M:%S.%f') + Style.RESET_ALL,
                                        ' ' * spaces, task_id, text)
    print_lock.acquire()
    print(MESSAGE, Style.RESET_ALL)
    print_lock.release()

def get_password(name):
    return f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{"Hermannprut+234553"}'

def get_session_proxy():
    with open('files/proxies.txt', 'r') as proxy_file:
        read_proxies = proxy_file.read()
    if len(read_proxies) < 2:
        return None
    proxies = read_proxies.splitlines()
    if len(proxies[0]) > 1:
        proxy = proxies[0]
        del proxies[0]
        with open('files/proxies.txt', 'w') as new_proxy_file:
            new_proxy_file.write('\n'.join(proxies))
    
    proxy_info = proxy.split(':')
    final_proxies = {
        "http": f"http://{proxy_info[2]}:{proxy_info[3]}@{proxy_info[0]}:{proxy_info[1]}",
        "https": f"http://{proxy_info[2]}:{proxy_info[3]}@{proxy_info[0]}:{proxy_info[1]}"
    }
    return final_proxies

def x_mid() -> str:
        return "".join([base36(randint(2**29, 2**32), 36) for _ in range(8)])

def instagen(task_id, sms_api_key=None, country_code=None, webhook=None):
    fake = Faker()

    device_id = str(uuid.uuid4).lower()
    fam_device_id = str(uuid.uuid4).lower()
    waterfall_id = str(uuid.uuid4).lower()
    x_mid_token = x_mid()

    name = fake.name()
    username = name.replace(" ", ".")+"129"
    password = get_password(name)
    print("USERNAME: ", username)
    print("PASSWORD: ", password)
    s = requests.Session()
    try:
        s.proxies = get_session_proxy()
    except ValueError as err:
        error(err, task_id)
        return

    try:
        r = requests.get(
            "https://5sim.net/v1/user/buy/activation/germany/any/instagram",
            headers={
                "Authorization": f"Bearer {sms_api_key}",
                "Accept": "application/json"
            }
        )
        phone_number = r.json()["phone"]
        phone_id = r.json()["id"]
    except:
        error('Error while getting phone number, please check your api_key and balance...', task_id)
    
    try:
        r = s.post(
            "https://i.instagram.com/api/v1/accounts/check_phone_number/",
            headers={
                "host": "i.instagram.com",
                "x-ig-app-locale": "de_DE",
                "x-ig-device-locale": "de_DE",
                "x-ig-mapped-locale": "de_DE",
                "x-pigeon-session-id": "UFS-27bc2bfa-6c52-4a25-baa8-78abb574e356-0", #
                "x-pigeon-rawclienttime": str(time.time())[:-4], #
                "x-ig-bandwidth-speed-kbps": "-1.000",
                "x-ig-bandwidth-totalbytes-b": "0",
                "x-ig-bandwidth-totaltime-ms": "0",
                "x-bloks-version-id": "0928297a84f74885ff39fc1628f8a40da3ef1c467555d555bfd9f8fe1aaacafe",
                "x-ig-www-claim": "0",
                "x-bloks-is-layout-rtl": "false",
                "x-ig-device-id": device_id, #
                "x-ig-family-device-id": fam_device_id, #
                "x-ig-android-id": "android-28ed903f00073477", #
                "x-ig-timezone-offset": "3600",
                "x-fb-connection-type": "WIFI",
                "x-ig-connection-type": "WIFI",
                "x-ig-capabilities": "3brTv10=",
                "x-ig-app-id": "567067343352427",
                "priority": "u=3",
                "user-agent": "Instagram 256.0.0.18.105 Android (25/7.1.2; 300dpi; 900x1600; samsung; SM-N975F; SM-N975F; intel; de_DE; 407843051)",
                "accept-language": "de-DE, en-US",
                "x-mid": x_mid_token, #
                "ig-intended-user-id": "0",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "accept-encoding": "zstd, gzip, deflate",
                "x-fb-http-engine": "Liger",
                "x-fb-client-ip": "True",
                "x-fb-server-cluster": "True"
            }, data={
                "signed_body": 'SIGNATURE.{"phone_id":"%s","login_nonce_map":"{}","phone_number":"%s","guid":"%s","device_id":"android-28ed903f00073477","prefill_shown":"False"}' % (fam_device_id, phone_number, device_id)
            }
        )
        if r.status_code != 200:
            raise Exception
        status("Phone number valid", task_id)
    except:
        error('Error while checking phone number, trying again...', task_id)
        s = requests.Session()
        try:
            s.proxies = get_session_proxy()
        except ValueError as err:
            error(err, task_id)
            return
        time.sleep(2)


    try:
        r = s.post(
            "https://i.instagram.com/api/v1/accounts/send_signup_sms_code/",
            headers={
                "host": "i.instagram.com",
                "x-ig-app-locale": "de_DE",
                "x-ig-device-locale": "de_DE",
                "x-ig-mapped-locale": "de_DE",
                "x-pigeon-session-id": "UFS-27bc2bfa-6c52-4a25-baa8-78abb574e356-0", #
                "x-pigeon-rawclienttime": str(time.time())[:-4], #
                "x-ig-bandwidth-speed-kbps": "-1.000",
                "x-ig-bandwidth-totalbytes-b": "0",
                "x-ig-bandwidth-totaltime-ms": "0",
                "x-bloks-version-id": "0928297a84f74885ff39fc1628f8a40da3ef1c467555d555bfd9f8fe1aaacafe",
                "x-ig-www-claim": "0",
                "x-bloks-is-layout-rtl": "false",
                "x-ig-device-id": device_id, #
                "x-ig-family-device-id": fam_device_id, #
                "x-ig-android-id": "android-28ed903f00073477", #
                "x-ig-timezone-offset": "3600",
                "x-fb-connection-type": "WIFI",
                "x-ig-connection-type": "WIFI",
                "x-ig-capabilities": "3brTv10=",
                "x-ig-app-id": "567067343352427",
                "priority": "u=3",
                "user-agent": "Instagram 256.0.0.18.105 Android (25/7.1.2; 300dpi; 900x1600; samsung; SM-N975F; SM-N975F; intel; de_DE; 407843051)",
                "accept-language": "de-DE, en-US",
                "x-mid": x_mid_token, #
                "ig-intended-user-id": "0",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "accept-encoding": "zstd, gzip, deflate",
                "x-fb-http-engine": "Liger",
                "x-fb-client-ip": "True",
                "x-fb-server-cluster": "True"
            }, data={
                "signed_body": 'SIGNATURE.{"phone_id":"%s","phone_number":"%s","guid":"%s","device_id":"android-28ed903f00073477","android_build_type":"release","waterfall_id":"%s"}' % (fam_device_id, phone_number, device_id, waterfall_id)
            }
        )
        print(r.text)
        if r.status_code != 200:
            raise Exception
        status("Sent sms code", task_id)
    except:
        error('Error while sending sms, trying again...', task_id)
        s = requests.Session()
        try:
            s.proxies = get_session_proxy()
        except ValueError as err:
            error(err, task_id)
            return
        time.sleep(2)


    try:
        x = 0
        while x < 25:
            r = requests.get(
                f"https://5sim.net/v1/user/check/{phone_id}",
                headers={
                "Authorization": f"Bearer {sms_api_key}",
                "Accept": "application/json"
            })
            data = r.json()["sms"]
            if data:
                sms_code = data[0]["code"]
                break
            x += 1
            time.sleep(3)
    except:
        error('Error while getting sms', task_id)
        r = requests.get(
            f"https://5sim.net/v1/user/cancel/{phone_id}",
            headers={
            "Authorization": f"Bearer {sms_api_key}",
            "Accept": "application/json"
        })

    
    try:
        r = s.post(
            "https://i.instagram.com/api/v1/accounts/validate_signup_sms_code/",
            headers={
                "host": "i.instagram.com",
                "x-ig-app-locale": "de_DE",
                "x-ig-device-locale": "de_DE",
                "x-ig-mapped-locale": "de_DE",
                "x-pigeon-session-id": "UFS-27bc2bfa-6c52-4a25-baa8-78abb574e356-0", #
                "x-pigeon-rawclienttime": str(time.time())[:-4], #
                "x-ig-bandwidth-speed-kbps": "-1.000",
                "x-ig-bandwidth-totalbytes-b": "0",
                "x-ig-bandwidth-totaltime-ms": "0",
                "x-bloks-version-id": "0928297a84f74885ff39fc1628f8a40da3ef1c467555d555bfd9f8fe1aaacafe",
                "x-ig-www-claim": "0",
                "x-bloks-is-layout-rtl": "false",
                "x-ig-device-id": device_id, #
                "x-ig-family-device-id": fam_device_id, #
                "x-ig-android-id": "android-28ed903f00073477", #
                "x-ig-timezone-offset": "3600",
                "x-ig-nav-chain": "PhoneConfirmationFragment:phone_confirmation:1:button::",
                "x-fb-connection-type": "WIFI",
                "x-ig-connection-type": "WIFI",
                "x-ig-capabilities": "3brTv10=",
                "x-ig-app-id": "567067343352427",
                "priority": "u=3",
                "user-agent": "Instagram 256.0.0.18.105 Android (25/7.1.2; 300dpi; 900x1600; samsung; SM-N975F; SM-N975F; intel; de_DE; 407843051)",
                "accept-language": "de-DE, en-US",
                "x-mid": x_mid_token, #
                "ig-intended-user-id": "0",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "accept-encoding": "zstd, gzip, deflate",
                "x-fb-http-engine": "Liger",
                "x-fb-client-ip": "True",
                "x-fb-server-cluster": "True"
            }, data={
                "signed_body": 'SIGNATURE.{"verification_code":"%s","phone_number":"%s","guid":"%s","device_id":"android-28ed903f00073477","waterfall_id":"%s"}' % (sms_code, phone_number, device_id, waterfall_id)
            }
        )
        print(r.text)
        if r.status_code != 200:
            raise Exception
        status("SMS code valid", task_id)
    except:
        error('Error while validating sms, trying again...', task_id)
        s = requests.Session()
        try:
            s.proxies = get_session_proxy()
        except ValueError as err:
            error(err, task_id)
            return
        time.sleep(2)


    try:
        r = s.post(
            "https://i.instagram.com/api/v1/accounts/create_validated/",
            headers={
                "host": "i.instagram.com",
                "x-ig-app-locale": "de_DE",
                "x-ig-device-locale": "de_DE",
                "x-ig-mapped-locale": "de_DE",
                "x-pigeon-session-id": "UFS-27bc2bfa-6c52-4a25-baa8-78abb574e356-0", #
                "x-pigeon-rawclienttime": str(time.time())[:-4], #
                "x-ig-bandwidth-speed-kbps": "-1.000",
                "x-ig-bandwidth-totalbytes-b": "0",
                "x-ig-bandwidth-totaltime-ms": "0",
                "x-bloks-version-id": "0928297a84f74885ff39fc1628f8a40da3ef1c467555d555bfd9f8fe1aaacafe",
                "x-ig-www-claim": "0",
                "x-bloks-is-layout-rtl": "false",
                "x-ig-device-id": device_id, #
                "x-ig-family-device-id": fam_device_id, #
                "x-ig-android-id": "android-28ed903f00073477", #
                "x-ig-timezone-offset": "3600",
                "x-ig-nav-chain": "PhoneConfirmationFragment:phone_confirmation:1:button::,OnePageRegistrationFragment:one_page_registration:2:button::,AddBirthdayFragment:add_birthday:3:button::,UsernameSuggestionSignUpFragment:username_sign_up:4:button::",
                "x-fb-connection-type": "WIFI",
                "x-ig-connection-type": "WIFI",
                "x-ig-capabilities": "3brTv10=",
                "x-ig-app-id": "567067343352427",
                "priority": "u=3",
                "user-agent": "Instagram 256.0.0.18.105 Android (25/7.1.2; 300dpi; 900x1600; samsung; SM-N975F; SM-N975F; intel; de_DE; 407843051)",
                "accept-language": "de-DE, en-US",
                "x-mid": x_mid_token, #
                "ig-intended-user-id": "0",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "accept-encoding": "zstd, gzip, deflate",
                "x-fb-http-engine": "Liger",
                "x-fb-client-ip": "True",
                "x-fb-server-cluster": "True"
            }, data={
                "signed_body": 'SIGNATURE.{"is_secondary_account_creation":"false","jazoest":"22236","tos_version":"eu","suggestedUsername":"","verification_code":"%s","sn_result":"eyJhbGciOiJSUzI1NiIsIng1YyI6WyJNSUlGYkRDQ0JGU2dBd0lCQWdJUWVXM2IyVVlEZ1A4UVZIWjVPUHpQQ0RBTkJna3Foa2lHOXcwQkFRc0ZBREJHTVFzd0NRWURWUVFHRXdKVlV6RWlNQ0FHQTFVRUNoTVpSMjl2WjJ4bElGUnlkWE4wSUZObGNuWnBZMlZ6SUV4TVF6RVRNQkVHQTFVRUF4TUtSMVJUSUVOQklERkVOREFlRncweU1qRXdNamN3TmpNME5EZGFGdzB5TXpBeE1qVXdOak0wTkRaYU1CMHhHekFaQmdOVkJBTVRFbUYwZEdWemRDNWhibVJ5YjJsa0xtTnZiVENDQVNJd0RRWUpLb1pJaHZjTkFRRUJCUUFEZ2dFUEFEQ0NBUW9DZ2dFQkFMWnFzcldZNHV0Sk9DN2NPZlVTeDN1Rms1aEY5WWhNTFk3WlJzQjhOcFJMZExVMElLRTB5N0hURnl2V3NzMjczMVdJNUJYYUQyUldSQXc3UEdqK0Evd283K0prUnpiWXBtU3FscWFoZFI5bGNCcjJ1azVtWGhsRWdaTUhyL1prQ3RBdGFsYysyMFJZYUlRbUhKUVFoNG5EKy9nays1cW52dmxmNWhNQ3liOXFEVXdyYzlyV2JCUVRmVUdVb28rWWNJVExCUHlEb0ZSaWh1UU1iNlJmZW1DaU9ENEhXZE9KeFphMXRXNDRvL3NjaWQwOVVHS3IvYWJuRStlckZSbjhQd2ZLaGRrbThWV1FESTl6Z1FVaTNTZWdCdEFQY0tSV1pBTHN5T1lwcHlqbzFlR1k4Z1pxdmw3R0hoR2R6Y291MXZFejNSaXpzNGpDMElPdXFiQXhGZk1DQXdFQUFhT0NBbjB3Z2dKNU1BNEdBMVVkRHdFQi93UUVBd0lGb0RBVEJnTlZIU1VFRERBS0JnZ3JCZ0VGQlFjREFUQU1CZ05WSFJNQkFmOEVBakFBTUIwR0ExVWREZ1FXQkJTNm5Kcm1LQXZjeWdPODJpYk5qQkxMQnVSU0NqQWZCZ05WSFNNRUdEQVdnQlFsNGhnT3NsZVJsQ3JsMUYyR2tJUGVVN080a2pCN0JnZ3JCZ0VGQlFjQkFRUnZNRzB3T0FZSUt3WUJCUVVITUFHR0xHaDBkSEE2THk5dlkzTndMbkJyYVM1bmIyOW5MM012WjNSek1XUTBhVzUwTDE4Mk1YVTNlVnBMY21Kek1ERUdDQ3NHQVFVRkJ6QUNoaVZvZEhSd09pOHZjR3RwTG1kdmIyY3ZjbVZ3Ynk5alpYSjBjeTluZEhNeFpEUXVaR1Z5TUIwR0ExVWRFUVFXTUJTQ0VtRjBkR1Z6ZEM1aGJtUnliMmxrTG1OdmJUQWhCZ05WSFNBRUdqQVlNQWdHQm1lQkRBRUNBVEFNQmdvckJnRUVBZFo1QWdVRE1EOEdBMVVkSHdRNE1EWXdOS0F5b0RDR0xtaDBkSEE2THk5amNteHpMbkJyYVM1bmIyOW5MMmQwY3pGa05HbHVkQzg0YlhWaVVubzFNbU5rVlM1amNtd3dnZ0VDQmdvckJnRUVBZFo1QWdRQ0JJSHpCSUh3QU80QWRRRG9QdERhUHZVR05UTG5WeWk4aVd2SkE5UEwwUkZyN090cDRYZDliUWE5YmdBQUFZUVlYWGd3QUFBRUF3QkdNRVFDSUZldDlDQ0Q0b0F1Y0kxbkVGb1Y5VlNpdmdYQnpyTEtkUklzSjdocVdlQjJBaUJsWWtLTXRnYlhNRnNtR05renhIQjR5NEVBYzRXYlZrNEhZeUxkZWtySWFRQjFBTGMrK3lUZm5FMjZkZkk1eGJwWTlHeGQvRUxQZXA4MXhKNGRDWUVsN2JTWkFBQUJoQmhkZUQ0QUFBUURBRVl3UkFJZ1l0bVh1azlqK1BLRk9JTDd0WG1PTU1YV0xBMkR4TmFFbkRRT2w3cFZhZTRDSUJrdlJKZzNqNXdoa1c5b1FVRG1McllWRHFLVzJzYkk5RlY5VGdOUFA3ck1NQTBHQ1NxR1NJYjNEUUVCQ3dVQUE0SUJBUUF4aTVLVDN3WFl4WFFLdnM5T2loaSt6cXVMZzlNKy8xMXJ1aWIyMmtPNEVYZHFnNnBxamt5UDhqWEZkVkdDSDB6clJCZHZ1emV0YW5vMGpEZTRDUzJzN1g0SEY1UEpMbXc5SUdWUUxmRWlNNTV1R0dqMUduRkJVMFA1TzI3aW4yeEdCclJ5K29uTHhIVDVkR0lxMTNBdkllYW1XVnhMSzJVSkk0dTEzZFNJSjNEVXBHcEtINWYxdTJEdnp5Y1VOY1F2U1NUTzJyQnBlMjJUY2NBbHJZVjlsc3FlL3dkeGZUU3Y5VUFOQTZCSGQ4eEFvRTBOS0dKVmxsZGM0T3NVUzdSY2dURTRZQSs4LzY2OFFmWmlPUjRVa05vanpYekhJVFBMaXlBQ2ZtTmM3bjVPZTNQR1dkRkhMdkdkV2k4Nmp4R0ZnTEc5SGR5R2JKNHdKSWhRWHJTYyIsIk1JSUZqRENDQTNTZ0F3SUJBZ0lOQWdDT3NnSXpObVdMWk0zYm16QU5CZ2txaGtpRzl3MEJBUXNGQURCSE1Rc3dDUVlEVlFRR0V3SlZVekVpTUNBR0ExVUVDaE1aUjI5dloyeGxJRlJ5ZFhOMElGTmxjblpwWTJWeklFeE1RekVVTUJJR0ExVUVBeE1MUjFSVElGSnZiM1FnVWpFd0hoY05NakF3T0RFek1EQXdNRFF5V2hjTk1qY3dPVE13TURBd01EUXlXakJHTVFzd0NRWURWUVFHRXdKVlV6RWlNQ0FHQTFVRUNoTVpSMjl2WjJ4bElGUnlkWE4wSUZObGNuWnBZMlZ6SUV4TVF6RVRNQkVHQTFVRUF4TUtSMVJUSUVOQklERkVORENDQVNJd0RRWUpLb1pJaHZjTkFRRUJCUUFEZ2dFUEFEQ0NBUW9DZ2dFQkFLdkFxcVBDRTI3bDB3OXpDOGRUUElFODliQSt4VG1EYUc3eTdWZlE0YyttT1dobFVlYlVRcEsweXYycjY3OFJKRXhLMEhXRGplcStuTElITjFFbTVqNnJBUlppeG15UlNqaElSMEtPUVBHQk1VbGRzYXp0SUlKN08wZy84MnFqL3ZHRGwvLzN0NHRUcXhpUmhMUW5UTFhKZGVCKzJEaGtkVTZJSWd4NndON0U1TmNVSDNSY3NlamNxajhwNVNqMTl2Qm02aTFGaHFMR3ltaE1Gcm9XVlVHTzN4dElIOTFkc2d5NGVGS2NmS1ZMV0szbzIxOTBRMExtL1NpS21MYlJKNUF1NHkxZXVGSm0ySk05ZUI4NEZrcWEzaXZyWFdVZVZ0eWUwQ1FkS3ZzWTJGa2F6dnh0eHZ1c0xKekxXWUhrNTV6Y1JBYWNEQTJTZUV0QmJRZkQxcXNDQXdFQUFhT0NBWFl3Z2dGeU1BNEdBMVVkRHdFQi93UUVBd0lCaGpBZEJnTlZIU1VFRmpBVUJnZ3JCZ0VGQlFjREFRWUlLd1lCQlFVSEF3SXdFZ1lEVlIwVEFRSC9CQWd3QmdFQi93SUJBREFkQmdOVkhRNEVGZ1FVSmVJWURySlhrWlFxNWRSZGhwQ0QzbE96dUpJd0h3WURWUjBqQkJnd0ZvQVU1SzhySm5FYUswZ25oUzlTWml6djhJa1RjVDR3YUFZSUt3WUJCUVVIQVFFRVhEQmFNQ1lHQ0NzR0FRVUZCekFCaGhwb2RIUndPaTh2YjJOemNDNXdhMmt1WjI5dlp5OW5kSE55TVRBd0JnZ3JCZ0VGQlFjd0FvWWthSFIwY0RvdkwzQnJhUzVuYjI5bkwzSmxjRzh2WTJWeWRITXZaM1J6Y2pFdVpHVnlNRFFHQTFVZEh3UXRNQ3N3S2FBbm9DV0dJMmgwZEhBNkx5OWpjbXd1Y0d0cExtZHZiMmN2WjNSemNqRXZaM1J6Y2pFdVkzSnNNRTBHQTFVZElBUkdNRVF3Q0FZR1o0RU1BUUlCTURnR0Npc0dBUVFCMW5rQ0JRTXdLakFvQmdnckJnRUZCUWNDQVJZY2FIUjBjSE02THk5d2Eya3VaMjl2Wnk5eVpYQnZjMmwwYjNKNUx6QU5CZ2txaGtpRzl3MEJBUXNGQUFPQ0FnRUFJVlRveTI0andYVXIwckFQYzkyNHZ1U1ZiS1F1WXczbkxmbExmTGg1QVlXRWVWbC9EdTE4UUFXVU1kY0o2by9xRlpiaFhrQkgwUE5jdzk3dGhhZjJCZW9EWVk5Q2svYitVR2x1aHgwNnpkNEVCZjdIOVA4NG5ucndwUis0R0JEWksrWGgzSTB0cUp5MnJnT3FORGZscjVJTVE4WlRXQTN5bHRha3pTQktaNlhwRjBQcHF5Q1J2cC9OQ0d2MktYMlR1UENKdnNjcDEvbTJwVlR0eUJqWVBSUStRdUNRR0FKS2p0TjdSNURGcmZUcU1XdllnVmxwQ0pCa3dsdTcrN0tZM2NUSWZ6RTdjbUFMc2tNS05MdUR6K1J6Q2NzWVRzVmFVN1ZwM3hMNjBPWWhxRmt1QU9PeERaNnBIT2o5K09KbVlnUG1PVDRYMys3TDUxZlhKeVJIOUtmTFJQNm5UMzFENW5tc0dBT2daMjYvOFQ5aHNCVzF1bzlqdTVmWkxaWFZWUzVIMEh5SUJNRUt5R01JUGhGV3JsdC9oRlMyOE4xemFLSTBaQkdEM2dZZ0RMYmlEVDlmR1hzdHBrK0ZtYzRvbFZsV1B6WGU4MXZkb0VuRmJyNU0yNzJIZGdKV28rV2hUOUJZTTBKaSt3ZFZtblJmZlhnbG9Fb2x1VE5jV3pjNDFkRnBnSnU4ZkYzTEcwZ2wyaWJTWWlDaTlhNmh2VTBUcHBqSnlJV1hoa0pUY01KbFByV3gxVnl0RVVHclgybDBKRHdSalcvNjU2cjBLVkIwMnhIUkt2bTJaS0kwM1RnbExJcG1WQ0sza0JLa0tOcEJOa0Z0OHJoYWZjQ0tPYjlKeC85dHBORmxRVGw3QjM5ckpsSldrUjE3UW5acVZwdEZlUEZPUm9abUZ6TT0iLCJNSUlGWWpDQ0JFcWdBd0lCQWdJUWQ3ME5iTnMyK1JycUlRL0U4RmpURFRBTkJna3Foa2lHOXcwQkFRc0ZBREJYTVFzd0NRWURWUVFHRXdKQ1JURVpNQmNHQTFVRUNoTVFSMnh2WW1Gc1UybG5iaUJ1ZGkxellURVFNQTRHQTFVRUN4TUhVbTl2ZENCRFFURWJNQmtHQTFVRUF4TVNSMnh2WW1Gc1UybG5iaUJTYjI5MElFTkJNQjRYRFRJd01EWXhPVEF3TURBME1sb1hEVEk0TURFeU9EQXdNREEwTWxvd1J6RUxNQWtHQTFVRUJoTUNWVk14SWpBZ0JnTlZCQW9UR1VkdmIyZHNaU0JVY25WemRDQlRaWEoyYVdObGN5Qk1URU14RkRBU0JnTlZCQU1UQzBkVVV5QlNiMjkwSUZJeE1JSUNJakFOQmdrcWhraUc5dzBCQVFFRkFBT0NBZzhBTUlJQ0NnS0NBZ0VBdGhFQ2l4N2pvWGViTzl5L2xENjNsYWRBUEtIOWd2bDlNZ2FDY2ZiMmpILzc2TnU4YWk2WGw2T01TL2tyOXJINXpvUWRzZm5GbDk3dnVmS2o2YndTaVY2bnFsS3IrQ01ueTZTeG5HUGIxNWwrOEFwZTYyaW05TVphUncxTkVEUGpUckVUbzhnWWJFdnMvQW1RMzUxa0tTVWpCNkcwMGowdVlPRFAwZ21IdTgxSThFM0N3bnFJaXJ1Nnoxa1oxcStQc0Fld25qSHhnc0hBM3k2bWJXd1pEclhZZmlZYVJRTTlzSG1rbENpdEQzOG01YWdJL3Bib1BHaVVVKzZET29nckZaWUpzdUI2akM1MTFwenJwMVprajVaUGFLNDlsOEtFajhDOFFNQUxYTDMyaDdNMWJLd1lVSCtFNEV6Tmt0TWc2VE84VXBtdk1yVXBzeVVxdEVqNWN1SEtaUGZtZ2hDTjZKM0Npb2o2T0dhSy9HUDVBZmw0L1h0Y2QvcDJoL3JzMzdFT2VaVlh0TDBtNzlZQjBlc1dDcnVPQzdYRnhZcFZxOU9zNnBGTEtjd1pwRElsVGlyeFpVVFFBczZxemttMDZwOThnN0JBZStkRHE2ZHNvNDk5aVlINlRLWC8xWTdEemt2Z3RkaXpqa1hQZHNEdFFDdjlVdyt3cDlVN0RiR0tvZ1BlTWEzTWQrcHZlejdXMzVFaUV1YSsrdGd5L0JCakZGRnkzbDNXRnBPOUtXZ3o3enBtN0FlS0p0OFQxMWRsZUNmZVhra1VBS0lBZjVxb0liYXBzWld3cGJrTkZoSGF4MnhJUEVEZ2ZnMWF6Vlk4MFpjRnVjdEw3VGxMbk1RLzBsVVRiaVN3MW5INjlNRzZ6TzBiOWY2QlFkZ0FtRDA2eUs1Nm1EY1lCWlVDQXdFQUFhT0NBVGd3Z2dFME1BNEdBMVVkRHdFQi93UUVBd0lCaGpBUEJnTlZIUk1CQWY4RUJUQURBUUgvTUIwR0ExVWREZ1FXQkJUa3J5c21jUm9yU0NlRkwxSm1MTy93aVJOeFBqQWZCZ05WSFNNRUdEQVdnQlJnZTJZYVJRMlh5b2xRTDMwRXpUU28vL3o5U3pCZ0JnZ3JCZ0VGQlFjQkFRUlVNRkl3SlFZSUt3WUJCUVVITUFHR0dXaDBkSEE2THk5dlkzTndMbkJyYVM1bmIyOW5MMmR6Y2pFd0tRWUlLd1lCQlFVSE1BS0dIV2gwZEhBNkx5OXdhMmt1WjI5dlp5OW5jM0l4TDJkemNqRXVZM0owTURJR0ExVWRId1FyTUNrd0o2QWxvQ09HSVdoMGRIQTZMeTlqY213dWNHdHBMbWR2YjJjdlozTnlNUzluYzNJeExtTnliREE3QmdOVkhTQUVOREF5TUFnR0JtZUJEQUVDQVRBSUJnWm5nUXdCQWdJd0RRWUxLd1lCQkFIV2VRSUZBd0l3RFFZTEt3WUJCQUhXZVFJRkF3TXdEUVlKS29aSWh2Y05BUUVMQlFBRGdnRUJBRFNrSHJFb285QzBkaGVtTVhvaDZkRlNQc2piZEJaQmlMZzlOUjN0NVArVDRWeGZxN3ZxZk0vYjVBM1JpMWZ5Sm05YnZoZEdhSlEzYjJ0NnlNQVlOL29sVWF6c2FMK3l5RW45V3ByS0FTT3NoSUFyQW95WmwrdEphb3gxMThmZXNzbVhuMWhJVnc0MW9lUWExdjF2ZzRGdjc0elBsNi9BaFNydzlVNXBDWkV0NFdpNHdTdHo2ZFRaL0NMQU54OExaaDFKN1FKVmoyZmhNdGZUSnI5dzR6MzBaMjA5Zk9VMGlPTXkrcWR1Qm1wdnZZdVI3aFpMNkR1cHN6Zm53MFNrZnRoczE4ZEc5WktiNTlVaHZtYVNHWlJWYk5RcHNnM0JabHZpZDBsSUtPMmQxeG96Y2xPemdqWFBZb3ZKSkl1bHR6a011MzRxUWI5U3oveWlscmJDZ2o4PSJdfQ.eyJub25jZSI6Ikt6UTVNVFV5TVRjM09EWTBNemg4TVRZMk9EQTROamMzTVh3SjlIVXR6UjFYRzJIRi9nR0hDUG1Yc1A5ZlUxYnVCZDg9IiwidGltZXN0YW1wTXMiOjE2NjgwODY3NzMwMTQsImFwa1BhY2thZ2VOYW1lIjoiY29tLmluc3RhZ3JhbS5hbmRyb2lkIiwiYXBrRGlnZXN0U2hhMjU2IjoiSUxlZXJhRFdwY2N2MW85SjBqNDdOY25iNWlPeFVTT3BOeVFhK0dPclc3WT0iLCJjdHNQcm9maWxlTWF0Y2giOmZhbHNlLCJhcGtDZXJ0aWZpY2F0ZURpZ2VzdFNoYTI1NiI6WyJHTGVhNENERC9ZSW1qdkJPTkJqcSttYlFWVTA4VTdwM0tWa0xIc3lmNlRnPSJdLCJiYXNpY0ludGVncml0eSI6ZmFsc2UsImFkdmljZSI6IlJFU1RPUkVfVE9fRkFDVE9SWV9ST00iLCJldmFsdWF0aW9uVHlwZSI6IkJBU0lDIn0.qSoJro-ORYnBMSZLj5i2kb9kuyX8lQpTtAd6eYEIM4icqe_h-eKNlRTX5BLOQKU8yHxRW8Vr3IuvRXoI0nuBkETLtoPFpcr1T02J5PL9uq1_eaddO0hL7w8N-_aCbPKlMKQOsDQbggHR3_JN_UVySLDM3YkTDrr3Aq6PA6Y0140WxOOGJP6Oaq14uKh8xfQOJNp8tsJUvDmu8rDxW8FuEfPuSG8b3CA_MGLuGJ1a_gr_JIiLSc8MAFQ83oBhbJ89hz4wDP77kMlQanTS42835Z_VPkbB73iyInzYgtsa9XH0u5ZN47jM_OFmswtYKMvHJ40xDSmtnVamDCkHDLCbdA","do_not_auto_login_if_credentials_match":"true","phone_id":"%s","enc_password":"%s","phone_number":"%s","username":"%s","first_name":"%s","day":"%s","adid":"dc090db0-4098-4ee0-baef-e20514f403c3","guid":"%s","year":"%s","device_id":"android-28ed903f00073477","_uuid":"%s","month":"%s","sn_nonce":"KzQ5MTUyMTc3ODY0Mzh8MTY2ODA4Njc3MXwJ9HUtzR1XG2HF/gGHCPmXsP9fU1buBd8=","force_sign_up_code":"","waterfall_id":"%s","qs_stamp":"","has_sms_consent":"true","one_tap_opt_in":"true"}' % (sms_code, fam_device_id, password, phone_number, username, name, str(random.randint(10,25)), device_id, str(random.randint(1960,2000)), device_id, str(random.randint(1,12)), waterfall_id)
            }
        )
        print(r.text)
        if r.status_code != 200:
            raise Exception
        status("Account created", task_id)
    except:
        error('Error while creating account, trying again...', task_id)
        s = requests.Session()
        try:
            s.proxies = get_session_proxy()
        except ValueError as err:
            error(err, task_id)
            return
        time.sleep(2)

    try:
        s = requests.Session()
        try:
            s.proxies = get_session_proxy()
        except ValueError as err:
            error(err, task_id)
            return
        for retries in range(3):
            time.sleep(15)

            res = requests.get('https://www.instagram.com/accounts/login/')
            csrf = res.text.replace("\\", "").split('csrf_token\":\"')[1].split('"')[0]

            res = s.post(
                "https://www.instagram.com/api/v1/web/accounts/login/ajax/",
                headers={
                    "accept": "*/*",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "en-US,en;q=0.9",
                    "content-type": "application/x-www-form-urlencoded",
                    "origin": "https://www.instagram.com",
                    "referer": "https://www.instagram.com/",
                    "sec-ch-prefers-color-scheme": "dark",
                    "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
                    "viewport-width": "864",
                    "x-asbd-id": "198387",
                    "x-csrftoken": csrf,
                    "x-ig-app-id": "936619743392459",
                    "x-ig-www-claim": "0",
                    "x-instagram-ajax": "1006578552",
                    "x-requested-with": "XMLHttpRequest"
                }, data={
                    "enc_password": password,
                    "username": username,
                    "queryParams": "{}",
                    "optIntoOneTap": "false",
                    "trustedDeviceRecords": "{}"
                }
            )

            try:
                if res.json()["authenticated"]:                 #successfull logged in:
                    status('Logged in', task_id)
                    insta_claim = res.headers["x-ig-set-www-claim"]
                    res = s.post(
                        'https://www.instagram.com/api/v1/web/friendships/20311520/follow/',
                        headers={
                            "accept": "*/*",
                            "accept-encoding": "gzip, deflate, br",
                            "accept-language": "en-US,en;q=0.9",
                            "content-type": "application/x-www-form-urlencoded",
                            "origin": "https://www.instagram.com",
                            "referer": "https://www.instagram.com/",
                            "sec-ch-prefers-color-scheme": "dark",
                            "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
                            "sec-ch-ua-mobile": "?0",
                            "sec-ch-ua-platform": '"Windows"',
                            "sec-fetch-dest": "empty",
                            "sec-fetch-mode": "cors",
                            "sec-fetch-site": "same-origin",
                            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
                            "viewport-width": "864",
                            "x-asbd-id": "198387",
                            "x-csrftoken": csrf,
                            "x-ig-app-id": "936619743392459",
                            "x-ig-www-claim": insta_claim,
                            "x-instagram-ajax": "1006578552",
                            "x-requested-with": "XMLHttpRequest"
                    })
                    try:
                        #account got clipped
                        if res.json()["message"]:
                            error('Account got clipped', task_id)
                            #clipurl = res.json()["checkpoint_url"]
                            with open('files/clipped_accounts.txt', 'a') as acc_file:
                                acc_file.write(f'{username}:{password}\n')
                    except:
                        #account is not clipped!
                        success('Account is valid', task_id)
                        with open('files/working_accounts.txt', 'a') as acc_file:
                            acc_file.write(f'{username}:{password}\n')
                        #sending message to discord webhook if specified
                        webhook_body = {
                            "content": None,
                            "embeds": [
                                {
                                    "title": "Successfully Instragram Account Created",
                                    "color": 720640,
                                    "fields": [
                                        {
                                            "name": "username",
                                            "value": f"||{username}||",
                                            "inline": True
                                        },
                                        {
                                            "name": "Password",
                                            "value": f"||{password}||",
                                            "inline": True
                                        }
                                    ],
                                    "thumbnail": {
                                        "url": "https://cdn.discordapp.com/attachments/938484202704355328/938900345080414278/Instagram-logo.png"
                                    }
                                }
                            ],
                            "username": "Instagram Gen",
                            "avatar_url": "https://cdn.discordapp.com/attachments/938484202704355328/938900345080414278/Instagram-logo.png"
                        }
                        res = requests.post(webhook, data=json.dumps(webhook_body), headers={"Content-Type":"application/json"})
                    break
                else:
                    #login failed
                    if retries < 2:
                        error('Login failed', task_id)
                    else:
                        error('Login failed -> stopping task', task_id)

            except Exception as e:
                #login failed
                if retries < 2:
                    error('Login failed', task_id)
                else:
                    error('Login failed -> stopping task', task_id)

    except:
        error('Error while checking account, trying again...', task_id)
        s = requests.Session()
        try:
            s.proxies = get_session_proxy()
        except ValueError as err:
            error(err, task_id)
            return
        time.sleep(2)

with open('files/proxies.txt', 'r') as proxy_file:
    read_proxies = proxy_file.read()
    if len(read_proxies) < 2:
        print('proxy file empty -> continue without proxies')

with open("files/config.json", "r") as config_file:
    read_config = json.load(config_file)
sms_api_key = read_config["sms_api_key"]
webhook_url = read_config["webhook_url"]

system('title Instagram Gen |-| made by @devlenni -> devlenni#5659')

HEADER = """


                        ____           __                                      ______         
                       /  _/___  _____/ /_____ _____ __________ _____ ___     / ____/__  ____ 
                       / // __ \/ ___/ __/ __ `/ __ `/ ___/ __ `/ __ `__ \   / / __/ _ \/ __ \ 
                     _/ // / / (__  ) /_/ /_/ / /_/ / /  / /_/ / / / / / /  / /_/ /  __/ / / /
                    /___/_/ /_/____/\__/\__,_/\__, /_/   \__,_/_/ /_/ /_/   \____/\___/_/ /_/ 
                                             /____/                                           






"""
print(Fore.MAGENTA, HEADER, Style.RESET_ALL)

print('how many accounts?')
ts = int(input('>>> '))
threadlist = []
for i in range(ts):
    i = str(i).replace(" ", "")
    t = threading.Thread(target=lambda h=i:instagen(str(h), sms_api_key=sms_api_key, country_code="", webhook=webhook_url))
    threadlist.append(t)
    status('Starting generation...', i)
    t.start()
    time.sleep(0.3)

#wait till all tasks finished
for thread in threadlist:
    thread.join()

input("press enter to exit...")
