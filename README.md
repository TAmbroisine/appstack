# Application 3-Tiers - React, Flask, PostgreSQL, Kubernetes

Projet de démonstration d'une application web full-stack de gestion de taches, concue pour illustrer une demarche complete: developpement, conteneurisation, orchestration Kubernetes et diagnostic d'incident en production.

Ce repository est principalement destine a un usage portfolio/recrutement pour montrer des competences concretes en architecture applicative et en DevOps.

## Objectif du projet

Concevoir et déployer une application simple mais réaliste selon une architecture 3-tiers:

1. Frontend: interface utilisateur en React/Vite
2. Backend: API REST en Flask
3. Data layer: base PostgreSQL persistante

Le projet met l'accent sur la séparation des responsabilités, la configuration par environnement et la robustesse du deploiement.

## Ce que ce projet démontre

- Conception d'une architecture 3-tiers maintenable
- Développement d'une API REST (GET/POST/DELETE)
- Intégration frontend/backend avec gestion de la configuration runtime
- Conteneurisation Docker de chaque composant
- Déploiement Kubernetes (Deployment, StatefulSet, Service, Ingress)
- Bonnes pratiques d'exploitation: probes, ressources, rolling update
- Diagnostic et correction d'un incident réseau/CORS en environnement cluster

## Stack technique

- Frontend: React, Vite, Axios
- Backend: Python, Flask, SQLAlchemy, Flask-CORS
- Base de données: PostgreSQL 16
- Conteneurisation: Docker, Docker Compose
- Orchestration: Kubernetes (manifests YAML)

## Architecture

```text
Client navigateur
	|
	v
Ingress (/ -> frontend, /api -> backend)
	|                         |
	v                         v
Frontend (React)        Backend (Flask)
										|
										v
								PostgreSQL (StatefulSet)
```

## Structure du repository

- `todo-front/`: application frontend React/Vite
- `backend/`: API Flask et acces base de données
- `k8s/`: manifests Kubernetes (frontend, backend, database, ingress, namespace)
- `docker-compose.yml`: orchestration locale rapide des services

## Fonctionnalites implementees

- Consultation de la liste des taches
- Ajout d'une nouvelle tache
- Suppression d'une tache
- Persistance en base PostgreSQL

## Execution locale avec Docker Compose

Prerequis:

- Docker
- Docker Compose

Lancer les services:

```bash
docker compose up -d
```

Acces:

- Frontend: http://localhost:3000
- Backend API: http://localhost:5000/api/tasks

Arreter:

```bash
docker compose down
```

## Deploiement Kubernetes

Les manifests sont organises dans `k8s/`:

- `k8s/namespace.yaml`
- `k8s/database/`
- `k8s/backend/`
- `k8s/frontend/`
- `k8s/ingress.yaml`

Séquence type:

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/database
kubectl apply -f k8s/backend
kubectl apply -f k8s/frontend
kubectl apply -f k8s/ingress.yaml
```

Vérification:

```bash
kubectl get pods -n todo
kubectl get svc -n todo
kubectl get ingress -n todo
```

## Point technique notable: incident CORS

Un blocage CORS apparent est survenu en cluster. La cause était un appel frontend vers un DNS interne Kubernetes (`backend-service`) non resolvable depuis le navigateur.

Correction appliquee:

- Passage a un routage same-origin via Ingress
- Consommation API via `/api/...` depuis le frontend
- Alignement des routes Ingress (`/api` vers backend)

## Competences mobilisees

- Architecture applicative 3-tiers
- API REST et integration full-stack
- Docker et cycle de build/déploiement
- Kubernetes: Deployments, StatefulSet, Services, Ingress
- Troubleshooting reseau applicatif et fiabilisation production

## Ameliorations envisagees

- Ajout d'authentification (JWT/OAuth)
- Pipeline CI/CD (tests + build + deploy)
- Monitoring/observabilite (Prometheus/Grafana)
- Gestion HTTPS et certificats
- Tests automatisés frontend/backend plus complets

## Auteur

Projet réalisé par Tyron dans une logique de portfolio technique.
