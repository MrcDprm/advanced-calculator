<p align="center">
  <img src="assets/icon.png" alt="Advanced Calculator icon" width="96">
</p>

<h1 align="center">Advanced Calculator</h1>

<p align="center">
  <b>English</b> | <a href="README.tr.md">Türkçe</a>
</p>

<p align="center">
  A standard and scientific calculator written in Python and Tkinter, inspired by the Windows Calculator.<br>
  Expressions are evaluated by a parser written from scratch, without using <code>eval()</code>.
</p>

<p align="center">
  <a href="https://github.com/MrcDprm/advanced-calculator/releases/latest"><b>⬇️ Download for Windows</b></a>
</p>

<p align="center">
  <img src="docs/demo.gif" alt="Animation showing the calculator in use" width="360">
</p>

> The user interface is in Turkish (the app is called *Gelişmiş Hesap Makinesi*).

## Features

**Calculation**
- Four basic operations, exponents, parentheses and correct operator precedence (`2 + 3 * 4 = 14`)
- Implicit multiplication: `2(3)`, `(1+2)(3+4)`, `2π`
- Scientific functions: `sin`, `cos`, `tan` (degrees / radians), `log`, `ln`, `√`, `|x|`, `n!`, `x²`, `1/x`, `±`
- Constants: `π` and `e`
- Percent works like in Windows and Google: `200 + 10% = 220`
- Scientific notation for very large and very small numbers (`1e+25`), thousands separator (`1,234,567`)
- Floating-point noise is cleaned up: `0.1 + 0.2 = 0.3`, `sin(180°) = 0`
- Clear error messages: division by zero, undefined operations, unclosed parentheses, etc.

**Interface**
- Standard and scientific modes
- Light and dark themes
- History panel: clicking an old calculation brings it back to the display
- Memory keys: `MC`, `MR`, `M+`, `M-`
- Windows Calculator keyboard shortcuts and button tooltips
- Typing at the cursor position, deleting function names in one go
- Safe copy / paste
- Resizable window
- Theme, mode, angle unit and history are remembered after closing the app

**Other**
- Console version (`main.py`)
- 17 unit tests
- Setup wizard: Start menu shortcut, uninstall support

## Screenshots

| Standard (dark) | Scientific (light) |
|---|---|
| <img src="docs/standard-dark.png" alt="Standard mode, dark theme" width="300"> | <img src="docs/scientific-light.png" alt="Scientific mode, light theme" width="300"> |

**Scientific mode and history panel**

<img src="docs/scientific-history-dark.png" alt="Scientific mode and history panel" width="520">

## Installation

