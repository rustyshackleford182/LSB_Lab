from PIL import Image

#pip install bitarray 
from bitarray import bitarray

extracted_bin = []
with Image.open("source_secret.png") as img:
    width, height = img.size
    byte = []
    for x in range(0, width):
        for y in range(0, height):
            pixel = list(img.getpixel((x, y)))
            for n in range(0,3):
                byte.append(pixel[n]&1)
                if len(byte) > 24:
                    # Check last 24 bits for end of transmission flag
                    if byte[-24:] == [1,1,1,0,0,0,1,0,1,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0]:
                        for b in byte[0:-24]:
                            extracted_bin.append(b)

                #bitmask and &1 covers last bit, &3 the last 2, etc.
print(byte)
data = "".join([str(x) for x in extracted_bin])

print(str(bitarray(data).tobytes()))


#bitarray(data).tobytes().decode('ascii')


#b'a string'.decode('ascii')
#def bin_to_str(int (data))

# import binascii

# Ascii = binascii.b2a_uu(data)

# def bin_to_str(x):
#     ''' Converts a Binary String to an (ASCII) string'''
#     my_int = my_int = int(data, base=2)
#     my_str = my_int.to_bytes((my_int.bit_length() + 7)//8, 'big').decode()
#     return my_str

# my_int = bin_to_str(data)
# print(my_int)

#print (data)

# find way to trim binary data from output
# add symmetric encryption

# Would be cool to:
# Use large files
# use a key to scatter data
# use asymmetric encryption