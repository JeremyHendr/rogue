from PIL import Image 
starting_pic = 56
last_pic = 63
counter = -1
folder = "Ice_Spell/SW/"
while starting_pic+counter < last_pic:
    counter+=1
    im = Image.open(folder+str(starting_pic+counter)+'.png')
    im.save(folder+str(counter)+'.png')