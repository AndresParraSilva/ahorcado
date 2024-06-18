import base64 
import random

with open("media/dictionary.txt", 'r') as input_file, open("media/dictionary_encoded.txt", 'w') as output_file:
    for line in input_file:
        output_file.write(base64.b64encode(line.encode()).decode() + '\n')

print("Done!")
print("")

print("Verification:")
print("")
with open("media/dictionary_encoded.txt", 'r') as file:
    lines = file.readlines()
    for i in range(5):
        line = random.choice(lines)
        print(line, end="")
        print(base64.b64decode(line.encode()).decode())