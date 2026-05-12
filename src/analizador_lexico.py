"""
================================================================================
  ANALIZADOR LÉXICO — Compilador de Lenguaje de Comunicación Personal
  Herramienta: PLY (Python Lex-Yacc)
  Materia: Lenguajes y Autómatas
================================================================================
"""

import os
import ply.lex as lex
import json

BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "vocabulario.json"), "r", encoding="utf-8") as f:
    VOCAB = json.load(f)

TOKENS_VOCAB = {}
for categoria, items in VOCAB["tokens"].items():
    for token, significado in items.items():
        TOKENS_VOCAB[token] = (categoria, significado)

tokens = (
    # Peticiones
    "SONIDO_CORTO", "SONIDO_LARGO",
    "SENALAR_VASO", "SENALAR_COMIDA", "SENALAR_PUERTA", "SENALAR_CAMA",
    "SENALAR_BANO", "SENALAR_ROPA", "SENALAR_MEDICINA", "SENALAR_TELEFONO",
    "SENALAR_TELEVISION", "SENALAR_VENTANA", "EXTENDER_MANO", "SENALAR_RELOJ",
    # Emociones
    "MANOS_ARRIBA", "MANOS_ABAJO", "AGITAR_MANOS", "SONRISA", "FRUNCIR_CENO",
    "ABRAZAR_CUERPO", "SENALAR_CORAZON", "CUBRIR_CARA", "SALTAR", "BOSTEZAR",
    # Dolor
    "CABEZA_ABAJO", "SENALAR_CABEZA", "SENALAR_ESTOMAGO", "SENALAR_PECHO",
    "SENALAR_GARGANTA", "SENALAR_ESPALDA", "SENALAR_PIERNA", "TEMBLAR",
    "SUDAR", "SENALAR_OJOS", "SENALAR_OIDOS", "SENALAR_DIENTES",
    # Social
    "APLAUDIR", "SENALAR_PERSONA", "SALUDAR_MANO", "DESPEDIR_MANO",
    "SENALAR_FAMILIA", "SENALAR_DOCTOR", "SENALAR_ENFERMERA",
    "PULGAR_ARRIBA", "PULGAR_ABAJO", "SENALAR_AYUDA",
    # Respuestas
    "ASENTIR", "NEGAR", "ENCOGER_HOMBROS", "SENALAR_SI", "SENALAR_NO",
    "ESPERAR_MANO", "REPETIR_GESTO",
    # Intensidad
    "MUY", "POCO", "MUCHO",
    # Operadores
    "MAS", "CONTEXTO",
)

# ── Reglas léxicas ─────────────────────────────────────────────────────────────
# IMPORTANTE: las reglas más largas van primero para evitar conflictos

# Peticiones
def t_SONIDO_LARGO(t):      r'sonido_largo';        return t
def t_SONIDO_CORTO(t):      r'sonido_corto';        return t
def t_SENALAR_TELEVISION(t):r'señalar_television';  return t
def t_SENALAR_MEDICINA(t):  r'señalar_medicina';    return t
def t_SENALAR_TELEFONO(t):  r'señalar_telefono';    return t
def t_SENALAR_VENTANA(t):   r'señalar_ventana';     return t
def t_SENALAR_COMIDA(t):    r'señalar_comida';      return t
def t_SENALAR_PUERTA(t):    r'señalar_puerta';      return t
def t_SENALAR_RELOJ(t):     r'señalar_reloj';       return t
def t_SENALAR_VASO(t):      r'señalar_vaso';        return t
def t_SENALAR_CAMA(t):      r'señalar_cama';        return t
def t_SENALAR_BANO(t):      r'señalar_bano';        return t
def t_SENALAR_ROPA(t):      r'señalar_ropa';        return t
def t_EXTENDER_MANO(t):     r'extender_mano';       return t

# Emociones
def t_MANOS_ARRIBA(t):      r'manos_arriba';        return t
def t_MANOS_ABAJO(t):       r'manos_abajo';         return t
def t_AGITAR_MANOS(t):      r'agitar_manos';        return t
def t_ABRAZAR_CUERPO(t):    r'abrazar_cuerpo';      return t
def t_SENALAR_CORAZON(t):   r'señalar_corazon';     return t
def t_CUBRIR_CARA(t):       r'cubrir_cara';         return t
def t_FRUNCIR_CENO(t):      r'fruncir_ceno';        return t
def t_SONRISA(t):           r'sonrisa';             return t
def t_SALTAR(t):            r'saltar';              return t
def t_BOSTEZAR(t):          r'bostezar';            return t

# Dolor
def t_SENALAR_ESTOMAGO(t):  r'señalar_estomago';    return t
def t_SENALAR_GARGANTA(t):  r'señalar_garganta';    return t
def t_SENALAR_ESPALDA(t):   r'señalar_espalda';     return t
def t_SENALAR_DIENTES(t):   r'señalar_dientes';     return t
def t_SENALAR_PIERNA(t):    r'señalar_pierna';      return t
def t_CABEZA_ABAJO(t):      r'cabeza_abajo';        return t
def t_SENALAR_CABEZA(t):    r'señalar_cabeza';      return t
def t_SENALAR_PECHO(t):     r'señalar_pecho';       return t
def t_SENALAR_OIDOS(t):     r'señalar_oidos';       return t
def t_SENALAR_OJOS(t):      r'señalar_ojos';        return t
def t_TEMBLAR(t):           r'temblar';             return t
def t_SUDAR(t):             r'sudar';               return t

# Social
def t_SENALAR_ENFERMERA(t): r'señalar_enfermera';   return t
def t_SENALAR_FAMILIA(t):   r'señalar_familia';     return t
def t_SENALAR_PERSONA(t):   r'señalar_persona';     return t
def t_SENALAR_DOCTOR(t):    r'señalar_doctor';      return t
def t_SENALAR_AYUDA(t):     r'señalar_ayuda';       return t
def t_SALUDAR_MANO(t):      r'saludar_mano';        return t
def t_DESPEDIR_MANO(t):     r'despedir_mano';       return t
def t_PULGAR_ARRIBA(t):     r'pulgar_arriba';       return t
def t_PULGAR_ABAJO(t):      r'pulgar_abajo';        return t
def t_APLAUDIR(t):          r'aplaudir';            return t

# Respuestas
def t_ENCOGER_HOMBROS(t):   r'encoger_hombros';     return t
def t_ESPERAR_MANO(t):      r'esperar_mano';        return t
def t_REPETIR_GESTO(t):     r'repetir_gesto';       return t
def t_SENALAR_SI(t):        r'señalar_si';          return t
def t_SENALAR_NO(t):        r'señalar_no';          return t
def t_ASENTIR(t):           r'asentir';             return t
def t_NEGAR(t):             r'negar';               return t

# Intensidad
def t_MUCHO(t):             r'mucho';               return t
def t_POCO(t):              r'poco';                return t
def t_MUY(t):               r'muy';                 return t

# Operadores
def t_MAS(t):
    r'\+'
    return t

def t_CONTEXTO(t):
    r'\[(manana|noche|comida|dolor)\]'
    t.value = t.value[1:-1]
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"  ⚠  Token desconocido: '{t.value.split()[0]}' en columna {t.lexpos}")
    t.lexer.skip(len(t.value.split()[0]))

lexer = lex.lex()
