## FinBot on Python3 (telegram)
### Запуск
```bash
python3 -m venv venv
source ./venv/bin/activate
pip install -r deps.txt
echo TOKEN="<TOKEN>" > .env
echo DATABASE="sqlite:///db.sqlite3" >> .env # support msql/psql
make run
```

### Деплой (Linux)
```bash
sudo git clone https://github.com/rombintu/pyfinbot.git /opt/pyfinbot
sudo chown $USER:$USER -R /opt/pyfinbot
cd /opt/pyfinbot
python3 -m venv venv
source ./venv/bin/activate
pip install -r deps.txt
echo TOKEN="<TOKEN>" > .env
echo DATABASE="sqlite:///db.sqlite3" >> .env # support msql/psql
sudo cp ./system/finbot.service /etc/systemd/system/finbot.service
sudo systemctl daemon-reload
sudo systemctl enable --now finbot.service
```

### Использование
В запросе должны присутсвовать:
- Стоимость (C) - число
- Слитно "$" для перевода в рубли из долларов
- Слитно "к" для умножения на 1000 (опционально)
- Категория (К) - одно слово
- Комментарий в конце запроса (опционально)
Общий пример: **Стоимость[к] Категория [с комментарием]**

Примеры валидных запросов: 
* 200 обед -> С: 200р, К: Обед, Комм: None
* 10к одежда на лето -> С: 10,000р, К: Одежда, Комм: На лето
* 150$ инвестиции -> С: 150*(текущий курс), К: Инвестиции, Ком: None
* 1к$ Отпуск турция-> С: 1000*(текущий курс), К: Отпуск, Ком: Турция
