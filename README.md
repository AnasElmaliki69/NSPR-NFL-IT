# 🏈 Seahawks Monitoring — NSPR / MSPR Project

Projet MSPR TPRE552 – Bachelor Cyb3rXP 2025 / 2026  
Réalisation : **Anas EL MALIKI**, **Mariama BENKHALID**, **Xavier MEYER**

---

## 📘 Introduction

Dans le cadre de la MSPR Développement et Sécurité Informatique du Bachelor Cyb3r XP, notre groupe a été chargé de concevoir **une solution de supervision réseau** pour la société **NFL IT**, dans le cadre du programme _Seahawks Monitoring_.

L’objectif principal était de fournir une **solution simple, sécurisée et capable d’unifier la supervision réseau** entre plusieurs sites à distance, avec un système capable de :

- Collecter automatiquement les données réseau
- Centraliser les résultats
- Générer des rapports lisibles
- Offrir une interface de consultation fiable et sécurisée

---

## 📌 Contexte du projet

NFL IT est une entreprise spécialisée dans l’infogérance, la gestion d’infrastructures multi-sites, et l’accompagnement technique des équipes de football américain de la **National Football League (NFL)**.

Cependant, l’entreprise rencontre plusieurs difficultés :

- Une supervision réseau fragmentée
- Une absence d’outil centralisé
- Des diagnostics lents et coûteux
- Un manque de visibilité sur les performances

Notre projet vise à répondre à ce besoin en construisant un système simple, efficace et sécurisé.

---

## ❓ Problématique

L’entreprise ne dispose pas d’un outil capable de :

- Superviser le réseau en temps réel à distance
- Automatiser la collecte de données techniques
- Fournir un tableau de bord centralisé
- Garantir l’intégrité et la sécurité des rapports

👉 **Problème central :**  
**Comment créer une solution unifiée, automatisée et sécurisée capable de superviser plusieurs réseaux distants depuis un point central ?**

---

## 🎯 Objectifs du projet

### **Objectif principal :**

Créer un système composé de **Harvester** (collecteurs) et d’un **Nester** (serveur central) permettant la collecte, l’analyse et la visualisation des données réseau.

### **Objectifs secondaires :**

- Automatiser les scans réseau (hosts, ports, configurations)
- Générer des rapports structurés en temps réel
- Héberger les résultats sur un serveur web central (Nginx)
- Sécuriser l’accès au serveur (authentification + hash bcrypt)
- Faciliter la prise en main pour les techniciens N1/N2
- Documenter et standardiser la démarche

---

## 👥 Présentation des membres

| Nom                   | Rôle                          | Responsabilités principales                       |
| --------------------- | ----------------------------- | ------------------------------------------------- |
| **Anas EL MALIKI**    | Développeur / Intégrateur     | Scripts Python, intégration, gestion du dépôt Git |
| **Mariama BENKHALID** | Administratrice Système       | VM, réseau interne, configuration système         |
| **Xavier MEYER**      | Responsable Sécurité / DevOps | Nginx, sécurité, HTTPS, durcissement              |

---

## 🧱 Architecture du système

### 🗂️ Schéma global du projet


<img width="1143" height="557" alt="Architecture du système" src="https://github.com/user-attachments/assets/a09802c7-40fa-4415-ba67-c2d5b56aff89" />

Le système repose sur :

- **Harvester** (client) :  
  Collecte les informations réseau → génère un rapport → l’envoie au serveur

- **Nester** (serveur central) :  
  Reçoit les rapports → les organise → les affiche via un serveur web Nginx

### Composants :

- 2 VM VirtualBox (Debian)
- Nginx (serveur web)
- Python 3 + Nmap (scan)
- DuckDNS (nom de domaine dynamique)
- Système d’authentification sécurisé (bcrypt + JSON)
- Automatisation des tâches (cron)

---

## 🗂️ Gestion de projet — Planning

### 📅 Diagramme de Gantt / Chronologie


<img width="1054" height="637" alt="Planning du projet" src="https://github.com/user-attachments/assets/57962844-940c-43f3-a964-aecedd93bba8" />


### 📌 Phases principales

1. **Analyse du besoin**
2. **Modélisation & architecture**
3. **Installation des machines virtuelles**
4. **Configuration réseau & sécurité**
5. **Développement des scripts**
6. **Mise en place du serveur Nginx**
7. **Tests & validations**
8. **Rédaction du rapport**

---

## 🛠️ Technologies utilisées

| Technologie      | Rôle                   | Justification                   |
| ---------------- | ---------------------- | ------------------------------- |
| **Python 3**     | Scan & automatisation  | Flexible, puissant, maintenable |
| **python-nmap**  | Scan réseau            | Intégration simple avec Python  |
| **Nmap**         | Collecte réseau        | Standard industriel             |
| **Nginx**        | Serveur web            | Léger, rapide, sécurisé         |
| **DuckDNS**      | DNS dynamique          | Accès distant gratuit           |
| **bcrypt**       | Hash des mots de passe | Sécurisation                    |
| **VirtualBox**   | Environnement virtuel  | Simule un réseau complet        |
| **Git / GitHub** | Travail collaboratif   | Versioning & transparence       |

---

## 🔐 Sécurité

### Mesures mises en place :

- Hashage des mots de passe avec **bcrypt**
- Aucun mot de passe en clair
- Fichiers JSON protégés
- Accès contrôlé via Nginx
- Sécurisation du serveur (permissions, firewall, durcissement)
- Structure stable & modulaire des scripts

---

## 🧪 Tests (résumé)

Les tests ont permis de valider :

- La communication entre les machines
- L'exécution automatique des scans
- La génération correcte des rapports
- La transmission fiable au serveur
- Le fonctionnement du serveur web Nginx
- La solidité du système d’authentification

⚠️ _Les captures techniques (ping, résultats scans, terminal…) sont uniquement disponibles dans le rapport complet._

---

## 📄 Rapport complet

Le rapport complet (avec toutes les captures techniques, résultats détaillés, configurations et preuves) est disponible ici :

---

## 📚 Conclusion

Ce projet nous a permis de :

- Déployer une architecture réseau réaliste
- Mettre en place une solution complète de supervision
- Renforcer nos compétences en Python, sécurité, et administration système
- Collaborer efficacement en équipe
- Produire une documentation professionnelle

La solution Seahawk Monitoring fournit désormais une **base robuste, sécurisée et évolutive** pour la supervision réseau multi-sites.

---

## 👨‍💻 Auteurs

- **Anas EL MALIKI**
- **Mariama BENKHALID**
- **Xavier MEYER**
