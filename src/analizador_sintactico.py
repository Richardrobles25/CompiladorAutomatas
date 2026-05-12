"""
================================================================================
  ANALIZADOR SINTÁCTICO — Compilador de Lenguaje de Comunicación Personal
  Herramienta: PLY (Python Lex-Yacc)
  Materia: Lenguajes y Autómatas
================================================================================
"""

import os
import json
import ply.yacc as yacc
from analizador_lexico import tokens, lexer, VOCAB, TOKENS_VOCAB

BASE = os.path.dirname(os.path.abspath(__file__))

# ══════════════════════════════════════════════════════════════════════════════
#  UTILIDADES
# ══════════════════════════════════════════════════════════════════════════════

def capitalizar(texto: str) -> str:
    """Primera letra mayúscula."""
    return texto[0].upper() + texto[1:] if texto else texto

def significado(token_valor: str, contexto: str = None) -> str:
    """Devuelve el significado de un token, ajustado por contexto si aplica."""
    ctx_tabla = VOCAB.get("contexto", {})
    if contexto and contexto in ctx_tabla and token_valor in ctx_tabla[contexto]:
        return ctx_tabla[contexto][token_valor]
    if token_valor in TOKENS_VOCAB:
        return TOKENS_VOCAB[token_valor][1]
    return token_valor

def categoria(token_valor: str) -> str:
    """Devuelve la categoría de un token."""
    return TOKENS_VOCAB.get(token_valor, ("desconocido",))[0]

def construir_frase(partes: list, contexto: str = None) -> str:
    """
    Toma una lista de (valor_token, tipo_semantico) y construye
    una frase natural en español usando las plantillas del vocabulario.
    """
    plantillas = VOCAB.get("plantillas", {})

    # Clasificar cada parte
    peticiones  = [(v, s) for v, s in partes if categoria(v) == "peticiones"]
    emociones   = [(v, s) for v, s in partes if categoria(v) == "emociones"]
    dolores     = [(v, s) for v, s in partes if categoria(v) == "dolor"]
    sociales    = [(v, s) for v, s in partes if categoria(v) == "social"]
    respuestas  = [(v, s) for v, s in partes if categoria(v) == "respuestas"]
    intensidad  = [(v, s) for v, s in partes if categoria(v) == "intensidad"]

    urgente = any(v == "sonido_largo" for v, _ in peticiones)

    sig_peticion  = significado(peticiones[0][0],  contexto) if peticiones  else None
    sig_emocion   = significado(emociones[0][0],   contexto) if emociones   else None
    sig_dolor     = significado(dolores[0][0],     contexto) if dolores     else None
    sig_social    = significado(sociales[0][0],    contexto) if sociales    else None
    sig_respuesta = significado(respuestas[0][0],  contexto) if respuestas  else None
    sig_intensidad= significado(intensidad[0][0],  contexto) if intensidad  else None

    # Agregar dolores adicionales
    if len(dolores) > 1:
        extras = [significado(v, contexto) for v, _ in dolores[1:]]
        sig_dolor += " y también " + " y ".join(extras)

    # ── Elegir plantilla según combinación ───────────────────────────────────

    # Urgencia
    if urgente and dolores:
        return f"¡{capitalizar(sig_dolor)}! {capitalizar(sig_peticion)}, por favor ayúdenme."

    if urgente and peticiones:
        tmpl = plantillas.get("urgencia", "¡{peticion_cap}! Es urgente.")
        return tmpl.format(peticion_cap=capitalizar(sig_peticion))

    # Dolor + petición
    if dolores and peticiones:
        if sig_intensidad:
            return f"{capitalizar(sig_intensidad)}, {sig_dolor}. Por eso me gustaría {sig_peticion}, por favor."
        tmpl = plantillas.get("dolor_con_peticion", "{dolor_cap}. Por eso me gustaría {peticion}, por favor.")
        return tmpl.format(dolor_cap=capitalizar(sig_dolor), peticion=sig_peticion)

    # Dolor + social
    if dolores and sociales:
        return f"{capitalizar(sig_dolor)}. {capitalizar(sig_social)}."

    # Dolor solo
    if dolores:
        if sig_intensidad:
            return f"{capitalizar(sig_intensidad)}, {sig_dolor}. Necesito ayuda."
        tmpl = plantillas.get("dolor_simple", "{dolor_cap}. Necesito ayuda.")
        return tmpl.format(dolor_cap=capitalizar(sig_dolor))

    # Social + emoción
    if sociales and emociones:
        tmpl = plantillas.get("social_con_emocion", "{emocion_cap}. {social_cap}.")
        return tmpl.format(emocion_cap=capitalizar(sig_emocion), social_cap=capitalizar(sig_social))

    # Saludo
    if sociales and any(v == "saludar_mano" for v, _ in sociales):
        tmpl = plantillas.get("saludo", "{social_cap}.")
        return tmpl.format(social_cap=capitalizar(sig_social))

    # Despedida
    if sociales and any(v == "despedir_mano" for v, _ in sociales):
        tmpl = plantillas.get("despedida", "{social_cap}.")
        return tmpl.format(social_cap=capitalizar(sig_social))

    # Social solo
    if sociales:
        tmpl = plantillas.get("social_simple", "{social_cap}.")
        return tmpl.format(social_cap=capitalizar(sig_social))

    # Emoción + petición
    if emociones and peticiones:
        if sig_intensidad:
            return f"{capitalizar(sig_emocion)}. Con {sig_intensidad}, me gustaría {sig_peticion}, por favor."
        tmpl = plantillas.get("peticion_con_emocion", "{emocion_cap} y me gustaría {peticion}, por favor.")
        return tmpl.format(emocion_cap=capitalizar(sig_emocion), peticion=sig_peticion)

    # Petición sola
    if peticiones:
        if sig_intensidad:
            return f"{capitalizar(sig_intensidad)}, me gustaría {sig_peticion}, por favor."
        tmpl = plantillas.get("peticion_simple", "Me gustaría {peticion}, por favor.")
        return tmpl.format(peticion=sig_peticion)

    # Emoción sola
    if emociones:
        tmpl = plantillas.get("emocion_simple", "{emocion_cap}.")
        return tmpl.format(emocion_cap=capitalizar(sig_emocion))

    # Respuesta
    if respuestas:
        tmpl = plantillas.get("confirmacion", "{respuesta_cap}.")
        return tmpl.format(respuesta_cap=capitalizar(sig_respuesta))

    return "(expresión no reconocida)"


