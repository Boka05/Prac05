# pip install adafruit-circuitpython-pn532

import board
from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_B
from adafruit_pn532.i2c import PN532_I2C

ADDR = 0x24

i2c = board.I2C()
pn532 = PN532_I2C(i2c, ADDR)

ic, ver, rev, support = pn532.firmware_version
print(f"Found PN532 with firmware version: {ver}.{rev}")

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

print("Waiting for RFID/NFC card to write to!")

key = b"\xFF\xFF\xFF\xFF\xFF\xFF"

while True:
    #Check if a card is available to read
    uid = pn532.read_passive_target(timeout=0.5)
    print(".", end='')
    # Try again if no card is available
    if uid is not None:
        break
    
print()
print("Found card with UID: ", [hex(i) for i in uid])
print("Authenticating block 4...")

authenticated = pn532.mifare_classic_authenticate_block(uid, 4, MIFARE_CMD_AUTH_B, key)
if not authenticated:
    print("Authentication failed!")
    
# Set 16 bytes of block to 0xFEEDBEEF
data = bytearray(16)
data[0:16] = b"\xFE\xED\xBE\xEF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

# Write 16 byte block.
pn532.mifare_classic_write_block(4, data)

# Read block #6
mifare_block = pn532.mifare_classic_read_block(4)
if mifare_block is not None:
    print("Wrote to block 4, now trying to read that data: ",[hex(x) for x in mifare_block])

else:
    print("Read failed - did you remove the card?")