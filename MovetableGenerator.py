# generates a 320x256 movetable with interleaved UV coordinates encoded in 16 bit unsigned shorts (little endian).

import math

# the table is a bit larger than a GBA screen to be able to move the camera around
XRES = 320
YRES = 256

effect = "sphere"

ofs = open("lut_sphere.c", mode = "w", encoding = "utf-8")
ofs.write("const unsigned short lut_sphere[] = {\n")

for j in range(0, YRES):

    ydist = j - (YRES / 2)

    for i in range(0, XRES):

        xdist = i - (XRES / 2)

        # fixed point
        distance = int(math.sqrt(xdist * xdist + ydist * ydist))
        angle = int(math.atan2(float(xdist), float(ydist)) * 64)

        if distance <= 0:
            distance = 1

        if effect == "polar":
            u = angle
            v = distance

        if effect == "tunnel":
            u = angle
            v = int(32 * 256 / distance) & 0xFF

        if effect == "flower":
            u = angle
            v = distance + int(math.sin(math.atan2(float(xdist), float(ydist)) * 5) * 90)

        if effect == "swirl":
            u = (2 * angle / math.pi) + distance
            v = int(math.pow(float(distance), 1.2))
            
        if effect == "sphere":
            if (xdist == 0): xdist = 1
            if (ydist == 0): ydist = 1
            o = (0.0, 0.0, 0.5)
            aspect = float(XRES) / YRES
            d = (i / XRES * 2 - 1.0, j / YRES / aspect * 2 - 1.0, 0.0)
            c = (d[0] - o[0], d[1] - o[1], d[2] - o[2])
            
            r = c[0] * c[0] + c[1] * c[1] + c[2] * c[2]
            
            theta = math.acos(-c[1] / r) * 1.0
            phi = math.atan2(c[0], -c[2]) * 2.0
            
            u = (2 * int(255 * (0.5 + phi / (math.pi * 2.0)))) & 0xff
            v = (2 * int(255 * (theta / (math.pi * 1.0)))) & 0xff
            
        # GBA supports little endian byte-order
        short = ((int(u) << 8) + v) & 0xFFFF
        ofs.write('{}'.format(short))
        ofs.write(", ")

        if (i & 15) == 0:
            ofs.write("\n")

ofs.write("};")
ofs.close()