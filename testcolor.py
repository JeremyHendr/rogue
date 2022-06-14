
from time import sleep
from PIL import Image # import pillow library (can install with "pip install pillow")
a = 1
# for i in range(1):    
    # for k in range(1):
# for i in range(10):
#     a+=1
im = Image.open('64/upg_sword.png')

# im.show() # opens the imfrom PIL import im # import pillow library (can install with "pip install pillow")

#color = np.array([71, 108, 108])

# im_data = im.load()
# height,width = im.size
# print(im_data[0,16])
# for loop1 in range(height):
#     for loop2 in range(width):
#         if im_data[loop1,loop2] == 4:
#                 im_data[loop1,loop2] = 0


im = im.convert("RGBA")
datas = im.getdata()

newData = []
for item in datas:
    
    # if item[3]!=0:
    #     print(item)
    #     sleep(0.1)
    if item[0]>150 and item[1]>150 and item[2]>150 and item[3] !=0:
        newData.append((0, 0, 125, 255))
    else:
        newData.append(item)

im.putdata(newData)

im.save('64/swordfreezeig.png')

