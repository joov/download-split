# Download splitted files from akamai etc.

## Use-Case
A lot of video / audio downloads are presented as files splitted in subsequent segments. Examples can be seen in Mediathek of ARD, Arte etc.
Each file only covers less than a minute of the program. Manual download is tiresome.

## Solution
This downloader can download a sucession of files with filenames according to a pattern.
The downloader is controlled by a `yaml`-File.

## Usage

### Prereqs
You have to have `python3` installed to use this tool.

### Get URL
To initiate a download you first have to discover the file pattern. This is done by starting watching the video / listenning to the audio.
Then select "Developer Tools" -> Network in your browser. Identify the Media files (e.g. .mp3, .ts) which are loaded in straight succession.
Copy the URL.

### Configure Yaml-File
Then start editing or create a new `yaml`-File.

Here is an example:

```yaml
---
url: https://myprogram-vh.akamaihd.net/i/int/2018/01/04/some-strange-key-some-other-strange-key/,480-1,960-1,320-1,512-1,640-1,.mp4.csmil/segment{0}_1_av.ts?null=0
output: mymovie.ts
placeholders:
  - type: 
      - range
    start: 1
    end: 900
```

* `url` is the url-pattern. `{0}, {1}` are placeholders for ranges or sets.
* `output` is the output filename. All downloaded files are concatenated to this output (works with `ts`). Without this field each downloaded file is stored with it's original name as given in the url (filenname-part only).
* `placeholders` is an array of placeholders
 * `type` (array) can contain a `range`, a `set` or both.
 * `range` has a `start` and `end` value
 * `set` is an array of distinct values.

If both `range` and `set` are given, two paceholders are needed, one only in other cases.

More than one `type`s can be given but only max. one `range` or `set` inside a `type` is possible.

### Run program
Run the program with `python downlaod-split.py -h` for help (just `download-split.py -h` on linux).

Then run the program with your yaml-file.

## Limitations
Download of youtube videos is not possible with is tool.
No guarantee is given that the use of this program is legally correct in your country.
The `yaml`-file given above has purely educational content and is not guaranteed to work properly 

## License
Copyright joov (date of last commit)
GPL 3.0

