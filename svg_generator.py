import os
import urllib
from graphviz import Source
import re
"New"
SVG_CATALOGUE_PATH = 'pics'

class SVG_Generator:
    def __init__(self):
        if (not(os.path.exists(SVG_CATALOGUE_PATH))):
            os.mkdir(SVG_CATALOGUE_PATH)

    def generate_svg(self, token,graph):
        filename =  os.path.join(SVG_CATALOGUE_PATH,token+'.svg')
        graph_new = re.sub('dpi=\d*','dpi=0',graph)
        s = Source(graph_new, filename=filename, format="svg")
        s.save()
        return os.path.abspath(filename)

