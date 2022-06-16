from PIL import Image 
starting_pic = 0
last_pic = 80
counter = -1
folder = "Assets/Inv sprites/"
while starting_pic+counter < last_pic:
    counter+=1
    im = Image.open(folder+str(starting_pic+counter)+'.gif~Updated upstream')
    im.save(folder+str(counter)+'.png')