import streamlit as st
from streamlit_gsheets import GSheetsConnection
import random
import pandas as pd
from datetime import datetime, timedelta
import time
import re

st.set_page_config(page_title="Loot Manager PT", layout="wide")

# ==========================================
# 1. CONEXÕES
# ==========================================
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1RJljQ7UwxKCAnP1wmpMD4ZatGSaD-eN21I5CGEnR8K8/edit?usp=sharing"
URL_HORARIOS = "https://docs.google.com/spreadsheets/d/1gZoG2NVeY3KlJFGfoq1nVqjylLIalDXygmOmyXRgWy4/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados(url, aba=None):
    try:
        if aba: df = conn.read(spreadsheet=url, worksheet=aba, ttl=10)
        else: df = conn.read(spreadsheet=url, ttl=10)
        return df.dropna(how="all").fillna("").astype(str)
    except:
        return pd.DataFrame() 

df_equipamentos = carregar_dados(URL_PLANILHA, "Equipamentos")
df_tesouraria = carregar_dados(URL_PLANILHA, "Tesouraria")
df_config = carregar_dados(URL_PLANILHA, "Config")
df_interesses_db = carregar_dados(URL_PLANILHA, "Interesses")
df_horarios_bruto = carregar_dados(URL_HORARIOS)

if not df_config.empty and "Membros" in df_config.columns:
    membros_salvos = "\n".join(df_config["Membros"].tolist())
else:
    membros_salvos = "Isabela\nFelippe\nPlayer3"

