import random
chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
for n in range(1):
    password =''
    for i in range(8):
        password += random.choice(chars)
    print(password)