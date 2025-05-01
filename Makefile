# Subir o banco PostgreSQL com Docker
up:
	docker-compose up -d

# Parar os containers
down:
	docker-compose down

# Ver logs do banco
logs:
	docker-compose logs -f postgres

# Executar o script principal
run:
	python main.py

# Instalar dependências
install:
	pip install -r requirements.txt

# Carregar variáveis de ambiente e rodar
start:
	GITHUB_TOKEN=$$(cat .env | grep GITHUB_TOKEN | cut -d '=' -f2) python main.py
