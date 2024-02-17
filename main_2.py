# concurrency reference

import glob
from fpdf import FPDF

images = []
images = glob.glob(Outpath + "/IMG/*.jpg" ,recursive=False)

pdf = FPDF()

for x in range(len(images)):

    im_int = Image.open(images[x])
    width = im_int.width
    height = im_int.height
    if width > height:
        pdf.add_page(orientation='L')
        pdf.image(images[x],x=0,y=0,h=210,w=297)
    else:
        pdf.add_page()
        pdf.image(images[x],x=0,y=0,h=297,w=210)

pdf.output(Outpath + "/IMG/IO.pdf", "F")