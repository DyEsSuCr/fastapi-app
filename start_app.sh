docker compose --env-file .env.dev down -v

docker compose --env-file .env.dev up -d

echo "Esperando a que los servicios estén listos..."
sleep 2

alembic upgrade head

python main.py