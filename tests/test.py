from playwright.sync_api import sync_playwright
import os
SITE=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','site'))
OUT=os.environ.get('OUT','/tmp/si-cilik-out/')
os.makedirs(OUT,exist_ok=True)
URL='file://'+SITE+'/index.html'
D=OUT
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':400,'height':860},device_scale_factor=2)
    errs=[]
    pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.on('console',lambda m: errs.append(m.text) if m.type=='error' and 'ERR_' not in m.text else None)
    pg.goto(URL); pg.wait_for_timeout(900)
    pg.screenshot(path=D+'s1-splash.png')
    pg.wait_for_timeout(2200)
    assert pg.locator('[data-act=add]').count()==1, 'no players screen'
    pg.click('[data-act=add]'); pg.click('#addForm button[type=submit]'); pg.wait_for_timeout(100)
    print('empty name err:', pg.inner_text('#addErr'))
    pg.fill('#pName','Amin'); pg.click('[data-age="6"]'); pg.click('#addForm button[type=submit]'); pg.wait_for_timeout(500)
    pg.screenshot(path=D+'s2-map.png',full_page=True)
    pg.click('.place[data-z=reban]'); pg.wait_for_timeout(200); print('locked toast:', pg.inner_text('.toast'))
    pg.click('.place[data-z=pasar]'); pg.wait_for_timeout(500)
    pg.click('.stone[data-i="1"]'); pg.wait_for_timeout(200); print('locked level toast:', pg.inner_text('.toast'))
    pg.screenshot(path=D+'s3-path.png')
    def answer_all(level, wrong_count=0):
        pg.click('.stone[data-i="%d"]'%level); pg.wait_for_timeout(450)
        made=0
        for qi in range(6):
            q=pg.evaluate('()=>{var r=window.__siCilik.S.run,q=r.qs[r.i];return {kind:q.kind||"choice",ans:String(q.ans),price:q.price||0,prompt:q.prompt}}')
            if q['kind']=='coins':
                if made<wrong_count:
                    pg.click('[data-c="50"]');pg.click('[data-c="50"]');pg.click('#payBtn');made+=1;pg.wait_for_timeout(150);pg.click('[data-act=clearcoins]')
                r=q['price']
                for c in [50,20,10,5]:
                    while r>=c: pg.click('.drawer [data-c="%d"]'%c); r-=c
                if level==9 and qi==0: pg.screenshot(path=D+'s6-coins.png',full_page=True)
                pg.click('#payBtn')
            else:
                if made<wrong_count:
                    w=pg.locator('.opt:not([data-v="%s"])'%q['ans']).first; w.click(); made+=1; pg.wait_for_timeout(150)
                if (level,qi) in [(0,0),(5,0),(7,1)]:
                    frs=pg.locator('button.fr'); 
                    for k in range(min(3,frs.count())): frs.nth(k).click()
                    pg.screenshot(path=D+'s4-L%d.png'%(level+1),full_page=True)
                if (level,qi) in [(2,0),(3,0),(8,0)]: pg.screenshot(path=D+'s5-L%d.png'%(level+1),full_page=True)
                pg.click('.opt[data-v="%s"]'%q['ans'])
            pg.wait_for_timeout(1450)
        h=pg.inner_text('.sheet h2'); stars=pg.locator('#bigstars use[href="#i-star"]').count()
        return h,stars
    # level 1: 3 wrong -> 1 star, should not unlock
    print('L1 3 wrong:', answer_all(0,3))
    pg.click('[data-act=toPath]'); pg.wait_for_timeout(300)
    print('L2 open after 1 star?', 'locked' not in pg.get_attribute('.stone[data-i="1"]','class'))
    print('L1 again 1 wrong:', answer_all(0,1))
    pg.click('[data-act=toPath]'); pg.wait_for_timeout(300)
    print('L2 open after 2 stars?', 'locked' not in pg.get_attribute('.stone[data-i="1"]','class'))
    for L in range(1,10):
        res=answer_all(L,0)
        print('L%d:'%(L+1),res)
        if L==9: pg.screenshot(path=D+'s7-result.png'); print('unlock msg:', pg.locator('.unlock').all_inner_texts())
        pg.click('[data-act=toPath]'); pg.wait_for_timeout(300)
    pg.click('[data-act=toMap]'); pg.wait_for_timeout(300)
    print('reban state:', pg.get_attribute('.place[data-z=reban]','data-st'), '| total stars', pg.inner_text('.starchip'))
    # quit flow
    pg.click('.place[data-z=pasar]'); pg.wait_for_timeout(300); pg.click('.stone[data-i="0"]'); pg.wait_for_timeout(300)
    pg.click('[data-act=quit]'); pg.wait_for_timeout(100); pg.click('[data-act=stay]'); print('stay ok:', pg.locator('.overlay').count()==0)
    # age 8 profile
    pg.click('[data-act=quit]'); pg.click('.sheet [data-act=toPath]'); pg.click('[data-act=toMap]'); pg.click('.who')
    pg.click('[data-act=add]'); pg.fill('#pName','Aman'); pg.click('[data-age="8"]'); pg.click('#addForm button[type=submit]'); pg.wait_for_timeout(500)
    pg.screenshot(path=D+'s8-space.png',full_page=True)
    pg.click('.who'); pg.wait_for_timeout(300); pg.screenshot(path=D+'s9-players.png',full_page=True)
    # persistence
    pg.reload(); pg.wait_for_timeout(2900)
    print('players after reload:', pg.locator('.player:not(.add)').count())
    print('errors:', errs)
    b.close()
