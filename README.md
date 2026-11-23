# 🗑️ Poubelle intelligente – Projet IoT et IA

## 1. Présentation du projet

Ce projet consiste à concevoir une poubelle intelligente basée sur l'Internet des objets (IoT) et l'intelligence artificielle (IA).

L'objectif est de faciliter la gestion des déchets grâce à un système capable de détecter le niveau de remplissage de la poubelle, de signaler lorsqu'elle est presque pleine et de prévoir son évolution à l'aide de modèles d'apprentissage automatique.

## 2. Objectifs

- Mesurer automatiquement le niveau de remplissage de la poubelle.
- Détecter la présence d'une personne pour commander l'ouverture automatique du couvercle.
- Déclencher une alerte lorsque la poubelle atteint un niveau de remplissage élevé.
- Exploiter les données pour prévoir le niveau de remplissage futur.
- Visualiser les informations sur un tableau de bord.

## 3. Matériel utilisé

- ESP32 : carte de commande et de communication.
- Capteurs ultrasoniques HC-SR04 : mesure du niveau de remplissage et détection de la présence d'une main.
- Servomoteur SG90 : ouverture et fermeture du couvercle.
- LED rouge : signalisation visuelle.
- Buzzer : signalisation sonore.
- Résistance de 220 Ω.

## 4. Technologies utilisées

- **Arduino / C++** : programmation de l'ESP32.
- **Wokwi** : simulation du circuit électronique.
- **Python** : traitement et analyse des données.
- **Scikit-learn** : modèles d'apprentissage automatique.
- **Streamlit** : création du tableau de bord interactif.
- **Pandas et Matplotlib** : manipulation et visualisation des données.

## 5. Fonctionnement du système

1. Le capteur ultrasonique mesure le niveau de remplissage.
2. Lorsqu'une main est détectée, le servomoteur commande l'ouverture du couvercle.
3. Lorsque le niveau de remplissage dépasse le seuil défini, une alerte est déclenchée.
4. Les données collectées sont exploitées pour analyser et prévoir l'évolution du remplissage.
5. Un tableau de bord permet de visualiser les informations et les prévisions.

## 6. Intelligence artificielle

Le projet utilise des modèles d'apprentissage automatique pour estimer le niveau de remplissage futur de la poubelle.

Les modèles étudiés sont :
- La régression linéaire.
- La forêt aléatoire (Random Forest).

**Remarque :** les données actuellement utilisées pour les essais sont simulées. Les performances obtenues doivent être interprétées dans ce contexte.

## 7. Structure du dépôt

- `sketch.ino` : programme de l'ESP32.
- `diagram.json` : schéma de câblage du circuit dans Wokwi.
- `libraries.txt` : bibliothèques nécessaires à la simulation.
- `app.py` : application du tableau de bord Streamlit.
- `requirements.txt` : dépendances Python.
- `donnees_poubelle.csv` : jeu de données utilisé.
- `poubelle_intelligente_IA.ipynb` : notebook d'analyse et de prédiction.

## 8. Lancer le tableau de bord

Installer les dépendances :

```bash
pip install -r requirements.txt
```

Lancer l'application :

```bash
streamlit run app.py
```

## 9. État du projet

Projet en cours de développement. La simulation électronique, l'analyse des données et le tableau de bord constituent les différentes parties du travail. Des améliorations et des tests supplémentaires sont prévus.

## 10. Auteur

**PAPAKADYBA**

Projet académique – IoT et Intelligence artificielle.
