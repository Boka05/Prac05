import time
# pip install adafruit-circuitpython-fingerprint
import adafruit_fingerprint as fp
import serial


# import board
# uart = busio.UART(board.TX, board.RX, baudrate=57600)

# If using with a computer such as Linux/RaspberryPi, Mac, Windows with USB/serial converter:
uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)

# If using with Linux/Raspberry Pi and hardware UART:
# uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)

sensor = fp.Adafruit_Fingerprint(uart)


def get_fingerprint():
    """Get a finger print image, template it, and see if it matches!"""
    print("Waiting for image...")
    while sensor.get_image() != fp.OK:
        pass
    print("Templating...")
    if sensor.image_2_tz(1) != fp.OK:
        return False
    print("Searching...")
    if sensor.finger_search() != fp.OK:
        return False
    return True


# pylint: disable=too-many-branches
def get_fingerprint_detail():
    """Get a finger print image, template it, and see if it matches!
    This time, print out each error instead of just returning on failure"""
    print("Getting image...", end="")
    i = sensor.get_image()
    if i == fp.OK:
        print("Image taken")
    else:
        if i == fp.NOFINGER:
            print("No finger detected")
        elif i == fp.IMAGEFAIL:
            print("Imaging error")
        else:
            print("Other error")
        return False
    print("Templating...", end="")
    i = sensor.image_2_tz(1)
    if i == fp.OK:
        print("Templated")
    else:
        if i == fp.IMAGEMESS:
            print("Image too messy")
        elif i == fp.FEATUREFAIL:
            print("Could not identify features")
        elif i == fp.INVALIDIMAGE:
            print("Image invalid")
        else:
            print("Other error")
        return False
    print("Searching...", end="")
    i = sensor.finger_fast_search()
    # pylint: disable=no-else-return
    # This block needs to be refactored when it can be tested.
    if i == fp.OK:
        print("Found fingerprint!")
        return True
    else:
        if i == fp.NOTFOUND:
            print("No match found")
        else:
            print("Other error")
        return False


# pylint: disable=too-many-statements
def enroll_finger(location):
    """Take a 2 finger images and template it, then store in 'location'"""
    for fingerimg in range(1, 3):
        if fingerimg == 1:
            print("Place finger on sensor...", end="")
        else:
            print("Place same finger again...", end="")

        while True:
            i = sensor.get_image()
            if i == fp.OK:
                print("Image taken")
                break
            if i == fp.NOFINGER:
                print(".", end="")
            elif i == fp.IMAGEFAIL:
                print("Imaging error")
                return False
            else:
                print("Other error")
                return False

        print("Templating...", end="")
        i = sensor.image_2_tz(fingerimg)
        if i == fp.OK:
            print("Templated")
        else:
            if i == fp.IMAGEMESS:
                print("Image too messy")
            elif i == fp.FEATUREFAIL:
                print("Could not identify features")
            elif i == fp.INVALIDIMAGE:
                print("Image invalid")
            else:
                print("Other error")
            return False

        if fingerimg == 1:
            print("Remove finger")
            time.sleep(1)
            while i != fp.NOFINGER:
                i = sensor.get_image()

    print("Creating model...", end="")
    i = sensor.create_model()
    if i == fp.OK:
        print("Created")
    else:
        if i == fp.ENROLLMISMATCH:
            print("Prints did not match")
        else:
            print("Other error")
        return False

    print("Storing model #%d..." % location, end="")
    i = sensor.store_model(location)
    if i == fp.OK:
        print("Stored")
    else:
        if i == fp.BADLOCATION:
            print("Bad storage location")
        elif i == fp.FLASHERR:
            print("Flash storage error")
        else:
            print("Other error")
        return False

    return True


def save_fingerprint_image(filename):
    """Scan fingerprint then save image to filename."""
    while sensor.get_image():
        pass

    # let PIL take care of the image headers and file structure
    from PIL import Image  # pylint: disable=import-outside-toplevel

    img = Image.new("L", (256, 288), "white")
    pixeldata = img.load()
    mask = 0b00001111
    result = sensor.get_fpdata(sensorbuffer="image")

    # this block "unpacks" the data received from the fingerprint
    #   module then copies the image data to the image placeholder "img"
    #   pixel by pixel.  please refer to section 4.2.1 of the manual for
    #   more details.  thanks to Bastian Raschke and Danylo Esterman.
    # pylint: disable=invalid-name
    x = 0
    # pylint: disable=invalid-name
    y = 0
    # pylint: disable=consider-using-enumerate
    for i in range(len(result)):
        pixeldata[x, y] = (int(result[i]) >> 4) * 17
        x += 1
        pixeldata[x, y] = (int(result[i]) & mask) * 17
        if x == 255:
            x = 0
            y += 1
        else:
            x += 1

    if not img.save(filename):
        return True
    return False


##################################################


def get_num(max_number):
    """Use input() to get a valid number from 0 to the maximum size
    of the library. Retry till success!"""
    i = -1
    while (i > max_number - 1) or (i < 0):
        try:
            i = int(input("Enter ID # from 0-{}: ".format(max_number - 1)))
        except ValueError:
            pass
    return i


while True:
    print("----------------")
    if sensor.read_templates() != fp.OK:
        raise RuntimeError("Failed to read templates")
    print("Fingerprint templates: ", sensor.templates)
    if sensor.count_templates() != fp.OK:
        raise RuntimeError("Failed to read templates")
    print("Number of templates found: ", sensor.template_count)
    if sensor.read_sysparam() != fp.OK:
        raise RuntimeError("Failed to get system parameters")
    print("Size of template library: ", sensor.library_size)
    print("e) enroll print")
    print("f) find print")
    print("d) delete print")
    print("s) save fingerprint image")
    print("r) reset library")
    print("q) quit")
    print("----------------")
    c = input("> ")

    if c == "e":
        enroll_finger(get_num(sensor.library_size))
    if c == "f":
        if get_fingerprint():
            print("Detected #", sensor.finger_id, "with confidence", sensor.confidence)
        else:
            print("Finger not found")
    if c == "d":
        if sensor.delete_model(get_num(sensor.library_size)) == fp.OK:
            print("Deleted!")
        else:
            print("Failed to delete")
    if c == "s":
        if save_fingerprint_image("fingerprint.png"):
            print("Fingerprint image saved")
        else:
            print("Failed to save fingerprint image")
    if c == "r":
        if sensor.empty_library() == fp.OK:
            print("Library empty!")
        else:
            print("Failed to empty library")
    if c == "q":
        print("Exiting fingerprint example program")
        raise SystemExit
