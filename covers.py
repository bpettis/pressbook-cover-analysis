import internetarchive
import math
import requests
import csv
import argparse
import datetime
from dateutil import parser as dateParse
from io import BytesIO
from PIL import Image, ImageStat
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


parser = argparse.ArgumentParser(description='Evaluate the brightness and contrast of specified MHDL pressbook covers.')
parser.add_argument('--studio', '-s', required=False, help='specify the name of a studio to search for')
parser.add_argument('--limit', '-l', required=False, type=int, help="Limit the number of covers to search for. If specified, only the first X results will be plotted.")
parser.add_argument('--mode', '-m', required=False, type=int, help="Specify the graphing mode. Omit to default to (1). \n\nModes: (1) - X: Brightness Y: Contrast (2) - X: Year Y: Brightness")
parser.add_argument('--csv-only', '-c', required=False, action='store_false', help='Only write the CSV file and exit without creating an image.')
parser.add_argument('--output', '-o', required=False, help='Specify the name of the output files. Omit to default to (output.csv) and (output.png)')
args = parser.parse_args()


# Set font sizes for the plot:
SMALL_SIZE = 12
MEDIUM_SIZE = 14
BIGGER_SIZE = 18

# Set size for the plot:
WIDTH_INCHES = 50
HEIGHT_INCHES = 30

csvName = 'output.csv'
pngName = 'output.png'
if args.output:
    csvName = str(args.output) + '.csv'
    pngName = str(args.output) + '.png'

def main():
    imageArray = []
    studio = args.studio        
        
    setup_csv()
    search(imageArray, studio)
    if args.csv_only:
        return
    else:
        plot(imageArray)

def setup_csv():
    row = ['identifier', 'year', 'url', 'brightness', 'contrast']
    with open(csvName, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)

def write_row(row):
    with open(csvName, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)

def search(array, studio):
    
    # Check if something was set in the studio field. Append that to the query if so
    if studio:
        query = 'collection:mediahistory AND Format:Pressbooks AND Creator:' + studio
    else:
        query = 'collection:mediahistory AND Format:Pressbooks'
    
    outputArray = []
    counter = 0

    if args.limit:
        limit = args.limit
    else:
        print('--limit argument was not passed. Defaulting to a limit of 10 covers')
        limit = 10

    for i in internetarchive.search_items(query).iter_as_items():
        counter += 1
        if counter > limit:
            break
        try:
            identifier = i.item_metadata['metadata']['identifier']
            url = 'https://archive.org/download/' + identifier + '/page/n0_w250.jpg'
            image = download(url)
            brightness = calcBrightness(image)
            contrast = calcContrast(image)

            # Extract the Year
            # 1965-01-01T23:23:59Z
            dateStart = i.item_metadata['metadata']['date-start']
            dateObj = dateParse.parse(dateStart)
            year = dateObj.year


            print(f'{identifier} ({str(year)}): Brightness: {str(brightness)} Contrast: {str(contrast)}')
            arrayEntry = [identifier, year, url, brightness, contrast]
            array.append(arrayEntry)
            write_row(arrayEntry)

        except Exception as e:
            print('Download error :(')
            print(e)
            print('Waiting a bit before continuing...')
    
    return outputArray

def download(url):
    response = requests.get(url)
    if response.ok:
        return response.content
    else:
        return None

def calcBrightness( im_file ):
   # https://stackoverflow.com/questions/3490727/what-are-some-methods-to-analyze-image-brightness-using-python
   # Average the pixels and return the "perceived brightness"
   # those "magic numbers" come from http://alienryderflex.com/hsp.html

   # 0-255 - higher is brighter
   im = Image.open(BytesIO(im_file))
   stat = ImageStat.Stat(im)
   r,g,b = stat.mean
   return math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2))

def calcContrast (image):
    im = Image.open(BytesIO(image))
    stat = ImageStat.Stat(im)
    # Iterate through the color bands:
    # Bigger standard deviation means larger spread of pixel values
    # See: https://stackoverflow.com/questions/61658954/measuring-contrast-of-an-image-using-python

    stdevs = []
    for band,name in enumerate(im.getbands()): 
        stdevs.append(stat.stddev[band])
    
    # Average the standard deviations across all color bands:
    contrast = sum(stdevs) / len(stdevs)
    return contrast

def getImage(path, zoom=1):
    # Swap out the 250 pixels from the earlier request to a much smaller image to put on the chart
    path = path.replace('w250', 'w25')
    try:
        im = Image.open(BytesIO(download(path)))
        return OffsetImage(im, zoom=zoom)
    except:
        return None

def plot(array):
    x = []
    y = []
    images = []

    print('Procesing data for matplotlib...')
    print(f'{str(len(array))} items in array')

    # Clunky way to set the mode differently
    if args.mode == 2:
        for item in array:
            x.append(item[1]) # year
            y.append(item[3]) # brightness
            images.append(item[2]) # url
    else: 
        # Pull stuff out of the big array into the smaller array
        for item in array:
            x.append(item[3]) # brightness
            y.append(item[4]) # contrast
            images.append(item[2]) # url

    # create a matplotlib object
    fig, ax = plt.subplots()

    # Set up the formatting/display
    plt.title("Visual Trends of Pressbooks")
    if args.mode == 2:
        plt.xlabel("Year")
        plt.ylabel("Brightness")
        plt.xlim([1900, 2000])
        plt.ylim([0, 300])
    else:
        plt.xlabel("Brightness")
        plt.ylabel("Contrast")
        plt.xlim([0, 255])
        plt.ylim([-50, 200])
    fig.set_size_inches(WIDTH_INCHES, HEIGHT_INCHES)


    plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title


    # Plot the data:
    ax.scatter(x, y)

    # Place the images on the graph:
    print('Adding images')
    for x0, y0, path in zip(x, y, images):
        try:
            image = getImage(path)
            if image is None:
                print(f'{path} : Couldn\'t get image. Skipping to the next one.')
                continue
            ab = AnnotationBbox(image, (x0, y0), frameon=False)
            ax.add_artist(ab)
        except Exception as e:
            print(f'Something went wrong plotting this image: {path}')
            print(e)
            



    
    # Save the output
    plt.savefig(pngName, dpi=150)

if __name__ == "__main__":
    main()