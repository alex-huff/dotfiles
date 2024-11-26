import os

config.load_autoconfig(False)

# bindings
config.bind(",M", "hint links spawn mpv {hint-url}")
config.bind(",m", "spawn mpv {url}")
config.bind("<Ctrl+Shift+h>", "tab-prev")
config.bind("<Ctrl+Shift+l>", "tab-next")
config.bind("<Ctrl+d>", "jseval --quiet scrollHelper.scrollPage(0.8)")
config.bind("<Ctrl+u>", "jseval --quiet scrollHelper.scrollPage(-0.8)")
config.bind("G", "jseval --quiet scrollHelper.scrollToPercent(100)")
config.bind("H", "nop")
config.bind("J", "back")
config.bind("K", "forward")
config.bind("L", "edit-url")
config.bind(r"\h", "search")
config.bind(r"\m", "clear-messages")
config.bind("gH", "tab-move -")
config.bind("gL", "tab-move +")
config.bind("gg", "jseval --quiet scrollHelper.scrollTo(0)")
config.bind("j", "jseval --quiet scrollHelper.scrollBy(200)")
config.bind("k", "jseval --quiet scrollHelper.scrollBy(-200)")
config.bind("q", "tab-close")
config.bind("Q", "tab-close -o")
config.bind("yh", "hint links yank")
config.unbind("<Ctrl+h>")
config.unbind("d")

# colors
c.colors.webpage.darkmode.enabled = True
c.colors.webpage.darkmode.policy.images = "never"
c.colors.webpage.preferred_color_scheme = "dark"

# font
c.fonts.default_family = "Victor Mono"
c.fonts.default_size = "14pt"
c.fonts.hints = "10pt default_family"
for font_type in ("cursive", "fantasy", "fixed", "sans_serif", "serif", "standard"):
    config.set(f"fonts.web.family.{font_type}", "Victor Mono")

# posix specific
if os.name == "posix":
    # let window manager deal with managing tabs
    c.tabs.show = "never"
    c.tabs.tabs_are_windows = True

# editor
if os.name == "nt":
    editor_script = 'kitty --start-as=maximized nvim -c "normal {line}G{column}|zz" "$(wslpath -ua "$1")"'
    editor_command = ["wsl", "--exec", "sh",
                      "-c", editor_script, "_", "{file}"]
else:
    editor_command = ["kitty", "--app-id=kitty-dialogue",
                      "nvim", "-c", "normal {line}G{column}|zz", "{file}"]
c.editor.command = editor_command

# file selection
c.fileselect.handler = "external"
home_path = os.path.expanduser("~")
if os.name == "nt":
    file_selection_script = \
        ('export CHOICE=$(wslpath -ua "$1");'
         'cd "$(wslpath -ua "$2")";'
         "kitty --start-as=maximized")
    file_selection_command = ["wsl", "--exec", "env", r'CHOOSER=xargs -d "\n" -n1 wslpath -wa >> "$CHOICE"',
                              "sh", "-c", file_selection_script, "_", "{}", home_path]
else:
    file_selection_command = ["env", f"--chdir={home_path}", "CHOICE={}",
                              r'CHOOSER=xargs -d "\n" realpath >> "$CHOICE"', "kitty", "--app-id=kitty-dialogue"]
for selection_type in ("single_file", "multiple_files", "folder"):
    config.set(f"fileselect.{selection_type}.command", file_selection_command)

# various
c.auto_save.session = False

c.completion.quick = False
c.completion.open_categories = ["quickmarks", "bookmarks"]

c.content.blocking.enabled = True
c.content.blocking.method = "both"
c.content.blocking.hosts.lists = [
    "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts"]

c.content.media.audio_capture = "ask"
c.content.media.audio_video_capture = "ask"
c.content.desktop_capture = "ask"

c.content.headers.user_agent = "Mozilla/5.0 ({os_info}) AppleWebKit/{webkit_version} (KHTML, like Gecko) {qt_key}/{qt_version} {upstream_browser_key}/{upstream_browser_version} Safari/{webkit_version}"

c.content.javascript.clipboard = "access-paste"

c.content.notifications.enabled = False

c.content.prefers_reduced_motion = True

c.content.proxy = "system"

c.downloads.location.prompt = False
c.downloads.location.remember = False
c.downloads.location.suggestion = "both"

c.input.insert_mode.auto_enter = False
c.input.insert_mode.auto_leave = False
c.input.insert_mode.leave_on_load = False

c.keyhint.delay = 0

c.spellcheck.languages = ["en-US"]

c.tabs.focus_stack_size = 10
c.tabs.mode_on_change = "persist"
c.tabs.new_position.unrelated = "next"
c.tabs.position = "top"
c.tabs.wrap = False

c.url.default_page = "about:blank"
c.url.start_pages = "about:blank"
c.url.searchengines = {"DEFAULT": "https://duckduckgo.com/?q={}"}

c.search.wrap = False

# discord overrides
with config.pattern("*://discord.com") as discord_c:
    discord_c.content.desktop_capture = True
    discord_c.content.media.audio_capture = True
