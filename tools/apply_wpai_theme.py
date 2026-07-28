# -*- coding: utf-8 -*-
"""One-shot theme + login shell patcher for index.html"""
from pathlib import Path
import re

p = Path(__file__).resolve().parents[1] / "index.html"
text = p.read_text(encoding="utf-8")

# Title + fonts
text = text.replace(
    "    <title>PyMason — Building Code. Logically.</title>\n\n    <!-- Blockly core",
    """    <title>PyMason — Wizard Productions AI Studio</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

    <!-- Blockly core""",
    1,
)

text = text.replace(
    '    <script src="https://unpkg.com/@blockly/keyboard-navigation@3.0.5/dist/index.js"></script>\n\n    <style>',
    '    <script src="https://unpkg.com/@blockly/keyboard-navigation@3.0.5/dist/index.js"></script>\n'
    '    <script src="auth.config.js"></script>\n\n    <style>',
    1,
)

root_new = """:root {
            /* WPAI Studio (wpaistudio.net) forge tokens */
            --bg-dark:      #0A0807;
            --panel:         #110F0D;
            --panel-border:  #2A211C;
            --leather:       #1A1614;
            --brass:         #FF7A26;
            --brass-dim:     #C45A18;
            --parch-bg:      #0A0807;
            --parch-fg:      #E8DCC8;
            --accent:        #E84A18;
            --fg:            #F5F5F5;
            --fg-muted:      #A89078;
            --danger:        #7F1D1D;
            --success:       #166534;
            --code-bg:       #0C0A09;
            --code-fg:       #F5E6D3;
            --keyword:       #FF7A26;
            --string:        #34D399;
            --comment:       #6B7280;
            --number:        #A78BFA;
            --forge-glow:    0 0 16px rgba(255, 122, 38, 0.35);
            --font-ui:       "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
            --font-heading:  "Cinzel", Georgia, serif;
            --font-mono:     ui-monospace, "SF Mono", "Cascadia Code", Consolas, monospace;
            --radius:        0.5rem;
        }"""
text2, n = re.subn(r":root \{[\s\S]*?--font-ui:[^;]+;\s*\}", root_new, text, count=1)
assert n == 1, n
text = text2

# Remove matrix rain CSS and fix body
text = text.replace(
    """        body {
            font-family: var(--font-ui);
            background: var(--bg-dark);
            color: var(--fg);
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            letter-spacing: 0.02em;
        }

        /* Digital rain sits behind the app chrome */
        #matrixRain {
            position: fixed;
            inset: 0;
            z-index: 0;
            pointer-events: none;
            opacity: 0.28;
        }

        .header, .main, .status-bar, .chat-panel, .help-panel, .toast {
            position: relative;
            z-index: 1;
        }""",
    """        body {
            font-family: var(--font-ui);
            background: var(--bg-dark);
            color: var(--fg);
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .header, .main, .status-bar, .chat-panel, .help-panel, .toast, #appShell {
            position: relative;
            z-index: 1;
        }

        #appShell {
            display: none;
            flex-direction: column;
            flex: 1;
            min-height: 0;
            overflow: hidden;
        }
        #appShell.visible { display: flex; }
""",
)

# Header chrome
text = text.replace(
    """        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 8px 16px;
            background: rgba(0, 20, 0, 0.92);
            border-bottom: 1px solid var(--brass-dim);
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.12);
            min-height: 48px;
            flex-shrink: 0;
            backdrop-filter: blur(2px);
        }""",
    """        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 8px 16px;
            background: hsl(23 18% 9% / 0.98);
            border-bottom: 1px solid var(--panel-border);
            box-shadow: 0 1px 0 rgba(255, 122, 38, 0.15);
            min-height: 52px;
            flex-shrink: 0;
        }""",
)

