"""Catálogo dos módulos da Aurora Siger, herdado da Fase 5 (NCAS)."""

from __future__ import annotations

MODULOS = {
    "CTL": {
        "nome": "Centro de Controle",
        "tipo": "comunicacao",
        "prioridade": "P1",
        "peso_prioridade": 5,
        "essencial": True,
        "codigo_sensor": 419,  # 0x1A3
        "tensao_nominal_v": 48.0,
        "corrente_nominal_a": 0.32,
        "latencia_base_ms": 12.0,
    },
    "PWR": {
        "nome": "Complexo de Energia",
        "tipo": "energia",
        "prioridade": "P1",
        "peso_prioridade": 5,
        "essencial": True,
        "codigo_sensor": 692,  # 0x2B4
        "tensao_nominal_v": 120.0,
        "corrente_nominal_a": 0.22,
        "latencia_base_ms": 18.0,
    },
    "LSS": {
        "nome": "Sistema de Suporte de Vida",
        "tipo": "suporte",
        "prioridade": "P1",
        "peso_prioridade": 5,
        "essencial": True,
        "codigo_sensor": 973,  # 0x3CD
        "tensao_nominal_v": 48.0,
        "corrente_nominal_a": 0.41,
        "latencia_base_ms": 15.0,
    },
    "HAB": {
        "nome": "Complexo Habitacional",
        "tipo": "habitacao",
        "prioridade": "P2",
        "peso_prioridade": 4,
        "essencial": False,
        "codigo_sensor": 1262,  # 0x4EE
        "tensao_nominal_v": 24.0,
        "corrente_nominal_a": 0.55,
        "latencia_base_ms": 22.0,
    },
    "MED": {
        "nome": "Complexo Medico",
        "tipo": "suporte_medico",
        "prioridade": "P2",
        "peso_prioridade": 4,
        "essencial": True,
        "codigo_sensor": 1365,  # 0x555
        "tensao_nominal_v": 48.0,
        "corrente_nominal_a": 0.38,
        "latencia_base_ms": 14.0,
    },
    "COM": {
        "nome": "Sistema de Comunicacao",
        "tipo": "comunicacao",
        "prioridade": "P3",
        "peso_prioridade": 3,
        "essencial": True,
        "codigo_sensor": 1710,  # 0x6AE
        "tensao_nominal_v": 28.0,
        "corrente_nominal_a": 1.60,
        "latencia_base_ms": 35.0,
    },
    "AGR": {
        "nome": "Complexo de Agricultura",
        "tipo": "agricultura",
        "prioridade": "P3",
        "peso_prioridade": 3,
        "essencial": False,
        "codigo_sensor": 2001,  # 0x7D1
        "tensao_nominal_v": 24.0,
        "corrente_nominal_a": 0.70,
        "latencia_base_ms": 28.0,
    },
    "LOG": {
        "nome": "Complexo de Logistica",
        "tipo": "armazenamento",
        "prioridade": "P4",
        "peso_prioridade": 2,
        "essencial": False,
        "codigo_sensor": 2198,  # 0x896
        "tensao_nominal_v": 24.0,
        "corrente_nominal_a": 0.48,
        "latencia_base_ms": 40.0,
    },
    "MIN": {
        "nome": "Complexo de Mineracao",
        "tipo": "laboratorio",
        "prioridade": "P4",
        "peso_prioridade": 2,
        "essencial": False,
        "codigo_sensor": 2730,  # 0xAAA
        "tensao_nominal_v": 48.0,
        "corrente_nominal_a": 0.90,
        "latencia_base_ms": 55.0,
    },
    "RES": {
        "nome": "Centro de Pesquisa",
        "tipo": "laboratorio",
        "prioridade": "P5",
        "peso_prioridade": 1,
        "essencial": False,
        "codigo_sensor": 3017,  # 0xBC9
        "tensao_nominal_v": 12.0,
        "corrente_nominal_a": 0.35,
        "latencia_base_ms": 26.0,
    },
}

PALAVRAS_CHAVE = [
    "Comunicacao",
    "Comando",
    "Controle",
    "Contingencia",
    "Latencia",
    "Enlace",
    "Telemetria",
    "Redundancia",
    "Manutencao",
    "Alerta",
    "Habitat",
    "Medico",
    "Agricultura",
    "Energia",
    "Suporte",
]
