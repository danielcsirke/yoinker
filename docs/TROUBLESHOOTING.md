# Troubleshooting

🇭🇺 [Magyarul: HIBAELHARITAS.md](HIBAELHARITAS.md)

Find the message Yoinker showed you under the progress bar.

| Yoinker says | What it means | What to do |
|---|---|---|
| *Please paste a link first (step 1).* | The box in step 1 is empty. | Copy the video's address from the browser and press **Paste**. |
| *That does not look like a link.* | You pasted something that isn't a web address. | Links start with `https://`. Click the browser's address bar, copy the whole thing. |
| *The website refused the download. Please get the newest version…* | The site changed something; the Yoinker you have is too old. Yoinker opens the Downloads page for you. | Download the newest file from the [Downloads page](https://github.com/danielcsirke/yoinker/releases/latest), replace the old one, try again. |
| *No internet connection, or the website did not answer.* | The computer is offline, or the site is down. | Check that a web page loads in your browser. Try again in a minute. |
| *This video needs a login or is private.* | The video is private, members-only or needs an account. | If you can watch it in your browser while logged in: **Advanced tab → Use login from browser → pick that browser** (close the browser first on Windows), then try again. Otherwise nothing can be done. |
| *This video is age-restricted…* | Same as above, for 18+ videos. | Same. |
| *This video is not available (removed, private or blocked).* | The video is gone or hidden. | Check it still plays in your browser. |
| *This video is not available in your country.* | The uploader blocked your country. | Nothing to do. |
| *This link is not supported.* | The link isn't a video page (e.g. a channel home page or a search). | Open the actual video and copy that address. |
| *Could not save the file.* | The folder is read-only, or the disk is full. | Press **Change folder...** and choose e.g. Desktop. Free some space. |
| *The converter inside Yoinker did not work.* | The program file is damaged. | Download Yoinker again. |
| *A setting on the Advanced tab is wrong: …* | Something typed on the Advanced tab (a yt-dlp flag, the speed limit) isn't valid; the rest of the message says which. | Fix it, or press **Reset to defaults** on the Advanced tab. |
| (no error, but) the video won't play on Windows / no picture | The file is AV1/VP9, which Windows Media Player can't decode. Happens only if *Best quality* was chosen on the Advanced tab. | Advanced tab → *Plays everywhere (H.264 + AAC)* → download again. Or install VLC. |
| *The download failed. Open 'Details'…* | Something unusual. | Press **Details (only for helpers)**, copy the text, send it to your helper. |

## Problems before it even opens

**Windows: "Windows protected your PC".** Click **More info → Run anyway**. It appears because Yoinker isn't signed with a paid certificate. It's safe.

**Windows: antivirus deletes/quarantines the file.** Some antivirus tools are suspicious of any program that isn't well known. Restore it from quarantine and add an exception, or tell your helper.

**Mac: "Yoinker can't be opened because Apple cannot check it for malicious software".** Right-click (or Control-click) Yoinker → **Open** → **Open**. Only needed the first time.

**Mac: "Yoinker is damaged and can't be opened."** This happens on newer macOS when the file is downloaded with some browsers. Open **Terminal** (ask your helper) and run:
`xattr -cr /Applications/Yoinker.app` — then open it normally.

**Linux: double-clicking does nothing.** Make it executable: right-click → Properties → Permissions → "Allow executing as program". Also make sure `libxcb`/Tk libraries exist — on Ubuntu: `sudo apt install python3-tk` is *not* needed (Tk is bundled), but a very minimal system may lack basic X11 libraries.

**It opens, but the window is tiny / text overlaps.** Resize the window wider. If you use very high display scaling, tell your helper the OS and scaling %.

## For helpers

The **Details** box is yt-dlp's own log. Copy it and search the message on https://github.com/yt-dlp/yt-dlp/issues — most problems are site changes that yt-dlp fixes within days. Then publish a new Yoinker: see [MAINTAINERS.md](MAINTAINERS.md).
