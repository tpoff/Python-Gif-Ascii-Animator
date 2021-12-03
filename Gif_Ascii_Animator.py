'''
Gif_Ascii_Animator.py
this is a small project that I made in my free time :-)
This will load a gif, split the gif into seperate images, convert those images into
ascii representations, and then print those ascii representations to the console accompanied
by a background song. It's a fun little script to play around with!

This script will work with any gif or sound clip(within reason) but it
was designed to use the carlton dancing gif to the tune of 'It's not Unusual' by Tom Jones
but for the sake of copyright I'm not going to include either of those files in this project.
'''
from PIL import Image, ImageDraw, ImageFont
import os
import time
import sys
from pygame import mixer #you will need pygame in order to play the music, just a FYI

# extracts the frames from the animated gif, 
# takes in an allready open gif and returns an list of new image objects, one for each
# frame, additionally I like my ascii art to be full, however if our gif's background is 
#transparent it won't turn out right whenever we weight the ascii characters, so
#in order to render everything in ascii text we can paint the image over a canvas so it
#gets a proper color. however it also looks good without this fill.
def extract_gif_frames(gif, fillEmpty=False):
    frames=[]
    try:
        while True:
            gif.seek(gif.tell()+1)
            new_frame = Image.new('RGBA',gif.size)
            new_frame.paste(im, (0,0), im.convert('RGBA'))
            
            #check if we are painting over a canvas
            if fillEmpty:
                canvas=Image.new('RGBA', new_frame.size, (255,255,255,255))
                canvas.paste(new_frame, mask=new_frame)
                new_frame=canvas
            
            
            frames.append(new_frame)
    except EOFError:
        pass # end of sequence
    return frames
    
#debug function, to ensure that it actually extracts the frames correctly,
#this way you can see what frame is supposed to look like.
def save_frames_list(frames):        
    i=0
    for frame in frames:
        i+=1
        frame.save('test%d.png'%i,**frame.info)

        
#converts a single image to an ascii representation,
#this function was based on the code found here:
#http://code.activestate.com/recipes/580702-image-to-ascii-art-converter/
def convert_image_to_ascii(image):
    font = ImageFont.load_default() # load default bitmap monospaced font
    (chrx, chry) = font.getsize(chr(32))
    # calculate weights of ASCII chars
    weights = []
    for i in range(32, 127):
        chrImage = font.getmask(chr(i))
        ctr = 0
        for y in range(chry):
            for x in range(chrx):
                if chrImage.getpixel((x, y)) > 0:
                    ctr += 1
        weights.append(float(ctr) / (chrx * chry))
    
    output = ""
    (imgx, imgy) = image.size
    imgx = int(imgx / chrx)
    imgy = int(imgy / chry)
    # NEAREST/BILINEAR/BICUBIC/ANTIALIAS
    image = image.resize((imgx, imgy), Image.BICUBIC)
    image = image.convert("L") # convert to grayscale
    pixels = image.load()
    for y in range(imgy):
        for x in range(imgx):
            w = float(pixels[x, y]) / 255 / intensity_multiplier
            # find closest weight match
            wf = -1.0; k = -1
            for i in range(len(weights)):
                if abs(weights[i] - w) <= abs(wf - w):
                    wf = weights[i]; k = i
            output+=chr(k + 32)
        output+="\n"
    return output
    
    
#converts a list of frames into ascii representations.
def convert_frames_to_ascii(frames):
    ascii_frames = []
    for frame in frames:
        new_frame = convert_image_to_ascii(frame)
        ascii_frames.append(new_frame)
    return ascii_frames
    
    
    
    
    
#this functions takes in the ascii frames and animated them,
#there are a few options but you really don't need to mess with them unless you just want to.
#also, I did have a system call in this function, I think it looks better if we erase the previous
#frame before we draw the next one and the easiest way I found to do that is through a system
#call to clear the console, it works on windows platforms but it may not work on linux or macs
def animate_ascii(ascii_frames, frame_pause=.02, num_iterations=15, clear_prev_frame=True):
    for i in range(num_iterations):
        for frame in ascii_frames:
            print(frame)
            time.sleep(frame_pause)
            if clear_prev_frame:                
                os.system('cls')
 


#this function takes in the file name of a song and uses pygame to play it,
#ok, admittedly it's not the best solution, but I had the libraries allready installed
#and it was a quick way to get music into the project. 
def start_music(musicFileName):
    mixer.init()
    mixer.music.load(musicFileName)
    mixer.music.play()
    

im = Image.open("carlton.gif")
frames = extract_gif_frames(im, fillEmpty=True)

#defines how much sensitivity it has while looking for weights. Change to see the effects.
intensity_multiplier = 4

ascii_frames = convert_frames_to_ascii(frames)
start_music("song.mp3")
time.sleep(11)#I like the idea of carlton poping up just as Tom Jones starts singing, so we delay the animation a bit.
animate_ascii(ascii_frames, num_iterations=200)