import streamlit as st
from streamlit_gsheets import GSheetsConnection
import random
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Loot Manager PT", layout="wide")

# ==========================================
# 1. CONFIGURAÇÃO DO GOOGLE SHEETS
# ==========================================
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1RJljQ7UwxKCAnP1wmpMD4ZatGSaD-eN21I5CGEnR8K8/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

def carregar_dados(aba):
    try:
        df = conn.read(spreadsheet=URL_PLANILHA, worksheet=aba, ttl=0)
        df = df.dropna(how="all") 
        df = df.fillna("").astype(str)
        return df
    except:
        return pd.DataFrame() 

df_equipamentos = carregar_dados("Equipamentos")
df_tesouraria = carregar_dados("Tesouraria")

# ==========================================
# 2. ESTILOS VISUAIS E CSS
# ==========================================
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .boss-header {
        background-color: #1e2329; padding: 10px; border-radius: 10px 10px 0 0;
        display: flex; align-items: center; border: 1px solid #444; border-bottom: none;
    }
    .boss-photo { width: 32px; height: 32px; margin-right: 10px; border-radius: 5px; object-fit: contain; }
    .boss-name { font-size: 1.1rem; font-weight: bold; margin: 0; }
    .stExpander { border-radius: 0 0 10px 10px !important; border: 1px solid #444 !important; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("😈 Os Coisaruim guild loot management")

# ==========================================
# 3. BARRA LATERAL (CONFIGURAÇÕES)
# ==========================================
with st.sidebar:
    st.header("⚙️ Configurações da PT")
    nomes_input = st.text_area("Membros da PT (um por linha):", value="Isabela\nFelippe\nPlayer3")
    membros = [m.strip() for m in nomes_input.split("\n") if m.strip()]
    
    st.divider()
    st.caption("ℹ️ Os dados agora são salvos na nuvem (Google Sheets). Edições no histórico devem ser feitas diretamente na planilha ou via aba Caixa da PT.")

# ==========================================
# 4. DICIONÁRIO COMPLETO DE MINI BOSSES
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
    "Dragon Fly": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/3424.png", "drops": ["Sitting Dragontail", "Flying Helmet", "Carta Dragon Fly"]},
    "Eclipse": {"foto_boss": "https://static.divine-pride.net/images/mobs/png/1147.png", "drops": ["Carrot in mouth" , "Lunatic Brooch", "Carta Eclipse"]},
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

# ==========================================
# 5. ESTRUTURA DE ABAS (TABS)
# ==========================================
aba1, aba2 = st.tabs(["⚔️ Distribuição de Equipamentos", "💰 Caixa da PT (Vendas e Zeny)"])

# ------------------------------------------
# ABA 1: PRIORIDADE E EQUIPAMENTOS
# ------------------------------------------
with aba1:
    st.info("Distribua itens que os membros vão EQUIPAR usando prioridade de 1 a 5 e sorteio para desempate.")
    col1, col2, col3 = st.columns(3)

    for i, (boss_name, info) in enumerate(mini_bosses.items()):
        target_col = [col1, col2, col3][i % 3]
        with target_col:
            st.markdown(f'<div class="boss-header"><img src="{info["foto_boss"]}" class="boss-photo" onerror="this.src=\'https://via.placeholder.com/32x32.png?text=?\'"><span class="boss-name">{boss_name}</span></div>', unsafe_allow_html=True)
            
            with st.expander(f"📦 Drops ({len(info['drops'])} itens)", expanded=False):
                for item in info["drops"]:
                    st.write(f"**{item}**")
                    interessados = st.multiselect("Quem quer?", membros, key=f"sel_eq_{boss_name}_{item}")
                    
                    if interessados:
                        cols_prio = st.columns(len(interessados))
                        prioridades = {}
                        for idx, p in enumerate(interessados):
                            with cols_prio[idx]:
                                n = st.number_input(f"Prio {p}", 1, 5, key=f"n_eq_{boss_name}_{item}_{p}")
                                prioridades[p] = n
                        
                        if st.button(f"🎲 Sortear", key=f"roll_eq_{boss_name}_{item}"):
                            sorteio = {p: random.randint(1, 100) for p in interessados}
                            st.session_state[f"last_roll_{boss_name}_{item}"] = sorteio
                        
                        if f"last_roll_{boss_name}_{item}" in st.session_state:
                            st.code(" | ".join([f"{k}: {v}" for k, v in st.session_state[f"last_roll_{boss_name}_{item}"].items()]))
                        
                        vencedor = st.selectbox("Confirmar ganhador:", interessados, key=f"win_eq_{boss_name}_{item}")
                        
                        if st.button(f"✅ Registrar na Planilha", key=f"reg_eq_{boss_name}_{item}", use_container_width=True):
                            novo_dado = pd.DataFrame([{
                                "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                                "Boss": boss_name, "Item": item, "Ganhador": vencedor
                            }])
                            updated_df = pd.concat([df_equipamentos, novo_dado], ignore_index=True) if not df_equipamentos.empty else novo_dado
                            conn.update(spreadsheet=URL_PLANILHA, worksheet="Equipamentos", data=updated_df)
                            
                            st.toast(f"Item registrado para {vencedor} na Nuvem!")
                            st.rerun()
                    st.divider()

    st.divider()
    st.subheader("📜 Histórico de Equipamentos Distribuídos (Nuvem)")
    if not df_equipamentos.empty:
        st.dataframe(df_equipamentos, use_container_width=True, hide_index=True)
        csv_hist = df_equipamentos.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Baixar Histórico (CSV)", csv_hist, "historico_equipamentos.csv", "text/csv")
    else:
        st.write("Nenhum equipamento distribuído ainda na planilha.")

# ------------------------------------------
# ABA 2: TESOURARIA (ZENY E CONTROLE DE STATUS)
# ------------------------------------------
with aba2:
    st.info("Registre drops para vender ou que ficaram com a PT. Dê um duplo-clique na tabela abaixo para alterar o Status e sincronize com a nuvem!")
    
    with st.container(border=True):
        st.subheader("📝 Registrar Novo Drop no Caixa")
        
        c1, c2 = st.columns(2)
        with c1:
            boss_venda = st.selectbox("Qual Boss?", lista_bosses, key="sel_boss_venda")
        with c2:
            itens_possiveis = mini_bosses[boss_venda]["drops"]
            item_venda = st.selectbox("Qual item dropou?", itens_possiveis, key="sel_item_venda")
        
        pt_presente = st.multiselect("Quem estava na PT no momento do kill?", membros, key="pt_venda")
        
        if st.button("💾 Salvar Drop na Planilha", type="primary"):
            if not pt_presente:
                st.error("Selecione pelo menos uma pessoa que estava presente na PT!")
            else:
                novo_drop = pd.DataFrame([{
                    "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Boss": boss_venda,
                    "Item": item_venda,
                    "Presentes": ", ".join(pt_presente),
                    "Partes": len(pt_presente),
                    "Status": "Aguardando Venda", 
                    "Detalhes/Valor": ""          
                }])
                
                updated_tes = pd.concat([df_tesouraria, novo_drop], ignore_index=True) if not df_tesouraria.empty else novo_drop
                conn.update(spreadsheet=URL_PLANILHA, worksheet="Tesouraria", data=updated_tes)
                
                st.success("Drop adicionado ao banco da PT na Nuvem!")
                st.rerun() 
    
    st.divider()
    st.subheader("💰 Inventário do Caixa (Edite dando duplo-clique)")
    
    if not df_tesouraria.empty:
        # Cria a tabela interativa (data_editor) com a nova linha num_rows="dynamic"
        edited_df = st.data_editor(
            df_tesouraria,
            use_container_width=True,
            hide_index=True,
            num_rows="dynamic", # LINHA ADICIONADA PARA PERMITIR EXCLUSÃO E INSERÇÃO MANUAL
            column_config={
                "Status": st.column_config.SelectboxColumn(
                    "Status do Item",
                    help="O que aconteceu com esse item?",
                    width="medium",
                    options=["Aguardando Venda", "Vendido", "Ficou com a PT"],
                    required=True
                ),
                "Detalhes/Valor": st.column_config.TextColumn(
                    "Detalhes / Valor",
                    help="Ex: Vendido por 10kk ou Ficou com Felippe",
                    width="large"
                )
            },
            disabled=["Data", "Boss", "Item", "Presentes", "Partes"],
            key="editor_tesouraria"
        )
        
        # Botão para salvar edições manuais ou exclusões feitas na tabela
        if st.button("☁️ Sincronizar Edições com a Planilha", type="primary"):
            conn.update(spreadsheet=URL_PLANILHA, worksheet="Tesouraria", data=edited_df)
            st.success("Planilha atualizada com sucesso!")
            st.rerun()
        
        csv_tesouraria = edited_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Baixar Relatório do Caixa (CSV)", csv_tesouraria, "caixa_pt_zeny.csv", "text/csv")
    else:
        st.write("O caixa está vazio na planilha. Vão farmar!")