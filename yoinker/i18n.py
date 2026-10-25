"""Texts shown to the user, in English and Hungarian.

Every key must exist in every language (tests/test_i18n.py checks this).
"""

import locale

LANGUAGES = {"en": "English", "hu": "Magyar"}

STRINGS = {
    "en": {
        "window_title": "Yoinker",
        "step1": "1. Paste the link of the video or song",
        "paste": "Paste",
        "clear": "Clear",
        "step2": "2. What do you want?",
        "kind_video": "Video",
        "kind_audio": "Music only (MP3)",
        "quality": "Quality:",
        "q_best": "Best",
        "q_1080": "Good (1080p)",
        "q_720": "Medium (720p)",
        "q_480": "Small file (480p)",
        "playlist": "If the link is a playlist, download all of it",
        "step3": "3. Where should it be saved?",
        "choose_folder": "Change folder...",
        "download": "DOWNLOAD",
        "cancel": "Stop",
        "open_folder": "Open the folder",
        "details": "Details (only for helpers)",
        "language": "Language:",
        "about": "Yoinker {version} - All rights reserved",
        "status_ready": "Ready. Paste a link above.",
        "status_starting": "Starting...",
        "status_downloading": "Downloading... {percent}%  {speed}  {eta}",
        "status_converting": "Almost done, finishing the file...",
        "status_done": "Done! The file is in your folder.",
        "status_cancelled": "Stopped.",
        "status_error": "Something went wrong.",
        "eta": "{seconds} s left",
        "folder_choose_title": "Choose where to save",
        "err_empty": "Please paste a link first (step 1).",
        "err_not_link": "That does not look like a link. It should start with https://",
        "err_login": "This video needs a login or is private. If you are logged in in your browser, try Advanced -> 'Use login from browser'.",
        "err_unavailable": "This video is not available (removed, private or blocked).",
        "err_unsupported": "This link is not supported. Try the link of the video page itself.",
        "err_network": "No internet connection, or the website did not answer. Check the internet and try again.",
        "err_geo": "This video is not available in your country.",
        "err_age": "This video is age-restricted and needs a login. If you are logged in in your browser, try Advanced -> 'Use login from browser'.",
        "err_blocked": "The website refused the download. Please get the newest version of Yoinker and try again.",
        "err_ffmpeg": "The converter inside Yoinker did not work. Please reinstall Yoinker.",
        "err_disk": "Could not save the file. Is the folder writable and is there enough free space?",
        "err_generic": "The download failed. Open 'Details' and send them to your helper.",
        "tab_download": "Download",
        "tab_advanced": "Advanced",
        "adv_intro": "You normally don't need anything here. Changes are saved automatically.",
        "adv_codec": "Video codec:",
        "codec_compat": "Plays everywhere (H.264 + AAC) - recommended",
        "codec_best": "Best quality (AV1/VP9 - may not play on Windows, TVs)",
        "adv_container": "Video file type:",
        "adv_audio": "Music file type / quality:",
        "adv_thumbnail": "Put the cover picture into the file",
        "adv_subtitles": "Download subtitles, languages:",
        "adv_embed_subtitles": "put them inside the video",
        "adv_cookies": "Use login from browser:",
        "cookies_none": "none",
        "adv_cookies_hint": "Fixes 'needs a login' and age-restricted videos. The browser must be closed on Windows.",
        "adv_filename": "File name pattern:",
        "adv_rate_limit": "Speed limit (e.g. 2M):",
        "adv_extra_ytdlp": "Extra yt-dlp arguments:",
        "adv_extra_ffmpeg": "Extra FFmpeg arguments:",
        "adv_reset": "Reset to defaults",
        "err_settings": "A setting on the Advanced tab is wrong:",
    },
    "hu": {
        "window_title": "Yoinker",
        "step1": "1. Másold be a videó vagy a zene linkjét",
        "paste": "Beillesztés",
        "clear": "Törlés",
        "step2": "2. Mit szeretnél?",
        "kind_video": "Videó",
        "kind_audio": "Csak zene (MP3)",
        "quality": "Minőség:",
        "q_best": "Legjobb",
        "q_1080": "Jó (1080p)",
        "q_720": "Közepes (720p)",
        "q_480": "Kis fájl (480p)",
        "playlist": "Ha a link egy lejátszási lista, töltsd le az egészet",
        "step3": "3. Hova mentsem?",
        "choose_folder": "Mappa módosítása...",
        "download": "LETÖLTÉS",
        "cancel": "Leállítás",
        "open_folder": "A mappa megnyitása",
        "details": "Részletek (csak segítőnek)",
        "language": "Nyelv:",
        "about": "Yoinker {version} - Minden jog fenntartva",
        "status_ready": "Kész. Illessz be egy linket fent.",
        "status_starting": "Indítás...",
        "status_downloading": "Letöltés... {percent}%  {speed}  {eta}",
        "status_converting": "Mindjárt kész, a fájl befejezése...",
        "status_done": "Kész! A fájl a mappádban van.",
        "status_cancelled": "Leállítva.",
        "status_error": "Valami hiba történt.",
        "eta": "{seconds} mp van hátra",
        "folder_choose_title": "Válaszd ki, hova mentsem",
        "err_empty": "Előbb másolj be egy linket (1. lépés).",
        "err_not_link": "Ez nem úgy néz ki, mint egy link. https://-sel kell kezdődnie.",
        "err_login": "Ehhez a videóhoz bejelentkezés kell, vagy privát. Ha a böngészőben be vagy lépve, próbáld: Haladó -> 'Bejelentkezés átvétele a böngészőből'.",
        "err_unavailable": "Ez a videó nem érhető el (törölték, privát vagy le van tiltva).",
        "err_unsupported": "Ez a link nem támogatott. Próbáld a videó oldalának a linkjét.",
        "err_network": "Nincs internetkapcsolat, vagy az oldal nem válaszolt. Ellenőrizd a netet, és próbáld újra.",
        "err_geo": "Ez a videó a te országodban nem érhető el.",
        "err_age": "Ez a videó korhatáros és bejelentkezést kér. Ha a böngészőben be vagy lépve, próbáld: Haladó -> 'Bejelentkezés átvétele a böngészőből'.",
        "err_blocked": "Az oldal elutasította a letöltést. Szerezd be a Yoinker legújabb verzióját, és próbáld újra.",
        "err_ffmpeg": "A Yoinkerben lévő átalakító nem működik. Telepítsd újra a Yoinkert.",
        "err_disk": "Nem sikerült menteni a fájlt. Írható a mappa, és van elég szabad hely?",
        "err_generic": "A letöltés nem sikerült. Nyisd meg a 'Részletek'-et, és küldd el a segítődnek.",
        "tab_download": "Letöltés",
        "tab_advanced": "Haladó",
        "adv_intro": "Ide általában nem kell nyúlni. A módosítások automatikusan mentődnek.",
        "adv_codec": "Videó kódolás:",
        "codec_compat": "Mindenhol lejátszható (H.264 + AAC) - ajánlott",
        "codec_best": "Legjobb minőség (AV1/VP9 - Windowson, tévén lehet, hogy nem megy)",
        "adv_container": "Videófájl típusa:",
        "adv_audio": "Zenefájl típusa / minősége:",
        "adv_thumbnail": "Borítókép beletétele a fájlba",
        "adv_subtitles": "Feliratok letöltése, nyelvek:",
        "adv_embed_subtitles": "beletéve a videóba",
        "adv_cookies": "Bejelentkezés átvétele a böngészőből:",
        "cookies_none": "nincs",
        "adv_cookies_hint": "Megoldja a 'bejelentkezés kell' és a korhatáros videókat. Windowson a böngésző legyen bezárva.",
        "adv_filename": "Fájlnév minta:",
        "adv_rate_limit": "Sebességkorlát (pl. 2M):",
        "adv_extra_ytdlp": "Extra yt-dlp paraméterek:",
        "adv_extra_ffmpeg": "Extra FFmpeg paraméterek:",
        "adv_reset": "Alapértelmezések visszaállítása",
        "err_settings": "A Haladó fülön egy beállítás hibás:",
    },
}

