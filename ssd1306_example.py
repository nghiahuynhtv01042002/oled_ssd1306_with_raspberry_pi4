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

#Basic font definition (5x7)
font = [
    [0x00, 0x00, 0x00, 0x00, 0x00],  # Space
    [0x00, 0x00, 0x5F, 0x00, 0x00],  # !
    [0x00, 0x07, 0x00, 0x07, 0x00],  # "
    [0x14, 0x7F, 0x14, 0x7F, 0x14],  # #
    [0x24, 0x2A, 0x7F, 0x2A, 0x12],  # $
    [0x23, 0x13, 0x08, 0x64, 0x62],  # %
    [0x36, 0x49, 0x55, 0x22, 0x50],  # &
    [0x00, 0x05, 0x03, 0x00, 0x00],  # '
    [0x00, 0x1C, 0x22, 0x41, 0x00],  # (
    [0x00, 0x41, 0x22, 0x1C, 0x00],  # )
    [0x14, 0x08, 0x3E, 0x08, 0x14],  # *
    [0x08, 0x08, 0x3E, 0x08, 0x08],  # +
    [0x00, 0x50, 0x30, 0x00, 0x00],  # ,
    [0x08, 0x08, 0x08, 0x08, 0x08],  # -
    [0x00, 0x60, 0x60, 0x00, 0x00],  # .
    [0x20, 0x10, 0x08, 0x04, 0x02],  # /
    [0x3E, 0x51, 0x49, 0x45, 0x3E],  # 0
    [0x00, 0x42, 0x7F, 0x40, 0x00],  # 1
    [0x42, 0x61, 0x51, 0x49, 0x46],  # 2
    [0x21, 0x41, 0x45, 0x4B, 0x31],  # 3
    [0x18, 0x14, 0x12, 0x7F, 0x10],  # 4
    [0x27, 0x45, 0x45, 0x45, 0x39],  # 5
    [0x3C, 0x4A, 0x49, 0x49, 0x30],  # 6
    [0x01, 0x71, 0x09, 0x05, 0x03],  # 7
    [0x36, 0x49, 0x49, 0x49, 0x36],  # 8
    [0x06, 0x49, 0x49, 0x29, 0x1E],  # 9
    [0x00, 0x36, 0x36, 0x00, 0x00],  # :
    [0x00, 0x56, 0x36, 0x00, 0x00],  # ;
    [0x08, 0x14, 0x22, 0x41, 0x00],  # <
    [0x14, 0x14, 0x14, 0x14, 0x14],  # =
    [0x00, 0x41, 0x22, 0x14, 0x08],  # >
    [0x02, 0x01, 0x51, 0x09, 0x06],  # ?
    [0x32, 0x49, 0x79, 0x41, 0x3E],  # @
    [0x7E, 0x11, 0x11, 0x11, 0x7E],  # A
    [0x7F, 0x49, 0x49, 0x49, 0x36],  # B
    [0x3E, 0x41, 0x41, 0x41, 0x22],  # C
    [0x7F, 0x41, 0x41, 0x22, 0x1C],  # D
    [0x7F, 0x49, 0x49, 0x49, 0x41],  # E
    [0x7F, 0x09, 0x09, 0x09, 0x01],  # F
    [0x3E, 0x41, 0x49, 0x49, 0x7A],  # G
    [0x7F, 0x08, 0x08, 0x08, 0x7F],  # H
    [0x00, 0x41, 0x7F, 0x41, 0x00],  # I
    [0x20, 0x40, 0x41, 0x3F, 0x01],  # J
    [0x7F, 0x08, 0x14, 0x22, 0x41],  # K
    [0x7F, 0x40, 0x40, 0x40, 0x40],  # L
    [0x7F, 0x02, 0x0C, 0x02, 0x7F],  # M
    [0x7F, 0x04, 0x08, 0x10, 0x7F],  # N
    [0x3E, 0x41, 0x41, 0x41, 0x3E],  # O
    [0x7F, 0x09, 0x09, 0x09, 0x06],  # P
    [0x3E, 0x41, 0x51, 0x21, 0x5E],  # Q
    [0x7F, 0x09, 0x19, 0x29, 0x46],  # R
    [0x46, 0x49, 0x49, 0x49, 0x31],  # S
    [0x01, 0x01, 0x7F, 0x01, 0x01],  # T
    [0x3F, 0x40, 0x40, 0x40, 0x3F],  # U
    [0x1F, 0x20, 0x40, 0x20, 0x1F],  # V
    [0x3F, 0x40, 0x38, 0x40, 0x3F],  # W
    [0x63, 0x14, 0x08, 0x14, 0x63],  # X
    [0x07, 0x08, 0x70, 0x08, 0x07],  # Y
    [0x61, 0x51, 0x49, 0x45, 0x43],  # Z
    [0x00, 0x7F, 0x41, 0x41, 0x00],  # [
    [0x02, 0x04, 0x08, 0x10, 0x20],  # Backslash
    [0x00, 0x41, 0x41, 0x7F, 0x00],  # ]
    [0x04, 0x02, 0x01, 0x02, 0x04],  # ^
    [0x40, 0x40, 0x40, 0x40, 0x40],  # _
    [0x00, 0x03, 0x05, 0x00, 0x00],  # `
    [0x20, 0x54, 0x54, 0x54, 0x78],  # a
    [0x7F, 0x48, 0x44, 0x44, 0x38],  # b
    [0x38, 0x44, 0x44, 0x44, 0x20],  # c
    [0x38, 0x44, 0x44, 0x48, 0x7F],  # d
    [0x38, 0x54, 0x54, 0x54, 0x18],  # e
    [0x08, 0x7E, 0x09, 0x01, 0x02],  # f
    [0x08, 0x14, 0x54, 0x54, 0x3C],  # g
    [0x7F, 0x08, 0x04, 0x04, 0x78],  # h
    [0x00, 0x44, 0x7D, 0x40, 0x00],  # i
    [0x20, 0x40, 0x44, 0x3D, 0x00],  # j
    [0x7F, 0x10, 0x28, 0x44, 0x00],  # k
    [0x00, 0x41, 0x7F, 0x40, 0x00],  # l
    [0x7C, 0x04, 0x18, 0x04, 0x78],  # m
    [0x7C, 0x08, 0x04, 0x04, 0x78],  # n
    [0x38, 0x44, 0x44, 0x44, 0x38],  # o
    [0x7C, 0x14, 0x14, 0x14, 0x08],  # p
    [0x08, 0x14, 0x14, 0x18, 0x7C],  # q
    [0x7C, 0x08, 0x04, 0x04, 0x08],  # r
    [0x48, 0x54, 0x54, 0x54, 0x20],  # s
    [0x04, 0x3F, 0x44, 0x40, 0x20],  # t
    [0x3C, 0x40, 0x40, 0x20, 0x7C],  # u
    [0x1C, 0x20, 0x40, 0x20, 0x1C],  # v
    [0x3C, 0x40, 0x30, 0x40, 0x3C],  # w
    [0x44, 0x28, 0x10, 0x28, 0x44],  # x
    [0x0C, 0x50, 0x50, 0x50, 0x3C],  # y
    [0x44, 0x64, 0x54, 0x4C, 0x44],  # z
    [0x00, 0x08, 0x36, 0x41, 0x00],  # {
    [0x00, 0x00, 0x7F, 0x00, 0x00],  # |
    [0x00, 0x41, 0x36, 0x08, 0x00],  # }
    [0x08, 0x08, 0x2A, 0x1C, 0x08],  # ->
    [0x08, 0x1C, 0x2A, 0x08, 0x08]   # <-
]
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
            
