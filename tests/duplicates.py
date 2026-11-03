import json,sys
from playwright.sync_api import sync_playwright
import os
SITE=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','site'))
URL='file://'+SITE+'/index.html#uji'
JS="""()=>{
 const X=window.__siCilik,L=X.LEVELS,DB=X.DB(),S=X.S,out=[];
 const zones=Object.keys(L);
 for(const zk of zones){
  const [age,z]=zk.split(':');
  const p={id:'t'+zk,name:'T',age:+age,color:'#fff',progress:{},stats:{plays:0,last:0,lv:{}}};
  DB.players.length=0;DB.players.push(p);S.pid=p.id;S.zone=z;
  L[zk].forEach((lv,li)=>{
    S.lvl=li;p.recent={};
    let within=0,ov=0,ovn=0,prev=null,thrown=0;const pool=new Set();
    for(let r=0;r<40;r++){
      let run;try{run=X.buildRun();}catch(e){thrown++;out.push({z:zk,l:li+1,err:String(e)});break;}
      const sg=run.qs.map(q=>q.sig);
      if(run.qs.length<6)within+=100;
      if(new Set(sg).size<sg.length)within++;
      sg.forEach(k=>pool.add(k));
      if(prev){const ps=new Set(prev);ov+=sg.filter(k=>ps.has(k)).length/sg.length;ovn++;}
      prev=sg;
    }
    out.push({z:zk,l:li+1,pool:pool.size,within:within,replay:+(ov/ovn).toFixed(2)});
  });
 }
 return out;}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(URL); pg.wait_for_timeout(400)
    res=pg.evaluate(JS)
print('errors',errs[:3],[r for r in res if 'err' in r][:5])
lv=[r for r in res if 'pool' in r]
print('levels',len(lv))
print('runs with in-run duplicates:',[(r['z'],r['l'],r['within']) for r in lv if r['within']>0])
print('pool<12:',[(r['z'],r['l'],r['pool']) for r in lv if r['pool']<12])
print('replay overlap>0.34:',[(r['z'],r['l'],r['replay']) for r in lv if r['replay']>0.34])
import statistics
print('mean replay',round(statistics.mean(r['replay'] for r in lv),2))
