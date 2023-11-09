# Cary Fenwick
# StegEncoder.py
# 11/9/2023
# Insert encrypted message into an image


# pip install cryptography
# pip install PIL
from PIL import Image 
from cryptography.fernet import Fernet
import sys
import hashlib
from base64 import urlsafe_b64encode


def get_bin(string):
    # Convert message to binary for encoding.
    bin_list = []
    if isinstance (string, str):
        for character in string:
            bin_list.append(format(ord(character), '08b'))
        return bin_list
    if isinstance (string, int):
        return format(string, '08b')

def encrypter(plaintext, password):
    # Generate hash from password, convert to string
    hash = hashlib.md5(password.encode()).hexdigest()
    # Fernet key must be 32 bytes and urlsafe base 64 encoded
    key = urlsafe_b64encode(hash.encode())
    token = Fernet(key)
    ciphertext = token.encrypt(plaintext.encode())
    #print(ciphertext)
    return ciphertext.decode()

def encoder(image, message, password):
    encrypt_msg = encrypter(message, password)
    bin_msg_list = get_bin(encrypt_msg)
    bin_flag_list = ['11100010', '10010000', '10000100']
    encode_msg = ''

    for item in bin_msg_list:
         encode_msg = encode_msg + item
    for item in bin_flag_list:
         encode_msg = encode_msg + item
    image = Image.open(image, 'r')
    width, height = image.size
    # Warn user if image is too small to fit the message.
    if width * height < (len(encrypt_msg) + 5):
        print("WARNING: IMAGE HAS " + str(width * height) + "PIXELS. IMAGE MUST HAVE AT LEAST " + str((len(encrypt_msg) + 5)) + " PIXELS.")
        sys.exit()
    i = 0
    for x in range(0, width):
        for y in range(0, height):
            # Extract pixel color values
            pixel = list(image.getpixel((x, y)))
            r, g, b = pixel
            r = get_bin(r)
            g = get_bin(g)
            b = get_bin(b)
            # Encodes three bits per color value. Looks awful, but it works.
            if i < len(encode_msg):
                r = r[:-3] + encode_msg[i]
                i += 1
            if i < len(encode_msg):
                r += encode_msg[i]
                i += 1
            if i < len(encode_msg):
                r += encode_msg[i]
                i += 1
            if len(r) < 8:
                r += '0'*(8-len(r))
            pixel[0] = int(r, 2)
            if i < len(encode_msg):
                g = g[:-3] + encode_msg[i]
                i += 1
            if i < len(encode_msg):
                g += encode_msg[i]
                i += 1
            if i < len(encode_msg):
                g += encode_msg[i]
                i += 1
            if len(g) < 8:
                g += '0'*(8-len(g))
            pixel[1] = int(g, 2)
            if i < len(encode_msg):
                b = b[:-3] + encode_msg[i]
                i += 1
            if i < len(encode_msg):
                b += encode_msg[i]
                i += 1
            if i < len(encode_msg):
                b += encode_msg[i]
                i += 1
            if len(b) < 8:
                b += '0'*(8-len(b))
            pixel[2] = int(b, 2)
            """for n in range(0,3):
                if(i < len(encode_msg)):
                    
                    pixel[n] = pixel[n] & ~1 | int(encode_msg[i])
                    
                    # ~1 is bitwise not, this passes the first 7 bits in the byte
                    # I is bitwise or
                    i+=1"""
            image.putpixel((x,y), tuple(pixel))
    # Enter filename to save as. Must save as .png. PIL only works with .png.
    savename = input("Save as: (include .png) ")
    image.save(savename, "PNG")
    

def main():
    try:
        filename = input('What image to use? (Include file path and extension): ')
        Image.open(filename)
    # Shut down program if nonexistent or wrong file entered.
    except FileNotFoundError:
        print('Image not found')
        sys.exit()
    except:
        print("Wrong image type or not an image.")
        sys.exit()
    message = input('What message to encode? : ')
    password = input('Enter a password: ')
    encoder(filename, message, password)
    print('Encoding complete!')

if __name__ == '__main__':
    main()

