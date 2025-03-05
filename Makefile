IMAGE_NAME = tg_syncer
CONTAINER_NAME = tg_syncer
DATA_DIR = ./data
ENV_FILE = .env

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -it \
		--detach-keys="ctrl-x" \
		--network host \
		-v $(DATA_DIR):/data \
		--env-file $(ENV_FILE) \
		--name $(CONTAINER_NAME) \
		$(IMAGE_NAME)


clean:
	docker rm -f $(CONTAINER_NAME) 2>/dev/null || true
	docker rmi -f $(IMAGE_NAME) 2>/dev/null || true

up: build run

help:
	@echo "Использование:"
	@echo "  make build   - Собрать Docker-образ"
	@echo "  make run     - Запустить контейнер"
	@echo "  make up      - Собрать образ и запустить контейнер"
	@echo "  make clean   - Очистить контейнеры и образы"
	@echo "  make help    - Показать это сообщение"
