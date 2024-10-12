    carros = Carro.objects.all()
    energias = Energia.objects.all()
    dados_carro = {}
    dados_energia = {}
    error_message = None

    if request.method == 'POST':
        try:
            dados_carro = {}
            for carro in carros:
                km_por_mes_str = request.POST.get(f'km_por_mes_{carro.id}', None)
                if km_por_mes_str is None or not km_por_mes_str:
                    error_message = 'Quilometragem inválida, insira um valor para Km mensal'
                    return render(request, 'carbono/teste.html', {'carros': carros, 'energias': energias, 'error_message': error_message})
                
                dados_carro[carro] = {
                    'tipo_carro': carro.tipo,
                    'credito_mensal': round(carro[0](km_por_mes_str), 3),
                    'credito_anual': round(carro[1](km_por_mes_str), 3),
                    'arvores_a_plantar': math.ceil(arvores(carro[1](km_por_mes_str))),
                    'valor_credito': round(valor_da_tonelada(carro[1](km_por_mes_str)), 2),
                }
                
        except (ValueError, TypeError):
            error_message = "Insira um valor numérico válido para a quilometragem mensal."
        
        return render(request, "carbono/teste.html", {"carros": carros, "energias": energias, "error_message": error_message})

    #Algoritmo de Energia
    if 'tipo_de_energia' in request.POST:
        energia_selecionada = get_object_or_404(Energia, pk=request.POST['tipo_de_energia'])
        try:
            if energia_selecionada.modo_de_calculo == 'kWh':

                dados_energia = {
                    'tipo_energia': energia_selecionada.legenda,
                    'co2_por_mes': round(energia_kwh[0](), 3),
                    'co2_por_ano': round(energia_kwh[1](), 3),
                    'arvores_a_plantar': math.ceil(arvores(energia_kwh[1]())),
                    'valor_credito': round(valor_da_tonelada(energia_kwh[1]()), 2),
                }
            elif energia_selecionada.modo_de_calculo == 'Conta de Energia':
                valor_da_conta= float(request.POST.get('valor_da_conta'))
                
                dados_energia = {
                    'tipo_energia': energia_selecionada.legenda,
                    'co2_por_mes': round(energia_reais[0](valor_da_conta), 3),
                    'co2_por_ano': round(energia_reais[1](valor_da_conta), 3),
                    'arvores_a_plantar': math.ceil(arvores(energia_reais[1](valor_da_conta))),
                    'valor_credito': round(valor_da_tonelada(energia_reais[1](valor_da_conta)), 2),
                }
        except (ValueError, TypeError):
            error_message = 'Insira um valor numérico válido para os dados de energia'

        return render(request, "carbono/teste.html", {"carros": carros, "energias": energias, "dados_carro": dados_carro, "dados_energia": dados_energia, "error_message": error_message})

    return render(request, 'carbono/teste.html', {
        'carros': carros,
        'energias': energias,
        'dados_carro': dados_carro,
        'dados_energia': dados_energia,
        'error_message': error_message,
    })