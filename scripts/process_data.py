import pandas as pd
import json
import numpy as np

def process_data():
    # Read Dia a Dia
    df_dia = pd.read_excel('data/DADOS-DIA-A-DIA.xlsx', skiprows=2)
    
    # Filter rows with actual dates
    df_dia['Dia_str'] = df_dia['Dia'].astype(str)
    df_dia_dates = df_dia[df_dia['Dia_str'].str.match(r'\d{4}-\d{2}-\d{2}', na=False)].copy()
    df_dia_dates['Dia'] = pd.to_datetime(df_dia_dates['Dia'])
    
    # Identify relevant columns
    cols = df_dia_dates.columns
    col_investimento = [c for c in cols if 'Valor usado' in str(c)][0]
    col_faturamento = [c for c in cols if 'Valor dos resultados' in str(c)][0]
    
    # Find exact 'Resultados' column for Sales
    vendas_cols = [c for c in cols if 'Resultados' in str(c) and 'Tipo' not in str(c) and 'ROAS' not in str(c) and 'Custo' not in str(c) and c != 'Resultados (iniciais)']
    col_vendas = vendas_cols[0] if vendas_cols else 'Resultados'
    
    col_impressoes = [c for c in cols if 'Impress' in str(c)][0]
    col_cliques = [c for c in cols if 'Cliques' in str(c)][0]
    
    for c in [col_investimento, col_faturamento, col_vendas, col_impressoes, col_cliques]:
        df_dia_dates[c] = pd.to_numeric(df_dia_dates[c], errors='coerce').fillna(0)
        
    global_metrics = {
        'Investimento': float(df_dia_dates[col_investimento].sum()),
        'Faturamento': float(df_dia_dates[col_faturamento].sum()),
        'Vendas': int(df_dia_dates[col_vendas].sum()),
        'Impressoes': int(df_dia_dates[col_impressoes].sum()),
        'Cliques': int(df_dia_dates[col_cliques].sum()),
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
        
    # Group by Day
    daily_data = []
    for date_val, group in df_dia_dates.groupby(df_dia_dates['Dia'].dt.date):
        inv = float(group[col_investimento].sum())
        fat = float(group[col_faturamento].sum())
        ven = int(group[col_vendas].sum())
        imp = int(group[col_impressoes].sum())
        cli = int(group[col_cliques].sum())
        
        # Calculate daily proportions (if needed by frontend, though frontend will usually recalculate for sum)
        roas = round(fat / inv, 2) if inv > 0 else 0
        cpa = round(inv / ven, 2) if ven > 0 else 0
        cpc = round(inv / cli, 2) if cli > 0 else 0
        ctr = round((cli / imp) * 100, 2) if imp > 0 else 0
        
        date_str = date_val.strftime('%Y-%m-%d')
        daily_data.append({
            'Data': date_str,
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

    df_cri = pd.read_excel('data/CRIATIVO.xlsx')
    c_cols = df_cri.columns
    c_nome = [c for c in c_cols if 'ncios' in str(c) and 'conjunto' not in str(c)]
    if not c_nome:
        # Fallback if specific chars are parsed differently
        c_nome = [c for c in c_cols if 'ncios' in str(c)]
    c_nome = c_nome[0] if c_nome else c_cols[1] # fallback to second col usually
        
    c_fat = [c for c in c_cols if 'Valor dos resultados' in str(c)][0]
    
    vendas_cols_cri = [c for c in c_cols if 'Resultados' in str(c) and 'Tipo' not in str(c) and 'ROAS' not in str(c) and 'Custo' not in str(c) and c != 'Resultados (iniciais)']
    c_ven = vendas_cols_cri[0] if vendas_cols_cri else 'Resultados'
    
    c_inv = [c for c in c_cols if 'Valor usado' in str(c)][0]
    
    for c in [c_fat, c_ven, c_inv]:
         df_cri[c] = pd.to_numeric(df_cri[c], errors='coerce').fillna(0)
         
    # Filter valid creatives and group by name
    df_cri = df_cri[df_cri[c_nome].notna()]
    df_cri = df_cri[~df_cri[c_nome].astype(str).str.contains('All|Total', case=False)]
    
    cri_agg = df_cri.groupby(c_nome).agg({
        c_fat: 'sum',
        c_ven: 'sum',
        c_inv: 'sum'
    }).reset_index()
    
    cri_agg['ROAS'] = np.where(cri_agg[c_inv] > 0, cri_agg[c_fat] / cri_agg[c_inv], 0)
    
    top_5 = cri_agg.sort_values(by=c_fat, ascending=False).head(5)
    
    top_criativos = []
    for _, row in top_5.iterrows():
        top_criativos.append({
            'Nome': str(row[c_nome]),
            'Faturamento': float(row[c_fat]),
            'Vendas': int(row[c_ven]),
            'ROAS': round(float(row['ROAS']), 2)
        })
        
    # Process Idade Daily
    df_idade = pd.read_excel('data/DIAS E IDADE.xlsx', skiprows=2)
    idade_cols = df_idade.columns
    i_ven = [c for c in idade_cols if 'Resultados' in str(c) and 'Tipo' not in str(c) and 'ROAS' not in str(c) and 'Custo' not in str(c) and c != 'Resultados (iniciais)']
    col_vendas_idade = i_ven[0] if i_ven else 'Resultados'
    
    # Preencher hierarquia do Meta (ffill)
    df_idade['Idade'] = df_idade['Idade'].ffill()
    
    df_idade = df_idade[df_idade['Idade'].notna()]
    df_idade = df_idade[~df_idade['Idade'].astype(str).str.contains('All|Total', case=False)]
    df_idade['Dia_str'] = df_idade['Dia'].astype(str)
    df_idade = df_idade[df_idade['Dia_str'].str.match(r'\d{4}-\d{2}-\d{2}', na=False)].copy()
    
    df_idade['Dia'] = pd.to_datetime(df_idade['Dia'])
    df_idade[col_vendas_idade] = pd.to_numeric(df_idade[col_vendas_idade], errors='coerce').fillna(0)
    
    idade_agg = df_idade.groupby(['Dia', 'Idade'])[col_vendas_idade].sum().reset_index()
    idade_diario = []
    for _, row in idade_agg.iterrows():
        idade_diario.append({
            'Data': row['Dia'].strftime('%Y-%m-%d'),
            'Idade': str(row['Idade']),
            'Vendas': int(row[col_vendas_idade])
        })

    # Process Posicionamento Daily
    try:
        df_pos = pd.read_excel('data/POSICIONAMENTOS-COM-OS-DIAS.xlsx', skiprows=2)
        pos_cols = df_pos.columns
        p_ven = [c for c in pos_cols if 'Resultados' in str(c) and 'Tipo' not in str(c) and 'ROAS' not in str(c) and 'Custo' not in str(c) and c != 'Resultados (iniciais)']
        col_vendas_pos = p_ven[0] if p_ven else 'Resultados'
        
        # Preencher hierarquia do Meta (ffill)
        df_pos['Dia'] = df_pos['Dia'].ffill()
        
        df_pos = df_pos[df_pos['Posicionamento'].notna()]
        df_pos = df_pos[~df_pos['Posicionamento'].astype(str).str.contains('All|Total', case=False)]
        df_pos['Dia_str'] = df_pos['Dia'].astype(str)
        df_pos = df_pos[df_pos['Dia_str'].str.match(r'\d{4}-\d{2}-\d{2}', na=False)].copy()
        
        df_pos['Dia'] = pd.to_datetime(df_pos['Dia'])
        df_pos[col_vendas_pos] = pd.to_numeric(df_pos[col_vendas_pos], errors='coerce').fillna(0)
        
        pos_agg = df_pos.groupby(['Dia', 'Posicionamento'])[col_vendas_pos].sum().reset_index()
        pos_diario = []
        for _, row in pos_agg.iterrows():
            pos_diario.append({
                'Data': row['Dia'].strftime('%Y-%m-%d'),
                'Posicionamento': str(row['Posicionamento']),
                'Vendas': int(row[col_vendas_pos])
            })
    except Exception as e:
        print("Erro ao processar Posicionamentos:", e)
        pos_diario = []
        
    # Process Criativo Daily
    try:
        df_criativo_diario = pd.read_excel('data/CRIATIVO-DIAADIA.xlsx')
        criativo_diario_cols = df_criativo_diario.columns
        
        col_cria = [c for c in criativo_diario_cols if 'Anúncio' in str(c) or 'Anuncio' in str(c) or 'Anncio' in str(c)]
        col_cria_name = col_cria[0] if col_cria else 'Anúncios'
        
        c_inv = [c for c in criativo_diario_cols if 'Valor usado' in str(c)]
        col_c_inv = c_inv[0] if c_inv else 'Valor usado (BRL)'
        
        c_fat = [c for c in criativo_diario_cols if 'Valor dos resultados' in str(c)]
        col_c_fat = c_fat[0] if c_fat else 'Valor dos resultados'
        
        c_ven = [c for c in criativo_diario_cols if 'Resultados' in str(c) and 'Tipo' not in str(c) and 'ROAS' not in str(c) and 'Custo' not in str(c) and c != 'Resultados (iniciais)']
        col_c_ven = c_ven[0] if c_ven else 'Resultados'
        
        df_criativo_diario = df_criativo_diario[~df_criativo_diario[col_cria_name].astype(str).str.contains('All|Total', case=False)]
        df_criativo_diario['Dia_str'] = df_criativo_diario['Dia'].astype(str)
        df_criativo_diario = df_criativo_diario[df_criativo_diario['Dia_str'].str.match(r'\d{4}-\d{2}-\d{2}', na=False)].copy()
        
        df_criativo_diario['Dia'] = pd.to_datetime(df_criativo_diario['Dia'])
        df_criativo_diario[col_c_inv] = pd.to_numeric(df_criativo_diario[col_c_inv], errors='coerce').fillna(0)
        df_criativo_diario[col_c_fat] = pd.to_numeric(df_criativo_diario[col_c_fat], errors='coerce').fillna(0)
        df_criativo_diario[col_c_ven] = pd.to_numeric(df_criativo_diario[col_c_ven], errors='coerce').fillna(0)
        
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
    except Exception as e:
        print("Erro ao processar Criativos Diario:", e)
        criativos_diario = []
        
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
