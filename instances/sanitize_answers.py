FILE_NAME = "answer.out"

answer_file = open(FILE_NAME, "r").read()
lines = [line.strip() for line in answer_file.split("\n") if line != '']
for l in range(len(lines)):
    lines[l] = [str(int(x) + 1) for x in lines[l].split()]
    lines[l] = " ".join(lines[l])

open(FILE_NAME, "w").write("\n".join(lines))