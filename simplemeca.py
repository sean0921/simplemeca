#!/usr/bin/env python3

import sys
from time import sleep
import pygmt

if len(sys.argv) < 5:
    print(f"Usage: python3 {sys.argv[0]} <strike> <dip> <rake(slip)> <color of T-axis> <title>")
    sys.exit(1)

strike=float(sys.argv[1])
dip=float(sys.argv[2])
rake=float(sys.argv[3])
tcolor_str=str(sys.argv[4])

if len(sys.argv) < 6:
    title='Focal Mecanism'
else:
    title=''
    for i in range(5,len(sys.argv)):
        title+=str(sys.argv[i])
        if i != len(sys.argv):
            title+=" "

if not ( ( 0 <= strike <= 360 ) and ( 0 <= dip <= 90 ) and ( -180 <= rake <= 180 ) ):
    print("Format is not right!")
    print("(0 <= strike <= 360 && 0 <= dip <= 90 && -180 <= rake <= 180)")
    sys.exit(1)

tcolor=tcolor_str.split(sep='/')
if ( len(tcolor) != 3 ):
    print("Format of color is invalid! (<0~255>/<0~255>/<0~255>)")
    sys.exit(1)

for i in range(0,len(tcolor)):
    tcolor[i]=float(tcolor[i])

if not ( ( 0 <= tcolor[0] <= 255 ) and ( 0 <= tcolor[1] <= 255 ) and ( 0 <= tcolor[2] <= 255 ) ):
    print("Format of color is invalid! (<0~255>/<0~255>/<0~255>)")
    sys.exit(1)

##### main program

pygmt.config(FONT_TITLE=12)
pygmt.config(MAP_TITLE_OFFSET='-1c')
fig = pygmt.Figure()


print(title)
# generate a basemap near Washington state showing coastlines, land, and water
fig.basemap(
    region=[-1, 1, -1, 1],
    projection="M6c",
    frame=[f'+n+t"{title}"']
)

# store focal mechanisms parameters in a dict
#focal_mechanism = dict(strike=330, dip=30, rake=90, magnitude=3)
focal_mechanism = dict(strike=strike, dip=dip, rake=rake, magnitude=3)

# pass the focal mechanism data to meca in addition to the scale and event location
fig.meca(focal_mechanism, scale="6c", longitude=0, latitude=0, depth=0, G=f'{tcolor[0]}/{tcolor[1]}/{tcolor[2]}')

fig.text(x=0, y=0, text=f'{strike}/{dip}/{rake}', offset='0/2',font='8p')

fig.show(method='external')
sleep(0.1)
fig.savefig('test_meca.png')
