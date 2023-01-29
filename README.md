# eCommerce-Website-Project

Projekt sklepu internetowego związany z przedmiotem `Zaawansowane Programowanie Obiektowe` wykonany w `Django + Vue.js`.

## Konfiguracja

Pierwszą rzeczą, którą należy zrobić jest sklonowanie repozytorium:

```sh
git clone https://github.com/JakubKujawa/eCommerce-Website-Project.git
cd eCommerce-Website-Project
```

Utwórz środowisko wirtualne, w którym zainstalujesz zależności i aktywuj je:

```sh
virtualenv --no-site-packages env
source env/bin/activate
```

Następnie zainstaluj zależności:

```sh
(env) pip install -r requirements.txt
```
Zwróć uwagę na `(env)`. Wskazuje to, że ta sesja terminalowa działa w środowisku wirtualnym ustawionym przez `virtualenv`.

Gdy `pip` skończy pobierać zależności:
```sh
(env) cd project
(env) python manage.py runserver
```
I przejdź do `http://127.0.0.1:8000/`.
