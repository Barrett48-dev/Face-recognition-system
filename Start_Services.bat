@echo off

echo Starting Apache...
start cmd /k "cd /d C:\wamp64\bin\apache\apache2.4.65\bin && httpd.exe"

timeout /t 3

echo Starting MySQL...
start cmd /k "cd /d C:\wamp64\bin\mysql\mysql8.4.7\bin && mysqld.exe"

start http://127.0.0.1/phpmyadmin5.2.3/

echo Servers launched successfully.
pause