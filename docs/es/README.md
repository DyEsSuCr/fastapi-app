# start_app.sh - Script de Despliegue

Script para desplegar la aplicación en diferentes entornos usando Docker Compose con verificaciones de salud adecuadas y gestión de dependencias.

## Requisitos Previos

- Docker y Docker Compose instalados (verificado automáticamente por el script)
- Archivos de configuración de entorno (`.env.dev`, `.env.prod`, `.env.staging`)
- El script debe tener permisos de ejecución
- Contenedores Docker con verificaciones de salud configuradas:
  - `fastapi-app-db` (contenedor de base de datos)
  - `fastapi-app-redis` (contenedor Redis)
  - `fastapi-app-web` (contenedor de aplicación web)

## Uso

```bash
./start_app.sh -e [entorno] [-v]
```

### Parámetros

- **-e entorno**: Entorno de despliegue (obligatorio)
  - `dev` - Entorno de desarrollo
  - `prod` - Entorno de producción  
  - `staging` - Entorno de pruebas
- **-v**: Bandera opcional para remover volúmenes durante el apagado

### Ejemplos

```bash
# Desplegar en desarrollo (preservando volúmenes)
./start_app.sh -e dev

# Desplegar en producción con limpieza completa de volúmenes
./start_app.sh -e prod -v

# Desplegar en staging
./start_app.sh -e staging
```

## ¿Qué hace el script?

1. **Verificación de Requisitos**: Verifica automáticamente que Docker y Docker Compose estén instalados
2. **Análisis de Parámetros**: Usa análisis getopt adecuado para argumentos de línea de comandos
3. **Validación de Entorno**: Verifica que el entorno sea válido y que exista el archivo `.env` correspondiente
4. **Gestión de Contenedores**: Detiene contenedores existentes (con o sin eliminación de volúmenes)
5. **Inicio de Servicios**: Inicia todos los servicios usando Docker Compose
6. **Verificaciones de Salud**: Espera a que los servicios de base de datos y Redis estén saludables antes de continuar
7. **Migraciones de Base de Datos**: Ejecuta migraciones de Alembic una vez que todas las dependencias están listas
8. **Finalización**: Proporciona mensajes de estado claros con emojis para mejor visibilidad

## Archivos de Entorno Requeridos

El script busca automáticamente estos archivos según el entorno:

- `.env.dev` - Para entorno de desarrollo
- `.env.prod` - Para entorno de producción
- `.env.staging` - Para entorno de staging

## Dependencias de Contenedores

El script espera estos contenedores con verificaciones de salud:

- **fastapi-app-db**: Contenedor de base de datos (debe tener verificación de salud configurada)
- **fastapi-app-redis**: Contenedor Redis (debe tener verificación de salud configurada)  
- **fastapi-app-web**: Contenedor de aplicación web (para ejecutar migraciones)

## Configuración Inicial

1. Dar permisos de ejecución al script:
```bash
chmod +x start_app.sh
```

2. Asegurarse de que existan los archivos de entorno necesarios en el directorio raíz del proyecto.

3. Asegurar que tu `docker-compose.yml` incluya verificaciones de salud para los servicios de base de datos y Redis.

## Configuración de Verificaciones de Salud

Tu `docker-compose.yml` debe incluir verificaciones de salud como:

```yaml
services:
  db:
    container_name: fastapi-app-db
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U tu_usuario"]
      interval: 10s
      timeout: 5s
      retries: 5
      
  redis:
    container_name: fastapi-app-redis
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
```

## Características del Script

- **Manejo Robusto de Errores**: Falla rápidamente con mensajes de error claros
- **Retroalimentación Visual**: Usa emojis y mensajes de estado claros
- **Espera Inteligente**: Espera verificaciones de salud reales en lugar de tiempos de espera arbitrarios
- **Gestión de Dependencias**: Asegura que la base de datos y Redis estén listos antes de las migraciones
- **Opciones Flexibles**: Soporta limpieza de volúmenes y múltiples entornos

## Solución de Problemas

- **❌ Docker is not installed**: Instalar Docker y Docker Compose
- **❌ File .env.X not found**: Crear el archivo de entorno correspondiente
- **❌ Invalid environment**: Usar solo `dev`, `prod` o `staging`
- **❌ Failed to run Alembic migrations**: 
  - Verificar que el contenedor `fastapi-app-web` esté ejecutándose
  - Verificar la configuración de Alembic
  - Asegurar que la conexión a la base de datos esté configurada correctamente
- **Tiempos de espera en verificaciones de salud**: 
  - Verificar la configuración de verificaciones de salud en docker-compose.yml
  - Revisar los logs de contenedores para problemas de inicio
  - Asegurar que los servicios de base de datos/Redis estén configurados correctamente