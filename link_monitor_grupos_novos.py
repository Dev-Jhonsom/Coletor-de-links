import requests
from bs4 import BeautifulSoup
import re
import os
from datetime import datetime

# Configuração
TOKEN = "7585232781:AAGCEXAojfQbxc-tgCzifXbzD89AP4F7YIE"
CHAT_ID = "1289789994"
ARQUIVO_LINKS = "grupos_enviados.txt"

# ═══════════════════════════════════════════════════════════════
# 📋 LISTA DE PÁGINAS PARA MONITORAR
# ═══════════════════════════════════════════════════════════════
PAGINAS = [
    ("https://sndflw.com/i/5ISgEsCkPwfn1CWl8iye?utm_source=trafego-frio&utm_medium=00_%5BIG%5D_%5BCSM%5D_Captura_%5B030D_%2B_Checkout_%2B_Pag_vendas_180D&utm_campaign=csm1025l&utm_content=001_IMG_A_maior&utm_term=Instagram_Stories&utm_id=120232979337740780", "JHOM JHOM"),
("https://sndflw.com/i/eDaMch9TGpV3fy5IgiwK", "EXCEL JHON"),
("https://brunolucarelli.com.br/confirmar-inscricao-black/", "BLACK MATADOR"),
("https://sndflw.com/i/blackoutsiderschool", "Black Pass"),
    
]

# ═══════════════════════════════════════════════════════════════
# 🔧 FUNÇÕES PRINCIPAIS
# ═══════════════════════════════════════════════════════════════

