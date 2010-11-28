from glob import glob
from os import stat
logs = glob('logs/get*')
q = []
logs.sort(key=(lambda f : stat(f).st_mtime))
for log in logs:
    for line in file(log):
        if line.startswith('Error'): continue
        q.append(int(line.split()[-1][:-1]))
plot(q)