1. Download `AdvancedCalculator-x.y.z-Setup.exe` from the [Releases](https://github.com/MrcDprm/advanced-calculator/releases/latest) page.
2. Run it and follow the setup steps. No administrator rights are needed.
3. Find the app in the Start menu as **Gelişmiş Hesap Makinesi**.

> **Windows "protected your PC" warning:** The app is not digitally signed, so Windows SmartScreen may show a warning on first launch. Continue with **More info → Run anyway**. The full source code is open in this repository.

**Uninstall:** Settings → Apps → Installed apps → Gelişmiş Hesap Makinesi → Uninstall.
History and settings are kept in `%USERPROFILE%\.advanced-calculator` and are not deleted on uninstall.

## Keyboard Shortcuts

| Key | Action | Key | Action |
|---|---|---|---|
| `Enter` or `=` | Calculate | `Esc` | Clear |
| `Backspace` / `Delete` | Delete (function names are deleted as a whole) | `Ctrl+C` / `Ctrl+V` | Copy / paste |
| `s` / `o` / `t` | sin / cos / tan | `F3` / `F4` | Degrees / radians |
| `l` / `n` | log / ln | `p` / `e` | π / e |
| `q` | x² | `r` | 1/x |
| `@` | √ | `F9` | ± |
| `\|` | \|x\| | `!` / `%` | Factorial / percent |
| `Ctrl+L` / `Ctrl+R` | Memory clear / memory recall | `Ctrl+P` / `Ctrl+Q` | Memory add / memory subtract |
| `Ctrl+H` | History panel | `Alt+1` / `Alt+2` | Standard / scientific mode |

A dot is used as the decimal separator; the comma key on the keyboard (numpad included) automatically types a dot.

## Tech Stack

- **Python 3.12**: standard library only, no external packages
- **Tkinter**: user interface
- **unittest**: unit tests
- **PyInstaller**: Windows `.exe` build
- **Inno Setup**: setup wizard

## Project Structure

```
advanced-calculator/
├── gui.py          # Tkinter interface
├── main.py         # Console interface
├── tokenizer.py    # Splits the expression into tokens
├── evaluator.py    # Evaluates tokens by operator precedence (recursive descent parser)
├── formatter.py    # Formats the result for display
├── history.py      # Keeps the calculation history
├── storage.py      # Saves history and settings to a JSON file
├── tooltip.py      # Button tooltips
├── app_info.py     # App name, version, resource paths
├── assets/         # App icon
├── docs/           # README images
├── installer/      # Inno Setup script
└── tests/          # Unit tests
```

## Running from Source

Requires Python 3.12 or newer.

```bash
python gui.py     # interface
python main.py    # console version
python -m unittest -v    # tests
```

### Building the installer

Requires [PyInstaller](https://pyinstaller.org) and [Inno Setup 6](https://jrsoftware.org/isinfo.php).

```bash
python -m pip install pyinstaller
python -m PyInstaller --noconfirm AdvancedCalculator.spec
ISCC installer/advanced-calculator.iss
```

The installer is created in the `installer/Output/` folder.

**When releasing a new version:** update the version number in both `app_info.py` (`VERSION`) and `installer/advanced-calculator.iss` (`AppVersion`), run the tests, run both build commands and upload the installer to a new GitHub Release.

## What I Learned

- **A calculator is really a small language parser.** I learned to first split the text into tokens, then handle operator precedence by writing a separate function for each precedence level (recursive descent parser). Using `eval()` would have been a one-liner, but it is both unsafe and teaches nothing.
- **Computers cannot store decimal numbers exactly.** I saw why `0.1 + 0.2` gives `0.30000000000000004`, and why rounding and "very close to zero" checks are needed to show results correctly.
- **Splitting code into files by responsibility pays off.** Because the calculation code was separate, I did not touch it at all when moving from the console to the graphical interface.
- **Desktop UI with Tkinter.** I learned grid layout (`grid`), events (`bind`), `StringVar`, themes and writing my own tooltip widget. I learned the hard way about the "closure trap" of using `lambda` inside a loop and how much indentation matters in Python.
- **There is a big gap between "it works" and "it's user-friendly".** Thinking about small details such as where the cursor stays, what happens after an error, keyboard shortcuts and the comma key on a Turkish keyboard was most of the work.
- **Showing errors clearly to the user.** I learned to catch errors with `try/except` and turn them into readable messages, and to keep the program from crashing because of a broken settings file.
- **Automated tests.** I learned to write tests with `unittest` and to use `mock` so the tests do not touch my real files. The tests immediately show whether a later change broke an existing feature.
- **Distributing a program.** I learned to build an `.exe` that runs on computers without Python using PyInstaller, to create a setup wizard with Inno Setup, and why user data belongs in the user folder instead of the program folder.
- **Working with Git regularly.** I made it a habit to save every step in small, meaningful commits using the Conventional Commits format.

## Future Plans

- Automatically shrinking the font as the result gets longer
- Inverse trigonometric functions (`asin`, `acos`, `atan`) and hyperbolic functions
- Programmer mode (binary, octal, hexadecimal)
- Multiple memory slots (`MS` and a memory list)
- English interface option
- Packages for macOS and Linux

## License

[MIT](LICENSE) © 2026 Miraç Deprem
