from playwright.sync_api import sync_playwright
import os
SITE=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','site'))
OUT=os.environ.get('OUT','/tmp/si-cilik-out/')
os.makedirs(OUT,exist_ok=True)
BASE='file://'+SITE+'/index.html'
D=OUT
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':400,'height':860},device_scale_factor=2)
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.on('console',lambda m: errs.append(m.text) if m.type=='error' and 'ERR_' not in m.text else None)
    pg.goto(BASE+'#uji'); pg.wait_for_timeout(2900)
    pg.click('[data-act=add]'); pg.fill('#pName','Aman'); pg.click('[data-age="8"]'); pg.click('#addForm button[type=submit]'); pg.wait_for_timeout(400)
    pg.screenshot(path=D+'a8-map.png')
    for zone in ['enjin','makmal','komunikasi']:
        pg.click('.place[data-z=%s]'%zone); pg.wait_for_timeout(400)
        if zone=='enjin': pg.screenshot(path=D+'a8-path.png')
        for L in range(10):
            pg.click('.stone[data-i="%d"]'%L); pg.wait_for_timeout(350)
            for qi in range(6):
                q=pg.evaluate('()=>{var r=window.__siCilik.S.run,q=r.qs[r.i];return {kind:q.kind||"c",ans:String(q.ans),price:q.price||0}}')
                if qi==0: pg.screenshot(path=D+'a8-%s%d.png'%(zone[0],L+1))
                if q['kind']=='coins':
                    r=q['price']
                    for c in [50,20,10,5,1]:
                        while r>=c: pg.click('.drawer [data-c="%d"]'%c); r-=c
                    if qi==0: pg.screenshot(path=D+'a8-pay.png')
                    pg.click('#payBtn')
                else: pg.click('.opt[data-v="%s"]'%q['ans'])
                if qi==1: pg.screenshot(path=D+'a8-ok-%s%d.png'%(zone[0],L+1)) if L==0 else None
                pg.wait_for_timeout(1400)
            stars=pg.locator('#bigstars use[href="#i-star"]').count()
            assert stars==3,(zone,L,stars)
            pg.click('[data-act=toPath]'); pg.wait_for_timeout(250)
        print(zone,'ok 30/30 stars'); pg.click('[data-act=toMap]'); pg.wait_for_timeout(250)
    print('stars',pg.inner_text('.starchip'),'errors',errs); b.close()
