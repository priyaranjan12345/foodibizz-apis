import random
import time

def generate_random_number():
    ct = str(time.time()) + str(random.random())
    ct = ct.replace('.', '')
    
    return ct