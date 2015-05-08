# this will be run inside of a directory where
# it will merge ALL the files in that one directory

from os import listdir
from os.path import join, isfile
from graph import Graph

# takes two files, returns another one
# assume that a file is something that has been opened and read
def merge(file1, file2):
  file1_lines = [thing for thing in file1.strip().split("\n") if thing != '']
  file2_lines = [thing for thing in file2.strip().split("\n") if thing != '']
  output_lines = []
  for i in range(1,len(file1_lines) + 1):
    g = Graph(open("{0}{1}.in".format(INSTANCES_PATH, i)).read())
    index = i - 1
    file1_path = [int(node) for node in file1_lines[index].split(" ")]
    file2_path = [int(node) for node in file2_lines[index].split(" ")]
    output_lines.append(" ".join([str(node) for node in min([file1_path, file2_path], key=lambda path: g.path_cost(path))]))
  return "\n".join(output_lines).strip()

INSTANCES_PATH = "../instances/"
OUTPUT_FILE = "answer_merged.out"

onlyfiles = [f for f in listdir("./answers/") if isfile(join("./", f))]

last_file = open(onlyfiles[0]).read()
for next_file in onlyfiles[1:]:
  last_file = merge(last_file, open(next_file).read())

open(OUTPUT_FILE, 'w').write(last_file)
