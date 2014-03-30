#!/usr/bin/env python3

import re
import json

entities = {}

with open("HTMLEntityNames.in") as f:
    for s in f:
        s = s.strip()
        if not s:
            continue
        m = re.match(r'"(.*)","(.*)"$', s)
        ent = '&'+m.group(1)
        code = m.group(2)
        s = "".join(chr(int(re.match(r"U\+(\S+)", x).group(1), 16)) for x in code.split())
        if not s in entities:
            entities[s] = []
        entities[s].append(ent)

with open("data.json", "w") as f:
    json.dump(entities, f)

def dump(f, title):
    print()
    print("     "+title)
    for s, v in sorted(entities.items()):
        if any(f(s, ent) for ent in v):
            print("%s  :\t'%s'\t%s" % ("+".join(str(ord(c)) for c in s), s, " ".join(v)))


dump(lambda s, ent: any(ord(c) < 256 and not (c.isalnum() or c.isspace()) for c in s), "8-BIT-SPECIAL")
dump(lambda s, ent: ";" not in ent, "NO-SEMICOLON")
dump(lambda s, ent: len(s) > 1 and any(ord(c) < 256 for c in s), "MULTI-8BIT")
dump(lambda s, ent: len(s) > 1, "MULTI")
dump(lambda s, ent: any(ord(c) < 256 for c in s), "8-BIT")
dump(lambda s, ent: True, "ALL")




                                               
