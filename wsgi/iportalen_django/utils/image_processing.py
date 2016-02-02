from PIL import Image


def create_thumbnail(infile, outfile, size=(129, 129), file_format="JPEG"):
    if infile != outfile:
        try:
            im = Image.open(infile)
            im.thumbnail(size)
            im.save(outfile, file_format)
            return im
        except IOError:
            raise IOError