# ==========================================
# 2. DICIONÁRIO DE BOSSES ORIGINAL
# ==========================================
mini_bosses = {
    "Angeling": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/1096.png", "drops": ["Cherubin Wing Shoulders", "Angeling Hat", "Carta Angeling"]},
    "Anubis": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/1098.png", "drops": ["Teleknesis Orb", "Anubis Helm", "Carta Anubis"]},
    "Araccryo": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/3088.png", "drops": ["Armadura de Gelo", "araccryo legs", "Carta Araccryo"]},
    "Arc Angeling": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/1388.png", "drops": ["Angelic Ring", "Orlean's Necklace", "Carta Arc Angeling"]},
    "Baihu": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/20347.png", "drops": ["Rabo de gato preto", "Durga", "Jaguar Hat", "Carta Baihu"]},
    "Brain Sucker": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/20889.png", "drops": ["Cursed Star", "Blood Sucker", "Carta Brain Sucker"]},
    "Byrogue": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/1839.png", "drops": ["Armadura de Fogo", "Assassin's Mask", "Carta Byrogue"]},
    "Chepet": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/1250.png", "drops": ["Pom band" , "Scarlet Ribbon", "Carta Chepet"]},
    "Chimera": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/1283.png", "drops": ["White Snake Ring" , "Chimera Mane", "Carta Chimera"]},
    "Deviling": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/1767.png", "drops": ["Deviling Hat","Devil Wing Shoulders", "Carta Deviling"]},
    "Dragon Fly": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/1091.png", "drops": ["Sitting Dragontail", "Flying Helmet", "Carta Dragon Fly"]},
    "Eclipse": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/3424.png", "drops": ["Carrot in mouth" , "Lunatic Brooch", "Carta Eclipse"]},
    "Enraged Priest": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/3514.png", "drops": ["Linen Gloves", "Pontiff's Cassock","Doom Slayer", "Carta Enraged Priest"]},
    "Femmire": {"foto_boss": "https://i.imgur.com/ds86FSd.png", "drops": ["Capa de Água", "Swamp Crown", "Carta Femmire"]},
    "Ghostring": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/1120.png", "drops": ["Ghost Bandana","Librarian's Gloves", "Carta Ghostring"]},
    "Goblin Leader": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/1299.png", "drops": ["Goblin Leader's Mask", "Goblin Leader's Crown", "Carta Goblin Leader"]},
    "Gryphon": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/1259.png", "drops": ["Ahlspiess", "Falcon's Mask","Gryphon's Hat","Giant's Protection", "Carta Gryphon"]},
    "Hydrolancer": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/1720.png", "drops": ["Dragon's Temperance", "Elemental Ring", "Carta Hydrolancer"]},
    "Iskralisa": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/3173.png", "drops": ["Capa de Fogo", "Krathong Crown","Spiritual Ring", "Carta Iskralisa"]},
    "Ju-On": {"foto_boss": "https://i.imgur.com/dbhgzBu.png", "drops": ["Ancient Grudge","Water Lily Crown", "Carta Ju-On"]},
    "Kobold Leader": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/1296.png", "drops": ["Capa de Vento", "Zweinhander","Rock Ruin Shield", "Carta Kobold Leader"]},
    "Kublin": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/1980.png", "drops": ["Armadura de Terra", "Goblin Mask","Mjolnir Mine Shoes", "Carta Kublin"]},
    "Lockstep": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/3126.png", "drops": ["Cooling Device", "Engine Pilebunker","Schimidt's Helm","Observer", "Carta Lockstep"]},
    "Mastering": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/21325.png", "drops": ["Poring Beret", "Mastering Card"]},
    "Mayus": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/1289.png", "drops": ["Capa de Terra", "Mayus Feeler", "Carta Mayus"]},
    "Mime Monkey": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/1585.png", "drops": ["Combo Gloves", "Fallen Monk Rosary", "Carta Mime Monkey"]},
    "Morajin": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/1993.png", "drops": ["Armadura de Vento", "Jupiter Spear","Piabinha", "Carta Morajin"]},
    "Necromancer": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/1870.png", "drops": ["Necro Hood", "Lich's Bone Wand", "Orlean's Gloves", "Carta Necromancer"]},
    "Silver Thief Bug": {"foto_boss": "https://i.imgur.com/hMW8tGF.png", "drops": ["Navel Ring", "Mask of Bankrupt", "Carta Silver Thief Bug"]},
    "Taffy": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/3443.png", "drops": ["Horn Protector", "Spike", "Carta Taffy"]},
    "Tattler Sisters": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/20366.png", "drops": ["Dark Blinkers", "Poison Knife", "Carta Tattler Sisters"]},
    "Toad": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/1089.png", "drops": ["Capa do Toad", "Frog Hat", "Carta Toad"]},
    "Vagabond Wolf": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/21326.png", "drops": ["Drooping Baby Wolf", "Wolf Fur Coat", "Carta Vagabond Wolf"]},
    "Vocal": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/21327.png", "drops": ["Quaver", "Sound Amplifier", "Carta Vocal"]},
    "Vodyanoy": {"foto_boss": "https://i.imgur.com/iyTuoCm.png", "drops": ["Magic Stone Ring", "Skin of Lindwyrmm", "Carta Vodyanoy"]},
    "Zealotus": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/1200.png", "drops": ["Zealotus Doll", "Handcuffs", "Carta Zealotus"]},
    
    "Ancestral Warden": {
        "foto_boss": "https://static.divine-pride.net/images/mobs/png/20277.png", 
        "drops": ["Shoulder Protector", "Woodbone Shield", "Ancestral Warden card"]
    },
    "Blasphemous Ritual": {
        "foto_boss": "https://static.divine-pride.net/images/mobs/png/1957.png", 
        "drops": ["Thornbush Hairband", "Doom Bible", "Blasphemous Ritual card"]
    },
    "Blightwalker": {
        "foto_boss": "https://static.divine-pride.net/images/mobs/png/20420.png", 
        "drops": ["Ronin's Kosode", "Corrupted Geta", "Blightwalker Card"]
    },
    "Bramblehare": {
        "foto_boss": "https://static.divine-pride.net/images/mobs/png/2336.png", 
        "drops": ["Shield de Terra", "Jumping Manteau", "Bramblehare card"]
    },
    "Tiki Kanaloa": {
        "foto_boss": "https://wikimirror.lifeto.co/asset.103.ggftw.net/wiki/to-w/images/6/68/Ancient_Hero_Statue.gif", 
        "drops": ["Plastic Straw", "Tiki Talisman", "Tiki Kalanoa card"]
    },
    "Twinjaw": {
        "foto_boss": "https://static.divine-pride.net/images/mobs/png/1618.png", 
        "drops": ["Carapace Armor", "Twinjaw Axe", "Twinjaw card"]
    },
    "Twisted Twilight": {
        "foto_boss": "https://static.divine-pride.net/images/mobs/png/1681.png", 
        "drops": ["Dimensional Communicator", "Twilight Boots", "Twisted Twilight card"]
    },
    "Werewolf": {
        "foto_boss": "https://static.divine-pride.net/images/mobs/png/1022.png", 
        "drops": ["Ulle's Cap", "Beast Bone Bow", "Werewolf Card"]
    },
    "Shiosen": {
        "foto_boss": "https://static.divine-pride.net/images/mobs/png/2254.png", 
        "drops": ["Shiled de Água", "Ethernal Harmony", "Shiosen Scroll", "Shiosen Card"]
    },
    "Sludge Abomination": {
        "foto_boss": "https://static.divine-pride.net/images/mobs/png/1366.png", 
        "drops": ["Chemical Amalgam", "Chemistry Kit", "Sludge Abomination card"]
    },
    "Rotbloom": {
        "foto_boss": "https://static.divine-pride.net/images/mobs/png/2906.png", 
        "drops": ["Apothecary Robe", "Addiction Plant", "Rotbloom card"]
    },
    "Possessed Marble Idol": {
        "foto_boss": "https://www.spriters-resource.com/media/asset_icons/21/23101.png", 
        "drops": ["Marble Pillar", "Marble Mask", "Possessed Marble Idol card"]
    }
}

