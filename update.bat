@echo off
echo Processando dados...
python scripts/process_data.py
echo Gerando Dashboard...
python scripts/generate_html.py
echo Concluido!
pause
