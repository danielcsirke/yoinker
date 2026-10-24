"""The Yoinker window. Three numbered steps and one big button."""

import os
import queue
import subprocess
import sys
import threading
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import filedialog, ttk

from yoinker import APP_NAME, __version__, config
from yoinker.downloader import Job, looks_like_link
from yoinker.i18n import LANGUAGES, detect_language, tr

PAD = 10
BIG_FONT = ("TkDefaultFont", 14, "bold")
STATUS_FONT = ("TkDefaultFont", 12)
RELEASES_URL = "https://github.com/danielcsirke/yoinker/releases/latest"


def open_folder(path: str) -> None:
    """Show a folder in Finder / Explorer / the Linux file manager."""
    try:
        if sys.platform == "win32":
            os.startfile(path)  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
    except Exception:
        webbrowser.open(Path(path).as_uri())


def human_speed(bytes_per_s) -> str:
    if not bytes_per_s:
        return ""
    for unit in ("B/s", "KB/s", "MB/s", "GB/s"):
        if bytes_per_s < 1024:
            return f"{bytes_per_s:.0f} {unit}"
        bytes_per_s /= 1024
    return f"{bytes_per_s:.1f} TB/s"


class YoinkerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.settings = config.load()
        self.lang = self.settings.get("language") or detect_language()
        self.folder = Path(self.settings.get("folder") or config.default_download_dir())

        self.kind = tk.StringVar(value="video")
        self.quality = tk.StringVar(value="best")
        self.playlist = tk.BooleanVar(value=False)
        self.lang_var = tk.StringVar(value=LANGUAGES[self.lang])

        self.job: Job | None = None
        self.events: queue.Queue = queue.Queue()
        self.widgets: dict[str, tk.Widget] = {}

        self.minsize(560, 420)
        self.resizable(True, False)
        self._build()
        self._apply_texts()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(100, self._poll_events)

    # ----- building the window -------------------------------------------

    def _build(self):
        root = ttk.Frame(self, padding=PAD * 2)
        root.pack(fill="both", expand=True)
        root.columnconfigure(0, weight=1)
        w = self.widgets

        # Step 1: link
        w["step1"] = ttk.Label(root, font=BIG_FONT)
        w["step1"].grid(row=0, column=0, sticky="w")
        link_row = ttk.Frame(root)
        link_row.grid(row=1, column=0, sticky="ew", pady=(4, PAD * 2))
        link_row.columnconfigure(0, weight=1)
        self.url_entry = ttk.Entry(link_row, font=STATUS_FONT)
        self.url_entry.grid(row=0, column=0, sticky="ew", ipady=4)
        w["paste"] = ttk.Button(link_row, command=self._paste)
        w["paste"].grid(row=0, column=1, padx=(6, 0))
        w["clear"] = ttk.Button(link_row, command=lambda: self.url_entry.delete(0, "end"))
        w["clear"].grid(row=0, column=2, padx=(6, 0))

        # Step 2: what
        w["step2"] = ttk.Label(root, font=BIG_FONT)
        w["step2"].grid(row=2, column=0, sticky="w")
        what = ttk.Frame(root)
        what.grid(row=3, column=0, sticky="ew", pady=(4, PAD * 2))
        w["kind_video"] = ttk.Radiobutton(what, variable=self.kind, value="video",
                                          command=self._kind_changed)
        w["kind_video"].grid(row=0, column=0, sticky="w")
        w["kind_audio"] = ttk.Radiobutton(what, variable=self.kind, value="audio",
                                          command=self._kind_changed)
        w["kind_audio"].grid(row=0, column=1, sticky="w", padx=(PAD * 2, 0))
        w["quality"] = ttk.Label(what)
        w["quality"].grid(row=0, column=2, sticky="e", padx=(PAD * 3, 4))
        self.quality_box = ttk.Combobox(what, state="readonly", width=16)
        self.quality_box.grid(row=0, column=3, sticky="w")
        self.quality_box.bind("<<ComboboxSelected>>", self._quality_changed)
        w["playlist"] = ttk.Checkbutton(what, variable=self.playlist)
        w["playlist"].grid(row=1, column=0, columnspan=4, sticky="w", pady=(6, 0))

        # Step 3: where
        w["step3"] = ttk.Label(root, font=BIG_FONT)
        w["step3"].grid(row=4, column=0, sticky="w")
        where = ttk.Frame(root)
        where.grid(row=5, column=0, sticky="ew", pady=(4, PAD * 2))
        where.columnconfigure(0, weight=1)
        self.folder_label = ttk.Label(where, text=str(self.folder), font=STATUS_FONT)
        self.folder_label.grid(row=0, column=0, sticky="w")
        w["choose_folder"] = ttk.Button(where, command=self._choose_folder)
        w["choose_folder"].grid(row=0, column=1, padx=(6, 0))

        # The big button + progress
        style = ttk.Style(self)
        style.configure("Big.TButton", font=("TkDefaultFont", 16, "bold"), padding=12)
        w["download"] = ttk.Button(root, style="Big.TButton", command=self._download)
        w["download"].grid(row=6, column=0, sticky="ew")
        self.progress = ttk.Progressbar(root, mode="determinate", maximum=100)
        self.progress.grid(row=7, column=0, sticky="ew", pady=(PAD, 4))
        self.status = ttk.Label(root, font=STATUS_FONT, wraplength=520, justify="left")
        self.status.grid(row=8, column=0, sticky="w")
        after = ttk.Frame(root)
        after.grid(row=9, column=0, sticky="w", pady=(6, 0))
        w["open_folder"] = ttk.Button(after, command=lambda: open_folder(str(self.folder)))
        w["open_folder"].grid(row=0, column=0)
        w["cancel"] = ttk.Button(after, command=self._cancel)

        # Details (collapsed by default)
        self.details_open = False
        w["details"] = ttk.Button(root, command=self._toggle_details)
        w["details"].grid(row=10, column=0, sticky="w", pady=(PAD * 2, 0))
        self.log = tk.Text(root, height=8, state="disabled", font=("TkFixedFont", 9))
        self.log_row = 11

        # Footer: language + version
        footer = ttk.Frame(root)
        footer.grid(row=12, column=0, sticky="ew", pady=(PAD * 2, 0))
        footer.columnconfigure(2, weight=1)
        w["language"] = ttk.Label(footer)
        w["language"].grid(row=0, column=0, sticky="w")
        lang_box = ttk.Combobox(footer, textvariable=self.lang_var, state="readonly",
                                values=list(LANGUAGES.values()), width=10)
        lang_box.grid(row=0, column=1, sticky="w", padx=(6, 0))
        lang_box.bind("<<ComboboxSelected>>", self._lang_changed)
        w["about"] = ttk.Label(footer, foreground="gray")
        w["about"].grid(row=0, column=2, sticky="e")

        self.url_entry.focus_set()
        self.bind("<Return>", lambda _e: self._download())

    def _apply_texts(self):
        """Set every label in the current language (called on language change)."""
        t = lambda key, **kw: tr(self.lang, key, **kw)  # noqa: E731
        self.title(t("window_title"))
        for key, widget in self.widgets.items():
            if key == "about":
                widget.configure(text=t("about", version=__version__))
            else:
                widget.configure(text=t(key))
        self.quality_keys = ["best", "1080", "720", "480"]
        self.quality_box["values"] = [t("q_" + k) for k in self.quality_keys]
        self.quality_box.current(self.quality_keys.index(self.quality.get()))
        self._kind_changed()
        if self.job is None:
            self._set_status("status_ready")

    # ----- small handlers -------------------------------------------------

    def _paste(self):
        try:
            text = self.clipboard_get()
        except tk.TclError:
            return
        self.url_entry.delete(0, "end")
        self.url_entry.insert(0, text.strip())

    def _kind_changed(self):
        state = "disabled" if self.kind.get() == "audio" else "readonly"
        self.quality_box.configure(state=state)

    def _quality_changed(self, _event=None):
        self.quality.set(self.quality_keys[self.quality_box.current()])

    def _lang_changed(self, _event=None):
        for code, name in LANGUAGES.items():
            if name == self.lang_var.get():
                self.lang = code
        self.settings["language"] = self.lang
        config.save(self.settings)
        self._apply_texts()

    def _choose_folder(self):
        chosen = filedialog.askdirectory(
            title=tr(self.lang, "folder_choose_title"), initialdir=str(self.folder)
        )
        if chosen:
            self.folder = Path(chosen)
            self.folder_label.configure(text=str(self.folder))
            self.settings["folder"] = str(self.folder)
            config.save(self.settings)

    def _toggle_details(self):
        self.details_open = not self.details_open
        if self.details_open:
            self.log.grid(row=self.log_row, column=0, sticky="ew", pady=(4, 0))
        else:
            self.log.grid_forget()
        self.resizable(True, self.details_open)

    def _log(self, text: str):
        self.log.configure(state="normal")
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _set_status(self, key: str, **kw):
        self.status.configure(text=tr(self.lang, key, **kw))

    # ----- the download itself ---------------------------------------------

    def _download(self):
        if self.job is not None:
            return
        url = self.url_entry.get().strip()
        if not url:
            self._set_status("err_empty")
            return
        if not looks_like_link(url):
            self._set_status("err_not_link")
            return
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")
        self.progress["value"] = 0
        self.job = Job(url, self.kind.get(), self.quality.get(), self.folder,
                       self.playlist.get(), self.events.put)
        threading.Thread(target=self.job.run, daemon=True).start()
        self._busy(True)

    def _cancel(self):
        if self.job:
            self.job.cancel()

    def _busy(self, busy: bool):
        self.widgets["download"].configure(state="disabled" if busy else "normal")
        if busy:
            self.widgets["cancel"].grid(row=0, column=1, padx=(6, 0))
        else:
            self.widgets["cancel"].grid_forget()

    def _poll_events(self):
        """Runs on the GUI thread; drains what the download thread reported."""
        try:
            while True:
                event = self.events.get_nowait()
                self._handle(event)
        except queue.Empty:
            pass
        self.after(100, self._poll_events)

    def _handle(self, event: tuple):
        kind = event[0]
        if kind == "log":
            self._log(event[1])
        elif kind == "status":
            self._set_status("status_" + event[1])
        elif kind == "progress":
            _, percent, speed, eta = event
            self.progress["value"] = percent
            eta_text = tr(self.lang, "eta", seconds=int(eta)) if eta else ""
            self._set_status("status_downloading", percent=f"{percent:.0f}",
                             speed=human_speed(speed), eta=eta_text)
        elif kind == "done":
            self.progress["value"] = 100
            self._set_status("status_done")
            self._finish()
        elif kind == "cancelled":
            self.progress["value"] = 0
            self._set_status("status_cancelled")
            self._finish()
        elif kind == "error":
            _, err_key, detail = event
            self.progress["value"] = 0
            self._set_status(err_key)
            self._log(detail if detail.startswith("ERROR") else "ERROR: " + detail)
            if err_key == "err_blocked":
                webbrowser.open(RELEASES_URL)
            self._finish()

    def _finish(self):
        self.job = None
        self._busy(False)
        self.bell()

    def _on_close(self):
        if self.job:
            self.job.cancel()
        self.destroy()


def main():
    app = YoinkerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
