from playwright.sync_api import sync_playwright
import os
SITE=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','site'))
OUT=os.environ.get('OUT','/tmp/si-cilik-out/')
os.makedirs(OUT,exist_ok=True)
BASE='file://'+SITE+'/index.html'
D=OUT
VPS=[('phoneS',360,640),('phone',412,915),('phoneL',915,412),('tabP',768,1024),('tabL',1280,800),('desk',1920,1080)]
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,w,h in VPS:
        ctx=b.new_context(viewport={'width':w,'height':h},device_scale_factor=1,has_touch=w<1000)
        pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
        pg.goto(BASE+'#uji'); pg.wait_for_timeout(2800)
        pg.click('[data-act=add]'); pg.fill('#pName','Aman'); pg.click('[data-age="8"]'); pg.click('#addForm button[type=submit]'); pg.wait_for_timeout(500)
        pg.screenshot(path=D+f'r-{name}-map.png')
        pg.click('.place[data-z=enjin]'); pg.wait_for_timeout(500); pg.screenshot(path=D+f'r-{name}-path.png')
        pg.click('.stone[data-i="0"]'); pg.wait_for_timeout(500); pg.screenshot(path=D+f'r-{name}-play.png')
        m=pg.evaluate("()=>({z:getComputedStyle(document.documentElement).getPropertyValue('--z'),sw:document.documentElement.scrollWidth,iw:innerWidth,sh:document.documentElement.scrollHeight,ih:innerHeight})")
        print(name,w,h,m,'hscroll!' if m['sw']>m['iw']+1 else 'ok',errs)
        ctx.close()
    b.close()
