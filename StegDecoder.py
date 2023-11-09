# Cary Fenwick
# StegEncoder.py
# 11/9/2023
# Extract and decrypt a message from an image.

# pip install PIL
# pip install cryptography
from PIL import Image
from cryptography.fernet import Fernet
import sys
import hashlib
from base64 import urlsafe_b64encode
from bitarray import bitarray

def get_bin(value):
    return format(value, '08b')


def decrypter(cipher_bin, password):
    # Generate hash from password, convert to string
    hash = hashlib.md5(password.encode()).hexdigest()
    # Ciphertext has a b prepended when extracted. Remove or decryption fails.
    ciphertext = cipher_bin[1:]
    #print(ciphertext)
    # Fernet key must be 32 bytes and urlsafe base 64 encoded
    key = urlsafe_b64encode(hash.encode())
    token = Fernet(key)
    plaintext = token.decrypt(ciphertext.encode())
    return plaintext.decode()

def decoder(filename, password):
    image = Image.open(filename)
    width, height = image.size
    extracted_bin = []
    byte = []
    for x in range(0, width):
        for y in range(0, height):
            # Extract pixel color values
            pixel = list(image.getpixel((x, y)))
            r, g, b = pixel
            r = get_bin(r)
            g = get_bin(g)
            b = get_bin(b)
            # Iterate through the last three bits of each color.
            # If 24 bits have been extracted, check for stop sequence.
            # If stop sequence found, save extracted bits and stop extraction.
            # Check happens after every bit because it fails otherwise.
            # Looks horrible, but works
            if extracted_bin:
                 break
            byte.append(int(r[-3]))
            if len(byte) >= 24:
                if byte[-24:] == [1,1,1,0,0,0,1,0,1,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0]:
                        for b in byte[0:(len(byte)-24)]:
                            extracted_bin.append(b)
            if extracted_bin:
                 break
            byte.append(int(r[-2]))
            if len(byte) >= 24:
                if byte[-24:] == [1,1,1,0,0,0,1,0,1,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0]:
                        for b in byte[0:(len(byte)-24)]:
                            extracted_bin.append(b)
            if extracted_bin:
                 break
            byte.append(int(r[-1]))
            if len(byte) >= 24:
                if byte[-24:] == [1,1,1,0,0,0,1,0,1,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0]:
                        for b in byte[0:(len(byte)-24)]:
                            extracted_bin.append(b)
            if extracted_bin:
                 break
            byte.append(int(g[-3]))
            if len(byte) >= 24:
                if byte[-24:] == [1,1,1,0,0,0,1,0,1,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0]:
                        for b in byte[0:(len(byte)-24)]:
                            extracted_bin.append(b)
            if extracted_bin:
                 break
            byte.append(int(g[-2]))
            if len(byte) >= 24:
                if byte[-24:] == [1,1,1,0,0,0,1,0,1,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0]:
                        for b in byte[0:(len(byte)-24)]:
                            extracted_bin.append(b)
            if extracted_bin:
                 break
            byte.append(int(g[-1]))
            if len(byte) >= 24:
                if byte[-24:] == [1,1,1,0,0,0,1,0,1,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0]:
                        for b in byte[0:(len(byte)-24)]:
                            extracted_bin.append(b)
            if extracted_bin:
                 break
            byte.append(int(b[-3]))
            if len(byte) >= 24:
                if byte[-24:] == [1,1,1,0,0,0,1,0,1,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0]:
                        for b in byte[0:(len(byte)-24)]:
                            extracted_bin.append(b)
            if extracted_bin:
                 break
            byte.append(int(b[-2]))
            if len(byte) >= 24:
                if byte[-24:] == [1,1,1,0,0,0,1,0,1,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0]:
                        for b in byte[0:(len(byte)-24)]:
                            extracted_bin.append(b)
            if extracted_bin:
                 break
            byte.append(int(b[-1]))
            if len(byte) >= 24:
                if byte[-24:] == [1,1,1,0,0,0,1,0,1,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0]:
                        for b in byte[0:(len(byte)-24)]:
                            extracted_bin.append(b)
            if extracted_bin:
                 break
            """for n in range(0,3):
                byte.append(pixel[n]&1)
                if len(byte) > 24:
                    # Check last 24 bits for end of transmission flag
                    if byte[-24:] == [1,1,1,0,0,0,1,0,1,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0]:
                        for b in byte[0:(len(byte)-24)]:
                            extracted_bin.append(b)

                #bitmask and &1 covers last bit, &3 the last 2, etc."""
    
    # Convert extracted data to string for decryption
    data = "".join([str(x) for x in extracted_bin])
    ciphertext = (str(bitarray(data).tobytes()))
    return decrypter(ciphertext, password)

def main():
    try:
        filename = input('What file to decode? (Include file extension): ')
    # Shut down program if nonexistent or wrong file entered.
    except FileNotFoundError:
        print('Image not found')
        sys.exit()
    except:
         print('Wrong image type or not an image.')
         sys.exit()
    password = input('Enter password: ')
    print (decoder(filename, password))

if __name__ == '__main__':
    main()
