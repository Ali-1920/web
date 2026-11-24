# Gestion du cabinet médical

Application Django 5.2 de gestion des médecins, patients, spécialités et
rendez-vous, avec interface web, administration Django et API REST.

Les applications métier sont `AccountApp` (utilisateurs, médecins, patients,
spécialités) et `AppointmentApp` (rendez-vous). Le modèle utilisateur actif est
`AccountApp.User`.

## Installation

```powershell
uv sync
.\.venv\Scripts\Activate.ps1
```

Le projet utilise Python 3.12 ou une version ultérieure compatible avec Django
5.2. La configuration de la base SQLite se trouve dans
`firstProject/settings.py`.

## Initialisation et lancement

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Créer les relations en base

1. Ouvrir `http://127.0.0.1:8000/admin/` et se connecter avec le
   superutilisateur.
2. Créer d'abord un médecin dans **AccountApp > Médecins**. Le médecin est
   automatiquement lié à un utilisateur par son `user_ptr`.
3. Créer un patient dans **AccountApp > Patients**.
4. Depuis l'application, le patient se connecte puis clique sur
   **Prendre rendez-vous**.
5. Le rendez-vous enregistré contient automatiquement les relations :
   `appointment.doctor_id` vers le médecin sélectionné et
   `appointment.patient_id` vers le patient connecté.

Il est donc inutile de saisir manuellement `patient_id` dans le formulaire :
cela évite de relier un rendez-vous au mauvais patient. Les relations sont
également protégées par une contrainte empêchant un médecin d'avoir deux
rendez-vous au même créneau.

Pages principales :

- `http://127.0.0.1:8000/` : accueil du cabinet
- `http://127.0.0.1:8000/admin/` : back-office
- `http://127.0.0.1:8000/api/specialties/` : spécialités
- `http://127.0.0.1:8000/api/doctors/` : médecins
- `http://127.0.0.1:8000/api/patients/` : patients
- `http://127.0.0.1:8000/api/appointments/` : rendez-vous
- `http://127.0.0.1:8000/accounts/login/` : connexion

Un patient connecté peut demander un rendez-vous depuis
`/api/prendre-rendez-vous/`. Les accès d’écriture de l’API nécessitent une
authentification ; les lectures restent publiques.

L'API expose les ressources `specialties`, `doctors`, `patients` et
`appointments`. Les médecins et patients héritent du modèle utilisateur
personnalisé `AccountApp.User`.