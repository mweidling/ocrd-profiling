"""
this script profiles the ocrd.Workspace.resolve_image_exif() function
by inspecting several images.
To be executed from within the 'small_workspace' dir.
"""

from ocrd import Workspace, Resolver
from ocrd_models import OcrdMets, OcrdFile
import cProfile, pstats
import shutil, os

resolver = Resolver()
dir = "."
ws = Workspace(resolver, dir)

profiler = cProfile.Profile()
profiler.enable()

# URLs
ws.resolve_image_exif("http://gdz-srv1.sub.uni-goettingen.de/content/PPN134818105/500/0/00000001.jpg")
ws.resolve_image_exif("http://gdz-srv1.sub.uni-goettingen.de/content/PPN134818105/500/0/00000002.jpg")
ws.resolve_image_exif("http://gdz-srv1.sub.uni-goettingen.de/content/PPN134818105/500/0/00000003.jpg")
ws.resolve_image_exif("http://gdz-srv1.sub.uni-goettingen.de/content/PPN134818105/500/0/00000004.jpg")
ws.resolve_image_exif("http://gdz-srv1.sub.uni-goettingen.de/content/PPN134818105/500/0/00000005.jpg")

profiler.disable()
stats = pstats.Stats(profiler).sort_stats('tottime')
stats.dump_stats('resolve_image_exif.prof')