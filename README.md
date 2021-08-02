В данном проекте реализован фрагмент приложения который собирает данные с 
Moex биржы и анализирует эти данные, а так же визуализируют графически, математически

Запуск приложения:
  1) создайте файл secert_settings.py где конфиги укажите конфиги django secret key, бд после чего импортируете их в settings.py
  2) соберите данные с Moex, с помощью  команды python3 manage.py get_history_price начальная_дата конечная_дата
  3) запустите команду python3 manage.py runserver
  4) перейдите по url в /home для просмотра анализа

Скриншоты сайта:
  ![alt text](https://github.com/Stef16123/moex/blob/master/image.png?raw=true)
  ![alt text](https://github.com/Stef16123/moex/blob/master/home_page_1.png?raw=true)
  ![alt text](https://github.com/Stef16123/moex/blob/master/home_page_2.png?raw=true)
