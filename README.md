# Cyber Shooter - Jeu Contrôlé par Vision

Un jeu de tir basé sur la vision par ordinateur où vous contrôlez le viseur avec votre main et tirez en faisant un clin d'œil !

## Fonctionnalités

-   **Visée par Suivi de la Main** : Déplacez votre index pour contrôler le viseur à l'écran.
-   **Clin d'œil pour Tirer** : Faites un clin d'œil (d'un œil ou de l'autre) pour tirer.
-   **Gameplay Dynamique** : Tirez sur les formes pour marquer des points, évitez de rater !
-   **Classement** : Suivez vos meilleurs scores.
-   **Esthétique Néon** : Style visuel inspiré du cyberpunk.

## Prérequis

-   Python 3.8+
-   Webcam

## Installation

1.  **Cloner le dépôt** (si applicable) ou télécharger le code source.
2.  **Configurer un environnement virtuel** (recommandé) :
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Sur Windows utilisez : venv\Scripts\activate
    ```
3.  **Installer les dépendances** :
    ```bash
    pip install -r requirements.txt
    ```

## Comment Lancer le Jeu

Vous pouvez facilement démarrer le jeu en utilisant le script d'aide fourni :

```bash
./run_game.sh
```

Ou manuellement :

```bash
python3 main.py
```

## Comment Jouer

1.  **Démarrer le Jeu** : Cliquez sur "START" dans le menu principal en utilisant le curseur de votre main (survolez le bouton).
2.  **Entrer le Nom** : Tapez votre nom et appuyez sur ENTRÉE.
3.  **Viser** : Levez votre main. Le viseur suit le bout de votre **index**.
4.  **Tirer** : **Faites un clin d'œil** (fermez brièvement un œil) pour tirer sur la cible.
5.  **Score** :
    -   Touchez les formes pour gagner des points.
    -   Ne ratez pas ! Rater un tir entraîne la FIN DE LA PARTIE (GAME OVER).
    -   Le jeu dure 2 minutes.
6.  **Pause** : Appuyez sur `P` pour mettre en pause/reprendre.
7.  **Menu** : Appuyez sur `ESPACE` pour retourner au menu depuis l'écran de fin de partie.

## Contrôles

-   **Souris/Main** : Viser
-   **Clin d'œil** : Tirer
-   **P** : Pause
-   **ESPACE** : Retour au Menu / Reprendre

## Dépannage

-   **La caméra ne fonctionne pas ?** Assurez-vous que votre webcam est connectée et n'est pas utilisée par une autre application.
-   **Lenteurs ?** Assurez-vous d'avoir un bon éclairage pour que la caméra puisse suivre votre main et votre visage efficacement.

## Crédits

Développé par Yahya Ismail.
