"""
this script profiles the ocrd.Workspace.download_file() function
by inspecting several images.
To be executed from within the 'small_workspace' dir.
"""

from ocrd import Workspace, Resolver
from ocrd_models import OcrdMets, OcrdFile
from lxml import etree as ET
import cProfile, pstats
import shutil, os

NS = {"mets": "http://www.loc.gov/METS/"}

resolver = Resolver()
dir = "."
ws = Workspace(resolver, dir)

# prepare OcrdFiles
tree = ET.parse("mets.xml")
root = tree.getroot()
mets_f1 = root.findall(".//mets:file[@ID = '000000012']", NS)
mets_f2 = root.findall(".//mets:file[@ID = '000000013']", NS)
mets_f3 = root.findall(".//mets:file[@ID = '000000014']", NS)
mets_f4 = root.findall(".//mets:file[@ID = '000000015']", NS)

f1 = OcrdFile(mets_f1[0])
f2 = OcrdFile(mets_f2[0])
f3 = OcrdFile(mets_f3[0])
f4 = OcrdFile(mets_f4[0])

profiler = cProfile.Profile()
profiler.enable()

ws.download_file(f1)
ws.download_file(f2)
ws.download_file(f3)
ws.download_file(f4)

profiler.disable()
stats = pstats.Stats(profiler).sort_stats('tottime')
stats.dump_stats('../results/download_file.prof')