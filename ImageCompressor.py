import PIL, os, sys
from PIL import Image
from tkinter.filedialog import*

'''
size      = the size of the file in B
dim       = the dimensions of the image as a tuple (width, height)
ratio     = the scale ratio between the width and the height of the image
dec       = the decremental value of which the largest value
            between the width and height that the image will decrease in size by
wide      = a boolean to know whether the width is larger than the height
fFormat   = the format the file is (i.e. PNG, JPEG)
itr       = the number of compression iterations completed. The program will stop
            at its current compression and close. To avoid going for too long or
            somehow, if possible, finding an endless loop.
threshold = the maximum desired file size to compress to in bytes
'''

def ImageCompressor():
    wide = False
    compressed = True
    itr = 0
    max_itr = 50
    threshold = 256000
    
    try:
        files = askopenfilenames()
        for file in files:
            print(files)
            print(file)
            img = Image.open(file)
            size = os.path.getsize(file)
            
            dim = img.size
            dWidth, dHeight = dim
            fFormat = img.format

            # Finding the ratio between the width and height of the image
            if dWidth < dHeight:
                ratio = dHeight / dWidth
                wide = True
            else:
                ratio = dWidth / dHeight

            if (size <= threshold):
                print("Image is already under the threshold file size.")
                next

            # Decrease the dimensions of the image until it reaches the desired file size
            while size >= threshold:
                if itr == max_itr:
                    print("Interrupt: Compression taking too long.")
                    print("Please run again on the current result to continue.")
                    compressed = False
                    break
                
                dec = 10 ** (len(str(size)) - 5)
                
                if wide:
                    dim = dWidth - dec, int(dHeight - (dec * ratio))
                else:
                    dim = int(dWidth - (dec * ratio)), dHeight - dec
                    
                img = img.resize(dim)
                img.save(file + "_compressed." + fFormat, fFormat)
                size = os.path.getsize(file + "_compressed." + fFormat)
                dWidth, dHeight = dim
                ++itr
            if compressed:
                print("Compression Complete.")
            img.close()
    except PIL.UnidentifiedImageError:
        print("UnidentifiedImageError: Unsupported file type selected.")
    except IndexError as err:
        print("IndexError: No file found.")
    except Exception as err:
        print("Unexcepted error: ", err)
    finally:
        print("Script Complete.")

ImageCompressor()
sys.exit()

