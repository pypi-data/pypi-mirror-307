from datetime import datetime, timedelta

def get_code_indice(data=None, codigo='WIN'):
    """
    Calcula o código do contrato futuro do mini índice Bovespa na B3 (Bolsa de Valores do Brasil) para uma data específica.

    O código é composto pelo prefixo (por padrão 'WIN' para o mini índice), seguido de uma letra que representa o mês de vencimento, e os dois últimos dígitos do ano.

    A mudança de código ocorre nos meses pares (fevereiro, abril, junho, agosto, outubro e dezembro), na quarta-feira mais próxima do dia 15.

    Parâmetros:
        data (str, opcional): Data no formato 'YYYY-MM-DD'. Se não for fornecida, será utilizada a data atual.
        codigo (str, opcional): Prefixo do contrato. Pode ser 'WIN' para mini índice ou 'IND' para índice cheio. O padrão é 'WIN'.

    Retorna:
        str: O código do contrato futuro do mini índice correspondente à data fornecida.

    Exemplos:
        >>> get_code_indice('2024-10-14')
        'WINV24'

        >>> get_code_indice(data='2024-10-16', codigo='IND')
        'INDZ24'
    """
    # Meses em que ocorre a mudança de código
    code_change_months = [2, 4, 6, 8, 10, 12]

    # Mapeamento de códigos para os meses de mudança
    month_codes = {
        2: 'J',  # Fevereiro
        4: 'M',  # Abril
        6: 'Q',  # Junho
        8: 'V',  # Agosto
        10: 'Z', # Outubro
        12: 'G', # Dezembro (contratos para o ano seguinte)
    }

    def get_code_change_date(month, year):
        """
        Calcula a quarta-feira mais próxima do dia 15 para um mês e ano específicos.

        Parâmetros:
            month (int): Mês (1-12).
            year (int): Ano (ex: 2024).

        Retorna:
            datetime: A data da quarta-feira mais próxima do dia 15.
        """
        dia_15 = datetime(year, month, 15)
        # Calcula a diferença de dias até a quarta-feira mais próxima
        dias_diferenca = (2 - dia_15.weekday() + 7) % 7
        if dias_diferenca > 3:
            dias_diferenca -= 7
        code_change_date = dia_15 + timedelta(days=dias_diferenca)
        return code_change_date

    # Usar a data fornecida ou a data atual
    if data is None:
        data = datetime.now()
    else:
        data = datetime.strptime(data, '%Y-%m-%d')

    # Lista de datas de mudança de código e seus respectivos códigos
    code_change_dates = []
    for y in range(data.year - 1, data.year + 2):
        for m in code_change_months:
            code_change_date = get_code_change_date(m, y)
            # Ajuste do ano para o mês de dezembro (contratos do ano seguinte)
            if m == 12:
                code_year = str((y + 1) % 100).zfill(2)
            else:
                code_year = str(y % 100).zfill(2)
            code = f"{codigo}{month_codes[m]}{code_year}"
            code_change_dates.append((code_change_date, code))

    # Ordenar as datas de mudança de código
    code_change_dates.sort()

    # Encontrar o código aplicável à data fornecida
    codigo_atual = None
    for i in range(len(code_change_dates)):
        if code_change_dates[i][0] <= data:
            codigo_atual = code_change_dates[i][1]
        elif code_change_dates[i][0] > data:
            break
    if codigo_atual is None:
        codigo_atual = code_change_dates[0][1]
    return codigo_atual

# Exemplo de uso
if __name__ == "__main__":
    print(get_code_indice(data='2024-10-14'))  # Saída: 'WINV24'
    print(get_code_indice(data='2024-10-16', codigo='IND'))  # Saída: 'INDZ24'
