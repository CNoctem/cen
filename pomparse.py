VER = '<version>'
EVER = '</version>'

def get_version(pomfile):
    with open(pomfile) as pom:
        skip = False
        for l in pom.readlines():
            if '<parent>' in l:
                skip = True
            elif '</parent>' in l:
                skip = False
            if not skip and VER in l:
                if EVER in l:
                    return get_oneline_version(l)
                else:
                    return 'MultilineVersion'

def get_oneline_version(line):
    i = line.index(VER)
    j = line.index(EVER)
    return line[i + len(VER):j]
