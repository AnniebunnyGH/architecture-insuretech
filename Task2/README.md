# Задание 2. Динамическое горизонтальное масштабирование контейнеров (HPA)

## 1. Проблематика и цели решения

В ходе аудита инфраструктуры InsureTech выявлена проблема: в периоды пиковой нагрузки микросервисы компании в кластере Kubernetes сталкиваются с резким дефицитом оперативной памяти. Из-за превышения жестких лимитов контейнеры аварийно завершались по причине Out-Of-Memory (`OOMKilled`), вызывая деградацию доступности системы, перезагрузку подов (`CrashLoopBackOff`) и падение показателей удовлетворенности пользователей (NPS).

Постоянное содержание избыточного количества статически запущенных реплик для всех сервисов экономически нецелесообразно и приводит к перерасходу облачного бюджета.

**Цель решения**: Внедрить механизм горизонтального автоматического масштабирования подов (**Horizontal Pod Autoscaler, HPA**) на основе утилизации оперативной памяти (Memory Utilization) с порогом **80%**. Это позволяет динамически выделять вычислительные ресурсы строго при возрастании нагрузки и освобождать их при спаде трафика.

---

## 2. Архитектура и конфигурация

### 2.1. Сбор метрик (Metrics Server)
Для работы HPA требуется поставщик метрик ресурсов кластера. В Minikube задействован встроенный аддон `metrics-server`, транслирующий метрики потребления памяти и процессора от kubelet каждого узла в `metrics.k8s.io` API.

### 2.2. Манифест деплоймента ([deployment.yaml](deployment.yaml))
- **Имя**: `scaletestapp`
- **Образ**: `ghcr.io/yandex-practicum/scaletestapp:latest`
- **Начальное число реплик**: `1`
- **Конфигурация ресурсов**:
  ```yaml
  resources:
    requests:
      memory: "10Mi"
      cpu: "50m"
    limits:
      memory: "30Mi"
  ```
- **Обоснование подбора лимитов и запросов**:
  HPA высчитывает процент утилизации по формуле:
  $$\text{Utilization} = \frac{\text{Current Memory Usage}}{\text{requests.memory}} \times 100\%$$
  При значении `requests.memory: 10Mi` целевой порог в 80% соответствует **8 MiB**. Приложение `scaletestapp` под нагрузкой аллоцирует порядка 9–11 MiB памяти. Это значение гарантированно превышает порог утилизации (составляя 90–99% от request), что вызывает масштабирование, но остается значительно ниже лимита `limits.memory: 30Mi`, предотвращая перезапуск подов по OOM.

### 2.3. Манифест сетевого сервиса ([service.yaml](service.yaml))
- **Тип**: `NodePort` (порт `8080`, `nodePort: 30080`)
- **Селектор**: `app: scaletestapp`
- Обеспечивает равномерное распределение входящих запросов между всеми актуальными подами деплоймента.

### 2.4. Манифест автомасштабирования ([hpa.yaml](hpa.yaml))
- **Версия API**: `autoscaling/v2`
- **Диапазон масштабирования**: `minReplicas: 1`, `maxReplicas: 10`
- **Метрика**: память контейнеров со средней утилизацией `averageUtilization: 80%`.

### 2.5. Сценарий нагрузочного тестирования ([locustfile.py](locustfile.py))
- Использует фреймворк **Locust**
- Симулирует пользователей с паузой между запросами `between(1, 5)` секунд
- Выполняет HTTP GET-запросы на эндпоинт `/` сервиса.

---

## 3. Инструкция по воспроизведению

### Шаг 1. Запуск кластера и включение Metrics Server
```bash
minikube start --driver=docker
minikube addons enable metrics-server
```
Проверка доступности метрик:
```bash
kubectl top nodes
```

### Шаг 2. Развертывание приложения и HPA
```bash
kubectl apply -f Task2/deployment.yaml
kubectl apply -f Task2/service.yaml
kubectl apply -f Task2/hpa.yaml
```

### Шаг 3. Запуск нагрузочного теста (Locust)
Определение адреса сервиса:
```bash
# Для сред с Minikube tunnel или прямым IP:
minikube service scaletestapp --url
```

Запуск Locust в headless-режиме (или через веб-интерфейс на `http://localhost:8089`):
```bash
locust -f Task2/locustfile.py --host http://127.0.0.1:56498 --users 60 --spawn-rate 10 --autostart --run-time 5m
```

### Шаг 4. Мониторинг автомасштабирования
```bash
# Отслеживание метрик HPA в реальном времени:
kubectl get hpa scaletestapp-hpa -w

# Просмотр создаваемых подов:
kubectl get pods -l app=scaletestapp -o wide

# Просмотр потребления ресурсов подами:
kubectl top pods -l app=scaletestapp
```

---

## 4. Результаты нагрузочного тестирования и масштабирования

В ходе подачи нагрузки утилизация памяти одиночного пода возросла до **96–99%** от `request` (~10 MiB), что существенно превысило порог в 80%.

Контроллер HPA зафиксировал превышение порога и последовательно увеличил число реплик:
- **1 -> 2 реплики**: `SuccessfulRescale (New size: 2)`
- **2 -> 3 реплики**: `SuccessfulRescale (New size: 3)`
- **3 -> 4 реплики**: `SuccessfulRescale (New size: 4)`

### Фрагмент событий HPA (`kubectl describe hpa scaletestapp-hpa`):
```text
Events:
  Type     Reason             Age    From                       Message
  ----     ------             ----   ----                       -------
  Normal   SuccessfulRescale  2m24s  horizontal-pod-autoscaler  New size: 2; reason: memory resource utilization (percentage of request) above target
  Normal   SuccessfulRescale  84s    horizontal-pod-autoscaler  New size: 3; reason: memory resource utilization (percentage of request) above target
  Normal   SuccessfulRescale  24s    horizontal-pod-autoscaler  New size: 4; reason: memory resource utilization (percentage of request) above target
```

### Состояние подов после масштабирования:
```text
NAME                          READY   STATUS    RESTARTS   AGE     IP               NODE       NOMINATED NODE   READINESS GATES
scaletestapp-f7864785-s27xz   1/1     Running   0          4m41s   10.244.120.98    minikube   <none>           <none>
scaletestapp-f7864785-c8646   1/1     Running   0          2m26s   10.244.120.99    minikube   <none>           <none>
scaletestapp-f7864785-ljc4r   1/1     Running   0          86s     10.244.120.100   minikube   <none>           <none>
scaletestapp-f7864785-fkhg9   1/1     Running   0          26s     10.244.120.101   minikube   <none>           <none>
```

Полный лог верификации сохранен в файле [hpa_scaling.log](hpa_scaling.log).

---

## 5. Выводы

1. Внедрение **HorizontalPodAutoscaler** устранило угрозу сбоев из-за нехватки памяти: при превышении нагрузки система автоматически вводит в строй дополнительные реплики.
2. Входящий трафик эффективно распределяется между новыми подами через `Service`, снижая удельную нагрузку на каждый контейнер.
3. Система защищена от падений по OOM (`OOMKilled`), обеспечивая непрерывную доступность сервиса для клиентов InsureTech и сохранение высокого уровня NPS.
