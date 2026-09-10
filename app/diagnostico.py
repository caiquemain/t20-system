#!/usr/bin/env python3
"""
Script de diagnóstico para o bug do círculo máximo de magias
Executar com: docker compose exec api python diagnostico.py
"""
import sys
sys.path.insert(0, '/app')

try:
    from src.regras.magias import calcular_circulo_maximo, calcular_circulo_maximo_ficha
    from src.models import Personagem, ClasseInfo
    from src.dados_progressao_magias import PROGRESSAO_CIRCULOS_POR_CLASSE
    
    print("=" * 70)
    print("DIAGNÓSTICO: Cálculo de Círculo Máximo de Magias")
    print("=" * 70)

    # Teste 0: Verificar se o arquivo de dados existe
    print("\n[TESTE 0] Verificando dados_progressao_magias.py")
    print("-" * 70)
    if PROGRESSAO_CIRCULOS_POR_CLASSE:
        print(f"✅ Arquivo carregado com {len(PROGRESSAO_CIRCULOS_POR_CLASSE)} classes")
        print(f"   Classes disponíveis: {list(PROGRESSAO_CIRCULOS_POR_CLASSE.keys())}")
    else:
        print("❌ ERRO: PROGRESSAO_CIRCULOS_POR_CLASSE está vazio!")
        print("   Verifique se o arquivo dados_progressao_magias.py existe e tem conteúdo")

    # Teste 1: Função direta com diferentes classes
    print("\n[TESTE 1] Função calcular_circulo_maximo() - Diferentes Classes")
    print("-" * 70)

    testes = [
        ("Arcanista", 1, "Deveria ser 1"),
        ("Arcanista", 5, "Deveria ser 2"),
        ("Arcanista", 9, "Deveria ser 3"),
        ("Bruxo", 1, "Deveria ser 1"),
        ("Bruxo", 5, "Deveria ser 2"),
        ("Bardo", 1, "Deveria ser 1"),
        ("Bardo", 6, "Deveria ser 2"),
        ("Clérigo", 1, "Deveria ser 1"),
        ("Druida", 1, "Deveria ser 1"),
        ("Guerreiro", 1, "Deveria ser 0 (não conjura)"),
    ]

    for classe, nivel, esperado in testes:
        resultado = calcular_circulo_maximo(classe, nivel)
        status = "✅" if (classe == "Guerreiro" and resultado == 0) or (classe != "Guerreiro" and resultado >= 1) else "❌"
        print(f"{status} {classe:15s} Nv {nivel:2d} -> Círculo {resultado:2d} | {esperado}")

    # Teste 2: Com objeto Personagem completo
    print("\n[TESTE 2] Função calcular_circulo_maximo_ficha() - Objeto Completo")
    print("-" * 70)

    ficha_teste = Personagem(
        id="test123",
        nome="Mago Teste",
        raca="Humano",
        classes=[ClasseInfo(nome="Arcanista", nivel=1, primaria=True)],
        nivel_total=1
    )

    resultado_ficha = calcular_circulo_maximo_ficha(ficha_teste)
    print(f"Personagem: {ficha_teste.nome}")
    print(f"Classe: {ficha_teste.classes[0].nome} Nível {ficha_teste.classes[0].nivel}")
    print(f"Círculo Máximo Calculado: {resultado_ficha}")
    print(f"Status: {'✅ Correto' if resultado_ficha == 1 else '❌ INCORRETO (esperado 1)'}")

    # Teste 3: Verificar nomes de classe
    print("\n[TESTE 3] Variações de Nomes de Classe")
    print("-" * 70)

    variacoes = [
        "Arcanista",
        "arcanista", 
        "ARCANISTA",
        "Arcanista ",
        " Arcanista",
        "Bruxo",
        "bruxo",
        "BRUXO",
    ]

    for nome in variacoes:
        resultado = calcular_circulo_maximo(nome, 1)
        print(f"  '{nome}' -> Círculo {resultado}")

    print("\n" + "=" * 70)
    print("DIAGNÓSTICO CONCLUÍDO")
    print("=" * 70)
    print("\nSe todos os testes mostram círculo 0, o problema pode ser:")
    print("1. Arquivo dados_progressao_magias.py não existe ou está vazio")
    print("2. Nomes de classe não correspondem ao esperado")
    print("3. Função não está sendo chamada no fluxo de atualização")

except ImportError as e:
    print(f"❌ ERRO DE IMPORT: {e}")
    print("\nVerifique se os seguintes arquivos existem:")
    print("  - /app/src/regras/magias.py")
    print("  - /app/src/models.py")
    print("  - /app/src/dados_progressao_magias.py")
    
    import os
    print("\nArquivos encontrados em /app/src/:")
    if os.path.exists('/app/src'):
        for root, dirs, files in os.walk('/app/src'):
            level = root.replace('/app/src', '').count(os.sep)
            indent = ' ' * 2 * level
            print(f'{indent}{os.path.basename(root)}/')
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                print(f'{subindent}{file}')

except Exception as e:
    print(f"❌ ERRO INESPERADO: {e}")
    import traceback
    traceback.print_exc()