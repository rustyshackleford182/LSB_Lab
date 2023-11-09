#pip install pillow
from PIL import Image
import re

def getFile():
    try:
        filename = input('What image to use? (Include file path and extension): ')
        encode(filename)
    except FileNotFoundError:
        print('Image not found')

def encode(filename):
    with Image.open(filename) as img:
        width, height = img.size
        message = input('What message to encode? (MAX characters: ' + str((width * height) - 8) + '): ')
        if (len(message) > (width * height)-8):
            print('Message too long')
        else:
            bin_msg = list(map(bin, bytearray(message, 'utf8')))
            
            count = 0
            for i in bin_msg:
                bin_msg[count] =re.sub("b+", "", i)
                count += 1
            # Add end of transmission flag
            bin_msg.append('11100010')
            bin_msg.append('10010000')
            bin_msg.append('10000100')
            i = 0
            encode_msg = ''
            for j in bin_msg:
                encode_msg += j
            for x in range(0, width):
                for y in range(0, height):
                    pixel = list(img.getpixel((x, y)))
                    for n in range(0,3):
                        if(i < len(encode_msg)):
                            
                            pixel[n] = pixel[n] & ~1 | int(encode_msg[i])
                            # ~1 is bitwise not, this passes the first 7 bits in the byte
                            # I is bitwise or
                            i+=1
                    img.putpixel((x,y), tuple(pixel))
            img.save("source_secret.png", "PNG")

            
            

        


if __name__ == '__main__':
    getFile()