text = text.replace(
    """        .logo {
            font-family: var(--font-ui);
            font-size: 20px;
            font-weight: bold;
            color: var(--brass);
            text-shadow: var(--matrix-glow);
            text-transform: uppercase;
            letter-spacing: 0.12em;
        }

        .logo span {
            color: var(--accent);
            text-shadow: 0 0 10px rgba(182, 255, 0, 0.6);
        }

        .tagline {
            font-size: 11px;
            color: var(--fg-muted);
            font-style: normal;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }""",
    """        .logo {
            font-family: var(--font-heading);
            font-size: 20px;
            font-weight: 700;
            color: var(--brass);
            letter-spacing: 0.03em;
        }

        .logo span {
            color: var(--fg);
        }

        .tagline {
            font-size: 11px;
            color: var(--fg-muted);
            letter-spacing: 0.03em;
        }""",
)

text = text.replace(
    """        .btn {
            background: #001a00;
            color: var(--parch-fg);
            border: 1px solid var(--brass-dim);
            padding: 6px 12px;
            border-radius: 0;
            font-size: 11px;
            font-family: var(--font-ui);
            text-transform: uppercase;
            letter-spacing: 0.06em;
            cursor: pointer;
            transition: background 0.15s, color 0.15s, border-color 0.15s, box-shadow 0.15s;
        }

        .btn:hover {
            background: #003b00;
            color: var(--accent);
            border-color: var(--brass);
            box-shadow: var(--matrix-glow);
        }

        .btn-accent {
            background: #003b00;
            color: var(--brass);
            border-color: var(--brass);
            font-weight: 600;
            text-shadow: var(--matrix-glow);
        }

        .btn-accent:hover {
            background: #005500;
            color: #fff;
        }""",
    """        .btn {
            background: var(--panel);
            color: var(--parch-fg);
            border: 1px solid var(--panel-border);
            padding: 6px 12px;
            border-radius: var(--radius);
            font-size: 12px;
            font-family: var(--font-ui);
            font-weight: 500;
            cursor: pointer;
            transition: background 0.15s, color 0.15s, border-color 0.15s, box-shadow 0.15s;
        }

        .btn:hover {
            background: var(--leather);
            color: var(--brass);
            border-color: var(--brass-dim);
        }

        .btn-accent {
            background: var(--brass);
            color: #fff;
            border-color: var(--brass);
            font-weight: 600;
            box-shadow: var(--forge-glow);
        }

        .btn-accent:hover {
            background: #ff8f45;
            color: #fff;
        }""",
)

# Run / stop buttons
text = text.replace(
    """        .btn-run {
            background: #003b00;
            color: #00ff41;
            border: 1px solid #00ff41;
            font-weight: 700;
            padding: 6px 16px;
            text-shadow: var(--matrix-glow);
            box-shadow: 0 0 12px rgba(0, 255, 65, 0.25);
        }

        .btn-run:hover {
            background: #00ff41;
            color: #000;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.55);
        }""",
    """        .btn-run {
            background: var(--brass);
            color: #fff;
            border: 1px solid var(--brass);
            font-weight: 700;
            padding: 6px 16px;
            box-shadow: var(--forge-glow);
        }

        .btn-run:hover {
            background: #ff8f45;
            color: #fff;
        }""",
)

text = text.replace(
    """        .btn-stop {
            background: #2a0000;
            color: #ff4d4d;
            border: 1px solid #ff003c;
            font-weight: 600;
            display: none;
        }

        .btn-stop:hover {
            background: #4a0000;
            color: #fff;
        }""",
    """        .btn-stop {
            background: #3f1010;
            color: #fecaca;
            border: 1px solid #dc2626;
            font-weight: 600;
            display: none;
        }

        .btn-stop:hover {
            background: #7f1d1d;
            color: #fff;
        }""",
)

