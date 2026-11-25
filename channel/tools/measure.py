"""Measure the centre of every SVG item wrapper in the built chapter compositions.

GSAP cannot measure SVG boxes of hidden clips, so pops and wobbles get the wrong origin.
This renders each chapter's markup with every shot visible, reads getBBox() of each item
wrapper (they sit directly under the root <svg>, so the box is in 1920x1080 frame space)
and writes build/origins.json  {element_id: [cx, cy]}.
"""
import glob
import json
import os
import re
import subprocess
import sys
import tempfile

EP = sys.argv[1]
comp = f"{EP}/video/compositions"
pages = []
for f in sorted(glob.glob(f"{comp}/ch*.html")):
    html = open(f).read()
    body = html[html.index("<template>") + 10:html.index("<script>")]
    body = re.sub(r'class="shot clip"', 'class="shot"', body)
    pages.append(body)
doc = ("<html><head><style>.shot{position:absolute;inset:0}.cam{position:absolute;inset:0}"
       ".cam>svg,.lay>svg{position:absolute;left:0;top:0;width:1920px;height:1080px}.lay{position:absolute;left:0;top:0;width:1920px;height:1080px}</style></head><body>"
       + "".join(pages) + "</body></html>")
tmp = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False)
tmp.write(doc)
tmp.close()
js = r"""
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.goto('file://'+process.argv[1]);
const r=await p.evaluate(()=>{const o={};document.querySelectorAll('svg g[id]').forEach(g=>{
  if(!/^c\d+s\d+-[^-]+-g$/.test(g.id))return;try{const bb=g.getBBox();if(bb.width||bb.height)o[g.id.slice(0,-2)]=[+(bb.x+bb.width/2).toFixed(1),+(bb.y+bb.height/2).toFixed(1)];}catch(e){}});return o;});
console.log(JSON.stringify(r));await b.close();})();
"""
out = subprocess.run(["node", "-e", js, tmp.name], capture_output=True, text=True, check=True).stdout
os.unlink(tmp.name)
data = json.loads(out)
json.dump(data, open(f"{EP}/build/origins.json", "w"))
print(len(data), "origins")
