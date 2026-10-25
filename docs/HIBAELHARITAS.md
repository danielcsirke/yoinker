# Hibaelhárítás

🇬🇧 [In English: TROUBLESHOOTING.md](TROUBLESHOOTING.md)

Keresd meg az üzenetet, amit a Yoinker a csík alatt kiírt.

| A Yoinker azt írja | Mit jelent | Mit csinálj |
|---|---|---|
| *Előbb másolj be egy linket (1. lépés).* | Az 1. lépés mezője üres. | Másold ki a videó címét a böngészőből, és nyomd meg a **Beillesztés** gombot. |
| *Ez nem úgy néz ki, mint egy link.* | Olyat illesztettél be, ami nem webcím. | A linkek `https://`-sel kezdődnek. Kattints a böngésző címsorába, másold ki az egészet. |
| *Az oldal elutasította a letöltést. Szerezd be a legújabb verziót…* | Az oldal változtatott valamin; a nálad lévő Yoinker túl régi. A Yoinker megnyitja neked a Letöltések oldalt. | Töltsd le a legújabb fájlt a [Letöltések oldalról](https://github.com/danielcsirke/yoinker/releases/latest), cseréld le a régit, próbáld újra. |
| *Nincs internetkapcsolat, vagy az oldal nem válaszolt.* | A gép nincs neten, vagy az oldal nem elérhető. | Nézd meg, betöltődik-e egy weboldal a böngészőben. Próbáld újra egy perc múlva. |
| *Ehhez a videóhoz bejelentkezés kell, vagy privát.* | A videó privát, csak tagoknak szól, vagy fiók kell hozzá. | Ha a böngészőben bejelentkezve meg tudod nézni: **Haladó fül → Bejelentkezés átvétele a böngészőből → válaszd ki azt a böngészőt** (Windowson előbb zárd be), aztán próbáld újra. Különben nincs mit tenni. |
| *Ez a videó korhatáros…* | Ugyanaz, 18+-os videóknál. | Ugyanaz. |
| *Ez a videó nem érhető el (törölték, privát vagy le van tiltva).* | A videó eltűnt vagy el van rejtve. | Nézd meg, lejátszódik-e még a böngészőben. |
| *Ez a videó a te országodban nem érhető el.* | A feltöltő letiltotta az országodat. | Nincs mit tenni. |
| *Ez a link nem támogatott.* | A link nem videóoldal (pl. egy csatorna főoldala vagy egy keresés). | Nyisd meg magát a videót, és azt a címet másold. |
| *Nem sikerült menteni a fájlt.* | A mappa csak olvasható, vagy tele a lemez. | Nyomd meg a **Mappa módosítása...** gombot, és válaszd pl. az Asztalt. Szabadíts fel helyet. |
| *A Yoinkerben lévő átalakító nem működik.* | Sérült a programfájl. | Töltsd le újra a Yoinkert. |
| *A Haladó fülön egy beállítás hibás: …* | Valami, amit a Haladó fülre írtak (yt-dlp kapcsoló, sebességkorlát), nem érvényes; az üzenet vége megmondja, mi. | Javítsd, vagy nyomd meg az **Alapértelmezések visszaállítása** gombot a Haladó fülön. |
| (nincs hiba, de) a videót a Windows nem játssza le / nincs kép | A fájl AV1/VP9, amit a Windows Media Player nem tud. Csak akkor fordul elő, ha a Haladó fülön a *Legjobb minőség* volt kiválasztva. | Haladó fül → *Mindenhol lejátszható (H.264 + AAC)* → töltsd le újra. Vagy telepíts VLC-t. |
| *A letöltés nem sikerült. Nyisd meg a 'Részletek'-et…* | Valami szokatlan. | Nyomd meg a **Részletek (csak segítőnek)** gombot, másold ki a szöveget, küldd el a segítődnek. |

## Gondok, mielőtt egyáltalán elindulna

**Windows: "A Windows megvédte a számítógépet".** Kattints: **További információ → Futtatás mindenképp**. Azért jön elő, mert a Yoinker nincs fizetős tanúsítvánnyal aláírva. Biztonságos.

**Windows: a vírusirtó törli/karanténba teszi a fájlt.** Néhány vírusirtó gyanakszik minden programra, ami nem közismert. Állítsd vissza a karanténból és adj hozzá kivételt, vagy szólj a segítődnek.

**Mac: "A Yoinker nem nyitható meg, mert az Apple nem tudja ellenőrizni, hogy nem tartalmaz-e kártékony szoftvert".** Jobb klikk (vagy Control+kattintás) a Yoinkeren → **Megnyitás** → **Megnyitás**. Csak első alkalommal kell.

**Mac: "A Yoinker sérült, és nem nyitható meg."** Újabb macOS-en fordul elő, ha bizonyos böngészőkkel töltötted le. Nyisd meg a **Terminált** (kérj segítséget), és futtasd:
`xattr -cr /Applications/Yoinker.app` — utána nyisd meg normálisan.

**Linux: a dupla kattintás nem csinál semmit.** Tedd futtathatóvá: jobb klikk → Tulajdonságok → Jogosultságok → "Fájl végrehajtásának engedélyezése programként". Nagyon minimális rendszerről hiányozhatnak az alap X11 könyvtárak is.

**Megnyílik, de pici az ablak / összecsúszik a szöveg.** Húzd szélesebbre az ablakot. Ha nagyon nagy a kijelző-nagyítás, mondd meg a segítődnek, milyen rendszer és hány %-os nagyítás.

## Segítőknek

A **Részletek** doboz a yt-dlp saját naplója. Másold ki, és keress rá az üzenetre itt: https://github.com/yt-dlp/yt-dlp/issues — a legtöbb gond oldalváltozás, amit a yt-dlp napokon belül javít. Utána adj ki új Yoinkert: lásd [MAINTAINERS.md](MAINTAINERS.md).
