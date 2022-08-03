import random
chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
for n in range(2):
    password =''
    for i in range(20):
        password += random.choice(chars)
    print(password)