# Syntax highlight
text = text.replace(
    """        .py-keyword { color: #00ff41; font-weight: bold; text-shadow: 0 0 6px rgba(0,255,65,0.4); }
        .py-builtin { color: #b6ff00; }
        .py-string { color: #39ff14; }
        .py-fstring { color: #88ff88; }
        .py-comment { color: #006600; font-style: italic; }
        .py-number { color: #9aff9a; }
        .py-boolean { color: #00ff41; }
        .py-self { color: #66ff99; font-style: italic; }""",
    """        .py-keyword { color: #FF7A26; font-weight: 600; }
        .py-builtin { color: #FDBA74; }
        .py-string { color: #34D399; }
        .py-fstring { color: #6EE7B7; }
        .py-comment { color: #6B7280; font-style: italic; }
        .py-number { color: #A78BFA; }
        .py-boolean { color: #FF7A26; }
        .py-self { color: #FCA5A5; font-style: italic; }""",
)

# Code title / output
text = text.replace("var(--font-ui)", "var(--font-ui)")  # no-op guard

# Blockly theme component styles
text = text.replace(
    """            componentStyles: {
                workspaceBackgroundColour: '#000000',
                toolboxBackgroundColour: '#001a00',
                toolboxForegroundColour: '#00ff41',
                flyoutBackgroundColour: '#020a02',
                flyoutForegroundColour: '#39ff14',
                flyoutOpacity: 0.97,
                scrollbarColour: '#008f11',
                scrollbarOpacity: 0.7,
                insertionMarkerColour: '#00ff41',
                insertionMarkerOpacity: 0.55,
            },
            fontStyle: {
                family: 'Consolas, Courier New, monospace',
                weight: 'normal',
                size: 11,
            },""",
    """            componentStyles: {
                workspaceBackgroundColour: '#0A0807',
                toolboxBackgroundColour: '#1A1614',
                toolboxForegroundColour: '#E8DCC8',
                flyoutBackgroundColour: '#110F0D',
                flyoutForegroundColour: '#E8DCC8',
                flyoutOpacity: 0.97,
                scrollbarColour: '#C45A18',
                scrollbarOpacity: 0.65,
                insertionMarkerColour: '#FF7A26',
                insertionMarkerOpacity: 0.55,
            },
            fontStyle: {
                family: 'Inter, system-ui, sans-serif',
                weight: 'normal',
                size: 11,
            },""",
)

text = text.replace(
    """            grid: {
                spacing: 20,
                length: 2,
                colour: '#003b00',
                snap: true,
            },""",
    """            grid: {
                spacing: 22,
                length: 2,
                colour: '#2A211C',
                snap: true,
            },""",
)

# Toolbox CSS block - replace green matrix toolbox styles
old_tb = """        /* ── Blockly Theme Overrides (v12 class names) ─────── */
        .blocklyMainBackground {
            fill: #000000 !important;
        }

        /* Blockly 12 continuous toolbox */
        .blocklyToolbox,
        .blocklyToolboxDiv {
            background: #001a00 !important;
            border-right: 1px solid #00ff41 !important;
            box-shadow: 4px 0 18px rgba(0, 255, 65, 0.12);
            min-width: 140px !important;
            font-family: var(--font-ui) !important;
            color: #00ff41 !important;
            z-index: 20 !important;
        }

        .blocklyToolboxCategory,
        .blocklyTreeRow {
            padding: 8px 12px !important;
            margin: 2px 4px !important;
        }

        .blocklyToolboxCategoryLabel,
        .blocklyTreeLabel,
        .blocklyToolboxCategory .blocklyTreeLabel {
            font-family: var(--font-ui) !important;
            color: #00ff41 !important;
            text-shadow: 0 0 6px rgba(0, 255, 65, 0.35);
            font-size: 12px !important;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        .blocklyToolboxCategory:hover,
        .blocklyTreeRow:hover,
        .blocklyToolboxCategory.blocklyToolboxSelected,
        .blocklyToolboxSelected {
            background-color: rgba(0, 255, 65, 0.12) !important;
        }

        .blocklyToolboxCategoryIcon {
            filter: brightness(1.4) saturate(1.2);
        }

        .blocklyFlyoutBackground {
            fill: #020a02 !important;
            fill-opacity: 0.98 !important;
        }

        .blocklyFlyout {
            z-index: 30 !important;
        }

        .blocklyScrollbarBackground {
            fill: #001a00 !important;
        }

        .blocklyScrollbarHandle {
            fill: #008f11 !important;
        }

        /* Workspace sits above rain; toolbox must stay clickable */
        .blockly-panel,
        #blocklyDiv,
        .blocklySvg {
            z-index: 2;
        }"""

