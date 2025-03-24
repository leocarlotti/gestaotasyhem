import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pygsheets as pgs
from vega_datasets import data

crendencial = pgs.authorize(service_account_file="chave_google_sheets.json")
st.set_page_config(layout="wide")

#CONFIGURACOES GERAIS
tab1, tab2 = st.tabs(["PLANO DE AÇÃO", "GESTÃO DE RISCOS"])
url_planilha_gestao = "https://docs.google.com/spreadsheets/d/1wd3zPXnQRY4f2b_KwLr19HAttc-axLP-XrBRo9RMV-Q/edit?gid=0#gid=0"
planilha = crendencial.open_by_url(url_planilha_gestao)
aba = planilha.worksheet_by_title("dados")

df =  aba.get_as_df()
df_filtro = df

with st.sidebar:
    st.title("Gestão de Ações e Riscos")
    #distinct_agrupamento = df["AGRUPAMENTO"].sort_values().unique().tolist()
    #distinct_agrupamento.insert(0,"TODOS")
    #agrupamento_selected = st.selectbox("AGRUPAMENTO",distinct_agrupamento, index=0)
    #df_filtro = df
   
with tab1:
    containerKpis = st.container(border=True)
    containerGraf1 = st.container(border=True)
    containerGraf2 = st.container(border=True)
    
   
    
    #--- INCLUIR REGRAS DE FILTROS GERAIS ---#

    
    with containerKpis:
        st.markdown("<h4 style='text-align: center; color: white;'>PLANO DE AÇÂO - VISÃO GERAL HEM</h4>", unsafe_allow_html=True)
        df_filtro = df
        
        kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns([1,1,1,1,1])
        
        
        total_acoes = df_filtro.shape[0]
        #df_qtd_por_status = df_filtro.groupby("STATUS_ACAO")[["QTD"]].count().reset_index()
        #df_concluida = df_filtro[df_filtro['STATUS_ACAO'] == 'Concluída'].count()
        
        #st.write(df_filtro)
        df_qtd_concluida = df_filtro[df_filtro['STATUS_ACAO'] == 'Concluída']
        qtd_concluida = df_qtd_concluida.shape[0]
        #st.write(qtd_concluida)
        df_qtd_atrasado = df_filtro[df_filtro['STATUS_ACAO'] == 'Atrasada']
        qtd_atrasado = df_qtd_atrasado.shape[0]
        df_qtd_planejado = df_filtro[df_filtro['STATUS_ACAO'] == 'Planejada']
        qtd_planejado = df_qtd_planejado.shape[0]
        #df_qtd_Cancelado = df_filtro[df_filtro['STATUS_ACAO'] == 'Cancelada']
        #qtd_cancelado = df_qtd_Cancelado.shape[0]
        df_qtd_em_andamento = df_filtro[df_filtro['STATUS_ACAO'] == 'Em Andamento']
        qtd_em_andamento = df_qtd_em_andamento.shape[0]
        
        with kpi1: 
            st.metric("Total de Ações", total_acoes, "", border=True)
        with kpi2:
            st.metric("Ações Concluídas", df_qtd_concluida.shape[0], "", border=True)
        with kpi3: 
            st.metric("Ações Em Atraso", qtd_atrasado, "", border=True)
        with kpi4: 
            st.metric("Ações Planejadas", qtd_planejado, "", border=True)
        with kpi5:
            st.metric("Ações Em Andamento", qtd_em_andamento, "", border=True)
            
        
        coltreemap = st.columns(1)
        
        with st.expander("ANÁLISE GRÁFICA GERAL", expanded=True):
            col0_1, col0_2 = st.columns([1,1])   
            df_qtd_por_agrupamento_0 = df.groupby("AGRUPAMENTO")[["QTD"]].count().reset_index()
            df_qtd_por_agrupamento_0 = df_qtd_por_agrupamento_0.sort_values('AGRUPAMENTO')
            df_qtd_por_frente_0 = df.groupby("FRENTE")[["QTD"]].count().reset_index()
            df_qtd_por_frente_0 = df_qtd_por_frente_0.sort_values('FRENTE')
            
            fig_status_0_1 = px.bar(df_qtd_por_agrupamento_0, y="QTD", x="AGRUPAMENTO", title="QUANTITATIVO GERAL DE AÇÕES POR AGRUPAMENTO", text_auto=True,  color="AGRUPAMENTO", color_continuous_scale=px.colors.sequential.Rainbow)
           
            fig_status_0_1.update_traces(overwrite=True, marker={"opacity": 0.7})
            col0_1.plotly_chart(fig_status_0_1, use_container_width=True)
        
            df_qtd_por_status_geral = df.groupby("STATUS_ACAO")[["QTD"]].count().reset_index()
            
            #df_pie_status = []
            #df_pie_status["STATUS"] = {"Concluída","Atrasada","Planejada","Em Andamento"}
            #df_pie_status["PERCENTUAL"] = {percentual_concluida, percentual_atrasada, percentual_planejada, percentual_em_andamento}
            fig_status_0_2 = px.pie(df_qtd_por_status_geral, values='QTD', names='STATUS_ACAO', color='STATUS_ACAO', title="% POR STATUS DA AÇÃO",
             color_discrete_map={'Concluída':'green',
                                 'Atrasada':'red',
                                 'Planejada':'blue',
                                 'Em Andamento':'yellow'})
            fig_status_0_2.update_traces(textposition='inside', textinfo='percent+label')
            #fig_status_0_2.update_traces(overwrite=True, marker={"opacity": 0.4})
            col0_2.plotly_chart(fig_status_0_2, use_container_width=True)

            
            
    
    with containerGraf1:
        st.markdown("<h4 style='text-align: center; color: white;'>VISÃO DETALHADA POR AGRUPAMENTO</h4>", unsafe_allow_html=True)
        containerGraf1_filtro = st.container(border=True)
        col_filtroGraf1, col_filtroGraf2, col_filtroGraf3 = st.columns([1,1,1])
        #with containerGraf1_filtro:
        #    st.markdown("<h6 style='text-align: center; color: white;'>FILTROS</h6>", unsafe_allow_html=True)
        distinct_agrupamento = df["AGRUPAMENTO"].sort_values().unique().tolist()
        
        distinct_status = df["STATUS_ACAO"].sort_values().unique().tolist()
        distinct_status.insert(0,"TODOS")
        #distinct_agrupamento.insert(0,"TODOS")
        with col_filtroGraf1:
            agrupamento_selected = st.selectbox("Agrupamento:",distinct_agrupamento, index=0)
        
            
        #distinct_frente = df["AGRUPAMENTO"].sort_values().unique().tolist()
            
        df_filtro = df
        if agrupamento_selected:
            if agrupamento_selected == "TODOS":
                df_filtro = df.reset_index()
            if agrupamento_selected != "TODOS":
                df_filtro = df[df["AGRUPAMENTO"] == agrupamento_selected].reset_index()
                distinct_frente = df_filtro[df_filtro["AGRUPAMENTO"] == agrupamento_selected]["FRENTE"].sort_values().unique().tolist()
                distinct_frente.insert(0,"TODOS")
       
        with col_filtroGraf2:
            frente_selected = st.selectbox("Frente:", distinct_frente , index=0)
        with col_filtroGraf3:
            status_selected = st.selectbox("Status:",distinct_status, index=0)
            
        if frente_selected:
            if frente_selected == "TODOS":
                df_filtro = df_filtro
            if frente_selected != "TODOS":
                df_filtro = df_filtro[df_filtro["FRENTE"] == frente_selected].reset_index()
        if status_selected:
            if status_selected == "TODOS":
                df_filtro = df_filtro
            if status_selected != "TODOS":
                df_filtro = df_filtro[df_filtro["STATUS_ACAO"] == status_selected]
               
            
        with st.expander("ANÁLISE GRÁFICA POR AGRUPAMENTO", expanded=False):    
            col1_1, col1_2 = st.columns([1,1]) 
            col1_3, col1_4 = st.columns([100,1]) 
            df_qtd_por_agrupamento = df_filtro.groupby("AGRUPAMENTO")[["QTD"]].count().reset_index()
            df_qtd_por_agrupamento = df_qtd_por_agrupamento.sort_values('AGRUPAMENTO')
            df_qtd_por_frente = df_filtro.groupby(["FRENTE","STATUS_ACAO"])[["QTD"]].count().reset_index()
            df_qtd_por_frente = df_qtd_por_frente.sort_values('FRENTE')
            
            df_qtd_por_status = df_filtro.groupby("STATUS_ACAO")[["QTD"]].count().reset_index()
            
            #df_pie_status = []
            #df_pie_status["STATUS"] = {"Concluída","Atrasada","Planejada","Em Andamento"}
            #df_pie_status["PERCENTUAL"] = {percentual_concluida, percentual_atrasada, percentual_planejada, percentual_em_andamento}
            fig_status_1 = px.pie(df_qtd_por_status, values='QTD', names='STATUS_ACAO', color='STATUS_ACAO', title="% POR STATUS DA AÇÃO",
             color_discrete_map={'Concluída':'green',
                                 'Atrasada':'red',
                                 'Planejada':'blue',
                                 'Em Andamento':'yellow'})
            fig_status_1.update_traces(textposition='inside', textinfo='percent+label')
            col1_1.plotly_chart(fig_status_1, use_container_width=True)
            

            fig_status_2 = px.bar(title="QUANTITATIVO DE AÇÕES POR FRENTE", y=df_qtd_por_frente["QTD"], x=df_qtd_por_frente["FRENTE"], text_auto=True,  color=df_qtd_por_frente["STATUS_ACAO"], color_discrete_map={'Concluída':'green',
                                 'Atrasada':'red',
                                 'Planejada':'blue',
                                 'Em Andamento':'yellow'})
            #fig_status_2.add_bar(y=df_qtd_por_frente["QTD"], x=df_qtd_por_frente["FRENTE"], color=df_qtd_por_frente["STATUS_ACAO"], name="Quantidade", secondary_y=False)
            fig_status_2.update_traces(overwrite=True, marker={"opacity": 0.7})
            col1_2.plotly_chart(fig_status_2, use_container_width=True)
            
            df_qtd_por_responsavel = df_filtro.groupby(["RESPONSAVEL","STATUS_ACAO"])[["QTD"]].count().reset_index()
            df_qtd_por_responsavel = df_qtd_por_responsavel.sort_values('RESPONSAVEL')
            
            fig_status_3 = px.bar(title="QUANTITATIVO DE AÇÕES POR RESPONSÁVEL", y=df_qtd_por_responsavel["QTD"], x=df_qtd_por_responsavel["RESPONSAVEL"], text_auto=True, color=df_qtd_por_responsavel["STATUS_ACAO"], color_continuous_scale=[("Concluída", "green"), ("Atrasada", "red"), ("Em Andamento", "yellow"), ("Planejada", "blue")])
            #fig_status_2.add_bar(y=df_qtd_por_frente["QTD"], x=df_qtd_por_frente["FRENTE"], color=df_qtd_por_frente["STATUS_ACAO"], name="Quantidade", secondary_y=False)
            fig_status_3.update_traces(overwrite=True, marker={"opacity": 0.7})
            col1_3.plotly_chart(fig_status_3, use_container_width=True)

        with st.expander("Dados"):
            st.dataframe(df_filtro, use_container_width=True)
            #st.dataframe(df_qtd_por_frente, use_container_width=True)
            
    
with tab2:
    st.title("GESTÃO DE RISCOS - PROJETO TASY HEM")