# ══════════════════════════════════════════════════════════════════════════════
#  GRAMÁTICA (PLY Yacc)
# ══════════════════════════════════════════════════════════════════════════════

# Variable global de contexto activo
_contexto_activo = None

def p_programa(p):
    """programa : contexto_opt expresion"""
    p[0] = p[2]

def p_contexto_opt_con(p):
    """contexto_opt : CONTEXTO"""
    global _contexto_activo
    _contexto_activo = p[1]
    p[0] = p[1]

def p_contexto_opt_vacio(p):
    """contexto_opt : """
    global _contexto_activo
    _contexto_activo = None
    p[0] = None

def p_expresion_secuencia(p):
    """expresion : expresion MAS token_simple"""
    p[0] = p[1] + [p[3]]

def p_expresion_simple(p):
    """expresion : token_simple"""
    p[0] = [p[1]]

# ── Tokens de petición ────────────────────────────────────────────────────────
def p_token_peticion(p):
    """token_simple : SONIDO_CORTO
                    | SONIDO_LARGO
                    | SENALAR_VASO
                    | SENALAR_COMIDA
                    | SENALAR_PUERTA
                    | SENALAR_CAMA
                    | SENALAR_BANO
                    | SENALAR_ROPA
                    | SENALAR_MEDICINA
                    | SENALAR_TELEFONO
                    | SENALAR_TELEVISION
                    | SENALAR_VENTANA
                    | EXTENDER_MANO
                    | SENALAR_RELOJ"""
    p[0] = (p[1], "peticion")

# ── Tokens de emoción ─────────────────────────────────────────────────────────
def p_token_emocion(p):
    """token_simple : MANOS_ARRIBA
                    | MANOS_ABAJO
                    | AGITAR_MANOS
                    | SONRISA
                    | FRUNCIR_CENO
                    | ABRAZAR_CUERPO
                    | SENALAR_CORAZON
                    | CUBRIR_CARA
                    | SALTAR
                    | BOSTEZAR"""
    p[0] = (p[1], "emocion")

