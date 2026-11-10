#B5. Ascunzi un mesaj prin LSB
from PIL import Image
img = Image.open("probe/foto.jpg").convert("RGB")
px = list(img.getdata())
mesaj = b"FLAG{ascuns_in_pixeli}\00"
biti = "".join(f"{x:08b}" for x in mesaj)
canale = [c for pixel in px for c in pixel]
for i, bit in enumerate(biti):
    canale[i] = (canale[i] & ~1) | int(bit)

px_nou = [tuple(canale[i:i + 3]) for i in range(0, len(canale), 3)]
img.putdata(px_nou)
img.save("stego.png")
print("mesaj ascuns in stego.png:", len(biti), "biti")

#B6. Dezvalui mesajul inapoi
px = list(Image.open("stego.png").convert("RGB").getdata())
biti = ""
for (r, g, b) in px:
    biti += str(r & 1) + str(g & 1) + str(b & 1)

octeti = bytearray()
for i in range(0, len(biti), 8):
        octet = int(biti[i:i + 8], 2)
        if octet == 0:
                break
        octeti.append(octet)

print("mesaj dezvaluit:",octeti.decode("utf-8", errors = "replace"))
