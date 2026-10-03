<h1 align="center">🌀 whoosh.yazi</h1>
<p align="center">
  <b>A lightning-fast, keyboard-first bookmark manager for <a href="https://github.com/sxyazi/yazi">Yazi</a></b><br>
  <i>Save, search, and jump to your favorite paths in a blink</i>
</p>

<p align="center">
  <img src="image/plugin.png" width="900" alt="Plugin preview" />
</p>

---

> [!TIP]
> **Russian version:** [README-RU.md](README-RU.md)

> [!NOTE]
> [Yazi](https://github.com/sxyazi/yazi) plugin for bookmark management, supporting the following features:
>
> - **Persistent and temporary bookmarks** - Keep favorite paths across restarts or for the current session
> - **Quick navigation** - Jump, delete, and rename bookmarks by keymap
> - **Fuzzy search** - Support fuzzy search through [fzf](https://github.com/junegunn/fzf)
> - **Multiple bookmark deletion** - Select multiple bookmarks with TAB in fzf
> - **Configuration bookmarks** - Pre-configure bookmarks using Lua language
> - **Smart path truncation** - Configurable path shortening for better readability
> - **Directory history** - Browse recently visited directories or return to the previous location
> - **Project root navigation** - Jump to the current Git repository root with `-`
> - **Configurable menu shortcuts** - Override the default Tab/Backspace/Enter/Space/- bindings from `init.lua`

## Installation

> [!IMPORTANT]
> Requires Yazi v26.1.4+

```sh
ya pkg add WhoSowSee/whoosh
```

```sh
# Manual installation

# Linux/macOS
git clone https://github.com/WhoSowSee/whoosh.yazi.git ~/.config/yazi/plugins/whoosh.yazi

# Windows
git clone https://github.com/WhoSowSee/whoosh.yazi.git $env:APPDATA\yazi\config\plugins\whoosh.yazi
```

## Usage

Add this to your `init.lua`

```lua
-- You can configure your bookmarks using simplified syntax
local bookmarks = {
  { tag = "Desktop", path = "~/Desktop", key = "d" },
  { tag = "Documents", path = "~/Documents", key = "D" },
  { tag = "Downloads", path = "~/Downloads", key = "o" },
}

-- You can also configure bookmarks with key arrays
local bookmarks = {
  { tag = "Desktop", path = "~/Desktop", key = { "d", "D" } },
  { tag = "Documents", path = "~/Documents", key = { "d", "d" } },
  { tag = "Downloads", path = "~/Downloads", key = "o" },
}

-- Windows-specific bookmarks
if ya.target_family() == "windows" then
  local home_path = os.getenv("USERPROFILE")
  table.insert(bookmarks, {
    tag = "Scoop Local",
    path = os.getenv("SCOOP") or (home_path .. "\\scoop"),
    key = "p"
  })
  table.insert(bookmarks, {
    tag = "Scoop Global",
    path = os.getenv("SCOOP_GLOBAL") or "C:\\ProgramData\\scoop",
    key = "P"
  })
end

require("whoosh"):setup {
  -- Configuration bookmarks (cannot be deleted through plugin)
  bookmarks = bookmarks,

  -- Notification settings
  jump_notify = false,

  -- Key generation for auto-assigning bookmark keys
  keys = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",

  -- Configure the built-in menu action hotkeys
  -- false - hide menu item
  special_keys = {
    create_temp = "<Enter>",         -- Create a temporary bookmark from the menu
    fuzzy_search = "<Space>",        -- Launch fuzzy search (fzf)
    history = "<Tab>",               -- Open directory history
    previous_dir = "<Backspace>",    -- Jump back to the previous directory
    project_root = "-",              -- Jump to the current Git repository root
  },

  -- File path for storing user bookmarks
  bookmarks_path = (ya.target_family() == "windows" and os.getenv("APPDATA") .. "\\yazi\\config\\plugins\\whoosh.yazi\\bookmarks") or
         (os.getenv("HOME") .. "/.config/yazi/plugins/whoosh.yazi/bookmarks"),

  -- Replace home directory with "~"
  home_alias_enabled = true,                            -- Toggle home aliasing in displays

  -- Path truncation in navigation menu
  path_truncate_enabled = false,                        -- Enable/disable path truncation
  path_max_depth = 3,                                   -- Maximum path depth before truncation

  -- Path truncation in fuzzy search (fzf)
  fzf_path_truncate_enabled = false,                    -- Enable/disable path truncation in fzf
  fzf_path_max_depth = 5,                               -- Maximum path depth before truncation in fzf

  -- Long folder name truncation
  path_truncate_long_names_enabled = false,             -- Enable in navigation menu
  fzf_path_truncate_long_names_enabled = false,         -- Enable in fzf
  path_max_folder_name_length = 20,                     -- Max length in navigation menu
  fzf_path_max_folder_name_length = 20,                 -- Max length in fzf

  -- History directory settings
  history_size = 10,                                    -- Number of directories in history (default 10)
  history_fzf_path_truncate_enabled = false,            -- Enable/disable path truncation by depth for history
  history_fzf_path_max_depth = 5,                       -- Maximum path depth before truncation for history (default 5)
  history_fzf_path_truncate_long_names_enabled = false, -- Enable/disable long folder name truncation for history
  history_fzf_path_max_folder_name_length = 30,         -- Maximum length for folder names in history (default 30)
}
```

Add this to your `keymap.toml`:

```toml
[[mgr.prepend_keymap]]
on = "["
run = "plugin whoosh jump_by_key"
desc = "Jump bookmark by key"

# Direct fuzzy search access
[[mgr.prepend_keymap]]
on = "}"
run = "plugin whoosh jump_by_fzf"
desc = "Direct fuzzy search for bookmarks"

# Basic bookmark operations
[[mgr.prepend_keymap]]
on = [ "]", "a" ]
run = "plugin whoosh save"
desc = "Add bookmark (hovered file/directory)"

[[mgr.prepend_keymap]]
on = [ "]", "A" ]
run = "plugin whoosh save_cwd"
desc = "Add bookmark (current directory)"

# Temporary bookmarks
[[mgr.prepend_keymap]]
on = [ "]", "t" ]
run = "plugin whoosh save_temp"
desc = "Add temporary bookmark (hovered file/directory)"

[[mgr.prepend_keymap]]
on = [ "]", "T" ]
run = "plugin whoosh save_cwd_temp"
desc = "Add temporary bookmark (current directory)"

# Jump to bookmarks
[[mgr.prepend_keymap]]
on = "<A-k>"
run = "plugin whoosh jump_key_k"
desc = "Jump directly to bookmark with key k"

[[mgr.prepend_keymap]]
on = [ "]", "f" ]
run = "plugin whoosh jump_by_fzf"
desc = "Jump bookmark by fzf"

# Delete bookmarks
[[mgr.prepend_keymap]]
on = [ "]", "d" ]
run = "plugin whoosh delete_by_key"
desc = "Delete bookmark by key"

[[mgr.prepend_keymap]]
on = [ "]", "D" ]
run = "plugin whoosh delete_by_fzf"
desc = "Delete bookmarks by fzf (use TAB to select multiple)"

[[mgr.prepend_keymap]]
on = [ "]", "C" ]
run = "plugin whoosh delete_all"
desc = "Delete all user bookmarks"

# Rename bookmarks
[[mgr.prepend_keymap]]
on = [ "]", "r" ]
run = "plugin whoosh rename_by_key"
desc = "Rename bookmark by key"

[[mgr.prepend_keymap]]
on = [ "]", "R" ]
run = "plugin whoosh rename_by_fzf"
desc = "Rename bookmark by fzf"
```

## Features

### Directory History

<div style="text-align: center;">
  <img src="image/history.png" alt="History preview" width="1100px">
</div>

Each tab keeps its own session history, with recent directories first and the current directory excluded. Set `history_size` to change how many directories are kept (default: 10).

See [Navigation Menu Controls](#navigation-menu-controls) for shortcuts.

### Neovim `<Tab>` keymap (yazi.nvim)

When this plugin runs inside [mikavilpas/yazi.nvim](https://github.com/mikavilpas/yazi.nvim), the default `<Tab>` mapping (`cycle_open_buffers`) is handled by Neovim before Yazi sees it. If pressing `<Tab>` returns you to the buffer where Yazi was opened, disable or remap that key in the yazi.nvim configuration so the directory history picker can receive it:

```lua
  opts = {
    keymaps = {
      cycle_open_buffers = false,
    },
      -- OR
    keymaps = {
      cycle_open_buffers = "<S-Tab>",
    },
  },
```

Full config file example:

```lua
return {
  "mikavilpas/yazi.nvim",
  version = "*",
  event = "VeryLazy",
  dependencies = { { "nvim-lua/plenary.nvim", lazy = true } },
  keys = {
    { "<leader>-", mode = { "n", "v" }, "<cmd>Yazi<cr>", desc = "Open Yazi" },
    { "<leader>cw", "<cmd>Yazi cwd<cr>", desc = "Open Yazi at CWD" },
  },
  opts = {
    open_for_directories = false,
    keymaps = {
      cycle_open_buffers = false,
    },
  },

  init = function() vim.g.loaded_netrwPlugin = 1 end,
}
```

If you prefer to keep Neovim's `<Tab>` binding but still want access to the history picker, remap whoosh's shortcut via `special_keys` in the `init.lua` file:

```lua
require("whoosh"):setup {
  special_keys = {
    history = "<H>",
  },
}
```

### Alt+Shift keybindings in yazi.nvim

In affected Neovim versions, `Alt+Shift` combinations forwarded to an
application inside Neovim's built-in terminal may lose the Shift modifier.
For example, Yazi may receive `<A-d>` instead of `<A-D>` and execute
`jump_key_d` instead of `jump_key_D`.

This was reproduced with Neovim `0.12.4` and Kitty `0.43.1` and is tracked
in [neovim/neovim#36213](https://github.com/neovim/neovim/pull/36213).
Whoosh cannot restore a modifier that was lost before the plugin was invoked.

Until this is fixed in Neovim, avoid keybindings inside `yazi.nvim` that
differ only by Shift, such as `<A-d>` and `<A-D>`. Assign one of the
bookmarks a different key combination.

### Bookmark Types

The plugin supports three types of bookmarks:

1. **Configuration bookmarks** - Defined in `init.lua`, cannot be deleted through the plugin
2. **User bookmarks** - Created during usage, saved to file, can be deleted
3. **Temporary bookmarks** - Cleared on restart; marked `[TEMP]` in the menu and fzf

When paths conflict, user bookmarks override configuration bookmarks in the display

## Configuration Options

The plugin supports the following configuration options in the `setup()` function:

| Option                                 | Type    | Default                 | Description                                                        |
| -------------------------------------- | ------- | ----------------------- | ------------------------------------------------------------------ |
| `bookmarks`                            | table   | `{}`                    | Pre-configured bookmarks (cannot be deleted through plugin)        |
| `jump_notify`                          | boolean | `false`                 | Show notification when jumping to a bookmark                       |
| `keys`                                 | string  | `"0123456789abcdef..."` | Characters used for auto-generating bookmark keys                  |
| `special_keys`                         | table   | `see description`       | Override the built-in menu shortcuts (Enter/Space/-/Tab/Backspace); set to `false` to hide an item |
| `path`                                 | string  | OS-dependent            | File path where user bookmarks are stored                          |
| `home_alias_enabled`                  | boolean | `true`                  | Replace paths under the user's home directory with `~`              |
| `path_truncate_enabled`                | boolean | `false`                 | Enable/disable path truncation in navigation menu                  |
| `path_max_depth`                       | number  | `3`                     | Maximum path depth before truncation with "…" in navigation menu   |
| `fzf_path_truncate_enabled`            | boolean | `false`                 | Enable/disable path truncation in fuzzy search (fzf)               |
| `fzf_path_max_depth`                   | number  | `5`                     | Maximum path depth before truncation with "…" in fzf               |
| `path_truncate_long_names_enabled`     | boolean | `false`                 | Enable/disable long folder name truncation in navigation menu      |
| `fzf_path_truncate_long_names_enabled` | boolean | `false`                 | Enable/disable long folder name truncation in fzf                  |
| `path_max_folder_name_length`          | number  | `20`                    | Maximum folder name length before truncation in navigation menu    |
| `fzf_path_max_folder_name_length`      | number  | `20`                    | Maximum folder name length before truncation in fzf                |
| `history_size`                         | number  | `10`                    | Number of directories to keep in Tab history                        |
| `history_fzf_path_truncate_enabled`    | boolean | `false`                 | Enable/disable path truncation by depth for Tab history display    |
| `history_fzf_path_max_depth`           | number  | `5`                     | Maximum path depth before truncation for Tab history               |
| `history_fzf_path_truncate_long_names_enabled` | boolean | `false`         | Enable/disable long folder name truncation for Tab history         |
| `history_fzf_path_max_folder_name_length` | number | `30`                   | Maximum folder name length before truncation for Tab history       |

**Note:** Configuration bookmarks defined in the `bookmarks` option cannot be deleted through the plugin interface. They serve as permanent, protected bookmarks that are always available

### Bookmark Configuration

The plugin supports a simplified bookmark syntax in the configuration:

```lua
-- Simplified syntax (recommended)
local bookmarks = {
  { tag = "Desktop", path = "~/Desktop", key = "d" },
  { tag = "Projects", path = "~/Projects", key = "p" },
}
```

**Features of simplified syntax:**

- **Tilde expansion** - `~` is automatically expanded to home directory
- **Path normalization** - Separators `/` are automatically converted for your OS
- **Automatic trailing separator** - Directories get proper trailing separators

### Path Truncation

Shorten displayed paths by depth with `path_truncate_enabled` and `path_max_depth`, or by folder name length with `path_truncate_long_names_enabled` and `path_max_folder_name_length`. Both options are disabled by default and can be enabled independently.

Bookmark search (`fzf_path_*`) and directory history (`history_fzf_path_*`) have separate settings listed in the [configuration table](#configuration-options). These settings affect only how paths are displayed.

## Available Commands

| Command            | Description                                                   |
| ------------------ | ------------------------------------------------------------- |
| `save`             | Add bookmark for hovered file/directory                       |
| `save_cwd`         | Add bookmark for current working directory                    |
| `save_temp`        | Add temporary bookmark for hovered file/directory             |
| `save_cwd_temp`    | Add temporary bookmark for current working directory          |
| `jump_by_key`      | Open navigation menu to jump to bookmark by key               |
| `jump_key_<keys>`  | Jump instantly to bookmark matching the provided key sequence |
| `jump_by_fzf`      | Open fuzzy search to jump to bookmark                         |
| `delete_by_key`    | Delete bookmark by selecting with key                         |
| `delete_by_fzf`    | Delete multiple bookmarks using fzf (TAB to select)           |
| `delete_all`       | Delete all user-created bookmarks (excludes config bookmarks) |
| `delete_all_temp`  | Delete all temporary bookmarks                                |
| `rename_by_key`    | Rename bookmark by selecting with key                         |
| `rename_by_fzf`      | Rename bookmark using fuzzy search                            |

### Direct Key Shortcuts

You can jump without opening the menu by calling the plugin with an inline key sequence:

- `plugin whoosh jump_key_<keys>` - inline sequence such as `jump_key_k`, `jump_key_<Space>`, or `jump_key_bb`.

Sequences must be provided inline; whitespace-separated forms are not supported. The format matches the bookmark editing prompt, so you can mix plain characters, comma-separated tokens, and special keys like `<Space>` or `<A-l>`.

The project root shortcut is detected dynamically by walking upward from the current directory until whoosh finds a `.git` file or directory. It is not saved to your bookmarks file.

Special menu shortcuts are resolved before bookmark keys, so a bookmark using the same key will be shadowed by the special shortcut.

### Navigation Menu Controls

When using `jump_by_key`, the following special controls are available:

| Default key   | Action                                          |
| ------------  | ----------------------------------------------- |
| `<Enter>`     | Create temporary bookmark for current directory |
| `<Space>`     | Open fuzzy search                               |
| `<Tab>`       | Open directory history (only if history exists) |
| `<Backspace>` | Return to previous directory (if available)     |
| `-`           | Jump to current Git repository root             |
| `[a-zA-Z0-9]` | Jump to bookmark with corresponding key         |

## Inspiration

- [yamb](https://github.com/h-hg/yamb.yazi)
- [bunny](https://github.com/stelcodes/bunny.yazi)

---

<!-- Self-hosted star history, refreshed by .github/workflows/star-history.yml. -->
<p align="center">
  <a href="https://github.com/WhoSowSee/whoosh.yazi/stargazers">
    <picture>
      <source
        media="(prefers-color-scheme: dark)"
        srcset=".github/assets/star-history-dark.svg"
      />
      <source
        media="(prefers-color-scheme: light)"
        srcset=".github/assets/star-history-light.svg"
      />
      <img
        alt="Stargazers over time"
        src=".github/assets/star-history-light.svg"
        width="820"
      />
    </picture>
  </a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/footers/gray0_ctp_on_line.svg?sanitize=true" alt="catppuccin" />
</p>

<p align="center">
  <i><code>&copy 2026-present <a href="https://github.com/WhoSowSee">WhoSowSee</a></code></i>
</p>

<p align="center">
  <a href="https://github.com/WhoSowSee/whoosh.yazi/blob/main/LICENSE"><img src="https://img.shields.io/github/license/WhoSowSee/whoosh.yazi?style=for-the-badge&color=CBA6F7&logoColor=cdd6f4&labelColor=302D41" alt="LICENSE"></a>
</p>
