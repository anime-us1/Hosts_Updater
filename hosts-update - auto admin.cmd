@echo off
FSUTIL DIRTY query %SystemDrive% >NUL || (
    PowerShell "Start-Process -FilePath '%0' -Verb RunAs"
    EXIT
)
echo Creating combined hosts file...
del "%~dp0local_file.txt" 2>nul
del "%~dp0temp_hostnames.txt" 2>nul
del "%~dp0temp_hosts_file_combined.txt" 2>nul
del "%~dp0final_temp.txt" 2>nul
del "%~dp0main_combined_hosts.txt" 2>nul
del "%~dp0HOSTS" 2>nul

del "%~dp0adguard-extractor\local_file.txt" 2>nul
del "%~dp0adguard-extractor\temp_hostnames.txt" 2>nul
del "%~dp0adguard-extractor\temp_hosts_file_combined.txt" 2>nul

cd %~dp0
start /b /wait python normal.py
cd "%~dp0adguard-extractor"
start /b /wait python adguard.py
cd %~dp0
start /b /wait python combine.py

del "%~dp0local_file.txt" 2>nul
del "%~dp0temp_hostnames.txt" 2>nul
del "%~dp0temp_hosts_file_combined.txt" 2>nul
del "%~dp0final_temp.txt" 2>nul
del "%~dp0main_combined_hosts.txt" 2>nul

del "%~dp0adguard-extractor\local_file.txt" 2>nul
del "%~dp0adguard-extractor\temp_hostnames.txt" 2>nul
del "%~dp0adguard-extractor\temp_hosts_file_combined.txt" 2>nul

Xcopy "%~dp0HOSTS" c:\Windows\System32\Drivers\etc\hosts /E /H /C /I /Y

rem regedit /s "%~dp0dnscache_disable.reg"

ipconfig /flushdns

exit /b