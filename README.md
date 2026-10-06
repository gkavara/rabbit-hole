# ₿ Rabbit Hole

*Proof of Knowledge · SHA-256 · 0x00–0xFF*

Bitcoin quiz στα ελληνικά, για maxis. 256 ερωτήσεις σε τρία επίπεδα (Pleb · Maxi · Cypherpunk), πόντοι σε sats, Block της ημέρας και πλέγμα 16×16 για να κάνεις mine όλες τις ερωτήσεις.

## Παίξε τοπικά
Άνοιξε το `index.html` σε οποιονδήποτε browser.

## Αλλαγές
1. Επεξεργάσου το `data/questions.json` ή το `src/template.html`.
2. `python3 build.py` (ελέγχει και φτιάχνει το `index.html`).
3. `git commit`.

## Δημοσίευση (GitHub Pages)
1. Ανέβασε τον φάκελο σε repository στο GitHub.
2. Settings → Pages → Deploy from branch → `main` / root.
3. `python3 build.py --link https://<user>.github.io/<repo>/` και ξανά push, για να μπαίνει το σωστό link στα share.

Don't trust, verify.
