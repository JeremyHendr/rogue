# from PIL import Image # import pillow library (can install with "pip install pillow")
# a = -1
# for i in range(10):    
#     for k in range(10):
#         a+=1
#         im = Image.open('Orc.sprites/orc spritesheet calciumtrice.png')
#         im = im.crop((k*32,i*32,320,320))
#         im = im.crop( (0,0 , 32, 32) ) # previously, image was 826 pixels wide, cropping to 825 pixels wide
#         im.save("Orc.sprites/"+str(a)+".png") # saves the image
#  # opens the imagefrom PIL import Image # import pillow library (can install with "pip install pillow")

from PIL import Image # import pillow library (can install with "pip install pillow")
a = 2
im = Image.open('test gui/GUI/16x16_ultim6_GUI_item010618-1.png')
im = im.crop((170,93,528,448))
im = im.crop( (0,0 , 105, 150) ) # previously, image was 826 pixels wide, cropping to 825 pixels wide
im.save("test gui/GUI/Maps/"+str(a)+".gif") # saves the image

# im.show() # opens the imagefrom PIL import Image # import pillow library (can install with "p




