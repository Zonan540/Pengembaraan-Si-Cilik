from playwright.sync_api import sync_playwright
import os
SITE=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','site'))
OUT=os.environ.get('OUT','/tmp/si-cilik-out/')
os.makedirs(OUT,exist_ok=True)
BASE='file://'+SITE+'/index.html'
D=OUT
SHOTS={('reban',0):'z-r1',('reban',2):'z-r3',('reban',5):'z-r6',('reban',7):'z-r8',('taman',1):'z-t2',('taman',3):'z-t4',('taman',4):'z-t5',('taman',6):'z-t7',('taman',7):'z-t8',('taman',8):'z-t9'}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':400,'height':860},device_scale_factor=2)
    errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.on('console',lambda m: errs.append(m.text) if m.type=='error' and 'ERR_' not in m.text else None)
    pg.goto(BASE+'#uji'); pg.wait_for_timeout(2900)
    pg.click('[data-act=add]'); pg.fill('#pName','Amin'); pg.click('[data-age="6"]'); pg.click('#addForm button[type=submit]'); pg.wait_for_timeout(400)
    for zone in ['reban','taman']:
        pg.click('.place[data-z=%s]'%zone); pg.wait_for_timeout(400)
        for L in range(10):
            pg.click('.stone[data-i="%d"]'%L); pg.wait_for_timeout(350)
            for qi in range(6):
                q=pg.evaluate('()=>{var r=window.__siCilik.S.run,q=r.qs[r.i];return {ans:String(q.ans),n:q.opts.length}}')
                if (zone,L) in SHOTS and qi==0: pg.screenshot(path=D+SHOTS[(zone,L)]+'.png',full_page=True)
                pg.click('.opt[data-v="%s"]'%q['ans']); pg.wait_for_timeout(1400)
            stars=pg.locator('#bigstars use[href="#i-star"]').count()
            assert stars==3,(zone,L,stars)
            pg.click('[data-act=toPath]'); pg.wait_for_timeout(250)
        print(zone,'all 10 levels = 3 stars each')
        pg.click('[data-act=toMap]'); pg.wait_for_timeout(250)
    print('total stars:',pg.inner_text('.starchip'))
    # wrong-answer path on a Sains level, gentle feedback text
    pg.click('.place[data-z=reban]'); pg.click('.stone[data-i="1"]'); pg.wait_for_timeout(400)
    q=pg.evaluate('()=>{var q=window.__siCilik.S.run.qs[0];return String(q.ans)}')
    pg.locator('.opt:not([data-v="%s"])'%q).first.click(); pg.wait_for_timeout(200)
    print('wrong feedback:',pg.inner_text('#kSay'))
    print('errors:',errs); b.close()
