import requests
import sys
from bs4 import BeautifulSoup
import re

def get_body_text(url):
    response = requests.get(url)
    s=BeautifulSoup(response.text,'lxml')
    if s.body:
        return s.body.get_text()
    else:
        return ""


def word_freq(body_txt):
    words = re.findall(r'\b[a-zA-Z]+\b', body_txt.lower())
    body_word_freq = {}
    for word in words:
        if word in body_word_freq:
            body_word_freq[word] += 1
        else:
            body_word_freq[word] = 1
    return body_word_freq


def polynomial_hash(word):
    p = 53
    m = 2**64          
    hash_value = 0
    power = 1        
    for character in word:
        ascii_val = ord(character)     
        hash_value = (hash_value + ascii_val * power) % m
        power = (power * p) % m

    return hash_value


def calculate_simhash(body_freq_dict):
    vector = [0]* 64
    for word, count in body_freq_dict.items():
        h=polynomial_hash(word)

        for i in range(64):
            bit = (h >> i) & 1

            if bit == 1:
                vector[i] += count
            else:
                vector[i] -= count
    val = 0

    for i in range(64):
        if vector[i] > 0:
            val |= (1 << i)

    binary_output = format(val, '064b')

    return binary_output


def find_common_bits(h1, h2):
    h1 = int(h1, 2)  
    h2 = int(h2, 2)

    x = ~(h1 ^ h2) & ((1 << 64) - 1)

    count = 0
    while x:
        count += x & 1
        x >>= 1

    return count


if len(sys.argv) != 3:
    print("Please enter: python simhash_project.py <url1> <url2>")
   

url1 = sys.argv[1]
url2 = sys.argv[2]

text1 = get_body_text(url1)
text2 = get_body_text(url2)

freq1 = word_freq(text1)
freq2 = word_freq(text2)

val1 = calculate_simhash(freq1)
val2 = calculate_simhash(freq2)

print("\nSimhash 1:", val1)
print("Simhash 2:", val2)

common = find_common_bits(val1, val2)

print("\nCommon bits in simhashes:", common)


        
    




