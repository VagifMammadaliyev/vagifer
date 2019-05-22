# vaGIFer
Small [PIL](https://github.com/python-pillow/Pillow) wrapper for dynamically creating set of images that are combined into a sequence of frames using [imageio](http://imageio.github.io/) (*to create GIF*).

### How to create GIFs?
Create your own `Painter` that will fill your frame (image) with pixels. `Painter` will decide which pixels must fill each frame. For more information go ahead and look for [examples](src/examples.py) on how to create `Painter`s and for [this file](src/test.py) to see how you start the whole process of creating gif.

Quick start:
```bash
git clone 'https://github.com/VagifMammadaliyev/vagifer' vagifer/
cd vagifer/src/
python3 test.py
```
Then look for `.gif` file in folder just created.