new_tb = """        /* ── Blockly Theme Overrides (v12 class names) ─────── */
        .blocklyMainBackground {
            fill: #0A0807 !important;
        }

        .blocklyToolbox,
        .blocklyToolboxDiv {
            background: #1A1614 !important;
            border-right: 1px solid #2A211C !important;
            min-width: 148px !important;
            font-family: var(--font-ui) !important;
            color: #E8DCC8 !important;
            z-index: 20 !important;
        }

        .blocklyToolboxCategory,
        .blocklyTreeRow {
            padding: 8px 12px !important;
            margin: 2px 4px !important;
            border-radius: 6px !important;
        }

        .blocklyToolboxCategoryLabel,
        .blocklyTreeLabel,
        .blocklyToolboxCategory .blocklyTreeLabel {
            font-family: var(--font-ui) !important;
            color: #E8DCC8 !important;
            font-size: 12px !important;
            font-weight: 500;
        }

        .blocklyToolboxCategory:hover,
        .blocklyTreeRow:hover,
        .blocklyToolboxCategory.blocklyToolboxSelected,
        .blocklyToolboxSelected {
            background-color: rgba(255, 122, 38, 0.12) !important;
        }

        .blocklyFlyoutBackground {
            fill: #110F0D !important;
            fill-opacity: 0.98 !important;
        }

        .blocklyFlyout { z-index: 30 !important; }

        .blocklyScrollbarBackground { fill: #1A1614 !important; }
        .blocklyScrollbarHandle { fill: #C45A18 !important; }

        .blockly-panel, #blocklyDiv, .blocklySvg { z-index: 2; }"""

if old_tb in text:
    text = text.replace(old_tb, new_tb)
    print("toolbox css ok")
else:
    print("WARNING toolbox css block not found")

# Toast
text = text.replace(
    """        .toast {
            position: fixed;
            bottom: 48px;
            right: 20px;
            background: #001a00;
            color: var(--brass);
            border: 1px solid var(--brass);
            padding: 10px 18px;
            border-radius: 0;
            font-size: 12px;
            font-family: var(--font-ui);
            text-transform: uppercase;
            letter-spacing: 0.08em;
            text-shadow: var(--matrix-glow);
            box-shadow: 0 0 16px rgba(0, 255, 65, 0.35);
            opacity: 0;
            transition: opacity 0.3s;
            pointer-events: none;
            z-index: 9999;
        }""",
    """        .toast {
            position: fixed;
            bottom: 48px;
            right: 20px;
            background: var(--panel);
            color: var(--brass);
            border: 1px solid var(--brass-dim);
            padding: 10px 18px;
            border-radius: var(--radius);
            font-size: 13px;
            font-family: var(--font-ui);
            box-shadow: var(--forge-glow);
            opacity: 0;
            transition: opacity 0.3s;
            pointer-events: none;
            z-index: 9999;
        }""",
)

# Output content greens
text = text.replace(
    """            color: #00ff41;
            white-space: pre-wrap;
            background: #000000;
            min-height: 60px;
            text-shadow: 0 0 5px rgba(0, 255, 65, 0.35);""",
    """            color: #F5E6D3;
            white-space: pre-wrap;
            background: #0C0A09;
            min-height: 60px;""",
)

