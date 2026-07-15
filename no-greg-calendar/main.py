import ephem
from datetime import datetime
import requests

def obter_fase_lua():
    data = ephem.now()
    lua = ephem.Moon(data)
    fase_percentual = lua.phase
    
    # Mapeamento de abreviações IAU para nomes em português
    signos_map = {
        'Ari': 'Áries', 'Tau': 'Touro', 'Gem': 'Gêmeos', 'Cnc': 'Câncer',
        'Leo': 'Leão', 'Vir': 'Virgem', 'Lib': 'Libra', 'Sco': 'Escorpião',
        'Sgr': 'Sagitário', 'Cap': 'Capricórnio', 'Aqr': 'Aquário', 'Psc': 'Peixes'
    }
    
    abrev = ephem.constellation(lua)[0]
    signo_pt = signos_map.get(abrev, abrev)
    
    # Categorização simples da fase
    if fase_percentual < 1: status = "Lua Nova"
    elif fase_percentual < 45: status = "Crescente"
    elif fase_percentual < 55: status = "Quarto Crescente"
    elif fase_percentual < 95: status = "Gibosa"
    elif fase_percentual < 100: status = "Lua Cheia"
    else: status = "Minguante"
    
    print(f"Fase da Lua: {status} ({fase_percentual:.1f}%)")
    print(f"Signo da Lua: {signo_pt}")
    return status, signo_pt

def obter_dados_calendario():
    hoje_str = datetime.now().strftime("%Y-%m-%d")
    url_conversor = f"https://www.hebcal.com/converter?cfg=json&date={hoje_str}&g2h=1&strict=1"

    try:
        resposta_conv = requests.get(url_conversor)
        resposta_conv.raise_for_status()
        dados_data = resposta_conv.json()

        print("=" * 60)
        print(f"Data Gregoriana: {datetime.now().strftime('%d/%m/%Y')}")
        print(f"Data Judaica: {dados_data.get('hd')} de {dados_data.get('hm')} de {dados_data.get('hy')}")
        print("=" * 60)

        url_eventos = f"https://www.hebcal.com/hebcal?v=1&cfg=json&maj=on&min=on&mod=on&nx=on&mf=on&ss=on&s=on&start={hoje_str}&end={hoje_str}"
        
        resposta_evt = requests.get(url_eventos)
        resposta_evt.raise_for_status()
        eventos_hoje = resposta_evt.json().get("items", [])

        if eventos_hoje:
            print("\nEventos de Hoje:")
            for ev in eventos_hoje:
                print(f"\n🔸 {ev.get('title')}\n   Explicação: {ev.get('memo', 'N/A')}")
        else:
            print("\nNão há eventos listados.")
            
        print("\n" + "=" * 60 + "\n")

    except requests.exceptions.RequestException as e:
        print(f"Erro na API Hebcal: {e}")

if __name__ == "__main__":
    obter_fase_lua()
    obter_dados_calendario()