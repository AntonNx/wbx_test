import requests
import time

# Открываем файл с номерами для чтения
with open('input.txt', 'r') as f:
    numbers = f.read().splitlines()

# Открываем файл для записи результатов
with open('results.txt', 'w') as f:
    for number in numbers:
        # Делаем запрос к API
        response = requests.get(f'http://nm-info-api.wbx-ru.svc.k8s.wbxcat/api/nminfo/v1?nm={number}')
        data = response.json()
        # Ищем нужное значение
        for item in data['Data']:
            if item['Source'] == 'promo':
                rv = item['Changes'][0]['Rv']
                # Записываем значение в файл
                f.write(f'{rv}\n')

        # Добавляем таймаут в 1 секунду перед следующей итерацией
        time.sleep(1)

