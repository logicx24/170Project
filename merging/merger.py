# this will be run inside of a directory where
# it will merge ALL the files in that one directory

from os import listdir
from os.path import join, isfile
from graph import Graph

INSTANCES_PATH = "../instances/"
OUTPUT_FILE = "answer_merged.out"

onlyfiles = [f for f in listdir("./") if isfile(join("./", f))]
last_file = open(onlyfiles[0]).read()
for next_file in onlyfiles[1:]:
  last_file = merge(last_file, open(new_file).read())

open(OUTPUT_FILE, 'w').write(last_file)


# takes two files, returns another one
# assume that a file is something that has been opened and read
def merge(file1, file2):
  file1_lines = file1.split("\n")
  file2_lines = file2.split("\n")
  output_lines = []
  for i in range(1,496):
    g = Graph(open("{0}{1}".format(INSTANCES_PATH, i)).read())
    index = i - 1
    file1_path = [int(node) for node in file1_lines[index]]
    file2_path = [int(node) for node in file2_lines[index]]
    output_lines.append(" ".join(min([file1_path, file2_path], key=lambda path: g.path_cost(path))))
  return "\n".join(output_lines)
