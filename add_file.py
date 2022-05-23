"""
this script profiles the ocrd.Workspace.add_file() function
by inspecting several images.
To be executed from within the 'medium_workspace' dir.
"""

from ocrd import Workspace, Resolver
from ocrd_models import OcrdMets, OcrdFile
from lxml import etree as ET
import cProfile, pstats

NS = {"mets": "http://www.loc.gov/METS/"}

resolver = Resolver()
dir = "."
ws = Workspace(resolver, dir)

tree = ET.parse('mets.xml')
root = tree.getroot()

file_grp = "OCR-D-IMG"
content = "adsf_testitest"

profiler = cProfile.Profile()
profiler.enable()

for pos in range(1,101):
    ID = "ID_" + str(pos)
    pageId = "page_" + ID
    local_filename = ID + ".tif"

    ws.add_file(file_grp, content=content, ID=ID, pageId=pageId, local_filename=local_filename)

profiler.disable()
stats = pstats.Stats(profiler).sort_stats('tottime')
stats.dump_stats('../results/add_file.prof')

for pos in range(1,101):
    ID = "ID_" + str(pos)
    ws.remove_file(ID)