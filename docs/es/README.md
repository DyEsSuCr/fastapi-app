# start_app.sh - Deployment Script

Script para desplegar la aplicación en diferentes entornos usando Docker Compose.

## Requisitos Previos

- Docker y Docker Compose instalados
- Archivos de configuración de entorno (`.env.dev`, `.env.prod`, `.env.staging`)
- El script debe tener permisos de ejecución

## Uso

```bash
./start_app.sh [environment] [-v]
```

### Parámetros

- **environment**: Entorno de despliegue (obligatorio)
  - `dev` - Entorno de desarrollo
  - `prod` - Entorno de producción  
  - `staging` - Entorno de pruebas
- **-v**: Bandera opcional para remover volúmenes (opcional)

### Ejemplos

```bash
# Desplegar en desarrollo (preservando volúmenes)
./start_app.sh dev

# Desplegar en producción con limpieza completa de volúmenes
./start_app.sh prod -v

# Desplegar en staging
./start_app.sh staging
```

## ¿Qué hace el script?

1. **Validación**: Verifica que el entorno sea válido y que exista el archivo `.env` correspondiente
2. **Detener contenedores**: Ejecuta `docker compose down` (con o sin `-v` según se especifique)
3. **Iniciar contenedores**: Ejecuta `docker compose up -d` con el archivo de entorno correspondiente
4. **Espera**: Pausa 2 segundos para que los servicios estén listos
5. **Migraciones**: Ejecuta las migraciones de base de datos con Alembic

## Archivos de Entorno Requeridos

El script busca automáticamente estos archivos según el entorno:

- `.env.dev` - Para entorno de desarrollo
- `.env.prod` - Para entorno de producción
- `.env.staging` - Para entorno de staging

## Configuración Inicial

1. Dar permisos de ejecución al script:
```bash
chmod +x start_app.sh
```

2. Asegurarse de que existan los archivos de entorno necesarios en el directorio raíz del proyecto.

## Contenedor de Aplicación

El script asume que existe un contenedor llamado `fastapi-app-web` donde ejecuta las migraciones de Alembic. Si tu contenedor tiene un nombre diferente, modifica la última línea del script.

## Troubleshooting

- **Error "File .env.X not found"**: Crear el archivo de entorno correspondiente
- **Error "Invalid environment"**: Usar solo `dev`, `prod` o `staging`
- **Error en migraciones**: Verificar que el contenedor `fastapi-app-web` esté corriendo y que Alembic esté configurado correctamente