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
c.colors.webpage.darkmode.enabled = False
c.colors.webpage.darkmode.policy.images = "never"
c.colors.webpage.preferred_color_scheme = "light"

# font
c.fonts.default_family = "Fira Code"
c.fonts.default_size = "14pt"
c.fonts.hints = "10pt default_family"
for font_type in ("cursive", "fantasy", "fixed", "sans_serif", "serif", "standard"):
    config.set(f"fonts.web.family.{font_type}", "Fira Code")

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

# theme
full_white = "#ffffff"
full_black = "#000000"
alt_white = "#f2e5bc"
base00 = "#fbf1c7"
base01 = "#ebdbb2"
base02 = "#d5c4a1"
base03 = "#bdae93"
base04 = "#665c54"
base05 = "#504945"
base06 = "#3c3836"
base07 = "#282828"
base08 = "#9d0006"
base09 = "#af3a03"
base0A = "#b57614"
base0B = "#79740e"
base0C = "#427b58"
base0D = "#458588"
base0E = "#8f3f71"
base0F = "#d65d0e"
c.colors.completion.fg = base05
c.colors.completion.odd.bg = alt_white
c.colors.completion.even.bg = base00
c.colors.completion.category.fg = base0A
c.colors.completion.category.bg = base00
c.colors.completion.category.border.top = base00
c.colors.completion.category.border.bottom = base00
c.colors.completion.item.selected.fg = base05
c.colors.completion.item.selected.bg = base02
c.colors.completion.item.selected.border.top = base02
c.colors.completion.item.selected.border.bottom = base02
c.colors.completion.item.selected.match.fg = base0B
c.colors.completion.match.fg = base0B
c.colors.completion.scrollbar.fg = base05
c.colors.completion.scrollbar.bg = base00
c.colors.contextmenu.disabled.bg = base01
c.colors.contextmenu.disabled.fg = base04
c.colors.contextmenu.menu.bg = base00
c.colors.contextmenu.menu.fg = base05
c.colors.contextmenu.selected.bg = base02
c.colors.contextmenu.selected.fg = base05
c.colors.downloads.bar.bg = base00
c.colors.downloads.start.fg = base00
c.colors.downloads.start.bg = base0D
c.colors.downloads.stop.fg = base00
c.colors.downloads.stop.bg = base0C
c.colors.downloads.error.fg = base08
c.colors.hints.fg = base00
c.colors.hints.bg = base0A
c.colors.hints.match.fg = base05
c.colors.keyhint.fg = base05
c.colors.keyhint.suffix.fg = base05
c.colors.keyhint.bg = base00
c.colors.messages.error.fg = base00
c.colors.messages.error.bg = base08
c.colors.messages.error.border = base08
c.colors.messages.warning.fg = base00
c.colors.messages.warning.bg = base0E
c.colors.messages.warning.border = base0E
c.colors.messages.info.fg = base05
c.colors.messages.info.bg = base00
c.colors.messages.info.border = base00
c.colors.prompts.fg = base05
c.colors.prompts.border = base00
c.colors.prompts.bg = base00
c.colors.prompts.selected.bg = base02
c.colors.prompts.selected.fg = base05
c.colors.statusbar.normal.fg = full_black
c.colors.statusbar.normal.bg = base00
c.colors.statusbar.insert.fg = base00
c.colors.statusbar.insert.bg = base0D
c.colors.statusbar.passthrough.fg = base00
c.colors.statusbar.passthrough.bg = base0C
c.colors.statusbar.private.fg = base00
c.colors.statusbar.private.bg = base01
c.colors.statusbar.command.fg = full_black
c.colors.statusbar.command.bg = base00
c.colors.statusbar.command.private.fg = full_black
c.colors.statusbar.command.private.bg = base00
c.colors.statusbar.caret.fg = base00
c.colors.statusbar.caret.bg = base0E
c.colors.statusbar.caret.selection.fg = base00
c.colors.statusbar.caret.selection.bg = base0D
c.colors.statusbar.progress.bg = base0D
c.colors.statusbar.url.fg = full_black
c.colors.statusbar.url.error.fg = full_black
c.colors.statusbar.url.hover.fg = full_black
c.colors.statusbar.url.success.http.fg = full_black
c.colors.statusbar.url.success.https.fg = full_black
c.colors.statusbar.url.warn.fg = full_black
c.colors.tabs.bar.bg = full_black
c.colors.tabs.indicator.start = base0D
c.colors.tabs.indicator.stop = base0C
c.colors.tabs.indicator.error = base08
c.colors.tabs.odd.fg = base05
c.colors.tabs.odd.bg = alt_white
c.colors.tabs.even.fg = base05
c.colors.tabs.even.bg = base00
c.colors.tabs.pinned.even.bg = base0C
c.colors.tabs.pinned.even.fg = base07
c.colors.tabs.pinned.odd.bg = base0B
c.colors.tabs.pinned.odd.fg = base07
c.colors.tabs.pinned.selected.even.bg = base02
c.colors.tabs.pinned.selected.even.fg = base05
c.colors.tabs.pinned.selected.odd.bg = base02
c.colors.tabs.pinned.selected.odd.fg = base05
c.colors.tabs.selected.odd.fg = base05
c.colors.tabs.selected.odd.bg = base02
c.colors.tabs.selected.even.fg = base05
c.colors.tabs.selected.even.bg = base02
c.colors.webpage.bg = full_white
