"""
this script profiles the ocrd.Workspace.remove_file() function
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

ID_1 = "00000001"
ID_2 = "00000002"
ID_3 = "00000003"
ID_4 = "00000004"
ID_5 = "00000005"
ID_6 = "00000006"

profiler = cProfile.Profile()
profiler.enable()

ws.remove_file(ID_1)
ws.remove_file(ID_2)
ws.remove_file(ID_3)
ws.remove_file(ID_4)
ws.remove_file(ID_5)
ws.remove_file(ID_6)

profiler.disable()
stats = pstats.Stats(profiler).sort_stats('tottime')
stats.dump_stats('../results/remove_file.prof')
