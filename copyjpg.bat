@echo off
setlocal

copy C:\Users\YourUserName\AppData\Local\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets\*.* *.jpg

for /f "usebackq delims=;" %%A in (`dir /b *.jpg`) do If %%~zA LSS 100000 del "%%A"

python findsize.py
