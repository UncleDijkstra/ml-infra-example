# ml-infra-example
Это пример игрушечной задачи классификации URL адресов. Он содержит в себе простые, но полезные практики для построения ML-систем.

Тут есть:
* Веб-сервис для самой модели в докер образе
* Prometheus и grafana для мониторинга показателей
* Модульные и интеграционные тесты
* Автоматизированная проверка CodeStyle

Установить:
* docker
* docker-compose

Запуск:
docker-compose build
docker-compose up -d
python3 -m pytest test/integration/test_service_build.py --image ml-infra-example_urlclassifier:latest --scope class 
