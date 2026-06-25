import pandas as pd
import json
import numpy as np
import traceback

def safe_col(cols, keywords, default):
    found = [c for c in cols if any(kw.lower() in str(c).lower() for kw in keywords)]
    return found[0] if found else default

def filter_campaign(df):
    for c in df.columns:
        if 'campanha' in str(c).lower() or 'conjunto' in str(c).lower():
            df = df[~df[c].astype(str).str.contains('2.0', case=False, na=False)]
    return df

def process_data():
    # Read Dia a Dia
    df_dia = pd.read_excel('data/DADOS-DIA-A-DIA.xlsx', skiprows=2)
    df_dia = filter_campaign(df_dia)
    
    df_dia['Dia_str'] = df_dia['Dia'].astype(str)
    df_dia_dates = df_dia[df_dia['Dia_str'].str.match(r'\d{4}-\d{2}-\d{2}', na=False)].copy()
    df_dia_dates['Dia'] = pd.to_datetime(df_dia_dates['Dia'])
    
    cols = df_dia_dates.columns
    col_investimento = safe_col(cols, ['Valor usado'], 'Investimento')
    col_faturamento = safe_col(cols, ['Valor dos resultados', 'Valor de convers'], 'Faturamento')
    
    vendas_cols = [c for c in cols if 'Resultados' in str(c) and 'Tipo' not in str(c) and 'ROAS' not in str(c) and 'Custo' not in str(c) and c != 'Resultados (iniciais)']
    col_vendas = vendas_cols[0] if vendas_cols else 'Resultados'
    
    col_impressoes = safe_col(cols, ['Impress'], 'Impressoes')
    col_cliques = safe_col(cols, ['Cliques'], 'Cliques')
    
    df_dia_all = df_dia[df_dia['Dia'].astype(str).str.contains('All|Total', case=False, na=False)].copy()
    if df_dia_all.empty:
        df_dia_all = df_dia_dates
        
    for c in [col_investimento, col_faturamento, col_vendas, col_impressoes, col_cliques]:
        if c not in df_dia_all.columns: df_dia_all[c] = 0
        df_dia_all[c] = pd.to_numeric(df_dia_all[c], errors='coerce').fillna(0)
        if c not in df_dia_dates.columns: df_dia_dates[c] = 0
        df_dia_dates[c] = pd.to_numeric(df_dia_dates[c], errors='coerce').fillna(0)
        
    global_metrics = {
        'Investimento': float(df_dia_all[col_investimento].sum()),
        'Faturamento': float(df_dia_all[col_faturamento].sum()),
        'Vendas': int(df_dia_all[col_vendas].sum()),
        'Impressoes': int(df_dia_all[col_impressoes].sum()),
        'Cliques': int(df_dia_all[col_cliques].sum()),
    }
    
    if global_metrics['Investimento'] > 0:
        global_metrics['ROAS'] = round(global_metrics['Faturamento'] / global_metrics['Investimento'], 2)
        global_metrics['CPA'] = round(global_metrics['Investimento'] / global_metrics['Vendas'], 2) if global_metrics['Vendas'] > 0 else 0
        global_metrics['CPC'] = round(global_metrics['Investimento'] / global_metrics['Cliques'], 2) if global_metrics['Cliques'] > 0 else 0
    else:
        global_metrics['ROAS'] = 0
        global_metrics['CPA'] = 0
        global_metrics['CPC'] = 0

    if global_metrics['Impressoes'] > 0:
        global_metrics['CTR'] = round((global_metrics['Cliques'] / global_metrics['Impressoes']) * 100, 2)
    else:
        global_metrics['CTR'] = 0
        
    daily_data = []
    for date_val, group in df_dia_dates.groupby(df_dia_dates['Dia'].dt.date):
        inv = float(group[col_investimento].sum())
        fat = float(group[col_faturamento].sum())
        ven = int(group[col_vendas].sum())
        imp = int(group[col_impressoes].sum())
        cli = int(group[col_cliques].sum())
        
        roas = round(fat / inv, 2) if inv > 0 else 0
        cpa = round(inv / ven, 2) if ven > 0 else 0
        cpc = round(inv / cli, 2) if cli > 0 else 0
        ctr = round((cli / imp) * 100, 2) if imp > 0 else 0
        
        daily_data.append({
            'Data': date_val.strftime('%Y-%m-%d'),
            'Investimento': inv,
            'Faturamento': fat,
            'Vendas': ven,
            'Impressoes': imp,
            'Cliques': cli,
            'ROAS': roas,
            'CPA': cpa,
            'CPC': cpc,
            'CTR': ctr
        })

    # Criativos Diário e Top 5
    try:
        try:
            df_criativo_diario = pd.read_excel('data/CRIATIVO-DIAADIA.xlsx')
            if 'Dia' not in df_criativo_diario.columns and 'Nome da campanha' not in df_criativo_diario.columns:
                df_criativo_diario = pd.read_excel('data/CRIATIVO-DIAADIA.xlsx', skiprows=2)
        except:
            df_criativo_diario = pd.read_excel('data/CRIATIVO-DIAADIA.xlsx', skiprows=2)
            
        df_criativo_diario = filter_campaign(df_criativo_diario)
        
        criativo_diario_cols = df_criativo_diario.columns
        col_cria_name = [c for c in criativo_diario_cols if 'ncios' in str(c).lower() and 'conjunto' not in str(c).lower()]
        col_cria_name = col_cria_name[0] if col_cria_name else 'Anúncios'
        col_c_inv = safe_col(criativo_diario_cols, ['Valor usado'], 'Valor usado (BRL)')
        col_c_fat = safe_col(criativo_diario_cols, ['Valor dos resultados', 'Valor de convers'], 'Valor dos resultados')
        
        c_ven = [c for c in criativo_diario_cols if 'Resultados' in str(c) and 'Tipo' not in str(c) and 'ROAS' not in str(c) and 'Custo' not in str(c) and c != 'Resultados (iniciais)']
        col_c_ven = c_ven[0] if c_ven else 'Resultados'
        
        if col_c_fat not in df_criativo_diario.columns: df_criativo_diario[col_c_fat] = 0
        if col_c_inv not in df_criativo_diario.columns: df_criativo_diario[col_c_inv] = 0
        if col_c_ven not in df_criativo_diario.columns: df_criativo_diario[col_c_ven] = 0
        if col_cria_name not in df_criativo_diario.columns: df_criativo_diario[col_cria_name] = 'Desconhecido'
        
        df_criativo_diario = df_criativo_diario[~df_criativo_diario[col_cria_name].astype(str).str.contains('All|Total', case=False)]
        
        df_criativo_diario['Dia_str'] = df_criativo_diario['Dia'].astype(str)
        df_criativo_diario = df_criativo_diario[df_criativo_diario['Dia_str'].str.match(r'\d{4}-\d{2}-\d{2}', na=False)].copy()
        df_criativo_diario['Dia'] = pd.to_datetime(df_criativo_diario['Dia'])
        
        for c in [col_c_inv, col_c_fat, col_c_ven]:
            df_criativo_diario[c] = pd.to_numeric(df_criativo_diario[c], errors='coerce').fillna(0)
            
        cria_agg = df_criativo_diario.groupby(['Dia', col_cria_name])[[col_c_inv, col_c_fat, col_c_ven]].sum().reset_index()
        criativos_diario = []
        for _, row in cria_agg.iterrows():
            criativos_diario.append({
                'Data': row['Dia'].strftime('%Y-%m-%d'),
                'Nome': str(row[col_cria_name]),
                'Investimento': float(row[col_c_inv]),
                'Faturamento': float(row[col_c_fat]),
                'Vendas': int(row[col_c_ven])
            })
            
        cri_total = df_criativo_diario.groupby(col_cria_name).agg({
            col_c_fat: 'sum',
            col_c_ven: 'sum',
            col_c_inv: 'sum'
        }).reset_index()
        
        cri_total['ROAS'] = np.where(cri_total[col_c_inv] > 0, cri_total[col_c_fat] / cri_total[col_c_inv], 0)
        if cri_total[col_c_fat].sum() > 0:
            top_5 = cri_total.sort_values(by=col_c_fat, ascending=False).head(5)
        else:
            top_5 = cri_total.sort_values(by=col_c_ven, ascending=False).head(5)
            
        top_criativos = []
        for _, row in top_5.iterrows():
            top_criativos.append({
                'Nome': str(row[col_cria_name]),
                'Faturamento': float(row[col_c_fat]),
                'Vendas': int(row[col_c_ven]),
                'ROAS': round(float(row['ROAS']), 2)
            })
    except Exception as e:
        print("Erro ao processar Criativos Diario:", traceback.format_exc())
        criativos_diario = []
        top_criativos = []

    # Idade
    try:
        df_idade = pd.read_excel('data/DIAS E IDADE.xlsx', skiprows=2)
        df_idade = filter_campaign(df_idade)
        idade_cols = df_idade.columns
        i_ven = [c for c in idade_cols if 'Resultados' in str(c) and 'Tipo' not in str(c) and 'ROAS' not in str(c) and 'Custo' not in str(c) and c != 'Resultados (iniciais)']
        col_vendas_idade = i_ven[0] if i_ven else 'Resultados'
        
        if 'Idade' in df_idade.columns:
            df_idade['Idade'] = df_idade['Idade'].ffill()
            df_idade = df_idade[df_idade['Idade'].notna()]
            df_idade = df_idade[~df_idade['Idade'].astype(str).str.contains('All|Total', case=False)]
            df_idade['Dia_str'] = df_idade['Dia'].astype(str)
            df_idade = df_idade[df_idade['Dia_str'].str.match(r'\d{4}-\d{2}-\d{2}', na=False)].copy()
            df_idade['Dia'] = pd.to_datetime(df_idade['Dia'])
            if col_vendas_idade not in df_idade.columns: df_idade[col_vendas_idade] = 0
            df_idade[col_vendas_idade] = pd.to_numeric(df_idade[col_vendas_idade], errors='coerce').fillna(0)
            
            idade_agg = df_idade.groupby(['Dia', 'Idade'])[col_vendas_idade].sum().reset_index()
            idade_diario = []
            for _, row in idade_agg.iterrows():
                idade_diario.append({
                    'Data': row['Dia'].strftime('%Y-%m-%d'),
                    'Idade': str(row['Idade']),
                    'Vendas': int(row[col_vendas_idade])
                })
        else:
            idade_diario = []
    except Exception as e:
        print("Erro ao processar Idade:", traceback.format_exc())
        idade_diario = []

    # Posicionamento
    try:
        df_pos = pd.read_excel('data/POSICIONAMENTOS-COM-OS-DIAS.xlsx', skiprows=2)
        df_pos = filter_campaign(df_pos)
        pos_cols = df_pos.columns
        p_ven = [c for c in pos_cols if 'Resultados' in str(c) and 'Tipo' not in str(c) and 'ROAS' not in str(c) and 'Custo' not in str(c) and c != 'Resultados (iniciais)']
        col_vendas_pos = p_ven[0] if p_ven else 'Resultados'
        
        if 'Posicionamento' in df_pos.columns:
            df_pos['Dia'] = df_pos['Dia'].ffill()
            df_pos = df_pos[df_pos['Posicionamento'].notna()]
            df_pos = df_pos[~df_pos['Posicionamento'].astype(str).str.contains('All|Total', case=False)]
            df_pos['Dia_str'] = df_pos['Dia'].astype(str)
            df_pos = df_pos[df_pos['Dia_str'].str.match(r'\d{4}-\d{2}-\d{2}', na=False)].copy()
            df_pos['Dia'] = pd.to_datetime(df_pos['Dia'])
            if col_vendas_pos not in df_pos.columns: df_pos[col_vendas_pos] = 0
            df_pos[col_vendas_pos] = pd.to_numeric(df_pos[col_vendas_pos], errors='coerce').fillna(0)
            
            pos_agg = df_pos.groupby(['Dia', 'Posicionamento'])[col_vendas_pos].sum().reset_index()
            pos_diario = []
            for _, row in pos_agg.iterrows():
                pos_diario.append({
                    'Data': row['Dia'].strftime('%Y-%m-%d'),
                    'Posicionamento': str(row['Posicionamento']),
                    'Vendas': int(row[col_vendas_pos])
                })
        else:
            pos_diario = []
    except Exception as e:
        print("Erro ao processar Posicionamentos:", traceback.format_exc())
        pos_diario = []
        
    final_data = {
        'Global': global_metrics,
        'Diario': daily_data,
        'IdadeDiario': idade_diario,
        'PosicionamentoDiario': pos_diario,
        'CriativoDiario': criativos_diario,
        'TopCriativos': top_criativos
    }
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
        
    print("Dados processados com sucesso. JSON gerado!")

if __name__ == '__main__':
    process_data()
