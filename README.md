# Auto Subtitle - A tool to auto generate and translate subtitles from vidoes using Open AI's whisper and chatGPT

This is a repository to use open AI's whisper API and chatGPT for auto subtitle generation

  

## Requirement

1. install ffmpeg

```bash

# on Ubuntu or Debian

sudo apt  update && sudo apt  install  ffmpeg

  

# on Arch Linux

sudo pacman  -S  ffmpeg

  

# on MacOS using Homebrew (https://brew.sh/)

brew install  ffmpeg

  

# on Windows using Chocolatey (https://chocolatey.org/)

choco install  ffmpeg

  

# on Windows using Scoop (https://scoop.sh/)

scoop install  ffmpeg

```

2. install requirement

`pip3 install -r requirement.txt`

3. install whisper

`pip install git+https://github.com/openai/whisper.git`

  

## How to generate subtitle for a video

For example, if you want to generate the subtitle for mx.mp4. you can use the script below

- -i input video file path
- -l input file langulage
- -o output SRT file path
`python3 transcript.py -i ./mx.mp4 -l Japanese -o mx.srt`
  

## How to translate subtitle for a video

For example, if you want to translate mx2.srt from Japanese to Chinese, you can use the followinig command. This will output the translated result to mx_cn.srt

- -i input SRT file path
- -il input file langulage
- -o output SRT file path
- -ol output SRT language
- -t chatGPT API token

`python3 translate.py -i ./mx2.srt -il Japanese -o ./mx_cn.srt -ol Chinese -t <chatGPT API token>`

## How to merge the SRT file to the video
You can use the attached shell script to combine SRT and the video. Just use
```
./merge-srt-to-mp4.sh vidoe.mp4 subtitle.SRT
```
