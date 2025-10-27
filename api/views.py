from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# --- Nueva función con penalización más suave ---
def calcular_nivel_penalizado_suave(inputs, pesos=None):
    if pesos is None:
        pesos = [1] * len(inputs)

    def penalizar(x):
        # Normaliza a rango 0–1
        norm = x / 4
        # Penaliza mucho los bajos, pero suaviza los medios
        return norm**2 * 1.1 + 0.1 * norm

    penalizados = [penalizar(x) for x in inputs]
    total_pesos = sum(pesos)
    promedio_ponderado = sum(p * w for p, w in zip(penalizados, pesos)) / total_pesos
    salida = promedio_ponderado * 10  # escalar a 0–10
    return salida


def categoria(inputs, pesos=None):
    salida = calcular_nivel_penalizado_suave(inputs, pesos)
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

    valor = calcular_nivel_penalizado_suave(inputs)
    cat = categoria(inputs)

    return Response({
        'nivel_continuo': round(valor, 2),
        'categoria': cat
    })
