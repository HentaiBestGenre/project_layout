# Документация проекта LLMAssistant

## Обзор

LLMAssistant - это многофункциональный ассистент на основе искусственного интеллекта, предназначенный для различных сфер применения, включая медицину, образование и фармацевтику. Проект использует различные модели языкового моделирования (LLM) для обработки запросов пользователей и предоставления соответствующих ответов.

## Основные компоненты

### 1. Конфигурация

Файл конфигурации (`app/core/config_example.py`) содержит основные настройки проекта, включая параметры подключения к различным сервисам и API-ключи.

### 2. Состояния

Проект использует систему управления состояниями для обработки различных сценариев взаимодействия. Основные состояния включают:

- CreateDocState (`app/services/state_management_service/states/med/create_doc.py`)
- MakeRecordState (`app/services/state_management_service/states/med/make_record.py`)
- FetalMonitorAnalisisState (`app/services/state_management_service/states/med/fetal_monitor.py`)
- AboutState (`app/services/state_management_service/states/med/about_state.py`)
- MakeAppointmentState (`app/services/state_management_service/states/med/make_appointment.py`)
- OrderPillsState и ExtractPillsState (`app/services/state_management_service/states/med/order_pills.py`)
- ImgAnalisisState (`app/services/state_management_service/states/med/img_analisis.py`)
- GetConsultationState (`app/services/state_management_service/states/med/get_consultation copy.py`)
- SetBillState и PayBillState (`app/services/state_management_service/states/med/pay_services.py`)
- SolveTaskSession (`app/services/state_management_service/states/school/solve_task.py`)
- Colloquium (`app/services/state_management_service/states/school/colloquium.py`)

### 3. Сервисы

- Vidal Service (`app/services/vidal_service.py`): Сервис для работы с медицинской информацией и поиска лекарств.
- Matrix Server (`app/services/matrix_server.py`): Сервис для работы с Matrix-сервером для обмена сообщениями.

### 4. Утилиты

Файл `app/utils.py` содержит различные вспомогательные функции, включая генерацию PDF-документов, QR-кодов и обработку изображений.

### 5. Маршруты

Пример маршрута для школьного ассистента находится в файле `app/routes/assistants/school.py`.

### 6. Модели данных

Модели данных определены в файле `app/models/med.py`, например, модель `DoctorConsultation`.

### 7. Скрипты

Проект включает несколько вспомогательных скриптов:
- `app/scripts/test_jinja.py`: Тестирование шаблонов Jinja2 для генерации PDF.
- `app/scripts/create_room.py`: Создание комнаты в Matrix-сервере.
- `app/scripts/print_test.py`: Тестирование отправки документов на печать.

## Основные функции

1. Медицинские консультации
2. Анализ медицинских изображений
3. Заказ лекарств
4. Запись на прием к врачу
5. Создание и оплата счетов за медицинские услуги
6. Помощь в решении учебных задач
7. Проведение коллоквиумов

## Технологии

- FastAPI
- Redis
- MongoDB
- Matrix Server
- Jinja2
- pdfkit
- qrcode

## Установка и запуск

(Здесь должны быть инструкции по установке зависимостей и запуску проекта)

## Примечание

Этот проект содержит конфиденциальную информацию, такую как API-ключи и пароли. Убедитесь, что файл `app/core/config.py` добавлен в `.gitignore` и не публикуется в открытом доступе.

Для более подробной информации о каждом компоненте, пожалуйста, обратитесь к соответствующим файлам исходного кода.