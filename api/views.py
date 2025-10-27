from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import statistics

def calcular_nivel_penalizado_por_dispersion(inputs, pesos=None):
    """
    inputs: lista de 4 números entre 0 y 4
    Devuelve: valor continuo 0-10 que:
      - penaliza fuertemente valores bajos,
      - y además penaliza más cuando hay mucha dispersión (outliers bajos).
    """
    if pesos is None:
        pesos = [1] * len(inputs)
    if len(inputs) != len(pesos):
        raise ValueError("inputs y pesos deben coincidir en longitud")

    # normalizar a 0..1
    norms = [max(0.0, min(1.0, x / 4.0)) for x in inputs]

    # parámetros ajustables (puedes tunear k y m)
    k = 0.8            # cuánto reduce la media por la desviación estándar
    m = 0.0666666667   # pequeño "bonus" por homogeneidad (cuando std es baja)

    avg = sum(norms) / len(norms)
    std = statistics.pstdev(norms)  # desviación poblacional

    # fórmula: media ajustada por dispersión y homogeneidad
    score_norm = avg * (1 - k * std) * (1 + m * (1 - std))

    # aseguramos rango 0..1
    score_norm = max(0.0, min(1.0, score_norm))

    # escalamos a 0..10
    salida = score_norm * 10.0
    return salida


def categoria(inputs, pesos=None):
    salida = calcular_nivel_penalizado_por_dispersion(inputs, pesos)
    if salida < 4:
        return "baja"
    elif salida < 7:
        return "media"
    else:
        return "alta"


@api_view(['POST'])
def calcular(request):
    data = request.data
    inputs = data.get('inputs', [])

    if len(inputs) != 4:
        return Response({'error': 'Se requieren 4 valores de entrada'}, status=400)

    valor = calcular_nivel_penalizado_por_dispersion(inputs)
    cat = categoria(inputs)

    return Response({
        'nivel_continuo': round(valor, 2),
        'categoria': cat
    })
