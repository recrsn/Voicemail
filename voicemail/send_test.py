import os
from .send import generate_fuzzy_match_clients, create_message

files = os.listdir('/home/megha/Documents')

print(generate_fuzzy_match_clients(files))

print(create_message('me', 'amitosh.swain@gmail.com', 'Hello World', 'Hello World', ['/home/megha/Documents/cloud.odt']))