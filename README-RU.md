<h1 align="center">🌀 whoosh.yazi</h1>
<p align="center">
  <b>Молниеносный менеджер закладок для <a href="https://github.com/sxyazi/yazi">Yazi</a></b><br>
  <i>Сохраняйте, ищите и мгновенно переходите к любимым путям</i>
</p>

<p align="center">
  <img src="image/plugin.png" width="900" alt="Превью плагина" />
</p>

---
> [!TIP]
> **Английская версия:** [README.md](README.md)

> [!NOTE]
> Плагин для [Yazi](https://github.com/sxyazi/yazi) для управления закладками, поддерживающий следующие функции:
>
> - **Постоянные и временные закладки** - Сохраняйте любимые пути между перезапусками или только на текущую сессию
> - **Быстрая навигация** - Переход, удаление и переименование закладок по горячим клавишам
> - **Нечеткий поиск** - Поддержка нечеткого поиска через [fzf](https://github.com/junegunn/fzf) с контекстными промптами
> - **Множественное удаление закладок** - Выбор нескольких закладок с помощью TAB в fzf
> - **Конфигурационные закладки** - Предварительная настройка закладок с помощью языка Lua
> - **Умное сокращение путей** - Настраиваемое сокращение путей для лучшей читаемости
> - **История директорий** - Просматривайте недавно посещённые директории или возвращайтесь к предыдущей
> - **Переход в корень проекта** - Переход в корень текущего Git-репозитория через `-`
> - **Настраиваемые клавиши меню** - Переопределяйте привязки Tab/Backspace/Enter/Space/- через `init.lua`

## Установка

> [!IMPORTANT]
> Требуется Yazi v26.1.4+

```sh
ya pkg add WhoSowSee/whoosh
```

```sh
# Ручная установка

# Linux/macOS
git clone https://github.com/WhoSowSee/whoosh.yazi.git ~/.config/yazi/plugins/whoosh.yazi

# Windows
git clone https://github.com/WhoSowSee/whoosh.yazi.git $env:APPDATA\yazi\config\plugins\whoosh.yazi
```

## Использование

Добавьте это в ваш `init.lua`:

```lua
-- Вы можете настроить закладки, используя упрощенный синтаксис
local bookmarks = {
  { tag = "Рабочий стол", path = "~/Desktop",   key = "d" },
  { tag = "Документы",    path = "~/Documents", key = "D" },
  { tag = "Загрузки",     path = "~/Downloads", key = "o" },
}

-- Вы также можете настроить закладки с массивом ключей
local bookmarks = {
  { tag = "Рабочий стол", path = "~/Desktop",   key = { "d", "D" } },
  { tag = "Документы",    path = "~/Documents", key = { "d", "d" } },
  { tag = "Загрузки",     path = "~/Downloads", key = "o" },
}

-- Или же используя другой, более сложный синтаксис
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

--

require("whoosh"):setup {
  -- Конфигурационные закладки (нельзя удалить через плагин)
  bookmarks = bookmarks,

  -- Настройки уведомлений
  jump_notify = false,

  -- Генерация ключей для автоматического назначения клавиш закладок
  keys = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",

  -- Настройка клавиш для встроенных действий меню
  -- false - скрыть пункт меню
  special_keys = {
    create_temp = "<Enter>",         -- Создание временной закладки
    fuzzy_search = "<Space>",        -- Нечеткий поиск (fzf)
    history = "<Tab>",               -- Открыть историю директорий
    previous_dir = "<Backspace>",    -- Вернуться в предыдущую директорию
    project_root = "-",              -- Переход в корень текущего Git-репозитория
  },

  -- Путь к файлу для хранения пользовательских закладок
  bookmarks_path = (ya.target_family() == "windows" and os.getenv("APPDATA") .. "\\yazi\\config\\plugins\\whoosh.yazi\\bookmarks") or
         (os.getenv("HOME") .. "/.config/yazi/plugins/whoosh.yazi/bookmarks"),

  -- Подмена домашней директории на "~"
  home_alias_enabled = true,                            -- Управляет отображением домашнего каталога

  -- Сокращение путей в меню навигации
  path_truncate_enabled = false,                        -- Включить/выключить сокращение путей
  path_max_depth = 3,                                   -- Максимальная глубина пути перед сокращением

  -- Сокращение путей в нечетком поиске (fzf)
  fzf_path_truncate_enabled = false,                    -- Включить/выключить сокращение путей в fzf
  fzf_path_max_depth = 5,                               -- Максимальная глубина пути перед сокращением в fzf

  -- Сокращение длинных названий папок
  path_truncate_long_names_enabled = false,             -- Включить в меню навигации
  fzf_path_truncate_long_names_enabled = false,         -- Включить в fzf
  path_max_folder_name_length = 20,                     -- Максимальная длина в меню навигации
  fzf_path_max_folder_name_length = 20,                 -- Максимальная длина в fzf

  -- Настройки истории директорий
  history_size = 10,                                    -- Количество директорий в истории (по умолчанию 10)
  history_fzf_path_truncate_enabled = false,            -- Включить сокращение путей по глубине для истории
  history_fzf_path_max_depth = 5,                       -- Максимальная глубина путей для истории (по умолчанию 5)
  history_fzf_path_truncate_long_names_enabled = false, -- Включить сокращение длинных названий для истории
  history_fzf_path_max_folder_name_length = 30,         -- Максимальная длина названий папок для истории (по умолчанию 30)
}
```

Добавьте это в ваш `keymap.toml`:

```toml
[[mgr.prepend_keymap]]
on = "["
run = "plugin whoosh jump_by_key"
desc = "Перейти к закладке по клавише"

# Прямой доступ к нечеткому поиску закладок
[[mgr.prepend_keymap]]
on = "}"
run = "plugin whoosh jump_by_fzf"
desc = "Прямой вызов fuzzy search закладок"

# Основные операции с закладками
[[mgr.prepend_keymap]]
on = [ "]", "a" ]
run = "plugin whoosh save"
desc = "Добавить закладку (выделенный файл/директория)"

[[mgr.prepend_keymap]]
on = [ "]", "A" ]
run = "plugin whoosh save_cwd"
desc = "Добавить закладку (текущая директория)"

# Временные закладки
[[mgr.prepend_keymap]]
on = [ "]", "t" ]
run = "plugin whoosh save_temp"
desc = "Добавить временную закладку (выделенный файл/директория)"

[[mgr.prepend_keymap]]
on = [ "]", "T" ]
run = "plugin whoosh save_cwd_temp"
desc = "Добавить временную закладку (текущая директория)"

# Переход к закладкам
[[mgr.prepend_keymap]]
on = "<A-k>"
run = "plugin whoosh jump_key_k"
desc = "Мгновенный переход к закладке с клавишей k"

[[mgr.prepend_keymap]]
on = [ "]", "f" ]
run = "plugin whoosh jump_by_fzf"
desc = "Перейти к закладке через fzf"

# Удаление закладок
[[mgr.prepend_keymap]]
on = [ "]", "d" ]
run = "plugin whoosh delete_by_key"
desc = "Удалить закладку по клавише"

[[mgr.prepend_keymap]]
on = [ "]", "D" ]
run = "plugin whoosh delete_by_fzf"
desc = "Удалить закладки через fzf (используйте TAB для выбора нескольких)"

[[mgr.prepend_keymap]]
on = [ "]", "C" ]
run = "plugin whoosh delete_all"
desc = "Удалить все пользовательские закладки"

# Переименование закладок
[[mgr.prepend_keymap]]
on = [ "]", "r" ]
run = "plugin whoosh rename_by_key"
desc = "Переименовать закладку по клавише"

[[mgr.prepend_keymap]]
on = [ "]", "R" ]
run = "plugin whoosh rename_by_fzf"
desc = "Переименовать закладку через fzf"
```

## Функции

### История директорий

<div style="text-align: center;">
  <img src="image/history.png" alt="Превью истории директорий" width="1100px">
</div>

Каждая вкладка хранит собственную историю текущей сессии: недавние директории идут первыми, текущая директория исключена. Количество сохраняемых директорий задаётся через `history_size` (по умолчанию 10).

Горячие клавиши приведены в разделе [Управление меню навигации](#управление-меню-навигации).

### Примечание о клавише `<Tab>` в Neovim (yazi.nvim)

При запуске Whoosh внутри [mikavilpas/yazi.nvim](https://github.com/mikavilpas/yazi.nvim) стандартная привязка `<Tab>` (`cycle_open_buffers`) обрабатывается самим Neovim, поэтому Yazi не получает нажатие. Если нажатие `<Tab>` возвращает вас в буфер, из которого открывался Yazi, отключите или переназначьте эту клавишу в настройках yazi.nvim, чтобы корректно вызывать историю директорий:

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

Полный пример конфигурации:

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

Если вы хотите сохранить привязку `<Tab>` за Neovim, но при этом иметь доступ к истории директорий, переназначьте горячую клавишу whoosh через `special_keys` в файле `init.lua`:

```lua
require("whoosh"):setup {
  special_keys = {
    history = "<H>",
  },
}
```

### Сочетания Alt+Shift в yazi.nvim

В затронутых версиях Neovim сочетания `Alt+Shift`, переданные приложению
внутри встроенного терминала, могут потерять Shift. Например, Yazi может
получить `<A-d>` вместо `<A-D>` и выполнить `jump_key_d` вместо
`jump_key_D`.

Проблема воспроизводилась с Neovim `0.12.4` и Kitty `0.43.1` и отслеживается
в [neovim/neovim#36213](https://github.com/neovim/neovim/pull/36213).
Whoosh не может восстановить модификатор, который был потерян до вызова
плагина.

До исправления на стороне Neovim не используйте внутри `yazi.nvim`
сочетания, различающиеся только наличием Shift, например `<A-d>` и `<A-D>`.
Назначьте одной из закладок другое сочетание клавиш.

### Типы закладок

Плагин поддерживает три типа закладок:

1. **Конфигурационные закладки** - Определены в `init.lua`, нельзя удалить через интерфейс плагина
2. **Пользовательские закладки** - Созданы во время использования, сохранены в файл, можно удалить
3. **Временные закладки** - Очищаются при перезапуске; отмечены `[TEMP]` в меню и fzf

При конфликте путей пользовательские закладки переопределяют конфигурационные закладки в отображении

## Параметры конфигурации

Плагин поддерживает следующие параметры конфигурации в функции `setup()`:

| Параметр                                       | Тип     | По умолчанию            | Описание                                                                   |
| ---------------------------------------------- | ------- | ----------------------- | -------------------------------------------------------------------------- |
| `bookmarks`                                    | table   | `{}`                    | Предварительно настроенные закладки (нельзя удалить через плагин)          |
| `jump_notify`                                  | boolean | `false`                 | Показывать уведомление при переходе к закладке                             |
| `keys`                                         | string  | `"0123456789abcdef..."` | Символы, используемые для автогенерации ключей закладок                    |
| `special_keys`                                 | table   | `см. описание`           | Настройка клавиш встроенного меню (Enter/Space/-/Tab/Backspace); можно задать `false` для отключения |
| `path`                                         | string  | Зависит от ОС           | Путь к файлу, где хранятся пользовательские закладки                       |
| `home_alias_enabled`                          | boolean | `true`                  | Подменять домашнюю директорию на `~` в отображении пути                    |
| `path_truncate_enabled`                        | boolean | `false`                 | Включить/выключить сокращение путей в меню навигации                       |
| `path_max_depth`                               | number  | `3`                     | Максимальная глубина пути перед сокращением с "…" в меню навигации         |
| `fzf_path_truncate_enabled`                    | boolean | `false`                 | Включить/выключить сокращение путей в нечетком поиске (fzf)                |
| `fzf_path_max_depth`                           | number  | `5`                     | Максимальная глубина пути перед сокращением с "…" в fzf                    |
| `path_truncate_long_names_enabled`             | boolean | `false`                 | Включить/выключить сокращение длинных названий папок в меню навигации      |
| `fzf_path_truncate_long_names_enabled`         | boolean | `false`                 | Включить/выключить сокращение длинных названий папок в fzf                 |
| `path_max_folder_name_length`                  | number  | `20`                    | Максимальная длина названия папки перед сокращением в меню навигации       |
| `fzf_path_max_folder_name_length`              | number  | `20`                    | Максимальная длина названия папки перед сокращением в fzf                  |
| `history_size`                                 | number  | `10`                    | Количество директорий для хранения в истории                              |
| `history_fzf_path_truncate_enabled`            | boolean | `false`                 | Включить/выключить сокращение путей по глубине для отображения в истории |
| `history_fzf_path_max_depth`                   | number  | `5`                     | Максимальная глубина пути перед сокращением для истории                   |
| `history_fzf_path_truncate_long_names_enabled` | boolean | `false`                 | Включить/выключить сокращение длинных названий папок для истории          |
| `history_fzf_path_max_folder_name_length`      | number  | `30`                    | Максимальная длина названий папок перед сокращением для истории           |

### Конфигурация закладок

Плагин поддерживает упрощенный синтаксис закладок в конфигурации:

```lua
-- Упрощенный синтаксис (рекомендуется)
local bookmarks = {
  { tag = "Рабочий стол", path = "~/Desktop", key = "d" },
  { tag = "Проекты", path = "~/Projects", key = "p" },
}
```

**Особенности упрощенного синтаксиса:**

- **Расширение тильды** - `~` автоматически расширяется до домашней директории
- **Нормализация путей** - Разделители `/` автоматически конвертируются для вашей ОС
- **Автоматический завершающий разделитель** - Директории получают правильные завершающие разделители

### Сокращение путей

Сокращайте отображаемые пути по глубине через `path_truncate_enabled` и `path_max_depth` или по длине названий папок через `path_truncate_long_names_enabled` и `path_max_folder_name_length`. Оба режима по умолчанию выключены и включаются независимо.

Для поиска закладок (`fzf_path_*`) и истории директорий (`history_fzf_path_*`) есть отдельные настройки в [таблице параметров](#параметры-конфигурации). Они влияют только на отображение путей.

### Доступные команды

| Команда           | Описание                                                             |
| ----------------- | -------------------------------------------------------------------- |
| `save`            | Добавить закладку для выделенного файла/директории                   |
| `save_cwd`        | Добавить закладку для текущей рабочей директории                     |
| `save_temp`       | Добавить временную закладку для выделенного файла/директории         |
| `save_cwd_temp`   | Добавить временную закладку для текущей рабочей директории           |
| `jump_by_key`     | Открыть меню навигации для перехода к закладке по клавише            |
| `jump_key_<keys>` | Мгновенный переход к закладке по указанной последовательности клавиш |
| `jump_by_fzf`     | Открыть нечеткий поиск для перехода к закладке                       |
| `delete_by_key`   | Удалить закладку, выбрав по клавише                                  |
| `delete_by_fzf`   | Удалить несколько закладок с помощью fzf (TAB для выбора)            |
| `delete_all`      | Удалить все пользовательские закладки (исключая конфигурационные)    |
| `delete_all_temp` | Удалить все временные закладки                                       |
| `rename_by_key`   | Переименовать закладку, выбрав по клавише                            |
| `rename_by_fzf`   | Переименовать закладку с помощью нечеткого поиска                    |

### Прямой переход по ключу

Вы можете перейти к закладке без меню, передав последовательность клавиш напрямую в одном аргументе:

- `plugin whoosh jump_key_<keys>` - последовательность внутри аргумента, например `jump_key_k`, `jump_key_<Space>`, `jump_key_bb`.

Последовательности должны передаваться единым аргументом; формы с разделением пробелами не поддерживаются. Формат совпадает с окном редактирования закладки, поэтому можно комбинировать отдельные символы, значения через запятую и специальные клавиши вроде `<Space>` или `<A-l>`.

Корень проекта определяется динамически: whoosh идет вверх от текущей директории, пока не найдет файл или директорию `.git`. Этот путь не сохраняется в файл закладок.

Специальные клавиши меню обрабатываются раньше клавиш закладок, поэтому закладка с той же клавишей будет перекрыта специальным действием.

### Управление меню навигации

При использовании `jump_by_key` доступны следующие специальные элементы управления:

| Клавиша по умолчанию | Действие                                                 |
| -------------------- | -------------------------------------------------------- |
| `<Enter>`            | Создать временную закладку для текущей директории        |
| `<Space>`            | Открыть нечеткий поиск закладок                          |
| `<Tab>`              | Открыть историю директорий (только если есть история)    |
| `<Backspace>`        | Вернуться к предыдущей директории (только если доступно) |
| `-`                  | Перейти в корень текущего Git-репозитория                |
| `[a-zA-Z0-9]`        | Перейти к закладке с соответствующей клавишей            |

## Вдохновлено

- [yamb](https://github.com/h-hg/yamb.yazi)
- [bunny](https://github.com/stelcodes/bunny.yazi)

---

<!-- Локальная история звёзд, обновляется через .github/workflows/star-history.yml. -->
<p align="center">
  <a href="https://github.com/WhoSowSee/whoosh.yazi/stargazers">
    <picture>
      <source
        media="(prefers-color-scheme: dark)"
        srcset=".github/assets/star-history-dark-ru.svg"
      />
      <source
        media="(prefers-color-scheme: light)"
        srcset=".github/assets/star-history-light-ru.svg"
      />
      <img
        alt="История звёзд"
        src=".github/assets/star-history-light-ru.svg"
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
