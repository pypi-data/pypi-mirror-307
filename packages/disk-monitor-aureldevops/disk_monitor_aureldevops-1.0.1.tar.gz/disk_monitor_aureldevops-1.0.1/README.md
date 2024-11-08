# Démo : Créer et publier un module Python multi-fichiers

## Contexte

Nous allons structurer un module de surveillance disque avancé, appelé `disk_monitor`.

Il sera composé de plusieurs fichiers pour une meilleure organisation et contiendra des métadonnées comme la version et l'auteur. 

Ensuite, nous verrons comment l'utiliser dans un script.

Et enfin comment le publier sur PyPI afin de pouvoir l'installer avec pip :).

## Structure du projet

Organisons le projet comme suit :

```tree
disk_monitor_project/
├── disk_monitor/
│   ├── __init__.py
│   ├── disk_usage.py
│   ├── alert.py
│   └── version.py
├── monitor_script.py
└── setup.py
```

- **disk_monitor/** : dossier principal contenant les fichiers du module.
- **monitor_script.py** : script qui va utiliser le module `disk_monitor`.
- **setup.py** : fichier de configuration pour publier le module sur PyPI.

---

# Todo

- [ ] créer les fichiers du module
- [ ] utiliser le module dans un script
- [ ] préparer un fichier de setup pour PyPi
- [ ] publier le module sur PyPi