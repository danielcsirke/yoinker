# Yoinker — lépésről lépésre útmutató

🇬🇧 [In English: GUIDE.md](GUIDE.md)

Ez a leírás semmit nem feltételez. Ha meg tudsz nyitni egy weboldalt és ki tudsz másolni egy szöveget, menni fog.

---

## 1. rész — A Yoinker felrakása a gépre

### Windows

1. Kattints ide: **https://github.com/danielcsirke/yoinker/releases/latest**
2. Görgess kicsit lejjebb az **Assets** szóig. Kattints a **`Yoinker-Windows.exe`** fájlra. Letöltődik (pár másodperc).
3. Nyisd meg a **Letöltések** mappát, és kattints duplán a **Yoinker-Windows.exe** fájlra.
4. Felugorhat egy kék ablak: **"A Windows megvédte a számítógépet"**. Ez minden olyan kis programnál előjön, amit nem a Microsoft Store-ban árulnak.
   Kattints a kis **További információ** szövegre, aztán a **Futtatás mindenképp** gombra.
5. Megnyílik a Yoinker. Ennyi — nincs telepítő.

   *Tipp:* húzd ki a **Yoinker-Windows.exe** fájlt a Letöltésekből az Asztalra, hogy legközelebb megtaláld.

### Mac

1. Kattints ide: **https://github.com/danielcsirke/yoinker/releases/latest**
2. Az **Assets** résznél kattints a **`Yoinker-macOS.dmg`** fájlra.
3. Nyisd meg a letöltött fájlt. Megjelenik egy kis ablak a **Yoinker** ikonnal és egy **Applications** mappával. Húzd a Yoinkert az Applications-re.
4. Nyisd meg az **Applications** (Programok) mappát (Finder → Applications), keresd meg a **Yoinker**t.
5. **Csak az első alkalommal:** tartsd lenyomva a **Control** billentyűt, és úgy kattints a Yoinkerre (vagy jobb klikk), válaszd a **Megnyitás**t, majd a felugró ablakban megint a **Megnyitás**t.
   (Ha csak duplán kattintasz, a Mac azt írja: *"A Yoinker nem nyitható meg, mert az Apple nem tudja ellenőrizni"* — ez azért van, mert ez egy ingyenes program, nem az App Store-ból. A jobb klikkes trükkel megmondod a Macnek, hogy megbízol benne. Csak egyszer kell.)
6. Megnyílik a Yoinker. Ezután már simán dupla kattintással indítható, mint bármi más.

### Linux

1. Kattints ide: **https://github.com/danielcsirke/yoinker/releases/latest**
2. Az **Assets** résznél kattints a **`Yoinker-Linux`** fájlra.
3. A fájlkezelőben jobb klikk a letöltött **Yoinker-Linux** fájlon → **Tulajdonságok** → **Jogosultságok** → pipáld be: **"Fájl végrehajtásának engedélyezése programként"** (a pontos szöveg rendszerenként kicsit eltér).
4. Dupla kattintás. Megnyílik a Yoinker.

---

## 2. rész — Letöltés

Az ablakban három számozott lépés van és egy nagy gomb.

### 1. lépés — A link beillesztése

1. A böngészőben menj a videóra (vagy zenére), amit szeretnél.
2. Kattints egyszer a **címsorba** a böngésző legtetején (ahol olyasmi van, hogy `https://www.youtube.com/watch?v=...`). Az egész cím kijelölődik.
3. Másold ki: **Ctrl+C** (Windows/Linux) vagy **Cmd+C** (Mac). Vagy jobb klikk → Másolás.
4. Menj át a Yoinkerbe, és nyomd meg a **Beillesztés** gombot. A link megjelenik a mezőben.

### 2. lépés — Mit szeretnél?

- **Videó** — egy normál videófájlt kapsz (MP4). Mellette válaszd ki a minőséget:
  - **Legjobb** — a legjobb, ami az oldalon van (legnagyobb fájl).
  - **Jó (1080p)** — tévére, laptopra tökéletes.
  - **Közepes (720p)** — telefonra elég, kisebb fájl.
  - **Kis fájl (480p)** — ha kevés a hely vagy lassú a net.
- **Csak zene (MP3)** — csak a hangot kapod, MP3-ban, amit bármilyen telefonra vagy lejátszóra rá lehet tenni.

*Lejátszási lista pipa:* ha a link egy egész lejátszási lista/album, és az egészet akarod, pipáld be: **"Ha a link egy lejátszási lista, töltsd le az egészet"**. Ha nincs bepipálva, csak az egy videót kapod.

### 3. lépés — Hova mentsem?

A Yoinker kiírja, melyik mappát fogja használni. Alapból ez a **Letöltések → Yoinker**, ami jó is. Ha máshova szeretnéd (pl. pendrive-ra), nyomd meg a **Mappa módosítása...** gombot, és válassz egyet. A Yoinker megjegyzi.

