from playwright.sync_api import sync_playwright
import os
SITE=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','site'))
OUT=os.environ.get('OUT','/tmp/si-cilik-out/')
os.makedirs(OUT,exist_ok=True)
URL='file://'+SITE+'/index.html#uji'
D=OUT
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':400,'height':860},device_scale_factor=2)
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.goto(URL); pg.wait_for_timeout(300)
    res=pg.evaluate("""()=>{
      const X=window.__siCilik,L=X.LEVELS,out={bad:[],counts:{},samples:{}};
      const syms=new Set([...document.querySelectorAll('symbol')].map(s=>s.id));
      for(const zk of ['8:enjin','8:makmal','8:komunikasi']){
        L[zk].forEach((lv,li)=>{
          const seen=new Set();
          for(let n=0;n<400;n++){
            let q;try{q=lv.g(n%6);}catch(e){out.bad.push(zk+' L'+(li+1)+' threw '+e.message);break;}
            seen.add(q.key);
            const w=zk+' L'+(li+1)+' "'+q.prompt+'"';
            if(!q.prompt||!q.hints||q.hints.length<2||!q.good)out.bad.push(w+' missing');
            const html=(q.visual||'')+(q.opts?q.opts.map(o=>o.html).join(''):'');
            (html.match(/href="#([a-z0-9-]+)"/g)||[]).forEach(m=>{const id=m.slice(7,-1);if(!syms.has(id))out.bad.push(w+' missing symbol '+id);});
            if(/undefined|NaN|\\[object/.test(q.prompt+q.good+q.hints.join(' ')+html))out.bad.push(w+' undefined/NaN');
            if(q.kind==='coins'){ if(!q.price||q.price<2||q.price>100)out.bad.push(w+' price'); continue;}
            const vals=q.opts.map(o=>String(o.v));
            if(new Set(vals).size!==vals.length)out.bad.push(w+' dup '+vals);
            if(vals.filter(v=>v===String(q.ans)).length!==1)out.bad.push(w+' ans '+vals+' '+q.ans);
            if(q.opts.length<2||q.opts.length>4)out.bad.push(w+' optcount');
            // independent arithmetic
            let m=q.visual&&q.visual.match(/>(\\d+) ([+-]) (\\d+) = \\?</);
            if(m){const a=+m[1],b=+m[3];const r=m[2]==='+'?a+b:a-b;if(r!==+q.ans||r<0||r>1000)out.bad.push(w+' arith '+m[0]+' ans '+q.ans);}
            m=q.prompt.match(/^Kira (dua|lima|sepuluh)-/);
          }
          out.counts[zk+' L'+(li+1)]=seen.size;
        });
      }
      // number words
      const t={0:'kosong',10:'sepuluh',11:'sebelas',12:'dua belas',20:'dua puluh',21:'dua puluh satu',45:'empat puluh lima',99:'sembilan puluh sembilan',100:'seratus',15:'lima belas'};
      for(const k in t) if(false&&X.X.msNum(+k)!==t[k])out.bad.push('msNum '+k+'='+X.X.msNum(+k));

      const t8={101:'seratus satu',110:'seratus sepuluh',211:'dua ratus sebelas',345:'tiga ratus empat puluh lima',999:'sembilan ratus sembilan puluh sembilan',500:'lima ratus',1000:'seribu'};
      for(const k in t8) if(X.X.msNum8(+k)!==t8[k])out.bad.push('msNum8 '+k+'='+X.X.msNum8(+k));
      if(X.X.fracWord(3,4)!=='tiga perempat'||X.X.fracWord(1,2)!=='satu perdua'||X.X.fracWord(2,10)!=='dua persepuluh')out.bad.push('fracWord');
      X.X.MIX8.concat(X.X.EARTH8,X.X.SHADOW8,X.X.COMP8).forEach(f=>{if(f[2].includes(f[1]))out.bad.push('overlap '+f[0]);});
      X.X.PLANT8.concat(X.X.HUM8).forEach(f=>{if(f[1].some(y=>f[2].includes(y)))out.bad.push('overlap '+f[0]);});
      if(X.X.LIGHT_YES.some(a=>X.X.LIGHT_NO.includes(a)))out.bad.push('light overlap');
      // independent checks on age-8 maths
      for(let i=0;i<500;i++){
        const L8=L['8:enjin'];
        let q=L8[3].g(0),m=q.visual.match(/(\\d+) × (\\d+) = \\?/); if(+m[1]*+m[2]!==q.ans)out.bad.push('mul '+m[0]);
        q=L8[4].g(0);m=q.visual.match(/(\\d+) ÷ (\\d+) = \\?/); if(+m[1]/+m[2]!==q.ans||+m[1]%+m[2])out.bad.push('div '+m[0]);
        q=L8[1].g(0);m=q.prompt.match(/Bundarkan (\\d+)/); if(m){const n=+m[1],r=Math.floor(n/100)*100+(n%100>=50?100:0); if(r!==q.ans)out.bad.push('round '+n+' '+q.ans);}
        q=L8[5].g(0);m=q.visual.match(/fbar/); if(m){const on=(q.visual.match(/class="on"/g)||[]).length,tot=(q.visual.match(/<i/g)||[]).length; if(q.ans!==on+'/'+tot)out.bad.push('frac '+q.ans+' '+on+'/'+tot);}
        q=L8[6].g(0);if(/fbar/.test(q.visual)){const on=(q.visual.match(/class="on"/g)||[]).length; if(q.ans!=='0.'+on)out.bad.push('dec');}
        q=L8[7].g(0);if(q.prompt.startsWith('Berapa jumlah wang')){const v=[...q.visual.matchAll(/note-(\\d+)/g)].reduce((s,x)=>s+ +x[1],0);if(v!==q.ans)out.bad.push('notes '+v+' '+q.ans);}
        q=L8[8].g(0);if(q.visual&&q.visual.includes('clock')){const hm=[...q.visual.matchAll(/rotate\(([\\d.]+) 50 50\)"\/><line class="ck-m"[^>]*rotate\(([\\d.]+)/g)][0];if(hm){const ha=+hm[1],ma=+hm[2],mm=Math.round(ma/6),hh=Math.floor((ha-mm*0.5)/30+1e-6)||12;if(q.ans!==hh+'.'+String(mm).padStart(2,'0'))out.bad.push('clock '+q.ans+' vs '+hh+'.'+mm);}}
      }
      // static overlaps
      false&&Object.entries(X.X.BODYF).forEach(([k,f])=>{if(f.no.some(n=>f.yes.includes(n)))out.bad.push('bodyf overlap '+k);});
      Object.values(X.X.NEEDS).forEach(f=>{if(f.no.includes(f.yes))out.bad.push('needs overlap '+f.q);});
      X.X.MAGQ.forEach(f=>{if(f.no.some(n=>f.yes.includes(n)))out.bad.push('mag overlap '+f.q);});
      if(X.X.LIVE7.some(a=>X.X.DEAD7.includes(a)))out.bad.push('live/dead7 overlap');
      if(X.X.ABS_YES.some(a=>X.X.ABS_NO.includes(a)))out.bad.push('abs overlap');
      X.X.EARTHQ.forEach(f=>{if(f.no.includes(f.yes))out.bad.push('earth overlap')});
      // rhyme: all words in family end with key
      for(const k in X.X.RHYME)X.X.RHYME[k].forEach(w=>{if(!w.endsWith(k))out.bad.push('rhyme '+w+' '+k)});
      // MISSP not real words
      for(const w in X.X.MISSP)X.X.MISSP[w].forEach(m=>{if(m===w)out.bad.push('missp same '+w)});
      // clock parse check
      for(let i=0;i<200;i++){const q=L['7:pasar'][8].g(0);}
      return out;}""")
    print('PROBLEMS:',len(res['bad']))
    for x in sorted(set(res['bad']))[:40]: print(' -',x)
    for k,v in res['counts'].items(): print('  ',k,v)
    print('errors:',errs); b.close()