def ssd1306_set_cursor(x, y):
    # Set the page address (y-coordinate)
    ssd1306_command(0xB0 + (y // 8))  # Assuming y is in pixels and page address is y // 8

    # Set the lower nibble of the column address
    ssd1306_command(0x00 + (x & 0x0F))

    # Set the higher nibble of the column address
    ssd1306_command(0x10 + ((x >> 4) & 0x0F))

def ssd1306_print_char(char):
    if char < 32 or char > 127:
        char = 32  # Replace unsupported characters with space
    for i in range(5):
        ssd1306_data(font[char - 32][i])
    #ssd1306_data(0x00)  # Add space between characters

def ssd1306_print(text):
    for char in text:
        ssd1306_print_char(ord(char))
        
def main():
    # Initialize the display
    ssd1306_init()
    # Clear the display
    ssd1306_clear()
    # Set cursor to (0, 0)
    
    ssd1306_set_cursor(0,0)
    # Print "Hello"
    ssd1306_print("Hello i am TXN")
    ssd1306_set_cursor(0, 8)
    ssd1306_print("i am embedded engineer")
    ssd1306_set_cursor(0, 16)
    ssd1306_print("i study at HMCUT VNU")
    ssd1306_set_cursor(0, 24)
    ssd1306_print("i live at HCM city")
    ssd1306_set_cursor(0, 32)
    ssd1306_print("i am single:<")
    
    
if __name__ == "__main__":
    main()
