import time
import numpy
import sys
import argparse
import threading

#cad = threading.Lock()
pixels_list = []


def Message_to_Binary(message):  # convert all type of data to binary
    if type(message) == str:
        return ''.join([format(ord(i), "08b") for i in message])
    elif type(message) == bytes or type(message) == numpy.ndarray:
        return [format(ord(i), "08b") for i in message]
    elif type(message) == int or type(message) == numpy.uint8:
        return format(message, "08b")
    else:
        raise TypeError("Input type not supported")


def Eliminate_return_line(document):
    for i in range(document.count(b"\n#")):
        first_commentary = document.find(b"\n#")
        last_commentary = document.find(b"\n#", first_commentary + 1)
        document = document.replace(document[first_commentary:last_commentary], b"")
    return (document)


def Get_pixels_list(document):
    global pixels_list
    header = document[:15].decode()  # decode the first 15 character of the document
    header = header.replace("P6", "P3")  # get the magic number P3
    return (header)


def Set_up_binary_list(binary):  # Function that give each byte
    binarylist = []
    i = 0
    for value in binary:
        if i != 0:
            tmplist = tmplist + str(value)
        else:
            tmplist = str(value)
        i += 1
    for value in tmplist:
        tmp = str(value)
        binarylist.append(tmp)
    return binarylist


def Modif_red_pixels(base, list):
    global pixels_list

    beginning = (3 * (int(args.offset) - 1))  # set up the first position
    ending = beginning + len(list) * (int(args.interleave) * 3)  # set up the last position
    step = int(args.interleave) * 9  # set up the steps

    for p in range(beginning, ending, step):
        #cad.acquire()
        passing = 0
        if pixels_list[p] % 2 == 0 and list[base] == 0 and passing != 1:
            passing += 1
            pass
        elif pixels_list[p] % 2 == 0 and list[base] == 1 and passing != 1:
            passing += 1
            pixels_list[p] = pixels_list[p] - 1
            pass
        elif pixels_list[p] % 2 == 1 and list[base] == 0 and passing != 1:
            passing += 1
            pixels_list[p] = pixels_list[p] - 1
            pass
        elif pixels_list[p] % 2 == 1 and list[base] == 1 and passing != 1:
            passing += 1
            pass
        #cad.release()
    base += 3


def Modif_green_pixels(base, list):
    global pixels_list

    beginning = (3 * (int(args.offset)) + 1)
    ending = beginning + len(list) * (int(args.interleave) * 3)
    step = int(args.interleave) * 9
    if len(list) % 3 == 1:
        ending = ending - step

    for p in range(beginning, ending, step):
        #cad.acquire()
        passing = 0
        if pixels_list[p] % 2 == 0 and list[base] == 0 and passing != 1:
            passing += 1
            pass
        elif pixels_list[p] % 2 == 0 and list[base] == 1 and passing != 1:
            passing += 1
            pixels_list[p] = pixels_list[p] - 1
            pass
        elif pixels_list[p] % 2 == 1 and list[base] == 0 and passing != 1:
            passing += 1
            pixels_list[p] = pixels_list[p] - 1
            pass
        elif pixels_list[p] % 2 == 1 and list[base] == 1 and passing != 1:
            passing += 1
            pass
        #cad.release()
    base += 3


def Modif_blue_pixels(base, list):
    global pixels_list

    beginning = (3 * (int(args.offset) + 1) + 2)
    ending = beginning + len(list) * (int(args.interleave) * 3)
    step = int(args.interleave) * 9
    if len(list) % 3 == 1:
        ending = ending - step
    elif len(list) % 3 == 2:
        ending = ending - step

    for p in range(beginning, ending, step):
        #cad.acquire()
        passing = 0
        if pixels_list[p] % 2 == 0 and list[base] == 0 and passing != 1:
            passing += 1
            pass
        elif pixels_list[p] % 2 == 0 and list[base] == 1 and passing != 1:
            passing += 1
            pixels_list[p] = pixels_list[p] - 1
            pass
        elif pixels_list[p] % 2 == 1 and list[base] == 0 and passing != 1:
            passing += 1
            pixels_list[p] = pixels_list[p] - 1
            pass
        elif pixels_list[p] % 2 == 1 and list[base] == 1 and passing != 1:
            passing += 1
            pass
        #cad.release()
    base += 3


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Staganography program")
    parser.add_argument("-p", "--offset", default="0", type=str, help="First pixel to be change")
    parser.add_argument("-i", "--interleave", default="1", type=str, help="Frequency of pixels change")
    parser.add_argument("-s", "--size", default=3, type=int, help="Reading bloc")
    parser.add_argument("-f", "--file", default="dog.ppm", type=str, help="Image file")
    parser.add_argument("-m", "--message", default="message.txt", type=str, help="Message file")
    parser.add_argument("-o", "--output", default="stegano.ppm", type=str, help="Output file")
    args = parser.parse_args()

    if int(args.offset) < 0:
        print("This value can't be negative")
        sys.exit()
    elif int(args.interleave) <= 0:
        print("This value must be positive")
        sys.exit()
    elif args.size <= 0 or args.size % 3 != 0:
        print("Error with the size : it must be positive and a multiple of 3")

    try:
        image_doc = open(args.file, "rb")
    except FileNotFoundError:
        print("The document is not in the folder")
        sys.exit()

    mes = open(args.message, "r")  # open the message file and put it in a list
    letters = mes.read()
    mes.close()
    message_list = []
    for x in letters:
        binary = Message_to_Binary(x)
        message_list.append(binary)
    bina = Set_up_binary_list(message_list)

    #print(bina)
    image_doc = open(args.file, "rb")  # open image
    image = image_doc.read(1024)
    header = Get_pixels_list(Eliminate_return_line(image))  # get the header
    #print(header)
    first_commentary = image.find(b"\n#")  # see where are the pixels in the image
    last_commentary = image.find(b"\n#", first_commentary + 1)
    beginning_body = len(header) + (last_commentary - first_commentary)
    image_doc.seek(beginning_body)  # go to the offset position
    reading = image_doc.read()
    pixels_list = [x for x in reading]  # put the elements in the list
    #print(pixels_list)

    L_TOTAL = len(bina)  # message size
    number_pixels = len(pixels_list)  # size of pixels list
    if L_TOTAL * 8 * int(args.interleave) > number_pixels:  # see if the image got enought pixels for the message
        print("The image do not have enough pixels for that message. Please select another message or image")
        sys.exit()

    red_thread = threading.Thread(target=Modif_red_pixels, args=(0, bina))  # set up the threads
    green_thread = threading.Thread(target=Modif_blue_pixels, args=(1, bina))
    blue_thread = threading.Thread(target=Modif_green_pixels, args=(2, bina))

    time.sleep(1)  # start and join the threads
    red_thread.start()
    time.sleep(1)
    green_thread.start()
    time.sleep(1)
    blue_thread.start()

    red_thread.join()
    green_thread.join()
    blue_thread.join()

    final_doc = open(args.output, "w")  # open the document to write the header in it
    final_doc.write(header + "\n")
    final_doc.close()
    final_doc = open(args.output, "a")  # open the document to append
    final_doc.write("#UMCOMPU2 " + args.offset + " " + args.interleave + " " + str(len(message_list)) + "\n")
    final_doc.write(" ".join([str(x) for x in pixels_list]))
    final_doc.close()
