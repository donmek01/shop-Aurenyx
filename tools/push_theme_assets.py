from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import urllib.error
import urllib.request


THEME_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = THEME_ROOT.parents[2]
SHOPIFY_ENV = PROJECT_ROOT / "Picture_link" / "shopify_api.env"
SHOPIFY_HELPER = PROJECT_ROOT / "scripts" / "shopify_link_product_images.py"
API_VERSION = "2026-04"


def load_helper():
    spec = importlib.util.spec_from_file_location("shopify_link_product_images", SHOPIFY_HELPER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load Shopify helper: {SHOPIFY_HELPER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rest(auth, method: str, path: str, payload: dict | None = None) -> dict:
    url = f"https://{auth.shop}/admin/api/{API_VERSION}{path}"
    data = None
    headers = {
        "X-Shopify-Access-Token": auth.token(),
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        text = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Shopify REST {method} {path} failed HTTP {exc.code}: {text[:1600]}") from exc


def get_theme_id(auth, live: bool, theme_id: str | None) -> str:
    if theme_id:
        return theme_id
    payload = rest(auth, "GET", "/themes.json")
    themes = payload.get("themes", [])
    if live:
        for theme in themes:
            if theme.get("role") == "main":
                return str(theme["id"])
        raise RuntimeError("No live/main theme found.")
    print("Themes:")
    for theme in themes:
        print(f"- {theme.get('id')} role={theme.get('role')} name={theme.get('name')}")
    raise RuntimeError("Pass --live or --theme-id THEME_ID.")


def push_asset(auth, theme_id: str, relative_file: str) -> None:
    local_path = (THEME_ROOT / relative_file).resolve()
    try:
        local_path.relative_to(THEME_ROOT)
    except ValueError as exc:
        raise RuntimeError(f"Path outside theme root: {relative_file}") from exc
    if not local_path.exists():
        raise RuntimeError(f"Missing local file: {local_path}")
    key = relative_file.replace("\\", "/")
    value = local_path.read_text(encoding="utf-8")
    rest(auth, "PUT", f"/themes/{theme_id}/assets.json", {"asset": {"key": key, "value": value}})
    print(f"Pushed {key}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Push selected Shopify theme assets via Admin API.")
    parser.add_argument("files", nargs="+", help="Theme-relative files, e.g. layout/theme.liquid")
    parser.add_argument("--live", action="store_true", help="Push to live/main theme")
    parser.add_argument("--theme-id", help="Explicit Shopify theme ID")
    args = parser.parse_args()

    helper = load_helper()
    auth = helper.resolve_shopify_auth(helper.load_env(SHOPIFY_ENV))
    theme_id = get_theme_id(auth, live=args.live, theme_id=args.theme_id)
    print(f"Using theme_id={theme_id}")
    for file in args.files:
        push_asset(auth, theme_id, file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