# ── Tokens de dolor ───────────────────────────────────────────────────────────
def p_token_dolor(p):
    """token_simple : CABEZA_ABAJO
                    | SENALAR_CABEZA
                    | SENALAR_ESTOMAGO
                    | SENALAR_PECHO
                    | SENALAR_GARGANTA
                    | SENALAR_ESPALDA
                    | SENALAR_PIERNA
                    | TEMBLAR
                    | SUDAR
                    | SENALAR_OJOS
                    | SENALAR_OIDOS
                    | SENALAR_DIENTES"""
    p[0] = (p[1], "dolor")

# ── Tokens sociales ───────────────────────────────────────────────────────────
def p_token_social(p):
    """token_simple : APLAUDIR
                    | SENALAR_PERSONA
                    | SALUDAR_MANO
                    | DESPEDIR_MANO
                    | SENALAR_FAMILIA
                    | SENALAR_DOCTOR
                    | SENALAR_ENFERMERA
                    | PULGAR_ARRIBA
                    | PULGAR_ABAJO
                    | SENALAR_AYUDA"""
    p[0] = (p[1], "social")

# ── Tokens de respuesta ───────────────────────────────────────────────────────
def p_token_respuesta(p):
    """token_simple : ASENTIR
                    | NEGAR
                    | ENCOGER_HOMBROS
                    | SENALAR_SI
                    | SENALAR_NO
                    | ESPERAR_MANO
                    | REPETIR_GESTO"""
    p[0] = (p[1], "respuesta")

# ── Tokens de intensidad ──────────────────────────────────────────────────────
def p_token_intensidad(p):
    """token_simple : MUY
                    | POCO
                    | MUCHO"""
    p[0] = (p[1], "intensidad")

def p_error(p):
    if p:
        print(f"  ✗  Error sintáctico en token: '{p.value}'")
    else:
        print("  ✗  Error sintáctico: expresión incompleta")

parser = yacc.yacc()


# ══════════════════════════════════════════════════════════════════════════════
#  FUNCIÓN PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

def compilar(entrada: str, contexto: str = None):
    """
    Ejecuta el pipeline completo:
      1. Análisis léxico  → identifica tokens
      2. Análisis sintáctico → valida estructura
      3. Análisis semántico → construye frase natural
    """
    global _contexto_activo
    _contexto_activo = contexto

    print("=" * 68)
    print(f"  ENTRADA   : {entrada}")
    print(f"  CONTEXTO  : {contexto if contexto else '(sin contexto)'}")
    print("-" * 68)

    # ── 1. Léxico ─────────────────────────────────────────────────────────────
    lexer.input(entrada)
    print(f"  {'TOKEN':<28} {'VALOR':<24} {'CATEGORÍA'}")
    print(f"  {'-':<28} {'-':<24} {'-'}")

    for tok in lexer:
        if tok.type == "MAS":
            print(f"  {'MAS':<28} {'+':<24} operador")
            continue
        if tok.type == "CONTEXTO":
            print(f"  {'CONTEXTO':<28} {tok.value:<24} contexto")
            continue
        cat = categoria(tok.value)
        sig = significado(tok.value, contexto)
        print(f"  {tok.type:<28} {tok.value:<24} {cat}  → \"{sig}\"")

    # ── 2. Sintáctico + 3. Semántico ──────────────────────────────────────────
    resultado = parser.parse(entrada, lexer=lexer.clone())

    if resultado:
        frase = construir_frase(resultado, contexto)
        print("-" * 68)
        print(f"  TOKENS    : {' + '.join(v for v, _ in resultado)}")
        print(f"  FRASE     : {frase}")
    else:
        frase = "(error en el análisis)"
        print(f"  FRASE     : {frase}")

    print("=" * 68)
    print()
    return frase


# ══════════════════════════════════════════════════════════════════════════════
#  CASOS DE PRUEBA
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n╔════════════════════════════════════════════════════════════════════╗")
    print("║       COMPILADOR DE LENGUAJE DE COMUNICACIÓN PERSONAL             ║")
    print("║            Análisis Léxico + Sintáctico + Semántico               ║")
    print("╚════════════════════════════════════════════════════════════════════╝\n")

    casos = [
        # (entrada,                                        contexto,  descripción)
        
        ("señalar_estomago + sonrisa + señalar_medicina",
         None,     "Múltiples dolores + petición")

    ]

    for entrada, ctx, desc in casos:
        print(f"  ▶  {desc}")
        compilar(entrada, ctx)
