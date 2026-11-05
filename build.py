#!/usr/bin/env python3
# 実行: python3 build.py  → index.html を作り直す（CSSは既存index.htmlの<style>、地図の下地は akiba-where-to-eat から流用）
import re,os
cur=open('index.html').read()
css=re.findall(r'<style>(.*?)</style>',cur,flags=re.S)[-1]
src=open(os.path.expanduser('~/akiba-where-to-eat/index.html')).read()
svg0=re.search(r'<svg id="map".*?</svg>',src,flags=re.S).group(0)
base=svg0[:svg0.index('<line x1="376" y1="231"')].rstrip().replace('Simple sketch map of the 14 places','Simple sketch map of the 7 places')
lat0,lon0=35.69836,139.77311
def xy(la,lo): return round(425+(lo-lon0)*90350*0.44), round(249-(la-lat0)*111200*0.44)
# n, tile tag, short, name, img, genre, jp, text, hours(strip), hrs line, maps query, lat, lon
P=[
(1,"Goods","ANIMATE","ANIMATE AKIHABARA","animate.jpg","Anime goods, many series","アニメイト秋葉原","Several floors of anime and manga goods from many series. The Annex building has a floor of capsule toys.","10:00 to 21:00","10:00 to 21:00, open daily (official site, checked on 5 Nov 2026)","Animate Akihabara",35.700405,139.771667),
(2,"Figures","RADIO KAIKAN","AKIHABARA RADIO KAIKAN","radio-kaikan.jpg","Figures, cards, character goods","秋葉原ラジオ会館","A tall building full of small shops on every floor: figures, trading cards and character goods. We pick the floors that match your favourites.",None,None,"Akihabara Radio Kaikan",35.69788,139.77194),
(3,"Prizes","TRADER","TRADER","trader.jpg","Prize figures","トレーダー","Big and bright, with many prize figures at good prices.",None,None,"Trader Akihabara main store",35.7009,139.7713),
(4,"Character wear","COSPA","COSPA G-STORE AKIBA","cospa.jpg","Character clothes and goods","コスパ ジーストア・アキバ店","Character apparel and goods, and cosplay costumes, on the 4th floor of the Onoden main building. The photo shows the building.","10:00 to 20:00","10:00 to 20:00, no regular day off (official site, checked on 5 Nov 2026)","COSPA G-STORE Akiba Onoden",35.698345,139.771072),
(5,"Second-hand","BOOK OFF","BOOKOFF AKIHABARA EKIMAE","book-off.jpg","Second-hand manga, games, cards","ブックオフ 秋葉原駅前店","Second-hand manga, CDs, DVDs, game software and hobby goods. A good place to find old volumes and cheap games. The photo shows another Book Off branch.","10:00 to 22:00","10:00 to 22:00, open daily (official site, checked on 5 Nov 2026)","BOOKOFF Akihabara Ekimae",35.697826,139.773346),
(6,"Capsule toys","GACHAPON KAIKAN","AKIHABARA GACHAPON KAIKAN","gachapon.jpg","Capsule toys","秋葉原ガチャポン会館","A shop with hundreds of capsule toy machines. Stefan can try a few and keep what comes out.","Opens at 11:00","Opens at 11:00 (closing time not confirmed, please check at the door)","Akihabara Gachapon Kaikan",35.70185,139.77125),
(7,"Arcade","GIGO","GIGO AKIHABARA","gigo.jpg","Arcade and crane games","GiGO 秋葉原","An arcade with crane games and prizes, a good place to play for a while.",None,None,"GiGO Akihabara 3",35.699192,139.770889),
]
N={p[0]:p for p in P}
clock='<svg viewBox="0 0 16 16" width="15" height="15" aria-hidden="true"><circle cx="8" cy="8" r="6.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8 4.5V8l2.5 1.8" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
def tile(p): n,tag,short=p[0],p[1],p[2]; return f'<a class="tile" href="#p{n}"><img src="img/{p[4]}" alt="" loading="lazy"><b class="no">{n:02d}</b><span class="tt">{tag}</span><span class="tn">{short}</span></a>'
def card(p):
    n,_,_,title,img,genre,jp,tx,hours,hrs,maps=p[:11]
    strip=''
    if hours: strip=f'<p class="strip"><span class="hr">{clock}<b class="today">{hours}</b></span></p><p class="hrs">{hrs}</p>'
    q=maps.replace(' ','+')
    return f'<article class="card" id="p{n}"><div class="hd"><span class="big">{n:02d}</span><div><span class="genre">{genre}</span><h3>{title}</h3></div></div><img class="ph" src="img/{img}" alt="" loading="lazy"><p class="jp" lang="ja">{jp}</p><p class="tx">{tx}</p>{strip}<div class="bt"><a class="btn" href="https://www.google.com/maps/search/?api=1&amp;query={q}">Google Maps <i>&rarr;</i></a></div></article>'
