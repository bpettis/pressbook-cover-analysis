# Pressbook Cover Analysis

Early experimentation with using the Python Image Library (PIL) to assess large numbers of images and plot them on a graph them based on certain criteria.

The Python script `cover.py` works by searching the Internet Archive in the Media History Digital Library [collection](https://archive.org/details/mediahistory) for anything that has been specified as a [pressbook](https://mediahist.org/collections/pressbooks/). It downloads the cover of each item, and does some rudimentary analysis of how bright each image is.

## Installation

0. (Optional) Create a virtual environment to keep a tidier Python installation environment

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

1. Install required packages 

```bash
pip3 install -r requirements.txt
```

## Usage

Run the script:

```
python3 covers.py --help
```

```
usage: covers.py [-h] [--studio STUDIO] [--limit LIMIT] [--mode MODE] [--csv-only] [--write-json] [--output OUTPUT]

Evaluate the brightness and contrast of specified MHDL pressbook covers.

options:
  -h, --help            show this help message and exit
  --studio STUDIO, -s STUDIO
                        specify the name of a studio to search for
  --limit LIMIT, -l LIMIT
                        Limit the number of covers to search for. If specified, only the first X results will be plotted.
  --mode MODE, -m MODE  Specify the graphing mode. Omit to default to (1). Modes: (1) - X: Brightness Y: Contrast (2) - X: Year Y: Brightness
  --csv-only, -c        Only write the CSV file and exit without creating an image.
  --write-json, -j      Write a JSON file with your data as well. Omit to default to (False).
  --output OUTPUT, -o OUTPUT
                        Specify the name of the output files. Omit to default to (output.csv) and (output.png)
```

### Options:

- `-h`, `--help` -- display a help message
- `-s`, `--studio` -- specify the name of a studio to search for covers by - e.g. "Warner Bros." or "Paramount". If left blank, all studios will be included
- `-l`, `--limit` -- specify an integer to limit how many results are processed. Defaults to 10
- `-m`, `--mode` -- specify what mode shoudl be used for graphing. Mode 1 (default) plots brightness against contrast. Mode 2 plots brightness against year
- `-c`, `--csv-only` -- use this flag to skip creating an image file
- `-j`, `--write-json` -- use this flag to create a JSON file, suitable for use with the example Plot/D3 visualization
- `-o`, `--output` -- specify the base name to use for any files. Defaults to 'output', e.g. 'output.csv', 'output.png' and 'output.json'

---

## Outputs:

### CSV

```csv
identifier,year,url,brightness,contrast,creator
pressbook-20th-century-fox-your-air-raid-warden,1942,https://archive.org/download/pressbook-20th-century-fox-your-air-raid-warden/page/n0_w250.jpg,184.77791213764476,78.68772551716934,20th Century-Fox
pressbook-aip-beach-blanket-bingo,1965,https://archive.org/download/pressbook-aip-beach-blanket-bingo/page/n0_w250.jpg,158.54439721699814,84.52686159291777,American International Pictures
pressbook-aip-fireball-500,1966,https://archive.org/download/pressbook-aip-fireball-500/page/n0_w250.jpg,175.72042386516196,71.74104177498539,American International Pictures
pressbook-aip-how-to-stuff-a-wild-bikini,1965,https://archive.org/download/pressbook-aip-how-to-stuff-a-wild-bikini/page/n0_w250.jpg,159.51924237792596,77.32387843371721,American International Pictures
pressbook-aip-muscle-beach-party,1964,https://archive.org/download/pressbook-aip-muscle-beach-party/page/n0_w250.jpg,156.27340049758948,62.12222276427763,American International Pictures
pressbook-allied-artists-a-yank-in-viet-nam,1964,https://archive.org/download/pressbook-allied-artists-a-yank-in-viet-nam/page/n0_w250.jpg,158.89873578068367,59.9377915161354,Allied Artists International
pressbook-allied-artists-blood-on-the-arrow,1964,https://archive.org/download/pressbook-allied-artists-blood-on-the-arrow/page/n0_w250.jpg,140.57258605235177,77.87760876794347,Allied Artists International
pressbook-allied-artists-el-cid,1961,https://archive.org/download/pressbook-allied-artists-el-cid/page/n0_w250.jpg,180.79459095448303,53.22856953500416,Allied Artists International
pressbook-allied-artists-johnny-rocco,1958,https://archive.org/download/pressbook-allied-artists-johnny-rocco/page/n0_w250.jpg,145.75463706108516,68.18181521473451,Allied Artists International
pressbook-allied-artists-king-of-the-roaring-20s,1961,https://archive.org/download/pressbook-allied-artists-king-of-the-roaring-20s/page/n0_w250.jpg,121.5250785740349,59.713097937587065,Allied Artists International
```

### JSON

```
[
    {
        "identifier": "pressbook-20th-century-fox-your-air-raid-warden",
        "year": 1942,
        "url": "https://archive.org/download/pressbook-20th-century-fox-your-air-raid-warden/page/n0_w250.jpg",
        "brightness": 184.77791213764476,
        "contrast": 78.68772551716934,
        "creator": "20th Century-Fox"
    },
    {
        "identifier": "pressbook-aip-beach-blanket-bingo",
        "year": 1965,
        "url": "https://archive.org/download/pressbook-aip-beach-blanket-bingo/page/n0_w250.jpg",
        "brightness": 158.54439721699814,
        "contrast": 84.52686159291777,
        "creator": "American International Pictures"
    },
    {
        "identifier": "pressbook-aip-fireball-500",
        "year": 1966,
        "url": "https://archive.org/download/pressbook-aip-fireball-500/page/n0_w250.jpg",
        "brightness": 175.72042386516196,
        "contrast": 71.74104177498539,
        "creator": "American International Pictures"
    },
    {
        "identifier": "pressbook-aip-how-to-stuff-a-wild-bikini",
        "year": 1965,
        "url": "https://archive.org/download/pressbook-aip-how-to-stuff-a-wild-bikini/page/n0_w250.jpg",
        "brightness": 159.51924237792596,
        "contrast": 77.32387843371721,
        "creator": "American International Pictures"
    },
    {
        "identifier": "pressbook-aip-muscle-beach-party",
        "year": 1964,
        "url": "https://archive.org/download/pressbook-aip-muscle-beach-party/page/n0_w250.jpg",
        "brightness": 156.27340049758948,
        "contrast": 62.12222276427763,
        "creator": "American International Pictures"
    },
    {
        "identifier": "pressbook-allied-artists-a-yank-in-viet-nam",
        "year": 1964,
        "url": "https://archive.org/download/pressbook-allied-artists-a-yank-in-viet-nam/page/n0_w250.jpg",
        "brightness": 158.89873578068367,
        "contrast": 59.9377915161354,
        "creator": "Allied Artists International"
    },
    {
        "identifier": "pressbook-allied-artists-blood-on-the-arrow",
        "year": 1964,
        "url": "https://archive.org/download/pressbook-allied-artists-blood-on-the-arrow/page/n0_w250.jpg",
        "brightness": 140.57258605235177,
        "contrast": 77.87760876794347,
        "creator": "Allied Artists International"
    },
    {
        "identifier": "pressbook-allied-artists-el-cid",
        "year": 1961,
        "url": "https://archive.org/download/pressbook-allied-artists-el-cid/page/n0_w250.jpg",
        "brightness": 180.79459095448303,
        "contrast": 53.22856953500416,
        "creator": "Allied Artists International"
    },
    {
        "identifier": "pressbook-allied-artists-johnny-rocco",
        "year": 1958,
        "url": "https://archive.org/download/pressbook-allied-artists-johnny-rocco/page/n0_w250.jpg",
        "brightness": 145.75463706108516,
        "contrast": 68.18181521473451,
        "creator": "Allied Artists International"
    },
    {
        "identifier": "pressbook-allied-artists-king-of-the-roaring-20s",
        "year": 1961,
        "url": "https://archive.org/download/pressbook-allied-artists-king-of-the-roaring-20s/page/n0_w250.jpg",
        "brightness": 121.5250785740349,
        "contrast": 59.713097937587065,
        "creator": "Allied Artists International"
    }
]
```

## HTML Visualization

I have created a scatter plot using D3 and Plot (both from Observable) which will take the JSON data that this script outputs and make a somewhat fancy Web visualization.
See `visualization.html` for an example file which contains all the necessary code.