# Proyecto Find My Pet

## Descripción
Aplicación web interactiva para el registro y visualización de avistamientos de mascotas con geolocalización. Utiliza **FastAPI** para el backend, **Google Maps API** para la visualización en mapas, y **SQLAlchemy** para la gestión de la base de datos. El proyecto permite a los usuarios agregar, buscar y visualizar avistamientos en un mapa interactivo, con un enfoque en la usabilidad y el rendimiento.

Este proyecto fue realizado como parte del ciclo superior de Desarrollo de Aplicaciones Web y tiene como objetivo demostrar el uso de herramientas modernas en el desarrollo de aplicaciones web interactivas.

## Tecnologías utilizadas
- **FastAPI**: Framework para el desarrollo del backend.
- **SQLAlchemy**: ORM para la gestión de la base de datos.
- **Google Maps API**: Para la visualización de avistamientos en el mapa.
- **Python**: Lenguaje de programación utilizado.
- **HTML/CSS/JavaScript**: Tecnologías utilizadas en el frontend.

## Características
- **Registro de avistamientos**: Los usuarios pueden registrar avistamientos con detalles como la ubicación, fecha y descripción.
- **Visualización en mapa interactivo**: Los avistamientos se muestran en un mapa de Google Maps.
- **Búsqueda de avistamientos**: Los usuarios pueden buscar avistamientos por ubicación o fecha.

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/JoseConca/proyecto-final-DAW.git

2. Instala las dependencias:
    ```bash
    pip install -r requirements.txt

3. Ejecuta la aplicación:
    ```bash
    uvicorn main:app --reload

La aplicación estará disponible en http://127.0.0.1:8000.