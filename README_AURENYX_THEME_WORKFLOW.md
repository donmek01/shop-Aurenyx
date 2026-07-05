# AURENYX Shopify Theme Workflow

Dieses Verzeichnis ist das Arbeits-Theme fuer `shop.aurenyx.eu`.

## Wichtig

- Nicht mehr jedes Mal ZIP manuell hochladen.
- Theme-Dateien werden in Git versioniert.
- Shopify Live-Theme sollte spaeter per GitHub-Integration oder Shopify CLI verbunden werden.

## Sofort-Hotfix ohne ZIP

Wenn die Admin-App Theme-Rechte hat:

```powershell
python tools/push_theme_assets.py --live layout/theme.liquid snippets/meta-tags.liquid sections/header-group.json
```

Falls Shopify `read_themes/write_themes` verweigert, muss die Custom App in Shopify Admin diese Scopes bekommen und neu installiert werden.

## GitHub Workflow

1. In GitHub ein neues privates Repo erstellen, z. B. `aurenyx-shopify-theme`.
2. Lokal Remote setzen:

```powershell
git remote add origin https://github.com/DEIN-ACCOUNT/aurenyx-shopify-theme.git
git add .
git commit -m "Initial AURENYX Shopify theme"
git branch -M main
git push -u origin main
```

3. Shopify Admin:
   - Online Store -> Themes
   - Add theme -> Connect from GitHub
   - Repo und Branch `main` verbinden

Danach kann jede Theme-Aenderung per Git Commit/Push deployt werden.

## Navigation Deutsch

Der Header nutzt aktuell das Shopify-Menue `main-menu`.
Wenn im Shop `Home / Catalog / Contact` angezeigt wird, muss in Shopify Admin unter:

`Online Store -> Navigation -> Main menu`

die Linkliste deutsch angepasst werden:

- Wella -> `/collections/wella-professional`
- hioo / Eigenmarke -> `/collections/aurenyx-professional`
- Haarpflege -> `/collections/haarpflege`
- Coloration -> `/collections/haarfarbe-coloration`
- Styling -> `/collections/styling-finish`
- Friseurbedarf -> `/collections/friseurbedarf`
- Alle Produkte -> `/collections/alle-produkte`

Alternativ kann ein neues Menue mit Handle `main-menu` oder ein eigenes `aurenyx-shop-menu` genutzt werden.