pins=''
for p in P:
    n,name=p[0],p[2].title(); la,lo=p[11],p[12]; x,y=xy(la,lo); w=len(name)*9+24
    pins+=f'<a class="pin" href="#p{n}" data-n="{n}"><circle cx="{x}" cy="{y}" r="16" fill="#121212" stroke="#fff" stroke-width="3"/><text x="{x}" y="{y+6}" text-anchor="middle" font-size="16" font-weight="900" fill="#fff">{n}</text><g class="lbl"><rect x="{x-w//2}" y="{y-46}" width="{w}" height="28" fill="#121212"/><text x="{x}" y="{y-27}" text-anchor="middle" font-size="14" font-weight="800" fill="#fff">{name}</text></g></a>'
mapsvg=base+pins+'</svg>'
meet=("11:00","Meet inside Vie de France","The bakery café near Akihabara station. Use the map link in my message, because there is another Vie de France on the other side of the station.")
lunch=lambda t,n:(t,"Lunch or a snack, only if you want",n)
R=[("A","Figures first","For One Piece, Pok&eacute;mon and Jujutsu Kaisen goods. The big shops first, then clothes and capsule toys.",[
 meet,("11:10",1,"about 35 min"),("11:50",2,"about 30 min"),("12:25",3,"about 20 min"),("12:50",4,"about 30 min"),
 lunch("13:20","If you skip it, we stay longer at the shops."),("13:55",6,"capsule toys, about 25 min"),("14:20","Last look, then goodbye","We finish near the station at 14:45.")]),
("B","Second-hand finds","Old volumes, cheap games and cards first, then the goods shops.",[
 meet,("11:10",5,"look through manga, games and cards, about 45 min"),("12:00",4,"about 30 min"),("12:35",2,"about 30 min"),
 lunch("13:10","If you skip it, we stay longer at the shops."),("13:45",1,"about 35 min"),("14:20","Last look, then goodbye","We finish near the station at 14:45.")]),
("C","Games and capsule toys","More time to play, then the goods shops.",[
 meet,("11:10",6,"try a few machines, about 40 min"),("11:55",7,"crane games and prizes, about 45 min"),
 lunch("12:45","If you skip it, we play longer."),("13:20",3,"about 25 min"),("13:45",2,"about 35 min"),("14:20","Last look, then goodbye","We finish near the station at 14:45.")])]
routes=''
for L,name,desc,steps in R:
    routes+=f'<section class="route" id="route-{L}"><div class="hd"><span class="big">{L}</span><div><span class="genre">Model route</span><h3>{name.upper()}</h3></div></div><p class="tx">{desc}</p><ul class="tl">'
    for s in steps:
        if isinstance(s[1],int):
            n=s[1]; routes+=f'<li><b>{s[0]}</b><span><a href="#p{n}" style="color:inherit;font-weight:800">{n:02d} {N[n][3].title()}</a><em>{s[2]}</em></span></li>'
        else: routes+=f'<li><b>{s[0]}</b><span>{s[1]}<em>{s[2]}</em></span></li>'
    routes+='</ul></section>'
