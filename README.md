Aplikacja webowa z kompletnym środowiskiem Flask + Nginx + PostgreSQL działająca całkowicie w Dockerze.
1. Korzysta z wielostopniowego Dockerfile
2. Używa Docker Compose do uruchamiania wszystkich elementów
3. Wykorzystuje 2 sieci Dockerowe - front_net dla połączenia z nginx oraz back_net do połączenia z postgres
4. Korzysta z 3 wolumentów: db_data, nginx_log oraz seed_output
5. Implementuje etap migracji i seedowania bazy
6. Zawiera GitHub action dla budowania, testowania i pushowaniu obrazu do GHCR
7. Zawiera GitHub action do deployu (obecna implementacja zakłada logowanie po SSH do środowiska produkcyjnego, pobieranie najnowszego obrazu i restart) - nie używane ze względu na brak dedykowanego serwera
8. Zawiera podstawową konfigurację dla Azure IaC - resource group oraz Azure Container Registry (nie używane ze względu na brak subskrypcji Azure, konfiguracja sprawdzona jedynie na etapie kompilacji)


Opis aplikacji webowej:
Aplikacja napisana w Pythonie z użyciem frameworka Flask. Udostępnia następujące endpointy:
- GET /health
  - Opis: Sprawdzenie stanu aplikacji.
  - Przykład odpowiedzi: {"status": "ok"}

- GET /users
  - Opis: Zwraca listę wszystkich użytkowników.
  - Przykład odpowiedzi: [ {"id": 1, "name": "Alicja"}, ... ]

- POST /add_user/<name>
  - Opis: Tworzy użytkownika o podanej nazwie.
  - Parametr ścieżki: name (string)
  - Przykład odpowiedzi: {"id": 5, "name": "Marek"}

- GET /users/<int:user_id>/tasks
  - Opis: Zwraca listę zadań przypisanych do danego użytkownika.
  - Zachowanie: Zwraca 404 gdy użytkownik nie istnieje.
  - Przykład odpowiedzi: [ {"id": 1, "title": "Task 1 for Marek"}, ... ]

- POST /add_task/<int:user_id>
  - Opis: Dodaje zadanie dla istniejącego użytkownika.
  - Parametr ścieżki: user_id (integer)
  - Body (JSON): { "title": "Nazwa zadania" }
  - Błędy: Zwraca 400 gdy `title` nie jest przekazany.
  - Przykład odpowiedzi: {"id": 2, "title": "New Task"}