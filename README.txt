## run this on raspi zero w
1) ssh into pi (use Fing to find raspi ip addr)
- user: pi
- password: raspberry
2) install nodejs
https://warlord0blog.wordpress.com/2018/06/27/node-js-v8-on-raspberry-pi-zero/
https://nodejs.org/dist/v10.16.0/
3) install python3 modules
~/ $ sudo apt-get install libgeos++ 
- shapely requires geos
~/log_rain/ $ pip install -r requirements.txt
- python-telegram-bot==12.0.0b1 requires evdev
4) clone repos
- https://github.com/cheeaun/rain-geojson-sg
- https://github.com/GitMeGet/log_rain
5) run geojson node server
~/rain-geojson-sg/ $ npm i
~/rain-geojson-sg/ $ npm run dev
6) run logging service (spin up another terminal using tmux)
~/log_rain/ $ python log_rain.py
7) run telegram bot
~/log_rain/ $ python telegram_bot.py

## tmux guide (need to spin up 3 terminals to run)
https://www.hamvocke.com/blog/a-quick-and-easy-guide-to-tmux/
- split left, right: Ctrl + b, then %
- split top, btm: Ctrl + b, then "
- nav: Ctrl + b, then arrow key
- close: exit / Ctrl + d
- detach/attach
https://askubuntu.com/questions/8653/how-to-keep-processes-running-after-ending-ssh-session

## misc
- time series database
https://medium.com/schkn/4-best-time-series-databases-to-watch-in-2019-ef1e89a72377
- lightweight database
https://randomnerdtutorials.com/sqlite-database-on-a-raspberry-pi/
https://mariadb.org/

