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
git clone https://github.com/rombintu/pyfinbot.git /opt/pyfinbot
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

    Стоимость - 1 или 2 место
    Категория - 1 или 2 место
    Комментарий - в конце опционально

