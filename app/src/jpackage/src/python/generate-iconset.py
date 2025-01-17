import sys
import pathlib
import subprocess

if len(sys.argv) < 2:
    print("No path to original / hi-res icon provided")
    raise SystemExit

if len(sys.argv) > 2:
    print("Too many arguments")
    raise SystemExit

originalPicture = pathlib.Path(sys.argv[1])
if not (originalPicture.is_file()):
    print(f"There is no such file: {sys.argv[1]}")
    raise SystemExit

# if False, then sips will be used instead of ImageMagick
useMagick = False

fname = pathlib.Path(originalPicture).stem
ext = pathlib.Path(originalPicture).suffix
destDir = pathlib.Path(originalPicture).parent

iconsetDir = pathlib.Path(destDir / f"{fname}.iconset")
if not (iconsetDir.is_dir()):
    pathlib.Path(iconsetDir).mkdir(parents=False, exist_ok=True)


class IconParameters():
    width = 0
    scale = 1

    def __init__(self, width, scale):
        self.width = width
        self.scale = scale

    def getIconName(self):
        if self.scale != 1:
            return f"icon_{self.width}x{self.width}{ext}"
        else:
            return f"icon_{self.width//2}x{self.width//2}@2x{ext}"


# https://developer.apple.com/design/human-interface-guidelines/macos/icons-and-images/app-icon#app-icon-sizes
ListOfIconParameters = [
    IconParameters(16, 1),
    IconParameters(16, 2),
    IconParameters(32, 1),
    IconParameters(32, 2),
    IconParameters(64, 1),
    IconParameters(64, 2),
    IconParameters(128, 1),
    IconParameters(128, 2),
    IconParameters(256, 1),
    IconParameters(256, 2),
    IconParameters(512, 1),
    IconParameters(512, 2),
    IconParameters(1024, 1),
    IconParameters(1024, 2)
]

# generate iconset
for ip in ListOfIconParameters:
    if useMagick:
        subprocess.call(
            [
                "magick",
                "convert",
                originalPicture,
                "-resize",
                str(ip.width),
                iconsetDir / ip.getIconName()
            ]
        )
    else:
        subprocess.call(
            [
                "sips",
                "-z",
                str(ip.width),
                str(ip.width),
                originalPicture,
                "--out",
                iconsetDir / ip.getIconName()
            ]
        )
    #print(f"Generated {ip.getIconName()}")

# convert iconset to icns file
subprocess.call(
    [
        "iconutil",
        "-c",
        "icns",
        iconsetDir,
        "-o",
        destDir / f"{fname}.icns"
    ]
)