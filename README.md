# hockey_graphs

hockey_graphs is personal software project to create a yet another set of tools to render charts based on statistics from (P-)DEL

[Sneak Preview](https://hockeygraphs.dynamop.de/) of 2019/2020 season as well as Magenta Sport Hockey Cup.

## Project status

The project is under heavy development.  So far charts for single del-matches will be provided. Team-statistics, team benchmarking and player statistics are on my todo-list and will hopefully follow soon.

In case you are missing a certain chart you would like to see let me know. Just create an [issue](https://github.com/grindsa/hockey_graphs/issues/new) or drop me an email to <grindelsack@gmail.com>. Suggestions and objective criticism those refer to this project are welcome at any time. 

If you are interested in raw statistics please visit [leaffan.net](https://www.leaffan.net/del/#!/home).

## Disclaimer

I am not a professional software developer. Main aim was to do something useful while stuck in COVID prison. Keep this in mind while laughing about my code and don’t forget to send patches.

I am neither working for (P-)DEL or any related organisation nor for any of the German hockey clubs. I just found the raw data while checking [penny-del.org](https://www.penny-del.org/) and started playing with it.

# Architecture

the project is split into two parts:
- a [django](https://www.djangoproject.com/) based backend providing a [REST-API](https://hockeygraphs.dynamop.de/api/v1/) for data fetching
- a [ReactJS](https://reactjs.org/) based frontend

The charts are being generated by using [highcharts](https://www.highcharts.com/)
