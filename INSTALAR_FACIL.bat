@echo off
chcp 65001 >nul
title Monitor de Links - Instalação Fácil

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    MONITOR DE LINKS                          ║
echo ║                  INSTALAÇÃO AUTOMÁTICA                       ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🤖 Bot: @paginadecaptura_bot
echo 📱 CHAT_ID: 954773903
echo 🔑 TOKEN: Configurado ✅
echo.

echo ⏳ Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado!
    echo.
    echo 📥 SOLUÇÃO:
    echo 1. Baixa Python em: https://python.org/downloads/
    echo 2. Durante instalação, marca "Add Python to PATH"
    echo 3. Reinicia o computador
    echo 4. Executa este arquivo novamente
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado!
python --version
echo.

echo 📦 Instalando dependências necessárias...
echo ⏳ Isto pode demorar alguns minutos...
echo.

pip install requests beautifulsoup4 lxml

if %errorlevel% neq 0 (
    echo.
    echo ❌ Erro na instalação. Tentando método alternativo...
    python -m pip install requests beautifulsoup4 lxml
    
    if %errorlevel% neq 0 (
        echo ❌ Falha na instalação das dependências
        echo.
        echo 🔧 SOLUÇÕES:
        echo 1. Executa como Administrador
        echo 2. Verifica conexão à internet
        echo 3. Reinicia o computador e tenta novamente
        echo.
        pause
        exit /b 1
    )
)

echo.
echo ✅ Dependências instaladas com sucesso!
echo.

echo 🧪 Testando configuração do Telegram...
echo.

python teste_telegram.py

if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Teste do Telegram falhou, mas podes continuar
    echo 💡 Verifica se recebeste mensagem no Telegram
    echo.
)

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                     INSTALAÇÃO CONCLUÍDA!                   ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🎉 SISTEMA PRONTO PARA USAR!
echo.
echo 📋 PRÓXIMOS PASSOS:
echo.
echo 1️⃣  TESTAR AGORA:
echo    python link_monitor_expandido.py
echo.
echo 2️⃣  CONFIGURAR AGENDAMENTO:
echo    - Abre Agendador de Tarefas (taskschd.msc)
echo    - Cria 3 tarefas para 8h, 14h e 20h
echo    - Programa: python
echo    - Argumentos: link_monitor_expandido.py
echo    - Pasta: %CD%
echo.
echo 3️⃣  MONITORAR:
echo    - Verifica Telegram para novos links
echo    - Vê logs em link_monitor.log
echo.
echo 📖 GUIA COMPLETO: GUIA_WINDOWS_LEIGOS.md
echo.
echo 🔧 COMANDOS ÚTEIS:
echo    Testar Telegram:     python teste_telegram.py
echo    Executar sistema:    python link_monitor_expandido.py
echo    Ver esta pasta:      explorer .
echo.

echo ✅ TUDO PRONTO! Pressiona qualquer tecla para continuar...
pause >nul

echo.
echo 🚀 Queres testar agora? (S/N)
set /p resposta="Digite S para Sim ou N para Não: "

if /i "%resposta%"=="S" (
    echo.
    echo 🧪 Executando teste...
    echo ⏳ Verifica o teu Telegram para ver os resultados!
    echo.
    python link_monitor_expandido.py
    echo.
    echo ✅ Teste concluído!
    echo 📱 Verifica o Telegram para ver os links encontrados!
)

echo.
echo 🎯 Sistema configurado e pronto!
echo 📖 Lê o GUIA_WINDOWS_LEIGOS.md para mais detalhes
echo.
pause

