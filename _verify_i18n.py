import re, xml.etree.ElementTree as ET

def keys_vals(path):
    tree = ET.parse(path); root = tree.getroot()
    out = {}
    for s in root.findall('string'):
        n = s.get('name')
        text = s.text or ''
        out[n] = (text, s.get('formatted'), s.get('translatable'))
    return out

en = keys_vals('app/src/main/res/values/strings.xml')
zh = keys_vals('app/src/main/res/values-zh-rCN/strings.xml')

missing = [k for k in en if k not in zh]
extra = [k for k in zh if k not in en]
print("EN keys:", len(en), "ZH keys:", len(zh))
print("missing-in-zh (non-false):", [k for k in missing if en[k][2] != 'false'])
print("extra-in-zh:", extra)

ph = lambda t: re.findall(r'%(?:\d+\$)?[sd]|%%', t) if t else []
mism = []
for k in zh:
    if k in en and en[k][2] == 'false':
        continue
    a = ph(en.get(k, ('',))[0]); b = ph(zh[k][0])
    if sorted(a) != sorted(b):
        mism.append((k, en.get(k, ('',))[0], zh[k][0], a, b))
print("placeholder mismatches:", len(mism))
for m in mism[:30]:
    print(m)