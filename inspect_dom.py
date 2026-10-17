import json
import sys
from cdp import CDP, http_json
from config import Config

def main():
    cfg = Config()
    cdp_url = f"http://127.0.0.1:{cfg.cdp_port}/json"
    try:
        raw_tabs = http_json(cdp_url)
    except Exception as e:
        print(f"Cannot connect to CDP at {cdp_url}: {e}")
        return

    tabs = [t for t in raw_tabs if t.get("type") == "page" and "muse.ai" in t.get("url", "")]
    if not tabs:
        tabs = [t for t in raw_tabs if t.get("type") == "page"]
    if not tabs:
        print("No open browser tabs found!")
        return

    target = tabs[0]
    print(f"Inspecting active tab: {target.get('url')}")
    page = CDP(target["webSocketDebuggerUrl"])

    res = page.js("""
    (() => {
        const inputs = Array.from(document.querySelectorAll('input[type="file"]')).map(x => ({
            id: x.id,
            name: x.name,
            accept: x.accept,
            outerHTML: x.outerHTML.slice(0, 200)
        }));
        const buttons = Array.from(document.querySelectorAll('button')).map(b => ({
            ariaLabel: b.getAttribute('aria-label') || '',
            text: (b.innerText || '').slice(0, 50).trim(),
            className: (b.className || '').slice(0, 100),
            hasSvg: !!b.querySelector('svg')
        })).filter(b => b.ariaLabel || b.text || b.hasSvg);
        const composer = !!document.querySelector('[data-testid="hatch-composer-placeholder-overlay"]');
        const textarea = !!document.querySelector('textarea');
        return JSON.stringify({
            url: window.location.href,
            inputs: inputs,
            attachButtons: buttons.filter(b => /attach|file|clip|upload|add|plus|đính|ảnh|tệp|移除|添加/i.test(b.ariaLabel + ' ' + b.text)),
            allButtonsSample: buttons.slice(0, 15),
            hasComposerOverlay: composer,
            hasTextarea: textarea
        }, null, 2);
    })()
    """)

    print("=== DOM INSPECTION RESULT ===")
    print(res)

if __name__ == "__main__":
    main()
