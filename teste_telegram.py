#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste rápido para verificar se o TOKEN e CHAT_ID do Telegram estão funcionando
"""

import requests
import json
from datetime import datetime

# Configurações do Telegram
TOKEN = "7585232781:AAGCEXAojfQbxc-tgCzifXbzD89AP4F7YIE"
CHAT_ID = "1289789994"

def testar_telegram():
    """Testa se o bot consegue enviar mensagem"""
    
    print("🤖 TESTE DO BOT DO TELEGRAM")
    print("=" * 40)
    print(f"📱 TOKEN: {TOKEN[:20]}...")
    print(f"💬 CHAT_ID: {CHAT_ID}")
    print()
    
    # URL da API do Telegram
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    # Mensagem de teste
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    mensagem = f"""🧪 TESTE DO MONITOR DE LINKS

✅ Configuração funcionando!
🕐 Teste realizado em: {timestamp}

📋 Configuração atual:
• TOKEN: Configurado ✅
• CHAT_ID: {CHAT_ID} ✅
• Total de links: 15 páginas

🚀 Próximos passos:
1. Execute o script principal
2. Configure o agendamento
3. Monitore os logs

Sistema pronto para uso! 🎉"""
    
    # Dados para envio
    dados = {
        "chat_id": CHAT_ID,
        "text": mensagem
    }
    
    try:
        print("📤 Enviando mensagem de teste...")
        
        # Fazer requisição
        resposta = requests.post(url, data=dados, timeout=10)
        
        if resposta.status_code == 200:
            resultado = resposta.json()
            if resultado.get("ok"):
                print("✅ SUCESSO! Mensagem enviada com sucesso!")
                print("📱 Verifique seu Telegram para ver a mensagem.")
                print()
                print("🎯 PRÓXIMOS PASSOS:")
                print("1. Execute: python link_monitor_expandido.py")
                print("2. Configure agendamento: ./setup_cron.sh")
                print("3. Monitore: ./status.sh")
                return True
            else:
                print("❌ ERRO na resposta da API:")
                print(f"   {resultado}")
                return False
        else:
            print(f"❌ ERRO HTTP {resposta.status_code}:")
            print(f"   {resposta.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ ERRO: Timeout na conexão")
        print("🔧 Verifique sua conexão com a internet")
        return False
        
    except requests.exceptions.RequestException as e:
        print(f"❌ ERRO de conexão: {e}")
        return False
        
    except Exception as e:
        print(f"❌ ERRO inesperado: {e}")
        return False

def verificar_bot_info():
    """Verifica informações do bot"""
    
    url = f"https://api.telegram.org/bot{TOKEN}/getMe"
    
    try:
        resposta = requests.get(url, timeout=10)
        
        if resposta.status_code == 200:
            resultado = resposta.json()
            if resultado.get("ok"):
                bot_info = resultado.get("result", {})
                print("🤖 INFORMAÇÕES DO BOT:")
                print(f"   Nome: {bot_info.get('first_name', 'N/A')}")
                print(f"   Username: @{bot_info.get('username', 'N/A')}")
                print(f"   ID: {bot_info.get('id', 'N/A')}")
                print()
                return True
        
        print("⚠️  Não foi possível obter informações do bot")
        return False
        
    except Exception as e:
        print(f"⚠️  Erro ao obter informações do bot: {e}")
        return False

def main():
    print()
    
    # Verificar informações do bot
    verificar_bot_info()
    
    # Testar envio de mensagem
    sucesso = testar_telegram()
    
    print()
    if sucesso:
        print("🎉 CONFIGURAÇÃO PERFEITA!")
        print("📋 O sistema está pronto para monitorar os links!")
    else:
        print("🔧 PROBLEMAS ENCONTRADOS:")
        print("1. Verifique se o TOKEN está correto")
        print("2. Verifique se o CHAT_ID está correto")
        print("3. Certifique-se de ter enviado uma mensagem para o bot primeiro")
        print("4. Verifique sua conexão com a internet")
    
    print()

if __name__ == "__main__":
    main()

