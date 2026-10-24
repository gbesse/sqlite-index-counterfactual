# sqlite-index-counterfactual

## Français

Comparer des index sur une vraie requête et ses étapes de VM.

Données fictives ; aucun accès réseau ni secret requis.

```sh
python -m sqlite_index_counterfactual examples/demo.json --lang fr
python -m unittest discover -s tests -v
```

### Méthode et différence

Crée des bases SQLite distinctes, ajoute chaque index candidat puis observe EXPLAIN QUERY PLAN, callbacks VM et résultats sur les mêmes données. Les autorisations SQL refusent écritures et fonctions hors de la liste documentée.

### Limites

Mesure les callbacks du moteur installé, pas le temps ni une accélération universelle. Égalité des lignes observées seulement, pas équivalence de requêtes ; données et budget bornés, une table, fonctions scalaires/agrégats limités.

### Validation

Tests de domaine, cas limites et interface FR/EN/ES. La CI teste Python 3.11/3.13 et exécute la wheel installée hors du checkout. JSON conserve les identifiants techniques et les données fournis. Erreur d’entrée : code de sortie 2.

## English

Compare indexes on an actual query and its VM steps.

Synthetic data; no network access or secret required.

```sh
python -m sqlite_index_counterfactual examples/demo.json --lang en
python -m unittest discover -s tests -v
```

### Method and difference

Creates separate SQLite databases, adds candidate indexes and observes EXPLAIN QUERY PLAN, VM callbacks and results on identical data. SQL authorization denies writes and functions outside the documented allowlist.

### Limits

Measures callbacks of the installed engine, not time or universal speedup. Observed row equality only, not query equivalence; bounded data/budget, one table and limited scalar/aggregate functions.

### Validation

Domain tests, boundary cases and FR/EN/ES interface. CI tests Python 3.11/3.13 and runs the installed wheel outside the checkout. JSON preserves technical identifiers and supplied data. Invalid input exits with code 2.

## Español

Comparar índices en una consulta real y sus pasos de VM.

Datos sintéticos; no requiere red ni secretos.

```sh
python -m sqlite_index_counterfactual examples/demo.json --lang es
python -m unittest discover -s tests -v
```

### Método y diferencia

Crea bases SQLite separadas, añade índices candidatos y observa EXPLAIN QUERY PLAN, callbacks VM y resultados con datos idénticos. La autorización SQL rechaza escrituras y funciones fuera de la lista documentada.

### Límites

Mide callbacks del motor instalado, no tiempo ni aceleración universal. Solo igualdad observada de filas, no equivalencia; datos/presupuesto acotados, una tabla y funciones limitadas.

### Validación

Pruebas de dominio, casos límite e interfaz FR/EN/ES. CI prueba Python 3.11/3.13 y ejecuta la wheel instalada fuera del repositorio. JSON conserva identificadores técnicos y datos proporcionados. Entrada inválida termina con código 2.

## Sources / Fuentes

- https://www.sqlite.org/queryplanner.html
- https://docs.python.org/3/library/sqlite3.html
