import streamlit as st
import pandas as pd
import requests
import json

# Page Config
st.set_page_config(
    page_title="Passos Mágicos - Datathon",
    page_icon="🎓",
    layout="wide"
)

# Title and Intro
st.title("🎓 Passos Mágicos - Predição de Defasagem")
st.markdown("""
Esta interface permite explorar os dados dos estudantes e realizar simulações de risco de defasagem escolar 
utilizando o modelo de Machine Learning treinado.
""")

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Explorador de Dados", "🚀 Simulador de Predição", "📈 Monitoramento"])

# --- Tab 1: Data Explorer ---
with tab1:
    st.header("Base de Dados PEDE 2024")
    
    @st.cache_data
    def load_data():
        try:
            df = pd.read_excel("data/BASE DE DADOS PEDE 2024 - DATATHON.xlsx")
            return df
        except Exception as e:
            st.error(f"Erro ao carregar dados: {e}")
            return None

    df = load_data()
    
    if df is not None:
        # Search Filter
        search_term = st.text_input("🔍 Pesquisar por Nome/ID (se houver) ou Fase:")
        
        if search_term:
            # Simple string match across specific columns
            mask = df.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)
            df_display = df[mask]
        else:
            df_display = df
            
        st.dataframe(df_display, use_container_width=True)
        st.caption(f"Total de registros: {len(df_display)}")

# --- Tab 2: Prediction Simulator ---
with tab2:
    st.header("Simulador de Risco")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Indicadores Pessoais")
        iaa = st.slider("IAA (Autoavaliação)", 0.0, 10.0, 7.0)
        ieg = st.slider("IEG (Engajamento)", 0.0, 10.0, 7.0)
        ips = st.slider("IPS (Psicossocial)", 0.0, 10.0, 7.0)
        ida = st.slider("IDA (Aprendizagem)", 0.0, 10.0, 7.0)
        
    with col2:
        st.subheader("Desempenho Acadêmico")
        portug = st.number_input("Nota Português", 0.0, 10.0, 7.0)
        matem = st.number_input("Nota Matemática", 0.0, 10.0, 7.0)
        ingles = st.number_input("Nota Inglês", 0.0, 10.0, 7.0)
        ipv = st.slider("IPV (Ponto de Virada)", 0.0, 10.0, 7.0)
        ian = st.slider("IAN (Adequação Nível)", 0.0, 10.0, 7.0)

    with col3:
        st.subheader("Contexto")
        fase = st.selectbox("Fase Ideal", ["Fase 1", "Fase 2", "Fase 3", "Fase 4", "Outra"])
        dest_ieg = st.selectbox("Destaque IEG", ["Seu destaque", "Ponto de melhoria", "Não", "Outro"])
        dest_ida = st.selectbox("Destaque IDA", ["Seu destaque", "Ponto de melhoria", "Não", "Outro"])
        dest_ipv = st.selectbox("Destaque IPV", ["Seu destaque", "Ponto de melhoria", "Não", "Outro"])

    if st.button("🔮 Realizar Predição", type="primary"):
        # Payload construction
        payload = {
            "IAA": iaa, "IEG": ieg, "IPS": ips, "IDA": ida,
            "Matem": matem, "Portug": portug, "Inglês": ingles,
            "IPV": ipv, "IAN": ian,
            "Fase_ideal": fase,
            "Destaque_IEG": dest_ieg,
            "Destaque_IDA": dest_ida,
            "Destaque_IPV": dest_ipv
        }
        
        try:
            # Call API
            api_url = "http://127.0.0.1:8000/predict"
            with st.spinner("Consultando modelo..."):
                response = requests.post(api_url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                prediction = result['prediction']
                confidence = result['confidence']
                
                st.success("Predição Concluída!")
                
                # Display Result
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    st.metric("Resultado (Defas)", prediction)
                with res_col2:
                    st.metric("Confiança do Modelo", f"{confidence:.1%}")
                
                if str(prediction) == '0':
                    st.success("🎉 O aluno está **On Track** (Sem risco aparente).")
                elif int(str(prediction)) < 0:
                    st.info("🎓 O aluno apresenta indicadores de **Avanço/Outro nível**.")
                else:
                    st.warning("⚠️ **Atenção:** Indicativos de Defasagem Escolar.")
                    
            else:
                st.error(f"Erro na API: {response.status_code} - {response.text}")
                
        except Exception as e:
            st.error(f"Falha na conexão com a API. Verifique se o backend está rodando. Erro: {e}")

# --- Tab 3: Monitoring ---
with tab3:
    st.header("📈 Monitoramento de Drift (Real-Time)")
    
    log_file = "logs/predictions.jsonl"
    
    try:
        data = []
        with open(log_file, 'r') as f:
            for line in f:
                data.append(json.loads(line))
                
        if data:
            df_logs = pd.json_normalize(data)
            df_logs['timestamp'] = pd.to_datetime(df_logs['timestamp'])
            
            st.metric("Total de Predições", len(df_logs))
            
            # Layout
            col_m1, col_m2 = st.columns(2)
            
            with col_m1:
                st.subheader("Distribuição de Predições")
                pred_counts = df_logs['output.prediction'].value_counts()
                st.bar_chart(pred_counts)
                
            with col_m2:
                st.subheader("Confiança Média ao Longo do Tempo")
                if 'timestamp' in df_logs.columns and 'output.confidence' in df_logs.columns:
                    st.line_chart(df_logs.set_index('timestamp')['output.confidence'])
            
            # Input Drift Table
            st.subheader("Estatísticas de Input (Drift)")
            input_cols = [c for c in df_logs.columns if 'inputs.' in c]
            if input_cols:
                st.dataframe(df_logs[input_cols].describe().T)
                
        else:
            st.warning("O arquivo de logs está vazio.")
            
    except FileNotFoundError:
        st.warning("Nenhum log encontrado. Realize algumas predições primeiro!")
    except Exception as e:
        st.error(f"Erro ao ler logs: {e}")
