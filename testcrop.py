from PIL import Image 
a = -1
imgsize = 32
for i in range(9):    
    for k in range(8):
        a+=1
        im = Image.open('The_Abomination.sprites/tuxfire.png')
        im = im.crop((k*imgsize,i*imgsize,256,288))
        im = im.crop( (0,0 , imgsize, imgsize) ) # previously, image was 826 pixels wide, cropping to 825 pixels wide
        im.save("The_Abomination.sprites/"+str(a)+".png") # saves the image
  # opens the imagefrom PIL import Image # import pillow library (can install with "pip install pillow")
#
#from PIL import Image # import pillow library (can install with "pip install pillow")
#a = 2
#im = Image.open('test gui/GUI/16x16_ultim6_GUI_item010618-1.png')
#im = im.crop((170,93,528,448))
#im = im.crop( (0,0 , 105, 150) ) # previously, image was 826 pixels wide, cropping to 825 pixels wide
#im.save("test gui/GUI/Maps/"+str(a)+".gif") # saves the image

# im.show() # opens the imagefrom PIL import Image # import pillow library (can install with "p





# from PIL import Image
# a = -1
# for i in range(73):
#     a += 1
#     im = Image.open("Particles/Fire/"+str(a)+".png")
#     im = im.resize((64,64))
#     im.save("Particles/Fire/"+str(a)+".png")