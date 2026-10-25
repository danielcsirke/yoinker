# Yoinker — step-by-step guide

🇭🇺 [Magyarul: UTMUTATO.md](UTMUTATO.md)

This page assumes nothing. If you can open a web page and copy text, you can do this.

---

## Part 1 — Getting Yoinker onto your computer

### Windows

1. Click here: **https://github.com/danielcsirke/yoinker/releases/latest**
2. Scroll down a little to the word **Assets**. Click **`Yoinker-Windows.exe`**. The file downloads (a few seconds).
3. Open your **Downloads** folder and double-click **Yoinker-Windows.exe**.
4. A blue box may appear saying **"Windows protected your PC"**. This is normal for any small program that isn't sold in the Microsoft Store.
   Click the small text **More info**, then the button **Run anyway**.
5. Yoinker opens. That's it — there is no installer.

   *Tip:* drag **Yoinker-Windows.exe** from Downloads onto your Desktop so you can find it next time.

### Mac

1. Click here: **https://github.com/danielcsirke/yoinker/releases/latest**
2. Under **Assets**, click **`Yoinker-macOS.dmg`**.
3. Open the downloaded file. A small window appears with **Yoinker** and a folder called **Applications**. Drag Yoinker onto Applications.
4. Open **Applications** (Finder → Applications), find **Yoinker**.
5. **First time only:** hold the **Control** key and click Yoinker (or right-click), choose **Open**, then click **Open** again in the box that appears.
   (If you just double-click, the Mac says *"Yoinker can't be opened because Apple cannot check it"* — that's because this is a free program not sold in the App Store. The right-click trick tells the Mac you trust it. You only need to do it once.)
6. Yoinker opens. From now on you can double-click it like any other app.

### Linux

1. Click here: **https://github.com/danielcsirke/yoinker/releases/latest**
2. Under **Assets**, click **`Yoinker-Linux`**.
3. In your file manager, right-click the downloaded **Yoinker-Linux** → **Properties** → **Permissions** → tick **"Allow executing file as program"** (wording varies a bit between systems).
4. Double-click it. Yoinker opens.

---

## Part 2 — Downloading something

The window has three numbered steps and one big button.

### Step 1 — Paste the link

1. In your web browser, go to the video (or song) you want.
2. Click once in the **address bar** at the very top of the browser (where it says something like `https://www.youtube.com/watch?v=...`). The whole address becomes highlighted.
3. Copy it: press **Ctrl+C** (Windows/Linux) or **Cmd+C** (Mac). Or right-click → Copy.
4. Go to Yoinker and press the **Paste** button. The link appears in the box.

### Step 2 — What do you want?

- **Video** — you get a normal video file (MP4). Choose a quality next to it:
  - **Best** — the best the site has (biggest file).
  - **Good (1080p)** — great for a TV or laptop.
  - **Medium (720p)** — fine for a phone, smaller file.
  - **Small file (480p)** — when space or internet is tight.
- **Music only (MP3)** — you get just the sound, as an MP3 you can put on any phone or player.

*Playlist box:* if the link is a whole playlist/album and you want all of it, tick **"If the link is a playlist, download all of it"**. Leave it unticked to get just the one video.

### Step 3 — Where should it be saved?

Yoinker shows the folder it will use. Normally this is **Downloads → Yoinker**, which is fine. To use another folder (for example a USB stick), press **Change folder...** and pick one. Yoinker remembers your choice.

### Press DOWNLOAD

The bar fills up and the text under it tells you what's happening: *Downloading... 43%*, then *Almost done, finishing the file...*, then **Done!**

Press **Open the folder** — your file is there, named after the video.

To stop a download, press **Stop**.

---

## Part 2b — The Advanced tab (you can skip this)

At the top of the window there are two tabs: **Download** (what you just used) and **Advanced**. You never *need* Advanced. It is there for the one friend who knows what a codec is. Everything on it is saved automatically, and **Reset to defaults** puts it all back.

| Setting | What it does |
|---|---|
| **Video codec** | *Plays everywhere (H.264 + AAC)* is the default and is why your files open on any Windows PC, TV or phone. *Best quality* takes whatever the site has (often AV1/VP9) — smaller and sharper, but Windows Media Player and many TVs refuse it. |
| **Video file type** | mp4 (default), mkv or webm. |
| **Music file type / quality** | mp3 (default) at 128/192/256/320 kbps, or m4a, opus, flac, wav. |
| **Put the cover picture into the file** | The video's thumbnail becomes the album art of the MP3 / the poster of the MP4. |
| **Download subtitles** | Languages as codes separated by commas, e.g. `hu,en`. *Put them inside the video* embeds them so any player can switch them on. |
| **Use login from browser** | Yoinker reads the cookies of the browser you pick, so videos that say *needs a login* or *age-restricted* work if you are logged in there. On Windows, close the browser first. |
| **File name pattern** | yt-dlp's output template. Default: `%(title).150B [%(id)s].%(ext)s`. |
| **Speed limit** | e.g. `2M` for 2 MB/s, so a download doesn't hog the house's internet. Empty = no limit. |
| **Extra yt-dlp arguments** | Anything from `yt-dlp --help`, e.g. `--embed-chapters`. A wrong flag is reported under the progress bar, nothing breaks. |
| **Extra FFmpeg arguments** | Passed to every FFmpeg step, e.g. `-threads 2`. |

---

## Part 3 — Questions people ask

**I downloaded a video and Windows won't play it / plays it without picture.** Open the **Advanced** tab and make sure *Plays everywhere (H.264 + AAC)* is selected (it is, unless somebody changed it), then download again. Or install [VLC](https://www.videolan.org/), which plays everything.

**Is it free? Is there a catch?** Free, no account, no ads. It is "all rights reserved" only in the sense that you shouldn't copy or resell the program itself.

**Can I download from sites other than YouTube?** Yes — most video and audio sites work. Just paste the link and try.

**Where is the Language setting?** Bottom-left of the window. Yoinker starts in Hungarian if your computer is Hungarian, otherwise in English.

**The video is really long / it's a whole playlist — how long does it take?** Depends on your internet. The text under the bar shows the speed and how many seconds are left.

**It worked last month and now it says the site refused the download.** Video sites change their systems often. Download the newest Yoinker from the **[Downloads page](https://github.com/danielcsirke/yoinker/releases/latest)** and replace your old one. That fixes it 95% of the time.

**Something else is wrong.** See **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**. If that doesn't help, press **Details (only for helpers)** at the bottom of the window, copy the text that appears, and send it to whoever gave you Yoinker.
