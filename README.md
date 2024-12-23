# Docker-final_project-tasks_manager

Par : Hamza HANINE – TD 45,
Adil MAAYOU - TD 45,
Chadi ZABOUJ - TD 46,
Ayoub GANI - TD 44

Adil Maayou = user 'test' dans github

Dans le cadre de ce projet, nous avons développé un gestionnaire de tâches où chaque utilisateur peut ajouter ou supprimer des tâches spécifiques.

Les utilisateurs et leurs mots de passe sont enregistrés dans une base de données MySQL (gérée via phpMyAdmin). Ces informations doivent être ajoutées manuellement par l'administrateur du projet. Par exemple, si ce projet est installé sur une autre machine, un nouvel identifiant utilisateur et un mot de passe devront être créés pour permettre la connexion. Il est également possible d’ajouter autant d’utilisateurs que nécessaire.



Les tâches que les utilisateurs peuvent gérer incluent les éléments suivants :

Titre : le nom de la tâche.

Description : un résumé ou les détails de la tâche.

Date : la date prévue pour accomplir la tâche.

Priorité : un système de classification en trois niveaux (Haute, Moyenne, Basse).

Ce gestionnaire de tâches vise à fournir une solution intuitive et efficace pour organiser les responsabilités de chaque utilisateur.


Toutes les bibliothèques nécessaires au projet sont répertoriées dans le fichier requirements.txt. En cas de problème, veuillez consulter ce fichier pour le débogage.

Pour commencer, vous devez construire le projet en exécutant la commande suivante : docker-compose up --build

Ensuite, vous pourrez accéder au site via l’adresse suivante : http://localhost


Pour accéder a la base de donnée veuillez utiliser l'adresse suivante :  http:/localhost:8080

Pour ajouter un utilisateur ou une tâche, utilisez les commandes SQL suivantes :

Ajouter un utilisateur :

INSERT INTO user (id, password) VALUES ('example', 'example123');


Ajouter une tâche :

INSERT INTO task (title, description, due_date, priority, created_by) VALUES ('Apprendre Flask', 'Créer un projet Flask', '2024-12-31', 'High', 'example');

Comme vous pouvez le constater, la clé étrangère created_by doit correspondre à un utilisateur existant dans la table user de la base de données.

Une fois la connexion réussie, vos tâches seront chargées, et vous aurez la possibilité d'ajouter, de supprimer ou de consulter vos tâches.
Si les identifiants de connexion ne sont pas valides, l'accès sera refusé et un message d'erreur vous invitera à réessayer.