# ==========================================
# 2.5 O EXTRATOR EM MATRIZ 
# ==========================================
cronograma_por_hora = {} 
cronograma_por_boss = {} 

if not df_horarios_bruto.empty:
    colunas = df_horarios_bruto.columns.tolist()
    for idx, row in df_horarios_bruto.iterrows():
        val_primeira_col = str(row.iloc[0]).strip()
        match_hora = re.search(r'(\d{1,2}:\d{2})', val_primeira_col)
        
        if match_hora:
            try:
                h_obj = datetime.strptime(match_hora.group(1), "%H:%M")
                hora_formatada = h_obj.strftime("%H:%M")
                bosses_da_linha = []
                
                for col_name in colunas[1:]:
                    val_cell = str(row[col_name]).strip().lower()
                    if val_cell == 'sim':
                        b_name = str(col_name).strip()
                        if len(b_name) > 2 and "unnamed" not in b_name.lower():
                            bosses_da_linha.append(b_name)
                
                if bosses_da_linha:
                    if hora_formatada not in cronograma_por_hora:
                        cronograma_por_hora[hora_formatada] = set()
                    cronograma_por_hora[hora_formatada].update(bosses_da_linha)
                    
                    for b in bosses_da_linha:
                        if b not in cronograma_por_boss:
                            cronograma_por_boss[b] = set()
                        cronograma_por_boss[b].add(hora_formatada)
                        
                        if b not in mini_bosses:
                            mini_bosses[b] = {
                                "foto_boss": "https://via.placeholder.com/32x32.png?text=?", 
                                "drops": ["Drop Desconhecido"]
                            }
            except:
                pass

lista_bosses = sorted(list(mini_bosses.keys()))

