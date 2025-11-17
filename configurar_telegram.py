#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para configurar TOKEN e CHAT_ID do Telegram no monitor de links
"""

import os
import re

def configurar_telegram():
    print("🤖 CONFIGURAÇÃO DO TELEGRAM")
    print("=" * 40)
    print()
    
    # Verificar se o arquivo principal existe
    arquivo_principal = "link_monitor_expandido.py"
    if not os.path.exists(arquivo_principal):
        print("❌ Arquivo link_monitor_expandido.py não encontrado!")
        print("📁 Certifique-se de estar na pasta correta do projeto.")
        return False
    
    print("📋 INSTRUÇÕES:")
    print("1. Crie um bot no Telegram: @BotFather")
    print("2. Digite /newbot e siga as instruções")
    print("3. Copie o TOKEN do bot")
    print("4. Envie uma mensagem para o bot")
    print("5. Acesse: https://api.telegram.org/botSEU_TOKEN/getUpdates")
    print("6. Copie o CHAT_ID (número em 'chat' -> 'id')")
    print()
    
    # Solicitar TOKEN
    while True:
        token = input("🔑 Digite o TOKEN do bot: ").strip()
        if not token:
            print("❌ TOKEN não pode estar vazio!")
            continue
        
        # Validar formato básico do token
        if not re.match(r'^\d+:[A-Za-z0-9_-]+$', token):
            print("❌ Formato do TOKEN inválido!")
            print("💡 Deve ser algo como: 1234567890:ABCDEF...")
            continue
        
        break
    
    # Solicitar CHAT_ID
    while True:
        chat_id = input("💬 Digite o CHAT_ID: ").strip()
        if not chat_id:
            print("❌ CHAT_ID não pode estar vazio!")
            continue
        
        # Validar se é um número
        try:
            int(chat_id)
        except ValueError:
            print("❌ CHAT_ID deve ser um número!")
            continue
        
        break
    
    # Ler arquivo atual
    try:
        with open(arquivo_principal, 'r', encoding='utf-8') as f:
            conteudo = f.read()
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {e}")
        return False
    
    # Substituir TOKEN
    conteudo = re.sub(
        r'TOKEN = "[^"]*"',
        f'TOKEN = "{token}"',
        conteudo
    )
    
    # Substituir CHAT_ID
    conteudo = re.sub(
        r'CHAT_ID = "[^"]*"',
        f'CHAT_ID = "{chat_id}"',
        conteudo
    )
    
    # Salvar arquivo
    try:
        with open(arquivo_principal, 'w', encoding='utf-8') as f:
            f.write(conteudo)
    except Exception as e:
        print(f"❌ Erro ao salvar arquivo: {e}")
        return False
    
    print()
    print("✅ Configuração salva com sucesso!")
    print()
    print("🧪 TESTE AGORA:")
    print("Execute: python link_monitor_expandido.py")
    print("Você deve receber mensagens no Telegram!")
    print()
    
    return True

def main():
    try:
        configurar_telegram()
    except KeyboardInterrupt:
        print("\n\n❌ Configuração cancelada pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main()