text = text.replace(
    """        .output-content .error {
            color: #ff4d4d;
            text-shadow: 0 0 6px rgba(255, 0, 60, 0.4);
        }""",
    """        .output-content .error {
            color: #FCA5A5;
        }""",
)

text = text.replace(
    """        .output-content .input-field {
            background: #001a00;
            border: 1px solid var(--brass-dim);
            color: var(--brass);
            font-family: inherit;
            font-size: inherit;
            padding: 2px 6px;
            border-radius: 0;
            outline: none;
            width: 200px;
        }""",
    """        .output-content .input-field {
            background: var(--panel);
            border: 1px solid var(--panel-border);
            color: var(--fg);
            font-family: inherit;
            font-size: inherit;
            padding: 2px 6px;
            border-radius: 4px;
            outline: none;
            width: 200px;
        }""",
)

# Code output glow
text = text.replace(
    """            text-shadow: 0 0 4px rgba(0, 255, 65, 0.25);
        }

        .code-output .empty-state {
            color: var(--fg-muted);
            font-style: normal;
            font-family: var(--font-ui);
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }""",
    """        }

        .code-output .empty-state {
            color: var(--fg-muted);
            font-style: italic;
            font-family: var(--font-ui);
        }""",
)

# code-title uppercase matrix
text = text.replace(
    """        .code-title {
            font-family: var(--font-ui);
            font-size: 13px;
            color: var(--brass);
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            text-shadow: var(--matrix-glow);
        }""",
    """        .code-title {
            font-family: var(--font-heading);
            font-size: 14px;
            color: var(--brass);
            font-weight: 600;
        }""",
)

text = text.replace(
    """        .output-title {
            font-family: var(--font-ui);
            font-size: 12px;
            color: var(--brass);
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            text-shadow: var(--matrix-glow);
        }""",
    """        .output-title {
            font-family: var(--font-heading);
            font-size: 13px;
            color: var(--brass);
            font-weight: 600;
        }""",
)

# Selectors
text = text.replace(
    """        .ai-provider-select,
        .toolbox-mode-select,
        .lang-select {
            background: #001a00;
            color: var(--parch-fg);
            border: 1px solid var(--brass-dim);
            font-family: var(--font-ui);
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            padding: 4px 6px;
            border-radius: 0;
            max-width: 140px;
        }""",
    """        .ai-provider-select,
        .toolbox-mode-select,
        .lang-select {
            background: var(--panel);
            color: var(--parch-fg);
            border: 1px solid var(--panel-border);
            font-family: var(--font-ui);
            font-size: 12px;
            padding: 5px 8px;
            border-radius: var(--radius);
            max-width: 150px;
        }""",
)

