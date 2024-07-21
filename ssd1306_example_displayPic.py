import smbus2
import time

# Define some device parameters
I2C_ADDR = 0x3C  # I2C address of the SSD1306
WIDTH = 128
HEIGHT = 64
PAGES = HEIGHT // 8

# Define some SSD1306 command constants
SSD1306_CMD_DISPLAY_OFF = 0xAE
SSD1306_CMD_DISPLAY_ON = 0xAF
SSD1306_CMD_SET_DISPLAY_CLOCK_DIV = 0xD5
SSD1306_CMD_SET_MULTIPLEX = 0xA8
SSD1306_CMD_SET_DISPLAY_OFFSET = 0xD3
SSD1306_CMD_SET_START_LINE = 0x00
SSD1306_CMD_CHARGE_PUMP = 0x8D
SSD1306_CMD_MEMORY_MODE = 0x20
SSD1306_CMD_SEG_REMAP = 0xA1
SSD1306_CMD_COM_SCAN_DEC = 0xC8
SSD1306_CMD_SET_COM_PINS = 0xDA
SSD1306_CMD_SET_CONTRAST = 0x81
SSD1306_CMD_SET_PRECHARGE = 0xD9
SSD1306_CMD_SET_VCOM_DETECT = 0xDB
SSD1306_CMD_DISPLAY_ALL_ON_RESUME = 0xA4
SSD1306_CMD_NORMAL_DISPLAY = 0xA6

# Initialize I2C (SMBus)
bus = smbus2.SMBus(1)

def ssd1306_command(cmd):
    # Send command to the OLED display
    bus.write_byte_data(I2C_ADDR, 0x00, cmd)

def ssd1306_data(data):
    # Send data to the OLED display
    bus.write_byte_data(I2C_ADDR, 0x40, data)

def ssd1306_init():
    # Initialize the OLED display
    ssd1306_command(SSD1306_CMD_DISPLAY_OFF)
    ssd1306_command(SSD1306_CMD_SET_DISPLAY_CLOCK_DIV)
    ssd1306_command(0x80)
    ssd1306_command(SSD1306_CMD_SET_MULTIPLEX)
    ssd1306_command(HEIGHT - 1)
    ssd1306_command(SSD1306_CMD_SET_DISPLAY_OFFSET)
    ssd1306_command(0x00)
    ssd1306_command(SSD1306_CMD_SET_START_LINE | 0x00)
    ssd1306_command(SSD1306_CMD_CHARGE_PUMP)
    ssd1306_command(0x14)
    ssd1306_command(SSD1306_CMD_MEMORY_MODE)
    ssd1306_command(0x00)
    ssd1306_command(SSD1306_CMD_SEG_REMAP | 0x01)
    ssd1306_command(SSD1306_CMD_COM_SCAN_DEC)
    ssd1306_command(SSD1306_CMD_SET_COM_PINS)
    ssd1306_command(0x12)
    ssd1306_command(SSD1306_CMD_SET_CONTRAST)
    ssd1306_command(0xCF)
    ssd1306_command(SSD1306_CMD_SET_PRECHARGE)
    ssd1306_command(0xF1)
    ssd1306_command(SSD1306_CMD_SET_VCOM_DETECT)
    ssd1306_command(0x40)
    ssd1306_command(SSD1306_CMD_DISPLAY_ALL_ON_RESUME)
    ssd1306_command(SSD1306_CMD_NORMAL_DISPLAY)
    ssd1306_command(SSD1306_CMD_DISPLAY_ON)

def ssd1306_clear():
    # Clear the display
    for page in range(PAGES):
        ssd1306_command(0xB0 + page)
        ssd1306_command(0x00)
        ssd1306_command(0x10)
        for _ in range(WIDTH):
            ssd1306_data(0x00)

def ssd1306_display_bitmap(bitmap):
    for page in range(PAGES):
        ssd1306_command(0xB0 + page)
        ssd1306_command(0x00)
        ssd1306_command(0x10)
        for i in range(WIDTH):
            ssd1306_data(bitmap[page * WIDTH + i])

import cv2
import numpy as np

def resize_and_convert_to_bitmap(image_path):
    # Load image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Resize image to 128x64
    resized_img = cv2.resize(img, (128, 64), interpolation=cv2.INTER_AREA)

    # Convert to binary (black and white)
    _, binary_img = cv2.threshold(resized_img, 128, 255, cv2.THRESH_BINARY)

    # Create a bitmap (1-bit per pixel)
    bitmap = []
    for y in range(0, 64, 8):
        for x in range(128):
            byte = 0
            for bit in range(8):
                if binary_img[y + bit, x] == 255:
                    byte |= (1 << bit)
            bitmap.append(byte)
    
    return bitmap
def main():
    # Initialize the display
    ssd1306_init()
    # Clear the display
    ssd1306_clear()
    
    # Load and display the bitmap
    bitmap = resize_and_convert_to_bitmap('raspilogo')
    ssd1306_display_bitmap(bitmap)

if __name__ == "__main__":
    main()
