
# surainvestments-api-wrapper

Este paquete proporciona un wrapper en Python para interactuar con la API de inversiones de Sura Uruguay.

## Instalación

Puedes instalar el paquete utilizando `pip`:

```bash
pip install surainvestments-api-wrapper
```

## Uso

### Autenticación y obtención de información

Primero, debes inicializar la clase `BaseAPI` y pasar tus credenciales de inicio de sesión. El wrapper gestionará la autenticación y proporcionará métodos para interactuar con la API.

```python
from surainvestments_api_wrapper import BaseAPI

# Inicializa la API con la sesión autenticada
api = BaseAPI(document="XXXXXX", country=XX, document_type=X, password="XXXXXXX")

# Obtén información de un gadget específico
gadget_info = api.get_total_account()
print(gadget_info)
```

El método `login()` se llama automáticamente al inicializar la clase, por lo que no necesitas realizar pasos adicionales para autenticarte.

### Métodos disponibles

- **`get_gadget_info()`**: Devuelve la información de gadgets disponible en la API. 

- **`get_nominal_balance_by_last_year(account_number, first_date, last_date, tab_id)`**: Obtiene el balance nominal del último año para una cuenta específica. Requiere el número de cuenta (`account_number`), las fechas de inicio y fin (`first_date` y `last_date`), y el identificador de la pestaña (`tab_id`).

- **`get_statements(start_date, end_date)`**: Recupera los estados de cuenta entre las fechas especificadas (`start_date` y `end_date`).

- **`get_investment_position(first_date, account_number=None, last_date=None, tab_id="4911612639")`**: Devuelve la posición de inversión en función de una fecha de inicio (`first_date`). Opcionalmente, se puede proporcionar un número de cuenta (`account_number`), una fecha de fin (`last_date`) y un identificador de pestaña (`tab_id`).

- **`get_total_account()`**: Calcula y devuelve el balance total de la cuenta sumando los balances de todos los instrumentos disponibles. Utiliza el método `get_gadget_info()` y maneja cualquier error durante el proceso.


## Requisitos

- Python 3.x
- `requests`

## Contribuir

Si encuentras algún error o tienes sugerencias para mejorar el paquete, por favor crea un issue en el [repositorio del proyecto](https://github.com/yourusername/surainvestments-api-wrapper).

## Licencia

Este proyecto está licenciado bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.