# Append login gate CSS before </style>
login_css = """
        /* ── WPAI Login Gate (front door) ─────────────────── */
        #loginGate {
            position: fixed;
            inset: 0;
            z-index: 50000;
            display: flex;
            align-items: center;
            justify-content: center;
            background:
                radial-gradient(ellipse 80% 60% at 50% 0%, rgba(255, 122, 38, 0.18), transparent 55%),
                radial-gradient(ellipse 60% 50% at 80% 100%, rgba(232, 74, 24, 0.12), transparent 50%),
                #0A0807;
            padding: 24px;
        }
        #loginGate.hidden { display: none; }
        .login-card {
            width: min(420px, 100%);
            background: hsl(30 13% 6% / 0.95);
            border: 1px solid var(--panel-border);
            border-radius: 12px;
            padding: 32px 28px 28px;
            box-shadow: 0 0 40px rgba(255, 122, 38, 0.15), 0 24px 48px rgba(0,0,0,0.5);
        }
        .login-badge {
            display: inline-block;
            font-size: 11px;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--brass);
            border: 1px solid rgba(255,122,38,0.35);
            border-radius: 999px;
            padding: 4px 12px;
            margin-bottom: 16px;
        }
        .login-card h1 {
            font-family: var(--font-heading);
            font-size: 1.65rem;
            color: var(--fg);
            margin-bottom: 8px;
            line-height: 1.25;
        }
        .login-card h1 em {
            font-style: normal;
            color: var(--brass);
        }
        .login-card .lead {
            font-size: 13px;
            color: var(--fg-muted);
            margin-bottom: 22px;
            line-height: 1.55;
        }
        .login-card label {
            display: block;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--fg-muted);
            margin: 12px 0 6px;
        }
        .login-card input {
            width: 100%;
            background: var(--bg-dark);
            border: 1px solid var(--panel-border);
            color: var(--fg);
            border-radius: var(--radius);
            padding: 10px 12px;
            font-family: var(--font-ui);
            font-size: 14px;
            outline: none;
        }
        .login-card input:focus {
            border-color: var(--brass);
            box-shadow: 0 0 0 3px rgba(255,122,38,0.2);
        }
        .login-error {
            color: #FCA5A5;
            font-size: 12px;
            min-height: 18px;
            margin-top: 8px;
        }
        .login-actions {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-top: 18px;
        }
        .login-actions .btn-primary {
            width: 100%;
            padding: 12px;
            background: var(--brass);
            color: #fff;
            border: none;
            border-radius: var(--radius);
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            box-shadow: var(--forge-glow);
            font-family: var(--font-ui);
        }
        .login-actions .btn-primary:hover { background: #ff8f45; }
        .login-links {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            justify-content: center;
            margin-top: 18px;
            font-size: 12px;
        }
        .login-links a { color: var(--brass); text-decoration: none; }
        .login-links a:hover { text-decoration: underline; }
        .login-foot {
            margin-top: 16px;
            font-size: 11px;
            color: var(--fg-muted);
            text-align: center;
            line-height: 1.45;
        }
        .user-chip {
            font-size: 11px;
            color: var(--fg-muted);
            border: 1px solid var(--panel-border);
            border-radius: 999px;
            padding: 4px 10px;
            margin-right: 4px;
        }
        .user-chip strong { color: var(--brass); font-weight: 600; }

"""

if "/* ── WPAI Login Gate" not in text:
    text = text.replace("    </style>\n</head>", login_css + "    </style>\n</head>")
    print("login css ok")

# Body structure: remove canvas, wrap app, add login
text = text.replace(
    """<body>
    <canvas id="matrixRain" aria-hidden="true"></canvas>

    <!-- Header -->
    <div class="header" role="banner">
        <div class="header-left">
            <div class="logo" aria-label="PyMason">Py<span>Mason</span></div>
            <div class="tagline">Wake up, Neo… // Building Code. Logically.</div>
        </div>""",
    """<body>
    <!-- WPAI front-door login -->
    <div id="loginGate" role="dialog" aria-modal="true" aria-labelledby="loginTitle">
        <div class="login-card">
            <div class="login-badge">Human-directed · AI-assisted</div>
            <h1 id="loginTitle">Enter the <em>forge</em></h1>
            <p class="lead">PyMason is the front door to <strong>Wizard Productions AI Studio</strong> — visual Python, studio tools, and the work behind the brand.</p>
            <form id="loginForm" onsubmit="return handleLoginSubmit(event)">
                <label for="loginUser">Username or email</label>
                <input id="loginUser" name="username" autocomplete="username" required placeholder="studio">
                <label for="loginPass">Password</label>
                <input id="loginPass" name="password" type="password" autocomplete="current-password" required placeholder="••••••••">
                <div class="login-error" id="loginError" aria-live="polite"></div>
                <div class="login-actions">
                    <button type="submit" class="btn-primary">Sign in to PyMason</button>
                </div>
            </form>
            <div class="login-links">
                <a href="https://wpaistudio.net" target="_blank" rel="noopener">wpaistudio.net</a>
                <a href="https://wpaistudio.gumroad.com" target="_blank" rel="noopener">Storefront</a>
                <a href="https://github.com/MrWizard94-Compile" target="_blank" rel="noopener">GitHub</a>
            </div>
            <p class="login-foot" id="loginFootHint">Local demo: studio / wpai-forge — change users in auth.config.js for production.</p>
        </div>
    </div>

    <div id="appShell">
    <!-- Header -->
    <div class="header" role="banner">
        <div class="header-left">
            <div class="logo" aria-label="PyMason">Py<span>Mason</span></div>
            <div class="tagline">WPAI Studio · Building Code. Logically.</div>
        </div>""",
)