def sec(title,rng,ids,cls,red=False): return f'<section><div class="bar{" r" if red else ""}"><h2>{title}</h2><span>{rng}</span></div><div class="wall {cls}">'+''.join(tile(N[i]) for i in ids)+'</div></section>'
html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>Akihabara for Yulia and Stefan</title><meta name="robots" content="noindex,nofollow">
<meta name="description" content="Seven places to visit in Akihabara: figure and anime goods shops, Cospa, Book Off, capsule toys and games, with three model routes.">
<meta property="og:title" content="Akihabara for Yulia and Stefan"><meta property="og:description" content="Figure shops, second-hand finds, capsule toys and games.">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 64 64%22%3E%3Crect width=%2264%22 height=%2264%22 fill=%22%23D9342B%22/%3E%3C/svg%3E">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=Noto+Sans+JP:wght@500;700;900&display=swap" rel="stylesheet">
<style>{css}</style></head><body>
<div class="col"><div class="top"><span>GUEST GUIDE</span><span>AKIHABARA &middot; 7 PLACES</span></div>
<h1>Places to visit in <em>Akihabara</em></h1></div>
<div class="col" style="padding:0"><div class="hero"><img src="img/hero.jpg" alt="Akihabara at night"><div class="vt">秋葉原</div></div>
<div class="hb"><span>Fri 6 Nov &middot; 11:00 to 14:45</span><b>Meet inside Vie de France</b></div></div>
<div class="col"><p class="gp" style="margin-top:18px">Yulia and Stefan, this page shows places we can visit and three model routes. Pick one, or mix your own. Tell me your favourites (One Piece, Pok&eacute;mon, Jujutsu Kaisen, Death Note, or anything else) and we go where they are. You do not need to buy anything.</p>
<div class="maphd"><h2 class="map">The map</h2></div><p class="gp">Tap a pin to see the name, tap again to jump to the place.</p>{mapsvg}<div class="lg"><span><i class=""></i>All seven are about 5 minutes on foot from the station</span></div>
{sec("FIGURES AND GOODS","1-3",[1,2,3],"w3")}
{sec("CLOTHES AND SECOND-HAND","4-5",[4,5],"w2",True)}
{sec("CAPSULE TOYS AND GAMES","6-7",[6,7],"w2")}
<div class="bar"><h2>THREE ROUTES</h2><span>A &middot; B &middot; C</span></div><p class="gp">Pick one, or mix your own. Times are approximate and we can change as we go.</p>{routes}
{''.join(card(p) for p in P)}</div>
<div class="lunch"><div class="col"><h2>If you want lunch</h2><p>Lunch is not planned. If you would like to eat, tell me what you would like and any allergies or dietary needs, and I will pick a place near wherever we are.</p><p><a class="btn" href="https://yukitchy.github.io/akiba-where-to-eat/">Where to eat in Akihabara <i>&rarr;</i></a></p></div></div>
<details class="crd"><summary>Photo credits and sources</summary><p class="cr">The photos show the kind of place, not always the shop itself. All from Wikimedia Commons: Dick Thomas Johnson (Animate, CC BY 2.0), Aimaimyi (Radio Kaikan, CC BY-SA 3.0), Starchild1884 (Trader, CC BY-SA 3.0), Tokumeigakarinoaoshima (Onoden building for Cospa, and Book Off Tsuruhashi, both CC BY-SA 4.0), Steve Nagata (capsule toys, CC BY 2.0), BWard 1997 (GiGO, CC BY 4.0), ElHeineken (night view, CC BY 4.0). Opening hours for Animate, Cospa and Book Off come from their official sites, checked on November 5. Other hours were not confirmed. The map is a simple sketch, not to scale. Trader's position is approximate. Times are approximate and can move on the day.</p></details>
<script>
(function(){{var coarse=matchMedia('(pointer:coarse)').matches,onPin=null;
document.querySelectorAll('.pin').forEach(function(a){{a.addEventListener('click',function(ev){{ev.preventDefault();if(coarse&&onPin!==a){{if(onPin)onPin.classList.remove('on');onPin=a;a.classList.add('on');return}}var c=document.getElementById('p'+a.dataset.n);if(!c)return;c.scrollIntoView({{behavior:'smooth',block:'start'}});c.classList.add('hit');setTimeout(function(){{c.classList.remove('hit')}},1600);if(onPin){{onPin.classList.remove('on');onPin=null}}}})}});
document.getElementById('map').addEventListener('click',function(ev){{if(!ev.target.closest('.pin')&&onPin){{onPin.classList.remove('on');onPin=null}}}});}})();
</script></body></html>'''
open('index.html','w').write(html); print('built',len(html))
