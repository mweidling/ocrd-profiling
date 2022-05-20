"""
this script profiles the ocrd.Workspace.remove_file_group() function
by inspecting several images.
To be executed from within the 'medium_workspace' dir.
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

tree = ET.parse('mets.xml')
root = tree.getroot()

USES = []

for element in root.findall('.//mets:fileGrp[@USE]', NS):
    attrib_dict = element.attrib
    USES.append(attrib_dict.get("USE"))

profiler = cProfile.Profile()
profiler.enable()

for USE in USES:
    ws.remove_file_group(USE, recursive=True)

profiler.disable()
stats = pstats.Stats(profiler).sort_stats('tottime')
stats.dump_stats('../results/remove_file_group.prof')