def carregar_grupos_enviados():
    """Carrega grupos já enviados para evitar duplicatas"""
    if not os.path.exists(ARQUIVO_LINKS):
        return set()
    with open(ARQUIVO_LINKS, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

def salvar_grupo_enviado(grupo_link):
    """Salva grupo como já enviado"""
    with open(ARQUIVO_LINKS, "a", encoding="utf-8") as f:
        f.write(grupo_link + "\n")

def extrair_link_limpo(link_completo):
    """Extrai apenas o link limpo (sem tipo)"""
    if ": " in link_completo:
        return link_completo.split(": ", 1)[1]
    return link_completo

def eh_grupo_whatsapp_telegram(link):
    """Verifica se é realmente um grupo (não chat individual)"""
    link_limpo = extrair_link_limpo(link).lower()
    
    # Grupos do WhatsApp
    if "chat.whatsapp.com" in link_limpo:
        return True
    
    # Grupos/Canais do Telegram
    if "t.me/" in link_limpo or "telegram.me/" in link_limpo:
        # Excluir chats individuais (que geralmente têm números)
        if not re.search(r'/\+?\d+', link_limpo):  # Não tem número de telefone
            return True
    
    return False

def enviar_telegram(mensagem):
    """Envia mensagem para o Telegram"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    dados = {"chat_id": CHAT_ID, "text": mensagem}
    try:
        response = requests.post(url, data=dados, timeout=10)
        return response.status_code == 200
    except:
        return False

def buscar_links(url):
    """Busca links do WhatsApp, Telegram e SendFlow numa página"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        # Acessar página
        resposta = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        soup = BeautifulSoup(resposta.text, 'html.parser')
        
        # Buscar todos os links
        links_encontrados = set()
        
        # Padrões de busca
        padroes = {
            "WhatsApp": r'https?://(?:chat\.whatsapp\.com|api\.whatsapp\.com|wa\.me)/[^\s"\'<>]+',
            "Telegram": r'https?://(?:t\.me|telegram\.me)/[^\s"\'<>]+',
            "SendFlow": r'https?://(?:sendflow\.pro|sndflw\.com|i\.sendflow\.pro)/[^\s"\'<>]+'
        }
        
        # Buscar em todo o HTML
        html_completo = str(soup)
        for tipo, padrao in padroes.items():
            matches = re.findall(padrao, html_completo, re.IGNORECASE)
            for match in matches:
                # Limpar link
                link_limpo = match.rstrip('",\')}]')
                if link_limpo and len(link_limpo) > 10:
                    links_encontrados.add(f"{tipo}: {link_limpo}")
        
        return list(links_encontrados)
        
    except Exception as e:
        print(f"Erro ao acessar {url}: {e}")
        return []

def main():
    """Função principal - SÓ ENVIA SE FOR GRUPO NOVO"""
    print(f"\n🚀 Iniciando busca por GRUPOS NOVOS - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Carregar grupos já enviados
    grupos_enviados = carregar_grupos_enviados()
    grupos_novos_encontrados = []
    
    # Verificar cada página
    for url, nome in PAGINAS:
        print(f"\n📡 Verificando: {nome}")
        
        # Buscar links
        links = buscar_links(url)
        
        # Filtrar apenas GRUPOS (não chats individuais)
        grupos = [link for link in links if eh_grupo_whatsapp_telegram(link)]
        
        if grupos:
            print(f"   🔍 Encontrados {len(grupos)} grupo(s)")
            
            # Verificar quais são realmente NOVOS
            grupos_novos = []
            for grupo in grupos:
                link_limpo = extrair_link_limpo(grupo)
                if link_limpo not in grupos_enviados:
                    grupos_novos.append(grupo)
                    print(f"   ✅ NOVO: {grupo}")
                else:
                    print(f"   ❌ JÁ ENVIADO: {grupo}")
            
            # SÓ ENVIA SE HOUVER GRUPOS REALMENTE NOVOS
            if grupos_novos:
                # Criar mensagem
                mensagem = f"🆕 **GRUPO(S) NOVO(S) ENCONTRADO(S)!**\n\n"
                mensagem += f"🎯 **{nome}**\n"
                mensagem += f"🕐 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
                
                for i, grupo in enumerate(grupos_novos, 1):
                    tipo = grupo.split(": ")[0]
                    link = extrair_link_limpo(grupo)
                    mensagem += f"{i}. **{tipo}**: {link}\n"
                
                mensagem += f"\n📊 Total: {len(grupos_novos)} grupo(s) novo(s)"
                mensagem += f"\n📍 Fonte: {nome}"
                
                # Enviar para Telegram
                if enviar_telegram(mensagem):
                    print(f"✅ ENVIADO! {len(grupos_novos)} grupo(s) novo(s) de {nome}")
                    
                    # Salvar como enviados
                    for grupo in grupos_novos:
                        link_limpo = extrair_link_limpo(grupo)
                        salvar_grupo_enviado(link_limpo)
                    
                    grupos_novos_encontrados.extend(grupos_novos)
                else:
                    print(f"❌ ERRO ao enviar grupos de {nome}")
            else:
                print(f"   ℹ️  Nenhum grupo novo (todos já foram enviados)")
        else:
            print(f"   ❌ Nenhum grupo encontrado")
    
    # Relatório final
    print(f"\n🏁 RESUMO FINAL:")
    print(f"   📊 Páginas verificadas: {len(PAGINAS)}")
    print(f"   🆕 Grupos novos encontrados: {len(grupos_novos_encontrados)}")
    
    # SÓ ENVIA RELATÓRIO SE NÃO HOUVER GRUPOS NOVOS
    if not grupos_novos_encontrados:
        print(f"   📱 Enviando relatório de 'nenhum grupo novo'")
        
        mensagem_status = f"📊 **Relatório de Monitoramento**\n"
        mensagem_status += f"🕐 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
        mensagem_status += f"✅ {len(PAGINAS)} páginas verificadas\n"
        mensagem_status += f"❌ Nenhum grupo novo encontrado\n"
        mensagem_status += f"ℹ️  Todos os grupos já foram enviados anteriormente\n\n"
        mensagem_status += f"🔄 Próxima verificação conforme agendamento"
        
        enviar_telegram(mensagem_status)
    else:
        print(f"   ✅ Grupos novos foram enviados - sem relatório adicional")
    
    print(f"\n🎯 CONCLUÍDO - {len(grupos_novos_encontrados)} grupo(s) novo(s) processado(s)")

if __name__ == "__main__":
    main()

