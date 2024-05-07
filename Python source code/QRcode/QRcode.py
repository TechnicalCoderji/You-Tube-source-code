import qrcode
from PIL import Image

message = input("enter your data:")
code = qrcode.make(message)
code.save("coderji.png")
QR = Image.open("coderji.png")
QR.show()