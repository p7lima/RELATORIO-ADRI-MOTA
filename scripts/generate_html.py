import json
import os

def generate_html():
    if not os.path.exists('data.json'):
        print("data.json não encontrado. Execute process_data.py primeiro.")
        return
        
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    html_template = f"""<!DOCTYPE html>
<html lang="pt-BR" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Premium | Adri Mota Semijoias</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --gold-primary: #D4AF37;
            --gold-light: #F3E5AB;
            --rosegold: #B76E79;
        }}
        body {{
            font-family: 'Outfit', sans-serif;
            background-color: #050505;
            background-image: 
                radial-gradient(circle at 15% 50%, rgba(212, 175, 55, 0.04), transparent 25%),
                radial-gradient(circle at 85% 30%, rgba(183, 110, 121, 0.04), transparent 25%);
            color: #f8fafc;
            overflow-x: hidden;
        }}
        .font-serif {{
            font-family: 'Playfair Display', serif;
        }}
        .glass {{
            background: linear-gradient(135deg, rgba(30, 30, 30, 0.6) 0%, rgba(15, 15, 15, 0.8) 100%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.5);
        }}
        .glass:hover {{
            border: 1px solid rgba(212, 175, 55, 0.2);
            box-shadow: 0 8px 32px 0 rgba(212, 175, 55, 0.05), inset 0 1px 0 rgba(255, 255, 255, 0.1);
            transform: translateY(-2px);
        }}
        .text-gradient-gold {{
            background: linear-gradient(to right, #F3E5AB, #D4AF37);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .text-gradient-rose {{
            background: linear-gradient(to right, #F7E7CE, #B76E79);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        select {{
            background-color: rgba(15, 15, 15, 0.8) !important;
            background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%23D4AF37' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
            background-position: right 1rem center;
            background-repeat: no-repeat;
            background-size: 1.5em 1.5em;
            padding-right: 3rem;
            -webkit-appearance: none;
            -moz-appearance: none;
            appearance: none;
        }}
        select option {{
            background-color: #0f0f0f;
            color: #D4AF37;
        }}
        
        .fade-in {{
            animation: fadeIn 0.8s ease-out forwards;
            opacity: 0;
            transform: translateY(10px);
        }}
        @keyframes fadeIn {{
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .delay-1 {{ animation-delay: 0.1s; }}
        .delay-2 {{ animation-delay: 0.2s; }}
        .delay-3 {{ animation-delay: 0.3s; }}
        
        .orb {{
            position: absolute;
            border-radius: 50%;
            z-index: -1;
            opacity: 0.3;
        }}
        .orb-1 {{ width: 300px; height: 300px; background: radial-gradient(circle, rgba(212, 175, 55, 0.4) 0%, rgba(212, 175, 55, 0) 70%); top: -50px; left: -50px; }}
        .orb-2 {{ width: 400px; height: 400px; background: radial-gradient(circle, rgba(183, 110, 121, 0.3) 0%, rgba(183, 110, 121, 0) 70%); bottom: -50px; right: -50px; }}
    </style>
</head>
<body class="min-h-screen p-4 md:p-8 relative">
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    
    <div class="max-w-7xl mx-auto relative z-10">
        <!-- Header -->
        <header class="flex flex-col md:flex-row justify-between items-center mb-12 pb-6 border-b border-white/5 fade-in">
            <div class="flex items-center gap-4">
                <div class="w-12 h-12 rounded-full border border-[#D4AF37]/30 flex items-center justify-center bg-[#D4AF37]/5">
                    <svg class="w-6 h-6 text-[#D4AF37]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" /></svg>
                </div>
                <div>
                    <h1 class="text-4xl md:text-5xl font-serif text-gradient-gold font-bold tracking-wide">Adri Mota <span class="text-white/40 text-3xl font-sans font-light">| Semijoias</span></h1>
                    <p class="text-white/50 mt-1 text-xs uppercase tracking-[0.2em] font-medium">Dashboard de Performance Exclusivo</p>
                </div>
            </div>
            <div class="mt-6 md:mt-0 flex flex-row flex-wrap items-center gap-4 relative w-full md:w-auto">
                <div class="flex items-center gap-2">
                    <button onclick="setDateRange('month')" class="text-xs text-[#D4AF37]/70 hover:text-[#D4AF37] border border-[#D4AF37]/30 px-3 py-1.5 rounded-lg transition-colors">Este Mês</button>
                    <button onclick="setDateRange('all')" class="text-xs text-[#D4AF37]/70 hover:text-[#D4AF37] border border-[#D4AF37]/30 px-3 py-1.5 rounded-lg transition-colors">Global</button>
                </div>
                <div class="flex items-center gap-2">
                    <label class="text-[#D4AF37]/70 text-xs font-semibold uppercase tracking-widest">De:</label>
                    <input type="date" id="dateStart" onchange="updateDashboard()" class="glass text-[#D4AF37] text-sm md:text-base font-medium rounded-xl px-4 py-2.5 w-full outline-none focus:ring-1 focus:ring-[#D4AF37]/50 transition-all border border-[#D4AF37]/20 shadow-lg shadow-[#D4AF37]/5 [color-scheme:dark]">
                </div>
                <div class="flex items-center gap-2">
                    <label class="text-[#D4AF37]/70 text-xs font-semibold uppercase tracking-widest">Até:</label>
                    <input type="date" id="dateEnd" onchange="updateDashboard()" class="glass text-[#D4AF37] text-sm md:text-base font-medium rounded-xl px-4 py-2.5 w-full outline-none focus:ring-1 focus:ring-[#D4AF37]/50 transition-all border border-[#D4AF37]/20 shadow-lg shadow-[#D4AF37]/5 [color-scheme:dark]">
                </div>
            </div>
        </header>

        <!-- KPI Cards -->
        <div class="grid grid-cols-2 md:grid-cols-5 gap-4 md:gap-6 mb-12 fade-in delay-1">
            <div class="glass rounded-2xl p-6 transition-all duration-500 relative overflow-hidden group">
                <div class="absolute inset-0 bg-gradient-to-br from-white/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                <div class="flex justify-between items-start mb-4">
                    <h3 class="text-white/50 text-xs font-semibold uppercase tracking-widest">Investimento</h3>
                    <svg class="w-5 h-5 text-white/30 group-hover:text-white/60 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                </div>
                <p class="text-3xl font-serif text-white tracking-tight" id="kpi-investimento">R$ 0,00</p>
            </div>
            
            <div class="glass rounded-2xl p-6 transition-all duration-500 relative overflow-hidden group border border-[#D4AF37]/20">
                <div class="absolute inset-0 bg-gradient-to-br from-[#D4AF37]/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                <div class="flex justify-between items-start mb-4">
                    <h3 class="text-[#D4AF37]/70 text-xs font-semibold uppercase tracking-widest">Faturamento</h3>
                    <svg class="w-5 h-5 text-[#D4AF37]/50 group-hover:text-[#D4AF37] transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path></svg>
                </div>
                <p class="text-3xl font-serif text-gradient-gold tracking-tight" id="kpi-faturamento">R$ 0,00</p>
            </div>
            
            <div class="glass rounded-2xl p-6 transition-all duration-500 relative overflow-hidden group border border-[#B76E79]/20">
                <div class="absolute inset-0 bg-gradient-to-br from-[#B76E79]/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                <div class="flex justify-between items-start mb-4">
                    <h3 class="text-[#B76E79]/70 text-xs font-semibold uppercase tracking-widest">ROAS</h3>
                    <svg class="w-5 h-5 text-[#B76E79]/50 group-hover:text-[#B76E79] transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
                </div>
                <p class="text-3xl font-serif text-gradient-rose tracking-tight" id="kpi-roas">0.00x</p>
            </div>
            
            <div class="glass rounded-2xl p-6 transition-all duration-500 relative overflow-hidden group">
                <div class="flex justify-between items-start mb-4">
                    <h3 class="text-white/50 text-xs font-semibold uppercase tracking-widest">CPA</h3>
                    <svg class="w-5 h-5 text-white/30 group-hover:text-white/60 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
                </div>
                <p class="text-3xl font-serif text-white tracking-tight" id="kpi-cpa">R$ 0,00</p>
            </div>
            
            <div class="glass rounded-2xl p-6 transition-all duration-500 relative overflow-hidden group">
                <div class="flex justify-between items-start mb-4">
                    <h3 class="text-white/50 text-xs font-semibold uppercase tracking-widest">Vendas</h3>
                    <svg class="w-5 h-5 text-white/30 group-hover:text-white/60 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path></svg>
                </div>
                <p class="text-3xl font-serif text-white tracking-tight" id="kpi-vendas">0</p>
            </div>
        </div>

        <!-- Charts Row -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12 fade-in delay-2">
            <!-- Age Chart -->
            <div class="glass rounded-2xl p-6 relative overflow-hidden group hover:border-[#D4AF37]/30 transition-colors">
                <div class="absolute -top-10 -right-10 w-32 h-32 bg-[#D4AF37]/10 rounded-full blur-2xl group-hover:bg-[#D4AF37]/20 transition-colors duration-500"></div>
                <h3 class="text-xl font-serif text-[#F3E5AB] mb-1">Vendas por Idade</h3>
                <p class="text-xs text-white/40 uppercase tracking-widest mb-6 border-b border-white/5 pb-4">Período Selecionado</p>
                <div class="relative h-56">
                    <canvas id="ageChart"></canvas>
                </div>
            </div>
            <!-- Placement Chart -->
            <div class="glass rounded-2xl p-6 relative overflow-hidden group hover:border-[#B76E79]/30 transition-colors">
                <div class="absolute -top-10 -right-10 w-32 h-32 bg-[#B76E79]/10 rounded-full blur-2xl group-hover:bg-[#B76E79]/20 transition-colors duration-500"></div>
                <h3 class="text-xl font-serif text-[#F3E5AB] mb-1">Posicionamentos</h3>
                <p class="text-xs text-white/40 uppercase tracking-widest mb-6 border-b border-white/5 pb-4">Período Selecionado</p>
                <div class="relative h-56">
                    <canvas id="placementChart"></canvas>
                </div>
            </div>
            <!-- Top Regions -->
            <div class="glass rounded-2xl p-8 flex flex-col justify-center items-center text-center relative overflow-hidden group hover:border-[#D4AF37]/30 transition-colors">
                <div class="absolute inset-0 bg-gradient-to-t from-[#D4AF37]/5 to-transparent opacity-50 group-hover:opacity-100 transition-opacity duration-500"></div>
                <h3 class="text-xl font-serif text-[#F3E5AB] mb-1 w-full text-left">Regiões Campeãs</h3>
                <p class="text-xs text-white/40 uppercase tracking-widest mb-6 border-b border-white/5 pb-4 w-full text-left">Visão Global</p>
                <div class="flex-1 flex flex-col justify-center w-full z-10">
                    <p class="text-5xl md:text-6xl font-serif text-gradient-gold mb-4 group-hover:scale-[1.03] transition-transform duration-500">SP <span class="text-white/20 font-light text-4xl">|</span> RJ <span class="text-white/20 font-light text-4xl">|</span> MG</p>
                    <p class="text-white/50 text-sm font-light">Estados com maior concentração de demanda do público alvo.</p>
                </div>
            </div>
        </div>

        <!-- Top Creatives Table -->
        <div class="glass rounded-2xl p-8 mb-12 overflow-hidden fade-in delay-3 relative hover:border-[#D4AF37]/20 transition-colors">
            <div class="absolute top-0 left-0 w-full h-[2px] bg-gradient-to-r from-transparent via-[#D4AF37]/50 to-transparent"></div>
            <div class="flex justify-between items-end mb-6 border-b border-white/5 pb-4">
                <div>
                    <h3 class="text-2xl font-serif text-[#F3E5AB]">Top 5 Criativos</h3>
                    <p class="text-xs text-white/40 uppercase tracking-widest mt-1">Ranking de Conversão</p>
                </div>
                <div class="text-[#D4AF37] opacity-40">
                    <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" /></svg>
                </div>
            </div>
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="text-white/40 text-xs uppercase tracking-widest border-b border-white/5">
                            <th class="pb-4 px-4 font-semibold">Nome do Criativo</th>
                            <th class="pb-4 px-4 font-semibold text-right">Faturamento</th>
                            <th class="pb-4 px-4 font-semibold text-center">Vendas</th>
                            <th class="pb-4 px-4 font-semibold text-right">ROAS</th>
                        </tr>
                    </thead>
                    <tbody class="text-sm" id="topCreativesBody">
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Insights Row -->
        <div class="flex items-center gap-4 mb-8 fade-in delay-3">
            <h3 class="text-3xl font-serif text-gradient-gold">Insights & Ações Estratégicas</h3>
            <div class="flex-1 h-px bg-gradient-to-r from-[#D4AF37]/20 to-transparent"></div>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 fade-in delay-3 pb-10">
            <div class="glass rounded-2xl p-8 border-t border-t-emerald-500/50 hover:shadow-[0_0_30px_rgba(16,185,129,0.1)] transition-shadow">
                <div class="flex items-center gap-4 mb-6">
                    <div class="w-10 h-10 rounded-full bg-emerald-500/10 flex items-center justify-center text-emerald-400 border border-emerald-500/20">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                    </div>
                    <h4 class="text-xl font-serif text-emerald-400">O que funcionou</h4>
                </div>
                <p class="text-white/60 leading-relaxed text-sm font-light">
                    O criativo <span class="text-white font-medium">"2 - atemporal, moderna e clássica"</span> foi o grande destaque do período, sendo responsável por 75% das vendas (3 conversões) e gerando um <strong class="text-emerald-400">ROAS excepcional de 17.3x</strong>. O apelo visual/texto conectou perfeitamente com o público-alvo, provando que essa linha de comunicação é a vencedora absoluta deste teste.
                </p>
            </div>
            
            <div class="glass rounded-2xl p-8 border-t border-t-rose-500/50 hover:shadow-[0_0_30px_rgba(244,63,94,0.1)] transition-shadow">
                <div class="flex items-center gap-4 mb-6">
                    <div class="w-10 h-10 rounded-full bg-rose-500/10 flex items-center justify-center text-rose-400 border border-rose-500/20">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                    </div>
                    <h4 class="text-xl font-serif text-rose-400">Onde está o gargalo</h4>
                </div>
                <p class="text-white/60 leading-relaxed text-sm font-light">
                    A campanha dependeu quase que 100% de um único anúncio. Os outros +10 criativos testados apenas consumiram verba sem trazer retorno expressivo. Por exemplo, o criativo <span class="text-white font-medium">"1 - Pequenos detalhes..."</span> até gerou 1 venda, mas teve um ROAS de apenas 0.6x (prejuízo). Os demais rodaram, gastaram e não converteram.
                </p>
            </div>

            <div class="glass rounded-2xl p-8 border-t border-t-amber-500/50 hover:shadow-[0_0_30px_rgba(245,158,11,0.1)] transition-shadow">
                <div class="flex items-center gap-4 mb-6">
                    <div class="w-10 h-10 rounded-full bg-amber-500/10 flex items-center justify-center text-amber-400 border border-amber-500/20">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                    </div>
                    <h4 class="text-xl font-serif text-amber-400">Próximas ações</h4>
                </div>
                <div class="text-white/60 leading-relaxed text-sm font-light space-y-3">
                    <p><span class="text-[#D4AF37] font-medium mr-1">1. Pausar os Sanguessugas:</span> Desativar imediatamente o criativo "1" (ROAS negativo) e os demais que gastaram o CPA ideal e não trouxeram vendas.</p>
                    <p><span class="text-[#D4AF37] font-medium mr-1">2. Escalar o Vencedor:</span> Direcionar o orçamento livre para o criativo "2 - atemporal", aproveitando seu momento de tração e ROAS altíssimo.</p>
                    <p><span class="text-[#D4AF37] font-medium mr-1">3. Novas Variações:</span> Como a comunicação "Atemporal/Clássica" validou bem, a próxima leva deve focar em variações desse anúncio.</p>
                </div>
            </div>
        </div>
        
        <footer class="mt-8 pt-8 border-t border-white/5 text-center flex flex-col items-center pb-12">
            <svg class="w-8 h-8 text-[#D4AF37]/20 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" /></svg>
            <p class="text-white/30 text-xs tracking-widest uppercase font-medium">Dashboard Premium • Dados sujeitos a atualização</p>
        </footer>
    </div>

    <!-- Data Injection -->
    <script>
        const dashboardData = """ + json.dumps(data) + """;
        
        const formatCurrency = (val) => val.toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'});
        const formatNumber = (val) => val.toLocaleString('pt-BR');

        function updateCards(dataObj) {
            document.getElementById('kpi-investimento').innerHTML = formatCurrency(dataObj.Investimento);
            document.getElementById('kpi-faturamento').innerHTML = formatCurrency(dataObj.Faturamento);
            document.getElementById('kpi-roas').innerHTML = dataObj.ROAS.toFixed(2) + 'x';
            document.getElementById('kpi-cpa').innerHTML = formatCurrency(dataObj.CPA);
            document.getElementById('kpi-vendas').innerHTML = formatNumber(dataObj.Vendas);
        }

        let ageChartInst = null;
        let placementChartInst = null;

        function updateDashboard() {
            const startVal = document.getElementById('dateStart').value;
            const endVal = document.getElementById('dateEnd').value;
            
            if (!startVal || !endVal) return;
            
            const startDate = new Date(startVal + 'T00:00:00');
            const endDate = new Date(endVal + 'T23:59:59');
            
            let totalInv = 0;
            let totalFat = 0;
            let totalVen = 0;
            let totalImp = 0;
            let totalCli = 0;
            
            if (dashboardData.Diario) {
                dashboardData.Diario.forEach(dayData => {
                    const dayDate = new Date(dayData.Data + 'T12:00:00'); // Midday to avoid timezone issues
                    if (dayDate >= startDate && dayDate <= endDate) {
                        totalInv += dayData.Investimento;
                        totalFat += dayData.Faturamento;
                        totalVen += dayData.Vendas;
                        totalImp += dayData.Impressoes;
                        totalCli += dayData.Cliques;
                    }
                });
            }
            
            // Dynamic Charts Update
            let idadeDataMap = {};
            let posDataMap = {};
            
            if (dashboardData.IdadeDiario) {
                dashboardData.IdadeDiario.forEach(dayData => {
                    const dayDate = new Date(dayData.Data + 'T12:00:00');
                    if (dayDate >= startDate && dayDate <= endDate) {
                        idadeDataMap[dayData.Idade] = (idadeDataMap[dayData.Idade] || 0) + dayData.Vendas;
                    }
                });
            }
            
            if (dashboardData.PosicionamentoDiario) {
                dashboardData.PosicionamentoDiario.forEach(dayData => {
                    const dayDate = new Date(dayData.Data + 'T12:00:00');
                    if (dayDate >= startDate && dayDate <= endDate) {
                        posDataMap[dayData.Posicionamento] = (posDataMap[dayData.Posicionamento] || 0) + dayData.Vendas;
                    }
                });
            }
            
            // Criativos Update
            let criativosDataMap = {};
            if (dashboardData.CriativoDiario) {
                dashboardData.CriativoDiario.forEach(dayData => {
                    const dayDate = new Date(dayData.Data + 'T12:00:00');
                    if (dayDate >= startDate && dayDate <= endDate) {
                        if (!criativosDataMap[dayData.Nome]) {
                            criativosDataMap[dayData.Nome] = {Faturamento: 0, Vendas: 0, Investimento: 0};
                        }
                        criativosDataMap[dayData.Nome].Faturamento += dayData.Faturamento;
                        criativosDataMap[dayData.Nome].Vendas += dayData.Vendas;
                        criativosDataMap[dayData.Nome].Investimento += dayData.Investimento;
                    }
                });
            }

            let criativosArray = Object.keys(criativosDataMap).map(nome => {
                const c = criativosDataMap[nome];
                c.Nome = nome;
                c.ROAS = c.Investimento > 0 ? c.Faturamento / c.Investimento : 0;
                return c;
            });
            
            criativosArray.sort((a, b) => b.Vendas - a.Vendas);
            const top5 = criativosArray.slice(0, 5);
            
            const tbody = document.getElementById('topCreativesBody');
            if (tbody) {
                tbody.innerHTML = '';
                top5.forEach((creative, i) => {
                    const highlightBg = i === 0 ? "bg-[#D4AF37]/5" : "";
                    const medal = i === 0 ? "🥇 " : (i === 1 ? "🥈 " : (i === 2 ? "🥉 " : ""));
                    
                    const faturamentoStr = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(creative.Faturamento);
                    const roasStr = creative.ROAS.toFixed(2).replace('.', ',') + 'x';
                    
                    const tr = document.createElement('tr');
                    tr.className = `border-b border-white/5 hover:bg-white/5 transition-colors ${highlightBg}`;
                    tr.innerHTML = `
                        <td class="py-5 px-4 text-white/80 font-medium flex items-center gap-3">
                            <span class="text-xl">${medal}</span> ${creative.Nome}
                        </td>
                        <td class="py-5 px-4 text-right text-[#D4AF37] font-semibold tracking-wide">${faturamentoStr}</td>
                        <td class="py-5 px-4 text-center text-white/70">${creative.Vendas}</td>
                        <td class="py-5 px-4 text-right text-[#B76E79] font-semibold tracking-wide">${roasStr}</td>
                    `;
                    tbody.appendChild(tr);
                });
            }
            
            if (ageChartInst) {
                const labels = Object.keys(idadeDataMap);
                const data = Object.values(idadeDataMap);
                ageChartInst.data.labels = labels;
                ageChartInst.data.datasets[0].data = data;
                
                const baseColors = ['rgba(212, 175, 55, 0.8)', 'rgba(183, 110, 121, 0.6)', 'rgba(243, 229, 171, 0.6)', 'rgba(255, 255, 255, 0.4)', 'rgba(212, 175, 55, 0.4)'];
                const hoverColors = ['rgba(212, 175, 55, 1)', 'rgba(183, 110, 121, 1)', 'rgba(243, 229, 171, 1)', 'rgba(255, 255, 255, 0.8)', 'rgba(212, 175, 55, 0.8)'];
                ageChartInst.data.datasets[0].backgroundColor = labels.map((_, i) => baseColors[i % baseColors.length]);
                ageChartInst.data.datasets[0].hoverBackgroundColor = labels.map((_, i) => hoverColors[i % hoverColors.length]);
                ageChartInst.update();
            }
            
            if (placementChartInst) {
                // Filtra para remover posicionamentos com 0 vendas
                const filteredPosMap = Object.entries(posDataMap)
                    .filter(([pos, val]) => val > 0)
                    .sort((a, b) => b[1] - a[1]); // Ordena do maior pro menor
                
                // Se ainda tiver muitos, pega os Top 5 e soma o resto em "Outros"
                let finalLabels = [];
                let finalData = [];
                
                if (filteredPosMap.length > 5) {
                    finalLabels = filteredPosMap.slice(0, 5).map(e => e[0]);
                    finalData = filteredPosMap.slice(0, 5).map(e => e[1]);
                    const othersSum = filteredPosMap.slice(5).reduce((acc, curr) => acc + curr[1], 0);
                    if (othersSum > 0) {
                        finalLabels.push('Outros');
                        finalData.push(othersSum);
                    }
                } else {
                    finalLabels = filteredPosMap.map(e => e[0]);
                    finalData = filteredPosMap.map(e => e[1]);
                }
                
                placementChartInst.data.labels = finalLabels;
                placementChartInst.data.datasets[0].data = finalData;
                
                const pieColors = ['#D4AF37', '#B76E79', '#F3E5AB', '#ffffff', '#8a7322', '#6b4047'];
                placementChartInst.data.datasets[0].backgroundColor = finalLabels.map((_, i) => pieColors[i % pieColors.length]);
                placementChartInst.update();
            }
            
            const roas = totalInv > 0 ? totalFat / totalInv : 0;
            const cpa = totalVen > 0 ? totalInv / totalVen : 0;
            
            updateCards({
                Investimento: totalInv,
                Faturamento: totalFat,
                Vendas: totalVen,
                ROAS: roas,
                CPA: cpa
            });
        }
        
        function setDateRange(type) {
            if (!dashboardData.Diario || dashboardData.Diario.length === 0) return;
            const firstDate = dashboardData.Diario[0].Data;
            const lastDate = dashboardData.Diario[dashboardData.Diario.length - 1].Data;
            
            if (type === 'all') {
                document.getElementById('dateStart').value = firstDate;
                document.getElementById('dateEnd').value = lastDate;
            } else if (type === 'month') {
                // Pega o mês da última data disponível
                const lastDateObj = new Date(lastDate + 'T12:00:00');
                const year = lastDateObj.getFullYear();
                const month = String(lastDateObj.getMonth() + 1).padStart(2, '0');
                // O primeiro dia do mês e o último dia do mês
                const startOfMonth = `${year}-${month}-01`;
                const lastDay = new Date(year, lastDateObj.getMonth() + 1, 0).getDate();
                const endOfMonth = `${year}-${month}-${lastDay}`;
                
                document.getElementById('dateStart').value = startOfMonth;
                document.getElementById('dateEnd').value = endOfMonth;
            }
            updateDashboard();
        }

        // Init Dates
        if (dashboardData.Diario && dashboardData.Diario.length > 0) {
            const firstDate = dashboardData.Diario[0].Data;
            const lastDate = dashboardData.Diario[dashboardData.Diario.length - 1].Data;
            
            document.getElementById('dateStart').value = firstDate;
            document.getElementById('dateEnd').value = lastDate;
        }

        // Init charts
        Chart.defaults.color = 'rgba(255, 255, 255, 0.4)';
        Chart.defaults.font.family = "'Outfit', sans-serif";
        
        const ctxAge = document.getElementById('ageChart').getContext('2d');
        ageChartInst = new Chart(ctxAge, {
            type: 'bar',
            data: {
                labels: [],
                datasets: [{
                    label: 'Vendas',
                    data: [],
                    backgroundColor: [],
                    hoverBackgroundColor: [],
                    borderRadius: 6,
                    borderWidth: 1,
                    borderColor: 'rgba(255, 255, 255, 0.1)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: 'rgba(15, 15, 15, 0.95)',
                        titleFont: { family: 'Outfit', size: 13 },
                        bodyFont: { family: 'Outfit', size: 14, weight: 'bold' },
                        padding: 12,
                        borderColor: 'rgba(212, 175, 55, 0.3)',
                        borderWidth: 1,
                        displayColors: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: 'rgba(255, 255, 255, 0.05)', drawBorder: false },
                        border: { display: false }
                    },
                    x: {
                        grid: { display: false },
                        border: { display: false }
                    }
                }
            }
        });

        const ctxPlacement = document.getElementById('placementChart').getContext('2d');
        placementChartInst = new Chart(ctxPlacement, {
            type: 'doughnut',
            data: {
                labels: [],
                datasets: [{
                    data: [],
                    backgroundColor: [],
                    borderWidth: 0,
                    hoverOffset: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: { 
                            color: 'rgba(255, 255, 255, 0.6)', 
                            font: {family: 'Outfit', size: 12},
                            padding: 20,
                            usePointStyle: true,
                            pointStyle: 'circle'
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(15, 15, 15, 0.95)',
                        titleFont: { family: 'Outfit', size: 13 },
                        bodyFont: { family: 'Outfit', size: 14, weight: 'bold' },
                        padding: 12,
                        borderColor: 'rgba(212, 175, 55, 0.3)',
                        borderWidth: 1
                    }
                },
                cutout: '75%',
                layout: { padding: 10 }
            }
        });

        // Initialize with Selected Data
        updateDashboard();
    </script>
</body>
</html>
"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_template)
    print("Dashboard Premium gerado com sucesso em index.html")

if __name__ == '__main__':
    generate_html()
