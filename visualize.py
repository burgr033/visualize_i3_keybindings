from bs4 import BeautifulSoup
import json
from pathlib import Path

def get_modkey(line,mode):
    modkey = line.replace('set %s ' % mode,'')
    modkey = modkey.replace(' ','').replace('\n','')
    if(modkey == 'Mod4'):
        return "Super"
    elif(modkey == 'Mod1'):
        return "Alt"
    else:
        return modkey


keybindings = []
modline = ''
altline = ''
config_file = "config.json"
html_template_file = "i3_config.html.template"
if(Path(config_file).is_file()):
    with open(config_file,'r',encoding='utf-8') as f:
        config = json.load(f)
else:
    print("missing config file. exit")
    exit(1)

if(Path(html_template_file).is_file()):
    soup = BeautifulSoup(open(html_template_file), 'html.parser')
else:
    print("missing template file. exit")
    exit(1)

with open(config['i3_config_path'],'r') as file:
    for line in file.readlines():
        if(line.startswith('set $mod')):
            modkey = get_modkey(line,'$mod')
        if(line.startswith('set $alt')):
            altkey = get_modkey(line,"$alt")
        if(line.startswith('bindsym')):
            keybindings.append(line)
for item in keybindings:
    item = item.replace("bindsym ",'')
    item = item.split(' ',1)
    mod = item[0]
    command = item[1]
    mod_split = mod.split("+")
    mod_split = [sub.replace('$mod',modkey).replace('$alt',altkey) for sub in mod_split]
    for mod in mod_split:
        tag = soup.new_tag("kbd")
        tag.string = mod
        soup.body.append(tag)
    soup.body.append(" "+command)
    html_br = soup.new_tag('br')
    soup.body.append(html_br)
with open("i3_config.html", "w") as file:
    file.write(str(soup))