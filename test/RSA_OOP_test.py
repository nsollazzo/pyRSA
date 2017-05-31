'''
RSA_OOP_test

@author: Sollazzo Nicholas
@date: March 20th 2017
@version: 1.0
@status: GREEN

'''

from RSA import RSA

rsa = RSA()

print(rsa.dict())

#en = rsa.encrypt(input('>'))

en = rsa.encrypt('das')

print('encrypted:', en)

print('decrypted:', rsa.decrypt(en))
