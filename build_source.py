from pathlib import Path
import pypdf,pypdfium2 as pdfium,json,shutil,re
root=Path('ai-teaching-learning-site'); (root/'assets/pages').mkdir(parents=True,exist_ok=True)
src=next(Path('.').glob('*.pdf')); shutil.copy2(src,root/'assets/source.pdf'); r=pypdf.PdfReader(src); doc=pdfium.PdfDocument(str(src)); pages=[]
for i,p in enumerate(r.pages):
 t=p.extract_text() or ''; lines=[s.strip() for s in t.splitlines() if s.strip() and not s.strip().isdigit() and '楊梅高中施文賢' not in s]
 links=[]
 for a in p.get('/Annots',[]):
  a=a.get_object(); u=a.get('/A',{}).get('/URI','')
  if str(u).startswith(('https://','http://')): links.append(str(u))
 pages.append(dict(n=i+1,title=(lines[0] if lines else '圖像教材')[:95],text=t,links=list(dict.fromkeys(links))))
 target=root/f'assets/pages/{i+1:03}.webp'
 if not target.exists():
  page=doc[i]; bitmap=page.render(scale=1.65); im=bitmap.to_pil(); im.save(target,'WEBP',quality=88); bitmap.close(); page.close()
 if i%40==0: print('render',i+1,flush=True)
(root/'data.js').write_text('window.PAGES='+json.dumps(pages,ensure_ascii=False)+';',encoding='utf-8')
print('COMPLETE',len(pages))
