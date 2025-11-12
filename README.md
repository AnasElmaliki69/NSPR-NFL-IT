# Arborescence du projet

```
# VM Nester (dashboard)
/home/admin1/dashboard
├── app.py                     # API Flask + dashboard + persistance JSON
├── data.json                  # Base de données JSON (créée automatiquement)
├── requirements.txt           # Dépendances Python (Flask)
├── .venv/                     # Environnement virtuel Python
└── templates/
    └── index.html             # Page HTML (tableau des rapports)

# Service (Nester)
 /etc/systemd/system/nester-dashboard.service

# VM Harvester (agent)
/home/admin1/harvester
├── send_report.py             # Script agent : collecte & envoi des métriques
└── harvester.log (optionnel)  # Logs si vous les redirigez ici

# Cron (Harvester) – pas un fichier, mais une entrée crontab
(crontab -e)  ->  * * * * * /usr/bin/python3 /home/admin1/harvester/send_report.py >> /home/admin1/harvester/send_report.log 2>&1
```

---

# À quoi sert chaque fichier ? (résumé)

## VM Nester (dashboard)

* **`app.py`**

  * **Rôle :** Serveur **Flask** qui expose l’API et le mini dashboard.
  * **Routes :**

    * `POST /api/report` — reçoit un rapport JSON depuis les Harvesters, l’ajoute à `data.json`.
    * `GET /api/reports` — renvoie tous les rapports au format JSON.
    * `GET /` — affiche un **tableau HTML** (templates/index.html) des rapports.
  * **Persistance :** charge et sauvegarde les données dans **`data.json`** (atomic write).

* **`templates/index.html`**

  * **Rôle :** Vue HTML (Jinja) affichant un tableau des machines rapportées (node, IP, devices, latency, last update).

* **`data.json`**

  * **Rôle :** “petite base de données” JSON. **Créée automatiquement** lors du premier POST.
  * **Remarque :** survive aux redémarrages (contrairement à la mémoire RAM).

* **`.venv/`**

  * **Rôle :** Environnement virtuel Python (isoler Flask et les libs).

* **`requirements.txt`**

  * **Rôle :** Liste minimale des dépendances (`Flask`). Permet un `pip install -r requirements.txt`.

* **`/etc/systemd/system/nester-dashboard.service`**

  * **Rôle :** Service **systemd** pour lancer le dashboard **en arrière-plan** et **au démarrage** de la VM.
  * **Commandes utiles :**

    * `sudo systemctl enable --now nester-dashboard`
    * `sudo systemctl status nester-dashboard`
    * `sudo systemctl restart nester-dashboard`

---

## VM Harvester (agent)

* **`send_report.py`**

  * **Rôle :** Agent qui **collecte** de petites métriques (nom d’hôte, IP, latence ping, nombre d’hôtes — si `nmap` installé) et les **envoie** au Nester via `POST /api/report`.
  * **Config :** l’URL du Nester est dans la constante/variable `NESTER` (ex. `http://192.168.56.103:5000`).
  * **Dépendance :** `requests` (installée via `pip`).

* **Entrée `cron` (crontab)**

  * **Rôle :** Lance `send_report.py` **toutes les minutes** automatiquement.
  * **Exemple :**

    ```
    * * * * * /usr/bin/python3 /home/admin1/harvester/send_report.py >> /home/admin1/harvester/send_report.log 2>&1
    ```
  * **Effet :** Le dashboard se met à jour en continu, même si vous ne tapez aucune commande.

---

# (Optionnel) Sécurisation par clé API

* **Côté Nester (dans `app.py`) :** vérifier l’entête `X-API-Key` dans `/api/report`.
* **Côté service systemd :** définir la clé dans l’environnement
  `Environment="NESTER_API_KEY=MaCleTresSecrete"`
* **Côté Harvester :** ajouter l’entête `X-API-Key` dans la requête `requests.post(...)`.

---

# Ce que fait l’ensemble (vue d’ensemble)

1. Le **Harvester** exécute `send_report.py` (manuellement ou via **cron**) → envoie un JSON au **Nester**.
2. Le **Nester** (Flask) reçoit via `POST /api/report`, sauvegarde dans **`data.json`**, met à jour la mémoire.
3. La page `http://<ip-nester>:5000/` affiche le tableau actualisé ; `GET /api/reports` fournit le JSON brut.
4. Le service **systemd** garantit que le dashboard est **toujours en ligne**.




### 🖥️ Sur la machine **Nester (dashboard)** :


* `app.py` → l’application **Flask** (le cœur de l’API et du tableau de bord).
* `index.html` → le **modèle HTML** du tableau de bord (dans le dossier `/templates`).
* `server.py` → le **lanceur** du serveur (optionnel) qui exécute l’application Flask avec **Waitress**, un serveur web plus stable que celui de développement.

👉 Donc `server.py` sert uniquement **sur le Nester** — il fait tourner le tableau de bord.

---

### 💻 Sur la machine **Harvester (agent)** :


* `send_report.py` → le script qui **collecte les données** locales (nom de la machine, IP, latence, etc.) et les **envoie** au Nester via l’API `/api/report`.

C’est la partie **client**.

---

### 🧩 Résumé

| Machine       | Script                 | Rôle                                       |
| ------------- | ---------------------- | ------------------------------------------ |
| **Nester**    | `app.py`               | Définit l’API (logique du serveur)         |
| **Nester**    | `server.py`            | Lance le serveur Flask (dashboard)         |
| **Nester**    | `templates/index.html` | Affiche les rapports (interface web)       |
| **Harvester** | `send_report.py`       | Envoie les données au Nester régulièrement |

---