### Nyomd meg a LETÖLTÉS gombot

A csík töltődik, alatta a szöveg mondja, mi történik: *Letöltés... 43%*, aztán *Mindjárt kész, a fájl befejezése...*, végül **Kész!**

Nyomd meg **A mappa megnyitása** gombot — ott a fájlod, a videó címével elnevezve.

Ha le akarod állítani, nyomd meg a **Leállítás** gombot.

---

## 2/b. rész — A Haladó fül (nyugodtan kihagyhatod)

Az ablak tetején két fül van: **Letöltés** (ezt használtad az előbb) és **Haladó**. A Haladóra soha *nincs szükséged*. Annak az egy ismerősnek van ott, aki tudja, mi az a kodek. Minden automatikusan mentődik, és az **Alapértelmezések visszaállítása** gomb mindent visszarak.

| Beállítás | Mit csinál |
|---|---|
| **Videó kódolás** | A *Mindenhol lejátszható (H.264 + AAC)* az alapértelmezés, ezért nyílnak meg a fájljaid bármelyik Windowson, tévén, telefonon. A *Legjobb minőség* azt veszi, ami az oldalon van (sokszor AV1/VP9) — kisebb és élesebb, de a Windows Media Player és sok tévé nem hajlandó lejátszani. |
| **Videófájl típusa** | mp4 (alap), mkv vagy webm. |
| **Zenefájl típusa / minősége** | mp3 (alap) 128/192/256/320 kbps-en, vagy m4a, opus, flac, wav. |
| **Borítókép beletétele a fájlba** | A videó előnézeti képe lesz az MP3 albumborítója / az MP4 posztere. |
| **Feliratok letöltése** | Nyelvek kódokkal, vesszővel elválasztva, pl. `hu,en`. A *beletéve a videóba* beágyazza, így bármelyik lejátszóban bekapcsolható. |
| **Bejelentkezés átvétele a böngészőből** | A Yoinker beolvassa a kiválasztott böngésző sütijeit, így a *bejelentkezés kell* vagy *korhatáros* videók is mennek, ha ott be vagy lépve. Windowson előbb zárd be a böngészőt. |
| **Fájlnév minta** | A yt-dlp kimeneti sablonja. Alap: `%(title).150B [%(id)s].%(ext)s`. |
| **Sebességkorlát** | pl. `2M` = 2 MB/mp, hogy a letöltés ne egye meg a ház netjét. Üresen = nincs korlát. |
| **Extra yt-dlp paraméterek** | Bármi a `yt-dlp --help`-ből, pl. `--embed-chapters`. Rossz kapcsolót a csík alatt kiírja, semmi nem romlik el. |
| **Extra FFmpeg paraméterek** | Minden FFmpeg lépés megkapja, pl. `-threads 2`. |

---

## 3. rész — Gyakori kérdések

**Letöltöttem egy videót, és a Windows nem játssza le / nincs kép.** Nyisd meg a **Haladó** fület, és nézd meg, hogy a *Mindenhol lejátszható (H.264 + AAC)* van-e kiválasztva (alapból az van, hacsak valaki át nem állította), aztán töltsd le újra. Vagy telepítsd a [VLC](https://www.videolan.org/)-t, az mindent lejátszik.

**Ingyenes? Mi a trükk?** Ingyenes, nincs fiók, nincs reklám. A "minden jog fenntartva" csak annyit jelent, hogy magát a programot nem szabad másolni vagy árulni.

**Más oldalról is tudok tölteni, nem csak YouTube-ról?** Igen — a legtöbb videós és zenés oldal megy. Illeszd be a linket, és próbáld ki.

**Hol van a nyelv beállítás?** Az ablak bal alsó sarkában. A Yoinker magyarul indul, ha a géped magyar, különben angolul.

**Nagyon hosszú a videó / egész lejátszási lista — meddig tart?** A netedtől függ. A csík alatti szöveg mutatja a sebességet és hogy hány másodperc van hátra.

**Múlt hónapban ment, most azt írja, az oldal elutasította a letöltést.** A videós oldalak gyakran változtatnak a rendszerükön. Töltsd le a legújabb Yoinkert a **[Letöltések oldalról](https://github.com/danielcsirke/yoinker/releases/latest)**, és cseréld le a régit. Ez az esetek 95%-ában megoldja.

**Valami más a baj.** Nézd meg a **[HIBAELHARITAS.md](HIBAELHARITAS.md)** oldalt. Ha az sem segít, nyomd meg a **Részletek (csak segítőnek)** gombot az ablak alján, másold ki a megjelenő szöveget, és küldd el annak, akitől a Yoinkert kaptad.