# ==========================================
# 3. ESTILOS VISUAIS E TABELAS HTML
# ==========================================
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .boss-header { background-color: #1e2329; padding: 10px; border-radius: 10px 10px 0 0; display: flex; align-items: center; border: 1px solid #444; }
    .boss-photo { width: 32px; height: 32px; margin-right: 10px; border-radius: 5px; object-fit: contain; }
    .stExpander { border-radius: 0 0 10px 10px !important; border: 1px solid #444 !important; margin-bottom: 15px; }
    .main-save-container { background-color: #1e2329; padding: 20px; border-radius: 10px; border: 1px solid #58a6ff; margin-bottom: 20px; }
    
    .matrix-table { width: 100%; border-collapse: collapse; font-family: monospace; font-size: 1.1rem; text-align: center; margin-top: 15px; }
    .matrix-table th, .matrix-table td { border: 3px solid #30363d; padding: 10px; vertical-align: middle; text-align: center; }
    .matrix-table th { background-color: #21262d; color: #58a6ff; }
    
    .cell-boss-title { background-color: #21262d; color: #58a6ff; font-weight: bold; font-size: 1.2rem; width: 20%; text-align: center; }
    
    .cell-time-vivo { background-color: #238636; color: #ffffff; font-weight: bold; border: 2px solid #2ea043; width: 16%; text-align: center; }
    .cell-time-breve { background-color: #d29922; color: #ffffff; font-weight: bold; border: 2px solid #e3b341; width: 16%; text-align: center; }
    .cell-time-morto { background-color: #161b22; color: #8b949e; width: 16%; text-align: center; }
    
    .status-vivo { background-color: #0f2b16 !important; }
    .status-vivo td { color: #7ee787 !important; border-color: #238636 !important; font-weight: bold; }
    .status-breve { background-color: #3d2e04 !important; }
    .status-breve td { color: #e3b341 !important; border-color: #d29922 !important; font-weight: bold; }
    .status-morto { background-color: transparent; }
    
    .icon-table { width: 24px; height: 24px; border-radius: 4px; vertical-align: middle; margin-right: 8px; }
    .icon-large { width: 48px; height: 48px; border-radius: 8px; margin-bottom: 8px; }
    </style>
    """, unsafe_allow_html=True)

st.title("😈 Os Coisaruim guild management")

# ==========================================
# 4. BARRA LATERAL
# ==========================================
with st.sidebar:
    st.header("⚙️ Configurações")
    nomes_input = st.text_area("Membros da PT:", value=membros_salvos, height=250)
    membros = [m.strip() for m in nomes_input.split("\n") if m.strip()]
    if st.button("💾 Salvar Membros"):
        conn.update(spreadsheet=URL_PLANILHA, worksheet="Config", data=pd.DataFrame({"Membros": membros}))
        st.success("Lista salva!")
        st.rerun()

aba1, aba2, aba3 = st.tabs(["⚔️ Distribuição", "💰 Caixa da PT", "⏰ Matriz de Respawn"])

# ------------------------------------------
# ABA 1: DISTRIBUIÇÃO
# ------------------------------------------
with aba1:
    st.markdown('<div class="main-save-container">', unsafe_allow_html=True)
    st.subheader("📌 Controle de Wishlist Global")
    if st.button("☁️ SALVAR TODAS AS WISHLISTS", type="primary", use_container_width=True):
        reg = []
        for boss, info in mini_bosses.items():
            for item in info["drops"]:
                if f"sel_{boss}_{item}" in st.session_state:
                    for m in st.session_state[f"sel_{boss}_{item}"]:
                        reg.append({"Item": f"{boss}_{item}", "Membro": m})
        df_send = pd.DataFrame(reg, columns=["Item", "Membro"])
        conn.update(spreadsheet=URL_PLANILHA, worksheet="Interesses", data=df_send)
        st.success("Sincronizado! (Lembre de apagar as colunas velhas na planilha se ainda estiverem lá)")
        time.sleep(2)
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    for i, (boss_name, info) in enumerate(mini_bosses.items()):
        target_col = [col1, col2, col3][i % 3]
        with target_col:
            st.markdown(f'<div class="boss-header"><img src="{info["foto_boss"]}" class="boss-photo" onerror="this.src=\'https://via.placeholder.com/32\'"><span class="boss-name">{boss_name}</span></div>', unsafe_allow_html=True)
            with st.expander(f"📦 Drops", expanded=False):
                for item in info["drops"]:
                    st.write(f"**{item}**")
                    key_item = f"{boss_name}_{item}"
                    
                    if not df_interesses_db.empty and "Item" in df_interesses_db.columns:
                        def_int = df_interesses_db[df_interesses_db["Item"] == key_item]["Membro"].tolist()
                        def_int = [m for m in def_int if m in membros]
                    else:
                        def_int = []

                    int_agora = st.multiselect("Interessados:", membros, default=def_int, key=f"sel_{boss_name}_{item}")

                    if int_agora:
                        c_prio = st.columns(len(int_agora))
                        for idx, pl in enumerate(int_agora):
                            with c_prio[idx]: st.selectbox(f"Prio {pl}", [1,2,3,4,5], key=f"p_{boss_name}_{item}_{pl}")
                        
                        if st.button(f"🎲 Sortear", key=f"roll_{boss_name}_{item}"):
                            st.session_state[f"res_{boss_name}_{item}"] = {p: random.randint(1, 100) for p in int_agora}
                        
                        res_key = f"res_{boss_name}_{item}"
                        if res_key in st.session_state and isinstance(st.session_state[res_key], dict):
                            st.code(" | ".join([f"{k}: {v}" for k, v in st.session_state[res_key].items()]))
                        
                        venc = st.selectbox("Quem levou?", int_agora, key=f"v_{boss_name}_{item}")
                        if st.button(f"✅ Registrar Drop", key=f"reg_{boss_name}_{item}"):
                            n_h = pd.DataFrame([{"Data": datetime.now().strftime("%d/%m %H:%M"), "Boss": boss_name, "Item": item, "Ganhador": venc}])
                            df_up_h = pd.concat([df_equipamentos, n_h], ignore_index=True) if not df_equipamentos.empty else n_h
                            conn.update(spreadsheet=URL_PLANILHA, worksheet="Equipamentos", data=df_up_h)
                            
                            rest = df_interesses_db[~((df_interesses_db["Item"] == key_item) & (df_interesses_db["Membro"] == venc))]
                            conn.update(spreadsheet=URL_PLANILHA, worksheet="Interesses", data=rest)
                            st.rerun()
                    st.divider()

# ------------------------------------------
# ABA 2: CAIXA
# ------------------------------------------
with aba2:
    with st.container(border=True):
        st.subheader("📝 Registrar Venda")
        cx1, cx2 = st.columns(2)
        with cx1: b_v = st.selectbox("Boss", lista_bosses, key="bv")
        with cx2: i_v = st.selectbox("Item", mini_bosses[b_v]["drops"], key="iv")
        pt = st.multiselect("Quem estava?", membros, key="ptv")
        if st.button("💾 Salvar no Caixa"):
            if pt:
                n_c = pd.DataFrame([{"Data": datetime.now().strftime("%d/%m/%Y %H:%M"), "Boss": b_v, "Item": i_v, "Presentes": ", ".join(pt), "Partes": len(pt), "Status": "Aguardando Venda", "Detalhes/Valor": ""}])
                conn.update(spreadsheet=URL_PLANILHA, worksheet="Tesouraria", data=pd.concat([df_tesouraria, n_c], ignore_index=True) if not df_tesouraria.empty else n_c)
                st.rerun()
    if not df_tesouraria.empty:
        editado = st.data_editor(df_tesouraria, use_container_width=True, hide_index=True, num_rows="dynamic",
            column_config={"Status": st.column_config.SelectboxColumn("Status", options=["Aguardando Venda", "Vendido", "Ficou com a PT"])},
            disabled=["Data", "Boss", "Item", "Presentes", "Partes"], key="ed_tes"
        )
        if st.button("☁️ Sincronizar Alterações"):
            conn.update(spreadsheet=URL_PLANILHA, worksheet="Tesouraria", data=editado)
            st.rerun()

# ------------------------------------------
# ABA 3: MATRIZ DE RESPAWN COM FRAGMENTO DE AUTO-REFRESH
# ------------------------------------------
# O @st.fragment diz ao Streamlit para atualizar APENAS esta função sem piscar o resto do site!
@st.fragment(run_every=5)
def renderizar_cronograma():
    if not cronograma_por_hora:
        st.error("❌ Não encontrei dados de cruzamento na planilha de horários.")
        return

    agora_utc = datetime.utcnow()
    agora_br = agora_utc - timedelta(hours=3)
    agora_sv = agora_br + timedelta(hours=3)
    
    c_fuso, c_hora = st.columns([1, 1])
    fuso = c_fuso.radio("⌚ Fuso Horário Base:", ["Horário do Jogo (Servidor)", "Horário do Brasil (-3h)"], horizontal=True, key="fuso_radio")
    is_br = (fuso == "Horário do Brasil (-3h)")
    
    hora_atual_exibicao = agora_br if is_br else agora_sv
    agora_mins = hora_atual_exibicao.hour * 60 + hora_atual_exibicao.minute
    
    c_hora.info(f"🕒 **Hora Atual:** {hora_atual_exibicao.strftime('%H:%M')} (Ficam verdes por 1 hora)")

    # AJUSTA FUSO HORÁRIO
    cronograma_ajustado = {}
    for h_sv, bosses in cronograma_por_hora.items():
        if is_br:
            h_obj = datetime.strptime(h_sv, "%H:%M") - timedelta(hours=3)
            h_ajustado = h_obj.strftime("%H:%M")
        else:
            h_ajustado = h_sv
        cronograma_ajustado[h_ajustado] = bosses

    # LÓGICA DE ORDENAÇÃO CIRCULAR (A MÁGICA DA FILA)
    def sort_circular(h_str):
        h_obj = datetime.strptime(h_str, "%H:%M")
        h_mins = h_obj.hour * 60 + h_obj.minute
        diff = h_mins - agora_mins
        
        if diff < -720: diff += 1440
        elif diff > 720: diff -= 1440
        
        # Se diff é >= -60, ele é Vivo (0 a -60) ou Futuro (> 0). Ficam no topo.
        # Se diff < -60, ele é Passado Morto. Vão pro final.
        if diff >= -60:
            return diff
        else:
            return diff + 1440

    # CÁLCULO DA COR - 1 HORA DE VIDA (60 MINUTOS)
    status_map = {}
    futuros = {}
    
    for h in cronograma_ajustado.keys():
        h_obj = datetime.strptime(h, "%H:%M")
        h_mins = h_obj.hour * 60 + h_obj.minute
        diff = h_mins - agora_mins
        
        if diff < -720: diff += 1440
        elif diff > 720: diff -= 1440
        
        if -60 <= diff <= 0:
            status_map[h] = "status-vivo"
        elif diff > 0:
            futuros[h] = diff
            status_map[h] = "status-morto"
        else:
            status_map[h] = "status-morto"
    
    if futuros:
        proximo_h = min(futuros, key=futuros.get)
        status_map[proximo_h] = "status-breve"

    st.divider()

    f1, f2 = st.columns(2)
    modo_visao = f1.selectbox("👁️ Modo de Visualização:", ["Tabela Completa (Por Horário)", "Inverter: Filtrar por Boss"], key="modo_visao")
    
    # APLICANDO A ORDENAÇÃO CIRCULAR AQUI
    todas_horas = sorted(list(cronograma_ajustado.keys()), key=sort_circular)
    todos_bosses = sorted(list(cronograma_por_boss.keys()))
    
    def get_boss_img(b_name):
        if b_name in mini_bosses:
            return f"<img src='{mini_bosses[b_name]['foto_boss']}' class='icon-table' onerror=\"this.src='https://via.placeholder.com/24'\">"
        return ""

    if modo_visao == "Tabela Completa (Por Horário)":
        hora_filtro = f2.selectbox("🔍 Pular para Horário (Opcional):", ["Todos"] + sorted(list(cronograma_ajustado.keys())), key="hora_filtro")
        
        html_matriz = "<table class='matrix-table'><tr><th>Horário</th><th>Boss 1</th><th>Boss 2</th><th>Boss 3</th><th>Boss 4</th></tr>"
        
        for h in todas_horas:
            if hora_filtro != "Todos" and h != hora_filtro: continue
            
            bosses = sorted(list(cronograma_ajustado[h]))
            while len(bosses) < 4: bosses.append("-")
            
            status_classe = status_map.get(h, "status-morto")
            html_matriz += f"<tr class='{status_classe}'><td class='cell-time' style='text-align: center;'>{h}</td>"
            for b in bosses[:4]:
                if b == "-":
                    html_matriz += f"<td style='text-align: center;'>-</td>"
                else:
                    img_tag = get_boss_img(b)
                    html_matriz += f"<td><div style='display: flex; justify-content: center; align-items: center;'>{img_tag}{b}</div></td>"
            html_matriz += "</tr>"
        
        html_matriz += "</table>"
        st.markdown(html_matriz, unsafe_allow_html=True)
        st.caption("🟢 **VIVO:** Nasceu a menos de 1 hora | 🟡 **PRÓXIMO:** É o próximo da fila")

    else:
        boss_filtro = f2.selectbox("🔍 Selecione o Boss:", todos_bosses, key="boss_filtro")
        
        horas_deste_boss = []
        for h_ajustado, lista_b in cronograma_ajustado.items():
            if boss_filtro in lista_b: horas_deste_boss.append(h_ajustado)
        
        # ORDENA AS HORAS DO BOSS DE FORMA CIRCULAR TAMBÉM
        horas_deste_boss = sorted(horas_deste_boss, key=sort_circular)
        
        def separar_em_grupos(lista, tamanho):
            return [lista[i:i + tamanho] for i in range(0, len(lista), tamanho)]
        
        blocos_de_horas = separar_em_grupos(horas_deste_boss, 4)
        html_matriz = "<table class='matrix-table'>"
        
        for i, bloco in enumerate(blocos_de_horas):
            html_matriz += "<tr>"
            
            if i == 0:
                img_grande = ""
                if boss_filtro in mini_bosses:
                    img_grande = f"<img src='{mini_bosses[boss_filtro]['foto_boss']}' class='icon-large' onerror=\"this.src='https://via.placeholder.com/48'\"><br>"
                html_matriz += f"<td rowspan='{len(blocos_de_horas)}' class='cell-boss-title'>{img_grande}{boss_filtro}</td>"
            
            for h in bloco:
                status = status_map.get(h, "status-morto")
                if status == "status-vivo":
                    html_matriz += f"<td class='cell-time-vivo'>{h}<br><small>(VIVO)</small></td>"
                elif status == "status-breve":
                    html_matriz += f"<td class='cell-time-breve'>{h}<br><small>(PRÓX)</small></td>"
                else:
                    html_matriz += f"<td class='cell-time-morto'>{h}</td>"
            
            for _ in range(4 - len(bloco)):
                html_matriz += "<td class='cell-time-morto'>-</td>"
                
            html_matriz += "</tr>"
            
        html_matriz += "</table>"
        st.markdown(html_matriz, unsafe_allow_html=True)
        st.caption("🟢 **VIVO:** Nasceu a menos de 1 hora | 🟡 **PRÓXIMO:** É o próximo da fila")

with aba3:
    renderizar_cronograma()