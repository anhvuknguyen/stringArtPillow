from PIL import Image, ImageOps, ImageDraw, ImageFont
import math

radius = 750
#Import image
filename = "einstein.png"
img = Image.open(filename).convert("RGBA")

#Resize image
newsize = (2*radius+1,2*radius+1)
img = img.resize(newsize)

#Drawing Board
drawingBoard = Image.new("L", newsize)
board = ImageDraw.Draw(drawingBoard)
board.rectangle([0,0,radius*2+1,radius*2+1],fill=255,outline=None)

#Crop Into Circle
background = Image.new("RGBA", img.size, (0,0,0,0))
mask = Image.new("RGBA", img.size, 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((0,0,2*radius,2*radius), fill='green', outline=None)
new_img = Image.composite(img, background, mask)

#Instance Drawing Board
img1= ImageDraw.Draw(new_img)

#Draw Pins
pin = []
pinCount = 300
def drawPin(radius):
    r = radius
    for i in range(pinCount):
        angle = math.radians(0 + (360/pinCount)*i)
        img1.point((r * math.cos(angle)+r,-r * math.sin(angle)+r), fill=255)
        pin.append((r * math.cos(angle)+r,-r * math.sin(angle)+r))

#Draw Line
def drawLine(point1,point2):
    if (point1[0]<point2[0]):
        x1, y1 = point1
        x2, y2 = point2
    else:
        x1, y1 = point2
        x2, y2 = point1
    if (x1==x2):
        k=1
    else:
        k = ((y2-y1)/(x2-x1))
    if (abs(k)>=1):
        if (y1<y2):
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        else:
            temp = x1, y1
            x1, y1 = y2, x2
            y2, x2, = temp
        k = ((y2-y1)/(x2-x1))
        b = (y1-(x1*k))
        for i in range(round(x2-x1)):
            x = x1+i
            img1.point((x*k+b,x), fill=255)
    else:
        b = (y1-(x1*k))

        for i in range(round(x2-x1)):
            x = x1+i
            img1.point((x,x*k+b), fill=255)

def boardLine(point1,point2):
    if (point1[0]<point2[0]):
        x1, y1 = point1
        x2, y2 = point2
    else:
        x1, y1 = point2
        x2, y2 = point1
    if (x1==x2):
        k=1
    else:
        k = ((y2-y1)/(x2-x1))
    if (abs(k)>=1):
        if (y1<y2):
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        else:
            temp = x1, y1
            x1, y1 = y2, x2
            y2, x2, = temp
        k = ((y2-y1)/(x2-x1))
        b = (y1-(x1*k))
        for i in range(round(x2-x1)):
            x = x1+i
            board.point((x*k+b,x), fill=0)
    else:
        b = (y1-(x1*k))

        for i in range(round(x2-x1)):
            x = x1+i
            board.point((x,x*k+b), fill=0)

highestAvgDarkness = 255
darkestCoord = dx, dy = 0,0
a=0
#Find Darkness Value
def findDarkness(point1,point2):
    darkness=0
    if (point1[0]<point2[0]):
        x1, y1 = point1
        x2, y2 = point2
    else:
        x1, y1 = point2
        x2, y2 = point1
    if (x1==x2):
        k=1
    else:
        k = ((y2-y1)/(x2-x1))
    if (abs(k)>=1):
        if (y1<y2):
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        else:
            temp = x1, y1
            x1, y1 = y2, x2
            y2, x2, = temp
        k = ((y2-y1)/(x2-x1))
        b = (y1-(x1*k))
        for i in range(round(x2-x1)):
            x = x1+i
            xy = x*k+b,x
            darkness += new_img.getpixel(xy)
            ##img1.point((x*k+b,x), fill=255)
    else:
        b = (y1-(x1*k))

        for i in range(round(x2-x1)):
            x = x1+i
            xy = x,x*k+b
            darkness += new_img.getpixel(xy)
            ##img1.point((x,x*k+b), fill=255)
    darkness = darkness / round(x2-x1)
    return darkness

##Start Program
drawPin(radius)

#Grayscale Image and reset Drawing Board
new_img = ImageOps.grayscale(new_img)
img1= ImageDraw.Draw(new_img)
img1.ellipse((0,0,radius*2, radius*2),outline=0)

currentPin=pin[0]
restrictMin = 40
restrictMax = len(pin)-restrictMin

#Open Coord File
file = open("coord.txt","w")
file.close

for x in range(3000):
    file = open("coord.txt","a")
    file.write(str(x)+ ". "+str(pin.index(currentPin))+",\n")
    file.close
    highestAvgDarkness = 255
    for i in pin:
        darkness = 0
        if (pin.index(currentPin)<=restrictMin):
            rangeMin = pin.index(currentPin) + restrictMin
            rangeMax = restrictMax + pin.index(currentPin)
            if (pin.index(i)<=rangeMin or pin.index(i)>=rangeMax):
                continue
            else:
                darkness = findDarkness(currentPin,i)
        elif (pin.index(currentPin)>restrictMax):
            rangeMin = -1*restrictMax + pin.index(currentPin)
            rangeMax = pin.index(currentPin) - restrictMin
            if (pin.index(i)<=rangeMin or pin.index(i)>=rangeMax):
                continue
            else:
                darkness = findDarkness(currentPin,i)
        else:
            rangeMin = pin.index(currentPin)+restrictMin
            rangeMax = pin.index(currentPin)-restrictMin
            if (pin.index(i)<=rangeMin and pin.index(i)>=rangeMax):
                continue
            else:
                darkness = findDarkness(currentPin,i)
        if (darkness<highestAvgDarkness):
            highestAvgDarkness=darkness
            darkestCoord=i
    drawLine(currentPin,darkestCoord)
    boardLine(currentPin,darkestCoord)
    currentPin=darkestCoord
new_img.show()
drawingBoard.show()