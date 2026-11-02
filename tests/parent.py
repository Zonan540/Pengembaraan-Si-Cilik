from playwright.sync_api import sync_playwright
import os
SITE=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','site'))
OUT=os.environ.get('OUT','/tmp/si-cilik-out/')
os.makedirs(OUT,exist_ok=True)
BASE='file://'+SITE+'/index.html'
D=OUT
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':412,'height':915},device_scale_factor=2); ctx.grant_permissions(['clipboard-read','clipboard-write'])
    pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.on('console',lambda m: errs.append(m.text) if m.type=='error' and 'ERR_' not in m.text else None)
    pg.goto(BASE); pg.wait_for_timeout(2900)   # NO #uji: real play
    pg.click('[data-act=add]'); pg.fill('#pName','Amin'); pg.click('[data-age="6"]'); pg.click('#addForm button[type=submit]'); pg.wait_for_timeout(400)
    pg.click('.place[data-z=pasar]'); pg.wait_for_timeout(300)
    def play(level,wrong):
        pg.click('.stone[data-i="%d"]'%level); pg.wait_for_timeout(350)
        for qi in range(6):
            q=pg.evaluate('()=>{var r=window.__siCilik.S.run,q=r.qs[r.i];return {ans:String(q.ans),k:q.kind||"c",price:q.price||0}}')
            if q['k']=='coins':
                r=q['price']
                for c in [50,20,10,5]:
                    while r>=c: pg.click('.drawer [data-c="%d"]'%c); r-=c
                pg.click('#payBtn')
            else:
                if qi<wrong: pg.locator('.opt:not([data-v="%s"])'%q['ans']).first.click(); pg.wait_for_timeout(120)
                pg.click('.opt[data-v="%s"]'%q['ans'])
            pg.wait_for_timeout(1400)
        pg.click('[data-act=toPath]'); pg.wait_for_timeout(250)
    play(0,0); play(1,2); play(2,4)   # 3 stars, 2 stars, 1 star
    pg.click('[data-act=toMap]'); pg.wait_for_timeout(200); pg.click('[data-act=toPlayers]'); pg.wait_for_timeout(300)
    pg.screenshot(path=D+'p-players.png',full_page=True)
    # gate: wrong then right
    pg.click('[data-act=parent]'); pg.wait_for_timeout(200)
    pg.fill('#gAns','1'); pg.press('#gAns','Enter'); print('wrong ->',pg.inner_text('#gErr'),'| screen',pg.evaluate('()=>window.__siCilik.S.screen'))
    pg.screenshot(path=D+'p-gate.png')
    ans=pg.evaluate('()=>window.__siCilik.S.gate.ans'); pg.fill('#gAns',str(ans)); pg.press('#gAns','Enter'); pg.wait_for_timeout(300)
    print('after correct, screen:',pg.evaluate('()=>window.__siCilik.S.screen'))
    pg.screenshot(path=D+'p-parent.png',full_page=True)
    txt=pg.inner_text('.screen'); 
    for s in ['Amin','6 tahun','Tahap 2','Tahap 3','kali cuba','belum lulus','Versi 5.0']: print(s, s in txt)
    # export, then reset, then import
    code=pg.input_value('#expBox'); print('code ok:',code.startswith('SICILIK1:'),len(code))
    pg.click('[data-act=preset]'); pg.click('[data-act=pyes]'); pg.wait_for_timeout(200)
    print('after reset stars:',pg.evaluate('()=>window.__siCilik.DB().players[0].progress'))
    pg.fill('#impBox','SICILIK1:garbage'); pg.click('[data-act=pimport]'); print('bad import toast:',pg.inner_text('.toast'))
    pg.fill('#impBox',code); pg.click('[data-act=pimport]'); pg.click('[data-act=pyes]'); pg.wait_for_timeout(200)
    print('after import:',pg.evaluate('()=>window.__siCilik.DB().players[0].progress'))
    # uji toggle
    pg.click('[data-act=puji]'); print('uji on:',pg.evaluate('()=>window.__siCilik.DB().uji'))
    pg.click('[data-act=puji]'); print('uji off:',pg.evaluate('()=>window.__siCilik.DB().uji'))
    # delete
    pg.click('[data-act=pdel]'); pg.click('[data-act=pyes]'); pg.wait_for_timeout(200); print('players after delete:',pg.evaluate('()=>window.__siCilik.DB().players.length'))
    # leaving parent resets access: go back then check direct render guard
    pg.click('[data-act=toPlayers]'); pg.wait_for_timeout(200)
    print('parentOK after leaving:',pg.evaluate('()=>!!window.__siCilik.S.parentOK'))
    # QR still decodes from the rendered page
    pg.screenshot(path=D+'p-players2.png',full_page=True)
    print('errors:',errs); b.close()