# Close appShell before toast/end of status — find status bar end and toast
# After status bar and before toast, we need logout button in header
if 'id="btnLogout"' not in text:
    text = text.replace(
        """            <button class="btn" onclick="toggleHelp()" title="Help &amp; reference (F1)">Help</button>
        </div>
        <input type="file" id="importFile" accept=".json" style="display:none" onchange="handleImport(event)">
    </div>""",
        """            <button class="btn" onclick="toggleHelp()" title="Help &amp; reference (F1)">Help</button>
            <span class="user-chip" id="userChip" hidden>Signed in as <strong id="userChipName"></strong></span>
            <button class="btn" id="btnLogout" onclick="logoutWPAI()" title="Sign out">Sign out</button>
        </div>
        <input type="file" id="importFile" accept=".json" style="display:none" onchange="handleImport(event)">
    </div>""",
    )

# Close #appShell before end of body - after electron section or before last script close
# Structure: toast is after status, then toolbox, then script. App shell should wrap everything until before scripts?
# Actually toolbox and script should be outside visual shell but toolbox is hidden xml. Wrap from header through toast/status.

# Find toast and close shell after status bar section ends (before toast is ok, or after toast)
if "</div>\n\n    <!-- Toast -->" in text and "<!-- /appShell -->" not in text:
    text = text.replace(
        """    <!-- Toast -->
    <div class="toast" id="toast"></div>

    <!-- Toolbox Definition -->""",
        """    <!-- Toast -->
    <div class="toast" id="toast"></div>
    </div><!-- /appShell -->

    <!-- Toolbox Definition -->""",
    )
    print("appShell close ok")

# Version bump
text = text.replace("const PYMASON_VERSION = '0.3.0';", "const PYMASON_VERSION = '0.3.1';")
text = text.replace("System ready — v'", "Ready — v'")

# Remove matrix rain IIFE
text2, n = re.subn(
    r"\n\s*// ═+\s*\n\s*//  MATRIX DIGITAL RAIN[\s\S]*?\)\(\);\s*\n",
    "\n",
    text,
    count=1,
)
if n:
    text = text2
    print("removed rain")
else:
    print("WARNING rain not removed")

# Fix auto-load to use auth gate
text = text.replace(
    """        // Auto-load workspace from localStorage on startup
        loadWorkspace();
        showWelcome();
""",
    """        // Auth gate then app boot
        // (loadWorkspace/showWelcome called after successful login)
""",
)

# Bulk green hardcoded UI remnants → forge (dialogs)
replacements = {
    "#001a00": "#1A1614",
    "#00ff41": "#FF7A26",
    "#39ff14": "#E8DCC8",
    "#003300": "#2A211C",
    "#006600": "#A89078",
    "#b6ff00": "#E84A18",
    "#003b00": "#C45A18",
    "background:#2A6A1A": "background:#FF7A26",
    "color:#E8F4E0": "color:#ffffff",
    "border:1px solid #3A8A2A": "border:1px solid #FF7A26",
    "font-family:Consolas,Courier New,monospace": "font-family:Inter,system-ui,sans-serif",
}
for a, b in replacements.items():
    text = text.replace(a, b)

p.write_text(text, encoding="utf-8")
print("done", p, "len", len(text))
