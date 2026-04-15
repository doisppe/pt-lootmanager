import streamlit as st
from streamlit_gsheets import GSheetsConnection
import random
import pandas as pd
from datetime import datetime
import time

st.set_page_config(page_title="Loot Manager PT", layout="wide")

# ==========================================
# 1. CONEXÃO E CARREGAMENTO
# ==========================================
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1RJljQ7UwxKCAnP1wmpMD4ZatGSaD-eN21I5CGEnR8K8/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados(aba):
    try:
        df = conn.read(spreadsheet=URL_PLANILHA, worksheet=aba, ttl=5)
        return df.dropna(how="all").fillna("").astype(str)
    except:
        return pd.DataFrame() 

df_equipamentos = carregar_dados("Equipamentos")
df_tesouraria = carregar_dados("Tesouraria")
df_config = carregar_dados("Config")
df_interesses = carregar_dados("Interesses")

if not df_config.empty and "Membros" in df_config.columns:
    membros_salvos = "\n".join(df_config["Membros"].tolist())
else:
    membros_salvos = "Isabela\nFelippe\nPlayer3"

# ==========================================
# 2. ESTILOS VISUAIS
# ==========================================
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .boss-header {
        background-color: #1e2329; padding: 10px; border-radius: 10px 10px 0 0;
        display: flex; align-items: center; border: 1px solid #444;
    }
    .boss-photo { width: 32px; height: 32px; margin-right: 10px; border-radius: 5px; object-fit: contain; }
    .boss-name { font-size: 1.1rem; font-weight: bold; margin: 0; }
    .stExpander { border-radius: 0 0 10px 10px !important; border: 1px solid #444 !important; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("😈 Os Coisaruim guild loot management")

# ==========================================
# 3. BARRA LATERAL
# ==========================================
with st.sidebar:
    st.header("⚙️ Configurações")
    nomes_input = st.text_area("Membros da PT:", value=membros_salvos, height=250)
    membros = [m.strip() for m in nomes_input.split("\n") if m.strip()]
    
    if st.button("💾 Salvar Membros", type="primary", use_container_width=True):
        conn.update(spreadsheet=URL_PLANILHA, worksheet="Config", data=pd.DataFrame({"Membros": membros}))
        st.success("Lista salva!")
        st.rerun()

# ==========================================
# 4. DICIONÁRIO DE BOSSES
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
    "Zealotus": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/1200.png", "drops": ["Zealotus Doll", "Handcuffs", "Carta Zealotus"]}
}
lista_bosses = list(mini_bosses.keys())

aba1, aba2 = st.tabs(["⚔️ Distribuição", "💰 Caixa da PT"])

