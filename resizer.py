import cv2
import sys
import os

if len(sys.argv) >= 4:
    path = sys.argv[1]
    width = int(sys.argv[2])
    height = int(sys.argv[3])
else:
    print("error: specify path, width and height")
    sys.exit(1)


img = cv2.imread(os.path.normpath(f'{path}.png'))
resized = cv2.resize(img, (width, height))
cv2.imwrite(os.path.normpath(f'{path}-resized.png'), resized)
