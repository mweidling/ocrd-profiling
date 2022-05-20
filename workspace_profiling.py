from ocrd import Workspace, Resolver
from ocrd_models import OcrdMets, OcrdFile
import cProfile, pstats
from lxml import etree as ET

profiler = cProfile.Profile()
profiler.enable()

resolver = Resolver()
directory = "ocrd_workspace_small"
workspace = Workspace(resolver, directory, automatic_backup=True)

NS = {"mets": "http://www.loc.gov/METS/"}
url = "https://images.sub.uni-goettingen.de/iiif/image/gdz:PPN134818105:00000001/full/full/0/default.jpg"

#tree = ET.parse("ocrd_workspace_small/mets.xml")
#root = tree.getroot()
#el = root.find("./mets:fileSec/mets:fileGrp/mets:file[last()]", NS)
#f = OcrdFile(el)
#result = workspace.download_file(f)

workspace.remove_file("OCR-D-IMG_00000007", keep_file=True)

profiler.disable()
stats = pstats.Stats(profiler).sort_stats('tottime')
stats.print_stats()   

print("result")