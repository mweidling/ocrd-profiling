"""
this script profiles the ocrd.Workspace.merge() function
by

1. merging two small workspaces
2. merging a small and a medium ws
3. merging a small and a big ws
4. merging two medium ws
5. merging a medium and a large ws
6. merging two large ws

"""

from ocrd import Workspace, Resolver
from ocrd_models import OcrdMets, OcrdFile
import cProfile, pstats
import shutil, os

def find_and_replace(filename, search_text, replace_text):
    with open(filename, 'r') as file:
        data = file.read()
        data = data.replace(search_text, replace_text)

    with open(filename, 'w') as file:
        file.write(data)

def rename_files_in_dir(dir):
    for count, filename in enumerate(os.listdir(dir)):
        dst = f"0c0{str(count)}.tif"
        src =f"{dir}/{filename}"
        dst =f"{dir}/{dst}"
        os.rename(src, dst)

# set up testing env

resolver = Resolver()
dir_small = "small_workspace"
dir_large = "large_workspace"
dir_medium = "medium_workspace"

# since a merge alters the original mets, we provide separate workspaces for each merge combination.
dir_s1_copy = "ws_s_and_s"
dir_s2_copy = "ws_s_and_m"
dir_s3_copy = "ws_s_and_l"
dir_m1_copy = "ws_m_and_m"
dir_m2_copy = "ws_m_and_l"
dir_l_copy = "ws_l_and_l"

print("Create copies of directories.")

shutil.copytree(dir_small, dir_s1_copy)
shutil.copytree(dir_small, dir_s2_copy)
shutil.copytree(dir_small, dir_s3_copy)
shutil.copytree(dir_medium, dir_m1_copy)
shutil.copytree(dir_medium, dir_m2_copy)
shutil.copytree(dir_large, dir_l_copy)

dir_list = [dir_s1_copy, dir_s2_copy, dir_s3_copy, dir_m1_copy, dir_m2_copy, dir_l_copy]

for dir in dir_list:
    filename = dir + "/mets.xml"
    # in order to avoid ID clashes, we have to update the IDs of the copied directories.
    find_and_replace(filename, "000", "0c0")
    # bulk rename files to avoid name clashes
    subdirs = next(os.walk(dir))[1]
    for x in subdirs:
        subdir = dir + "/" + x
        rename_files_in_dir(subdir)
    


# initialize all workspaces

print("Create workspaces.")
workspace_small = Workspace(resolver, dir_small)
workspace_medium = Workspace(resolver, dir_medium)
workspace_large = Workspace(resolver, dir_large)
ws_s_and_s = Workspace(resolver, dir_s1_copy)
ws_s_and_m = Workspace(resolver, dir_s2_copy)
ws_s_and_l = Workspace(resolver, dir_s3_copy)
ws_m_and_m = Workspace(resolver, dir_m1_copy)
ws_m_and_l = Workspace(resolver, dir_m2_copy)
ws_l_and_l = Workspace(resolver, dir_l_copy)

# start profiling and merging

print("Start merging.")
profiler = cProfile.Profile()
profiler.enable()

ws_s_and_s.merge(workspace_small)
ws_s_and_m.merge(workspace_medium)
ws_s_and_l.merge(workspace_large)
ws_m_and_m.merge(workspace_medium)
ws_m_and_l.merge(workspace_large)
ws_l_and_l.merge(workspace_large)

profiler.disable()
stats = pstats.Stats(profiler).sort_stats('tottime')
stats.dump_stats('workspace_merge.prof')

print("Cleaning up...")
for dir in dir_list:
    shutil.rmtree(dir)