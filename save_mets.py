"""
this script profiles the ocrd.Workspace.save_mets() function
by inspecting several images.
To be executed from within the 'medium_workspace' dir.
"""

from ocrd import Workspace, Resolver
from ocrd_models import OcrdMets, OcrdFile
from lxml import etree as ET
import cProfile, pstats

resolver = Resolver()
dir = "."
ws = Workspace(resolver, dir)

profiler = cProfile.Profile()
profiler.enable()

for pos in range(1,101):
    ws.save_mets()

profiler.disable()
stats = pstats.Stats(profiler).sort_stats('tottime')
stats.dump_stats('../results/save_mets.prof')