# (substring to look for in the lowercase yt-dlp message, error key).
# Order matters: the first match wins.
_ERROR_RULES = [
    ("available in your country", "err_geo"),
    ("geo restriction", "err_geo"),
    ("geo-restrict", "err_geo"),
    ("confirm your age", "err_age"),
    ("age-restricted", "err_age"),
    ("private video", "err_login"),
    ("sign in", "err_login"),
    ("log in", "err_login"),
    ("login", "err_login"),
    ("members-only", "err_login"),
    ("unsupported url", "err_unsupported"),
    ("video unavailable", "err_unavailable"),
    ("has been removed", "err_unavailable"),
    ("is not available", "err_unavailable"),
    ("does not exist", "err_unavailable"),
    ("http error 403", "err_blocked"),
    ("http error 429", "err_blocked"),
    ("ffmpeg", "err_ffmpeg"),
    ("ffprobe", "err_ffmpeg"),
    ("no space left", "err_disk"),
    ("permission denied", "err_disk"),
    ("urlopen error", "err_network"),
    ("getaddrinfo", "err_network"),
    ("temporary failure in name resolution", "err_network"),
    ("timed out", "err_network"),
    ("connection", "err_network"),
    ("network", "err_network"),
]


def detect_language() -> str:
    """Pick 'hu' if the computer is set to Hungarian, otherwise 'en'."""
    try:
        code = locale.getlocale()[0] or locale.getdefaultlocale()[0] or ""
    except Exception:
        code = ""
    return "hu" if code.lower().startswith(("hu", "hungarian")) else "en"


def classify_error(message: str) -> str:
    """Turn a technical yt-dlp error message into one of the err_* keys."""
    low = message.lower()
    for needle, key in _ERROR_RULES:
        if needle in low:
            return key
    return "err_generic"


def tr(lang: str, key: str, **kwargs) -> str:
    """Look up a text; falls back to English, then to the key itself."""
    text = STRINGS.get(lang, {}).get(key) or STRINGS["en"].get(key) or key
    return text.format(**kwargs) if kwargs else text
