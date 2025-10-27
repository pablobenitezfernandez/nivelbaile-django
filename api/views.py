from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

def calcular_nivel_penalizado(inputs):
    """
    inputs: lista de 4 números entre 0 y 4
    Devuelve un valor continuo 0-10
    Penaliza fuertemente valores bajos (0 o 1)
    """
    # Normalizar a 0..1
    norms = [x / 4.0 for x in inputs]

    avg = sum(norms) / len(norms)
    min_norm = min(norms)

    # Mezcla ponderada: 0.8 promedio + 0.2 mínimo
    score_norm = 0.8 * avg + 0.2 * min_norm

    # Escalamos a 0-10
    salida = score_norm * 10
    return salida

def categoria(inputs):
    valor = calcular_nivel_penalizado(inputs)
    if valor < 5:
        return "baja"
    elif valor < 7.5:
        return "media"
    else:
        return "alta"

@api_view(['POST'])
def calcular(request):
    data = request.data
    inputs = data.get('inputs', [])
    if len(inputs) != 4:
        return Response({'error': 'Se requieren 4 valores de entrada'}, status=400)

    valor = calcular_nivel_penalizado(inputs)
    cat = categoria(inputs)
    return Response({'nivel_continuo': round(valor,2), 'categoria': cat})
