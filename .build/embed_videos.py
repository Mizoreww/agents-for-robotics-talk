"""Add native, self-contained click-to-play video shapes to an authored PPTX.
The title, poster and geometry stay unchanged. No presentation-authoring library.
"""
from pathlib import Path
from collections import defaultdict
import hashlib, json, zipfile, posixpath
from lxml import etree as E

ROOT=Path('/home/limx/Desktop/agent_for_robotics');B=ROOT/'.build'
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a':'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'p14':'http://schemas.microsoft.com/office/powerpoint/2010/main',
    'rel':'http://schemas.openxmlformats.org/package/2006/relationships',
    'ct':'http://schemas.openxmlformats.org/package/2006/content-types'}
def q(prefix,local):return '{'+NS[prefix]+'}'+local
def child(parent,prefix,local,**attrs):return E.SubElement(parent,q(prefix,local),attrs)
def xml(el):return E.tostring(el,xml_declaration=True,encoding='UTF-8',standalone=True)
placements=json.loads((B/'video_placements_focus.json').read_text())
with zipfile.ZipFile(B/'focus_draft.pptx') as z:parts={n:z.read(n) for n in z.namelist()}
ct=E.fromstring(parts['[Content_Types].xml'])
if not ct.xpath('ct:Default[@Extension="mp4"]',namespaces=NS):child(ct,'ct','Default',Extension='mp4',ContentType='video/mp4')
parts['[Content_Types].xml']=xml(ct)
by_slide=defaultdict(list)
for item in placements:by_slide[item['slide']].append(item)
receipts=[]
for number,items in by_slide.items():
 slide_name=f'ppt/slides/slide{number}.xml';rels_name=f'ppt/slides/_rels/slide{number}.xml.rels'
 s=E.fromstring(parts[slide_name]);rels=E.fromstring(parts[rels_name])
 assert not s.xpath('p:timing',namespaces=NS),'Do not replace an existing animation timeline'
 timing=E.Element(q('p','timing'));tn=child(timing,'p','tnLst');par=child(tn,'p','par');root=child(par,'p','cTn',id='1',dur='indefinite',restart='never',nodeType='tmRoot');nodes=child(root,'p','childTnLst')
 existing={r.get('Id') for r in rels};seq=1
 def rel_id():
  global seq
  while f'rIdVideo{seq}' in existing:seq+=1
  out=f'rIdVideo{seq}';existing.add(out);seq+=1;return out
 for i,item in enumerate(items,2):
  matches=s.xpath('.//p:pic[p:nvPicPr/p:cNvPr[@descr=$alt]]',namespaces=NS,alt=item['alt'])
  if not matches:
   # The authoring exporter currently drops picture alt strings. Match the
   # independently recorded fitted rectangle, then restore native alt text.
   expected=[item[k]*9525 for k in ['x','y','w','h']]
   for candidate in s.xpath('.//p:pic',namespaces=NS):
    off=candidate.find('p:spPr/a:xfrm/a:off',NS);extn=candidate.find('p:spPr/a:xfrm/a:ext',NS)
    if off is None or extn is None:continue
    actual=[int(off.get('x')),int(off.get('y')),int(extn.get('cx')),int(extn.get('cy'))]
    if all(abs(a-b)<3 for a,b in zip(actual,expected)):matches.append(candidate)
  assert len(matches)==1,(number,item['alt'],len(matches))
  pic=matches[0];nv=pic.find('p:nvPicPr',NS);cnv=nv.find('p:cNvPr',NS);sid=cnv.get('id');cnv.set('name',item['alt']);cnv.set('descr',item['alt']+'; '+item['sourceUrl'])
  for old in cnv.findall('a:hlinkClick',NS):cnv.remove(old)
  hlink=child(cnv,'a','hlinkClick',action='ppaction://media')
  nonvisual=nv.find('p:nvPr',NS)
  if nonvisual is None:nonvisual=child(nv,'p','nvPr')
  stem=Path(item['file']).stem;mp4=Path(item['file']).read_bytes();part=f'ppt/media/video_{stem}.mp4'
  assert part not in parts
  parts[part]=mp4;vr,mr=rel_id(),rel_id()
  child(rels,'rel','Relationship',Id=vr,Type=NS['r']+'/video',Target=f'../media/video_{stem}.mp4')
  child(rels,'rel','Relationship',Id=mr,Type='http://schemas.microsoft.com/office/2007/relationships/media',Target=f'../media/video_{stem}.mp4')
  vf=child(nonvisual,'a','videoFile');vf.set(q('r','link'),vr)
  exts=nonvisual.find('p:extLst',NS)
  if exts is None:exts=child(nonvisual,'p','extLst')
  ext=child(exts,'p','ext',uri='{DAA4B4D4-6D71-4841-9C94-3DE7FCFB9230}')
  em=E.SubElement(ext,q('p14','media'),nsmap={'p14':NS['p14']});em.set(q('r','embed'),mr)
  vid=child(nodes,'p','video');cm=child(vid,'p','cMediaNode',vol='0');c=child(cm,'p','cTn',id=str(i),fill='hold',display='0')
  st=child(c,'p','stCondLst');child(st,'p','cond',delay='indefinite')
  target=child(cm,'p','tgtEl');child(target,'p','spTgt',spid=sid)
  receipts.append({'slide':number,'shape_id':sid,'part':part,'sha256':hashlib.sha256(mp4).hexdigest(),'source':item['sourceUrl']})
 extlist=s.find('p:extLst',NS)
 if extlist is None:s.append(timing)
 else:s.insert(list(s).index(extlist),timing)
 parts[slide_name]=xml(s);parts[rels_name]=xml(rels)
# Check all package relationship targets, not only the added media.
for n,data in parts.items():
 if not n.endswith('.rels'):continue
 root=E.fromstring(data);folder=posixpath.dirname(posixpath.dirname(n)) if n!='_rels/.rels' else ''
 ids=[e.get('Id') for e in root];assert len(ids)==len(set(ids)),n
 for rel in root:
  if rel.get('TargetMode')=='External':continue
  target=rel.get('Target','');resolved=target.lstrip('/') if target.startswith('/') else posixpath.normpath(posixpath.join(folder,target))
  assert resolved in parts,(n,target,resolved)
assert len(receipts)==15,len(receipts)
out=B/'focus_media.pptx'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for n,data in parts.items():z.writestr(n,data)
with zipfile.ZipFile(out) as z:
 for r in receipts:assert hashlib.sha256(z.read(r['part'])).hexdigest()==r['sha256']
(B/'embedded_video_audit.json').write_text(json.dumps({'file':str(out),'count':len(receipts),'videos':receipts},indent=2))
print('Native embedded video validation passed:',len(receipts),'clips')