# ------------------------------------------
# ABA 1: DISTRIBUIÇÃO (FIXED WISHLIST)
# ------------------------------------------
with aba1:
    st.info("Wishlist: Os nomes salvos ficam fixos. Ao registrar o drop, o ganhador sai da lista.")
    
    # Botão de Sincronização Geral (Opcional, mas ajuda no erro 429)
    if st.button("☁️ SALVAR TODAS AS WISHLISTS (Mestre)", type="primary"):
        conn.update(spreadsheet=URL_PLANILHA, worksheet="Interesses", data=df_interesses.fillna(""))
        st.success("Tudo sincronizado!")
        st.rerun()

    col1, col2, col3 = st.columns(3)
    
    for i, (boss_name, info) in enumerate(mini_bosses.items()):
        target_col = [col1, col2, col3][i % 3]
        with target_col:
            st.markdown(f'<div class="boss-header"><img src="{info["foto_boss"]}" class="boss-photo"><span class="boss-name">{boss_name}</span></div>', unsafe_allow_html=True)
            with st.expander(f"📦 Drops", expanded=False):
                
                # Criamos um dicionário local para este Boss para não perder dados ao processar
                interesses_atuais_boss = {}
                
                for item in info["drops"]:
                    st.write(f"**{item}**")
                    key_item = f"{boss_name}_{item}"
                    
                    # Busca interessados salvos
                    if not df_interesses.empty and key_item in df_interesses.columns:
                        def_int = [x for x in df_interesses[key_item].tolist() if x and x in membros]
                    else:
                        def_int = []

                    interesses_atuais_boss[key_item] = st.multiselect("Wishlist:", membros, default=def_int, key=f"sel_{boss_name}_{item}")
                    
                    if interesses_atuais_boss[key_item]:
                        c_prio = st.columns(len(interesses_atuais_boss[key_item]))
                        for idx, pl in enumerate(interesses_atuais_boss[key_item]):
                            with c_prio[idx]:
                                st.selectbox(f"Prio {pl}", [1,2,3,4,5], key=f"p_{boss_name}_{item}_{pl}")
                        
                        if st.button(f"🎲 Sortear {item}", key=f"roll_{boss_name}_{item}"):
                            st.session_state[f"res_{boss_name}_{item}"] = {p: random.randint(1, 100) for p in interesses_atuais_boss[key_item]}
                        
                        res_key = f"res_{boss_name}_{item}"
                        if res_key in st.session_state and isinstance(st.session_state[res_key], dict):
                            st.code(" | ".join([f"{k}: {v}" for k, v in st.session_state[res_key].items()]))
                        
                        venc = st.selectbox("Quem levou?", interesses_atuais_boss[key_item], key=f"v_{boss_name}_{item}")
                        
                        # Botão REGISTRAR DROP (Sorteio e Limpeza da Wishlist)
                        if st.button(f"✅ Registrar Drop: {item}", key=f"reg_{boss_name}_{item}", use_container_width=True):
                            # 1. Salva no Histórico
                            novo = pd.DataFrame([{"Data": datetime.now().strftime("%d/%m %H:%M"), "Boss": boss_name, "Item": item, "Ganhador": venc}])
                            df_up = pd.concat([df_equipamentos, novo], ignore_index=True) if not df_equipamentos.empty else novo
                            conn.update(spreadsheet=URL_PLANILHA, worksheet="Equipamentos", data=df_up)
                            
                            # 2. Limpa da Wishlist na Planilha
                            restantes = [p for p in interesses_atuais_boss[key_item] if p != venc]
                            df_interesses[key_item] = pd.Series(restantes)
                            conn.update(spreadsheet=URL_PLANILHA, worksheet="Interesses", data=df_interesses.fillna(""))
                            
                            st.success(f"Salvo! {venc} removido da lista.")
                            time.sleep(1)
                            st.rerun()
                    st.divider()

                # BOTÃO PARA SALVAR A WISHLIST DESTE BOSS ESPECÍFICO (FIXAR)
                if st.button(f"📌 Salvar Wishlist de {boss_name}", key=f"fix_boss_{boss_name}", type="primary"):
                    # Atualiza o DataFrame global com todas as seleções desse boss
                    for k_it, lista_p in interesses_atuais_boss.items():
                        df_interesses[k_it] = pd.Series(lista_p)
                    
                    conn.update(spreadsheet=URL_PLANILHA, worksheet="Interesses", data=df_interesses.fillna(""))
                    st.toast(f"Wishlist de {boss_name} atualizada!")
                    time.sleep(1)
                    st.rerun()

    if not df_equipamentos.empty:
        st.subheader("📜 Histórico")
        st.dataframe(df_equipamentos, use_container_width=True, hide_index=True)

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
                novo_c = pd.DataFrame([{"Data": datetime.now().strftime("%d/%m/%Y %H:%M"), "Boss": b_v, "Item": i_v, "Presentes": ", ".join(pt), "Partes": len(pt), "Status": "Aguardando Venda", "Detalhes/Valor": ""}])
                up_c = pd.concat([df_tesouraria, novo_c], ignore_index=True) if not df_tesouraria.empty else novo_c
                conn.update(spreadsheet=URL_PLANILHA, worksheet="Tesouraria", data=up_c)
                st.rerun()

    if not df_tesouraria.empty:
        editado = st.data_editor(df_tesouraria, use_container_width=True, hide_index=True, num_rows="dynamic",
            column_config={
                "Status": st.column_config.SelectboxColumn("Status", options=["Aguardando Venda", "Vendido", "Ficou com a PT"]),
                "Detalhes/Valor": st.column_config.TextColumn("Valor/Detalhes")
            },
            disabled=["Data", "Boss", "Item", "Presentes", "Partes"], key="ed_tes"
        )
        if st.button("☁️ Sincronizar Alterações"):
            conn.update(spreadsheet=URL_PLANILHA, worksheet="Tesouraria", data=editado)
            st.rerun()