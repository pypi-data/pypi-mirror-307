from datetime import datetime, timedelta
import calendar
import holidays

def get_code_dolar(data=None, codigo='WDO'):
    """
    Calcula o código do contrato futuro de dólar na B3 (Bolsa de Valores do Brasil) para uma data específica.

    O código é composto pelo prefixo (por padrão 'WDO' para mini dólar), seguido de uma letra que representa o mês de vencimento, e os dois últimos dígitos do ano.

    Parâmetros:
        data (str, opcional): Data no formato 'YYYY-MM-DD'. Se não for fornecida, será utilizada a data atual.
        codigo (str, opcional): Prefixo do contrato. Pode ser 'WDO' para mini dólar ou 'DOL' para dólar cheio. O padrão é 'WDO'.

    Retorna:
        str: O código do contrato futuro de dólar correspondente à data fornecida.

    Exemplos:
        >>> get_code_dolar('2024-10-25')
        'WDOX24'

        >>> get_code_dolar(data='2024-12-31', codigo='DOL')
        'DOLF25'
    """
    # Mapeamento de códigos para meses (janeiro é 'F', dezembro é 'Z')
    month_codes = {
        1: 'G', 2: 'H', 3: 'J', 4: 'K', 5: 'M', 6: 'N',
        7: 'Q', 8: 'U', 9: 'V', 10: 'X', 11: 'Z', 12: 'F'
    }

    
    # Usar a data fornecida ou a data atual
    if data is None:
        data = datetime.now()
    else:
        data = datetime.strptime(data, '%Y-%m-%d')
        
    ano_atual = data.year
    ano = str(ano_atual)[-2:]  # Últimos dois dígitos do ano

    # Obter os feriados nacionais do Brasil para o ano atual
    feriados_nacionais = holidays.BR(years=[ano_atual])

    # Adicionar feriados específicos (vésperas de Natal e Ano Novo)
    feriados_especiais = [
        datetime(ano_atual, 12, 24),
        datetime(ano_atual, 12, 31),
    ]

    # Combinar feriados nacionais e especiais
    feriados = set(feriados_nacionais.keys()) | set(feriados_especiais)

    def ultimo_dia_util(mes, ano):
        """
        Encontra o último dia útil de um mês, considerando fins de semana e feriados.

        Parâmetros:
            mes (int): Mês (1-12).
            ano (int): Ano (ex: 2024).

        Retorna:
            datetime: O último dia útil do mês.
        """
        ultimo_dia = calendar.monthrange(ano, mes)[1]
        data_util = datetime(ano, mes, ultimo_dia)
        while data_util.weekday() >= 5 or data_util in feriados:
            data_util -= timedelta(days=1)
        return data_util

    # Encontrar o último dia útil do mês atual
    ultimo_dia_util_mes = ultimo_dia_util(data.month, data.year)

    # Determinar o código do contrato
    if data >= ultimo_dia_util_mes:
        # Se a data for após ou igual ao último dia útil do mês, avançar para o próximo mês
        mes_dolar = data.month + 1 if data.month < 12 else 1
        if mes_dolar == 1:
            ano_dolar = str(ano_atual + 1)[-2:]  # Incrementa o ano se for janeiro
        else:
            ano_dolar = ano
    else:
        # Usa o mês atual
        mes_dolar = data.month
        ano_dolar = ano

    # Monta o código do contrato
    codigo_dolar = f"{codigo}{month_codes[mes_dolar]}{ano_dolar}"
    return codigo_dolar

# Exemplo de uso
if __name__ == "__main__":
    print(get_code_dolar(codigo='DOL'))
