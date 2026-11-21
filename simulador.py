#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SIMULADOR INTERACTIVO PEU SUNASS - ECONOMÍA (VERSIÓN 2.0)
=========================================================
Banco oficial consolidado: 10 Módulos | 900 Preguntas
Mejoras v2.0:
  - Preservación estricta del orden y de cadenas de preguntas dependientes.
  - Inclusión de premisa de contexto para preguntas encadenadas.
  - Registro de preguntas saltadas [S] en el Cuaderno de Estudio.
  - Modos de estudio secuencial por bloques temáticos (A, B, C).
  - Filtros avanzados en el Cuaderno de Repaso (Falladas vs Saltadas).
"""

import os
import sys
import json
import re
import random
import time
import textwrap

if os.name == "nt":
    os.system("")
    for _stream in (sys.stdout, sys.stderr):
        if hasattr(_stream, "reconfigure"):
            _stream.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "banco_preguntas_consolidado.json")
ERRORS_FILE = os.path.join(BASE_DIR, "cuaderno_errores.json")
STATS_FILE = os.path.join(BASE_DIR, "historial_simulacros.json")

# ANSI Color Codes
CYAN = "\033[96m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

MODULE_NAMES = {
    1: "Módulo I: Teoría del Consumidor",
    2: "Módulo II: Teoría del Productor",
    3: "Módulo III: Competencia Perfecta",
    4: "Módulo IV: Equilibrio General y Bienestar",
    5: "Módulo V: Monopolio y Discriminación",
    6: "Módulo VI: Mercados de Factores",
    7: "Módulo VII: Competencia Imperfecta",
    8: "Módulo VIII: Otras Fallas de Mercado",
    9: "Módulo IX: Econometría",
    10: "Módulo X: Finanzas Corporativas y Proyectos"
}

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def load_database():
    if not os.path.exists(DB_FILE):
        print(f"{RED}Error: No se encontró la base de datos en {DB_FILE}.{RESET}")
        sys.exit(1)
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_errors():
    if not os.path.exists(ERRORS_FILE):
        return []
    try:
        with open(ERRORS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_errors(errors):
    with open(ERRORS_FILE, "w", encoding="utf-8") as f:
        json.dump(errors, f, ensure_ascii=False, indent=2)

def load_stats():
    if not os.path.exists(STATS_FILE):
        return []
    try:
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_stats(stats):
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

def print_banner():
    clear_screen()
    print(f"{CYAN}{BOLD}{'='*78}{RESET}")
    print(f"{BOLD}{YELLOW}   ★ SIMULADOR INTERACTIVO DE ADMISIÓN PEU SUNASS - ECONOMÍA v2.0 ★{RESET}")
    print(f"{DIM}        Superintendencia Nacional de Servicios de Saneamiento | Edición 2026{RESET}")
    print(f"{CYAN}{BOLD}{'='*78}{RESET}\n")

# -------------------------------------------------------------
# Lógica de Agrupamiento y Preservación de Cadenas de Preguntas
# -------------------------------------------------------------
def _natural_sort_key(q):
    return (q.get("module_num", 0), q.get("q_num", 0))

def hydrate_questions(questions, all_db=None):
    """Actualiza metadatos de preguntas guardadas usando el banco maestro."""
    by_id = {q["id"]: q for q in (all_db or [])}
    return [{**q, **by_id[q["id"]]} if q["id"] in by_id and by_id[q["id"]] is not q else q for q in (questions or [])]

def ensure_prerequisites(questions, all_db=None):
    """
    Garantiza que toda pregunta dependiente vaya precedida por sus preguntas
    previas obligatorias (depends_on / parent_id), hidratando metadatos desde
    el banco actualizado y manteniendo orden estricto sin duplicados.
    """
    by_id = {q["id"]: q for q in (all_db or [])}
    for q in (questions or []):
        by_id.setdefault(q["id"], q)

    hydrated = hydrate_questions(questions, all_db)

    emitted = set()
    ordered = []

    def get_missing_ancestors(item):
        stack = [item]
        seen = {item["id"]}
        ancestors = []
        while stack:
            cur = stack.pop()
            for ref_id in (cur.get("depends_on"), cur.get("parent_id")):
                if ref_id and ref_id not in seen and ref_id not in emitted and ref_id in by_id:
                    seen.add(ref_id)
                    parent_q = by_id[ref_id]
                    ancestors.append(parent_q)
                    stack.append(parent_q)
        ancestors.sort(key=_natural_sort_key)
        return ancestors

    for q in hydrated:
        if q["id"] in emitted:
            continue
        for anc in get_missing_ancestors(q):
            if anc["id"] not in emitted:
                emitted.add(anc["id"])
                ordered.append(anc)
        if q["id"] not in emitted:
            emitted.add(q["id"])
            ordered.append(q)

    return ordered

def get_clusters(questions):
    """
    Agrupa preguntas en clusters atómicos.
    Las preguntas dependientes quedan unidas a su pregunta raíz en orden estricto.
    """
    clusters = {}
    order = []
    for q in questions:
        cid = q.get("cluster_id") or q["id"]
        if cid not in clusters:
            clusters[cid] = []
            order.append(cid)
        clusters[cid].append(q)
    return [sorted(clusters[cid], key=_natural_sort_key) for cid in order]

def sample_clustered(questions, target_n, all_db=None):
    """
    Muestrea preguntas aleatorias respetando que ninguna cadena dependiente
    se desordene ni se corte por la mitad.
    """
    clusters = get_clusters(questions)
    random.shuffle(clusters)
    chosen_clusters = []
    count = 0
    for c in clusters:
        if count >= target_n and len(chosen_clusters) > 0:
            break
        chosen_clusters.append(c)
        count += len(c)

    # Si coinciden varios sub-clusters de un mismo escenario, ordenarlos cronológicamente
    scenario_slots = {}
    for idx, c in enumerate(chosen_clusters):
        sc = c[0].get("scenario_id") if c else None
        if sc:
            scenario_slots.setdefault(sc, []).append(idx)
    for indices in scenario_slots.values():
        if len(indices) > 1:
            sorted_clusters = sorted((chosen_clusters[i] for i in indices), key=lambda c: _natural_sort_key(c[0]))
            for slot_idx, c in zip(indices, sorted_clusters):
                chosen_clusters[slot_idx] = c

    selected = []
    for c in chosen_clusters:
        selected.extend(c)
    return ensure_prerequisites(selected, all_db if all_db is not None else questions)

_CLI_SYMBOLS = {
    "alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ", "epsilon": "ε",
    "varepsilon": "ε", "lambda": "λ", "rho": "ρ", "sigma": "σ", "tau": "τ",
    "pi": "π", "Pi": "Π", "Delta": "Δ", "Sigma": "Σ", "chi": "χ",
    "partial": "∂", "implies": "⇒", "approx": "≈", "neq": "≠",
    "ge": "≥", "geq": "≥", "le": "≤", "leq": "≤", "times": "×",
    "cdot": "·", "pm": "±", "sum": "∑", "int": "∫", "in": "∈",
    "infty": "∞", "dots": "…", "sim": "∼",
}
_SUP_MAP = str.maketrans("0123456789+-=n()*", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼ⁿ⁽⁾*")
_SUB_MAP = str.maketrans("0123456789+-=()aeijoprx", "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑᵢⱼₒₚᵣₓ")

def _read_tex_group(s, pos):
    while pos < len(s) and s[pos] == " ":
        pos += 1
    if pos >= len(s):
        return "", pos
    if s[pos] == "{":
        pos += 1
        depth = 1
        start = pos
        while pos < len(s) and depth > 0:
            if s[pos] == "\\" and pos + 1 < len(s):
                pos += 2
                continue
            if s[pos] == "{":
                depth += 1
            elif s[pos] == "}":
                depth -= 1
                if depth == 0:
                    return s[start:pos], pos + 1
            pos += 1
        return s[start:], pos
    if s[pos] == "\\" and pos + 1 < len(s):
        m = re.match(r"\\[a-zA-Z]+", s[pos:])
        if m:
            return m.group(0), pos + len(m.group(0))
        return s[pos:pos + 2], pos + 2
    return s[pos], pos + 1

def _tex_expr_to_unicode(expr):
    out = []
    i = 0
    while i < len(expr):
        ch = expr[i]
        if ch in ("^", "_"):
            grp, i = _read_tex_group(expr, i + 1)
            rendered = _tex_expr_to_unicode(grp)
            cmap = _SUP_MAP if ch == "^" else _SUB_MAP
            if rendered and all(ord(c) in cmap for c in rendered):
                out.append(rendered.translate(cmap))
            elif ch == "^":
                out.append(f"^({rendered})" if len(rendered) > 1 else f"^{rendered}")
            else:
                out.append(f"_{rendered}")
            continue
        if ch == "\\" and i + 1 < len(expr):
            m = re.match(r"^\\([a-zA-Z]+)", expr[i:])
            if m:
                cmd = m.group(1)
                p = i + len(m.group(0))
                if cmd in ("frac", "dfrac"):
                    num, p1 = _read_tex_group(expr, p)
                    den, p2 = _read_tex_group(expr, p1)
                    n_s = _tex_expr_to_unicode(num).strip()
                    d_s = _tex_expr_to_unicode(den).strip()
                    n_fmt = f"({n_s})" if any(op in n_s for op in "+-/× ") else n_s
                    d_fmt = f"({d_s})" if any(op in d_s for op in "+-/× ") else d_s
                    out.append(f"{n_fmt}/{d_fmt}")
                    i = p2
                    continue
                if cmd == "sqrt":
                    deg = ""
                    if p < len(expr) and expr[p] == "[":
                        end_b = expr.find("]", p)
                        if end_b != -1:
                            deg = expr[p + 1:end_b]
                            p = end_b + 1
                    body, p1 = _read_tex_group(expr, p)
                    b_s = _tex_expr_to_unicode(body)
                    prefix = "∛" if deg == "3" else (f"{deg.translate(_SUP_MAP)}√" if deg and all(c in _SUP_MAP for c in deg) else "√")
                    out.append(f"{prefix}({b_s})")
                    i = p1
                    continue
                if cmd == "text":
                    txt, p1 = _read_tex_group(expr, p)
                    out.append(txt)
                    i = p1
                    continue
                if cmd in ("hat", "bar", "tilde", "widehat"):
                    body, p1 = _read_tex_group(expr, p)
                    b_s = _tex_expr_to_unicode(body)
                    comb = {"bar": "\u0304", "tilde": "\u0303"}.get(cmd, "\u0302")
                    out.append(b_s + comb if len(b_s) <= 2 else f"{cmd}({b_s})")
                    i = p1
                    continue
                if cmd in ("min", "max", "ln"):
                    out.append(cmd)
                    i = p
                    continue
                if cmd in ("left", "right"):
                    i = p
                    continue
                if cmd in _CLI_SYMBOLS:
                    out.append(_CLI_SYMBOLS[cmd])
                    i = p
                    continue
                out.append(cmd)
                i = p
                continue
            nxt = expr[i + 1]
            out.append(" " if nxt in (",", ";", " ") else nxt)
            i += 2
            continue
        if ch in ("{", "}"):
            i += 1
            continue
        out.append(ch)
        i += 1
    return "".join(out)

def format_cli_math(text):
    """Convierte bloques TeX ($...$) a Unicode legible para terminal."""
    if not text:
        return ""
    parts = re.split(r"(\$[^$]+\$)", str(text))
    res = []
    for idx, part in enumerate(parts):
        if idx % 2 == 1 and len(part) >= 2:
            res.append(_tex_expr_to_unicode(part[1:-1]))
        else:
            res.append(part)
    return "".join(res)

def ask_question(item, index, total, tutor_mode=True):
    print(f"\n{BOLD}{CYAN}------------------------------------------------------------------------------{RESET}")
    print(f"{BOLD}{BLUE}[{index}/{total}] {item['module_name'].upper()}{RESET}  {DIM}(ID: {item['id']}){RESET}")
    if item.get("topic"):
        print(f"{DIM}Tema: {item['topic']}{RESET}")
    print(f"{BOLD}{CYAN}------------------------------------------------------------------------------{RESET}\n")

    # Si la pregunta depende de una premisa anterior o caso base, mostrar el contexto visual
    if item.get("context_premise"):
        ref = item.get("parent_id") or item.get("depends_on")
        header_label = f"PREMISA / CONTEXTO VINCULADO ({ref})" if ref else f"CONTEXTO DEL CASO ({item.get('cluster_id') or item['id']})"
        pad = "─" * max(4, 52 - len(header_label))
        print(f"  {YELLOW}{BOLD}┌─ 📌 {header_label} {pad}┐{RESET}")
        wrapped_premise = textwrap.fill(format_cli_math(item["context_premise"]), width=70, initial_indent="  │ ", subsequent_indent="  │ ")
        print(f"{DIM}{wrapped_premise}{RESET}")
        print(f"  {YELLOW}{BOLD}└{'─'*72}┘{RESET}\n")

    # Enunciado de la pregunta
    wrapped_q = textwrap.fill(format_cli_math(item["question"]), width=76, initial_indent="  ", subsequent_indent="  ")
    print(f"{BOLD}{wrapped_q}{RESET}\n")

    # Alternativas
    letters = ["A", "B", "C", "D"]
    for i, opt in enumerate(item["options"]):
        wrapped_opt = textwrap.fill(format_cli_math(opt), width=72, initial_indent="     ", subsequent_indent="     ")
        print(f"  {BOLD}{YELLOW}[{letters[i]}]{RESET} {wrapped_opt[5:]}")

    print()
    start_time = time.time()
    while True:
        try:
            choice = input(f"{BOLD}Tu respuesta [A/B/C/D] o [S]altar / [Q]uit: {RESET}").strip().upper()
        except (KeyboardInterrupt, EOFError):
            return None, 0

        if choice in ["A", "B", "C", "D", "S", "Q"]:
            elapsed = time.time() - start_time
            break
        print(f"{RED}Opción inválida. Ingrese A, B, C, D, S o Q.{RESET}")

    if choice == "Q":
        return "QUIT", elapsed

    correct_key = item["correct_key"]
    is_correct = (choice == correct_key)
    is_skipped = (choice == "S")

    if tutor_mode:
        print()
        if is_skipped:
            print(f"{YELLOW}↷ Pregunta saltada (se enviará a tu cuaderno para estudiar).{RESET} La respuesta correcta era {BOLD}[{correct_key}]{RESET}.")
        elif is_correct:
            print(f"{GREEN}{BOLD}✔ ¡CORRECTO!{RESET} {GREEN}Marcaste [{choice}] en {elapsed:.1f} segundos.{RESET}")
        else:
            print(f"{RED}{BOLD}✘ INCORRECTO.{RESET} {RED}Marcaste [{choice}], pero la clave correcta es {BOLD}[{correct_key}]{RESET}.")

        print(f"\n{CYAN}{BOLD}📖 SOLUCIONARIO:{RESET}")
        wrapped_expl = textwrap.fill(format_cli_math(item["explanation"]), width=74, initial_indent="  ", subsequent_indent="  ")
        print(f"{DIM}{wrapped_expl}{RESET}\n")
        try:
            input(f"{DIM}[Presione ENTER para continuar...]{RESET}")
        except (KeyboardInterrupt, EOFError):
            pass

    return {
        "item": item,
        "user_choice": choice,
        "correct_key": correct_key,
        "is_correct": is_correct,
        "is_skipped": is_skipped,
        "time": elapsed
    }, elapsed

def run_quiz(questions, title="SIMULACRO", tutor_mode=True):
    total = len(questions)
    results = []
    total_time = 0

    print_banner()
    print(f"{BOLD}{MAGENTA}MODO SELECCIONADO: {title}{RESET}")
    print(f"Número de preguntas: {BOLD}{total}{RESET} | Retroalimentación: {BOLD}{'Inmediata (Tutor)' if tutor_mode else 'Al finalizar (Examen)'}{RESET}\n")
    input(f"{GREEN}{BOLD}Presione ENTER para comenzar el cronómetro...{RESET}")

    for idx, q in enumerate(questions, 1):
        clear_screen()
        res, t = ask_question(q, idx, total, tutor_mode=tutor_mode)
        if res == "QUIT" or res is None:
            print(f"\n{YELLOW}Simulacro interrumpido por el usuario.{RESET}")
            break
        results.append(res)
        total_time += t

    if not results:
        return

    show_summary(results, total_time, title)

def show_summary(results, total_time, title):
    clear_screen()
    correct_count = sum(1 for r in results if r["is_correct"])
    skipped_count = sum(1 for r in results if r["is_skipped"])
    incorrect_count = len(results) - correct_count - skipped_count
    score_pct = (correct_count / len(results)) * 100 if results else 0

    print(f"{CYAN}{BOLD}{'='*78}{RESET}")
    print(f"{BOLD}{YELLOW}           ★ RESULTADOS FINALES: {title.upper()} ★{RESET}")
    print(f"{CYAN}{BOLD}{'='*78}{RESET}\n")

    print(f"  Preguntas respondidas: {BOLD}{len(results)}{RESET}")
    print(f"  Aciertos:              {GREEN}{BOLD}{correct_count} ({score_pct:.1f}%){RESET}")
    print(f"  Errores:               {RED}{BOLD}{incorrect_count}{RESET}")
    print(f"  Saltadas p/ estudiar:  {YELLOW}{BOLD}{skipped_count}{RESET}")
    print(f"  Tiempo total:          {BOLD}{total_time / 60:.1f} minutos{RESET} ({total_time / len(results):.1f} s/preg)\n")

    # Desglose por Módulo
    print(f"{BOLD}{CYAN}Desglose por Módulo:{RESET}")
    mod_stats = {}
    for r in results:
        m_num = r["item"]["module_num"]
        m_name = r["item"]["module_name"]
        if m_num not in mod_stats:
            mod_stats[m_num] = {"name": m_name, "correct": 0, "skipped": 0, "total": 0}
        mod_stats[m_num]["total"] += 1
        if r["is_correct"]:
            mod_stats[m_num]["correct"] += 1
        elif r["is_skipped"]:
            mod_stats[m_num]["skipped"] += 1

    for m_num in sorted(mod_stats.keys()):
        s = mod_stats[m_num]
        pct = (s["correct"] / s["total"]) * 100
        color = GREEN if pct >= 70 else (YELLOW if pct >= 50 else RED)
        tag = "DOMINADO" if pct >= 70 else ("REGULAR" if pct >= 50 else "REFORZAR!")
        print(f"  • {s['name'][:36]:<36} {color}{s['correct']}/{s['total']} ({pct:5.1f}%) [{tag}]{RESET} (Saltadas: {s['skipped']})")

    # Guardar tanto falladas como saltadas en el cuaderno de errores
    items_to_save = []
    for r in results:
        if not r["is_correct"]:
            error_type = "saltada" if r["is_skipped"] else "fallada"
            item_copy = dict(r["item"])
            item_copy["error_type"] = error_type
            item_copy["logged_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            items_to_save.append(item_copy)

    if items_to_save:
        existing_errors = load_errors()
        existing_map = {e["id"]: i for i, e in enumerate(existing_errors)}
        added_count = 0
        updated_count = 0

        for item in items_to_save:
            qid = item["id"]
            if qid in existing_map:
                existing_errors[existing_map[qid]]["error_type"] = item["error_type"]
                existing_errors[existing_map[qid]]["logged_at"] = item["logged_at"]
                updated_count += 1
            else:
                existing_errors.append(item)
                existing_map[qid] = len(existing_errors) - 1
                added_count += 1

        save_errors(existing_errors)
        print(f"\n{YELLOW}📓 Se registraron {added_count} preguntas nuevas y {updated_count} actualizadas en tu Cuaderno de Estudio ({len(existing_errors)} acumuladas).{RESET}")

    # Guardar historial
    stats_history = load_stats()
    stats_history.append({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "title": title,
        "total": len(results),
        "correct": correct_count,
        "skipped": skipped_count,
        "pct": round(score_pct, 1),
        "time_seconds": round(total_time, 1)
    })
    save_stats(stats_history)

    print(f"\n{CYAN}{BOLD}{'='*78}{RESET}")
    input(f"{DIM}Presione ENTER para volver al menú principal...{RESET}")

def mode_simulacro_general(db):
    print_banner()
    print(f"{BOLD}{CYAN}CONFIGURAR SIMULACRO GENERAL TIPO EXAMEN SUNASS:{RESET}")
    print(f"{DIM}(Las preguntas encadenadas se presentarán siempre juntas y en orden lógico){RESET}\n")
    print("  1. Simulacro Express (30 preguntas)")
    print("  2. Simulacro Estándar (50 preguntas)")
    print("  3. Simulacro Completo Oficial (90 preguntas - 150 min)")
    print("  4. Cantidad personalizada")
    print("  5. Volver")

    sub = input(f"\n{BOLD}Seleccione una opción [1-5]: {RESET}").strip()
    if sub == "1":
        n = 30
    elif sub == "2":
        n = 50
    elif sub == "3":
        n = 90
    elif sub == "4":
        try:
            n = int(input("Ingrese el número de preguntas (1-900): ").strip())
            n = max(1, min(len(db), n))
        except ValueError:
            return
    else:
        return

    print(f"\n{BOLD}Tipo de retroalimentación:{RESET}")
    print("  1. Modo Tutor (muestra solucionario y desarrollo tras cada pregunta)")
    print("  2. Modo Examen Oficial (silencioso, cronometrado, resultados al final)")
    fb = input("Seleccione [1-2] (default: 1): ").strip()
    tutor_mode = (fb != "2")

    sampled = sample_clustered(db, n, all_db=db)
    run_quiz(sampled, title=f"Simulacro General ({len(sampled)} Preguntas)", tutor_mode=tutor_mode)

def mode_por_modulo(db):
    print_banner()
    print(f"{BOLD}{CYAN}SELECCIONE EL MÓDULO A ESTUDIAR:{RESET}\n")
    for m in range(1, 11):
        print(f"  {m:2d}. {MODULE_NAMES[m]}")
    print("  11. Volver")

    choice = input(f"\n{BOLD}Elija módulo [1-11]: {RESET}").strip()
    try:
        mod_num = int(choice)
        if mod_num not in MODULE_NAMES:
            return
    except ValueError:
        return

    mod_questions = sorted([q for q in db if q["module_num"] == mod_num], key=lambda x: x["q_num"])

    print(f"\n{BOLD}MODO DE ESTUDIO DEL MÓDULO:{RESET}")
    print(f"  {GREEN}{BOLD}[1]{RESET} {BOLD}Orden Secuencial Oficial (Recomendado){RESET} {DIM}- Bloques A, B, C en orden lógico (1 al 90){RESET}")
    print(f"  {YELLOW}{BOLD}[2]{RESET} Bloque A: Fundamentos Teóricos (Preguntas 1 a 30)")
    print(f"  {YELLOW}{BOLD}[3]{RESET} Bloque B: Cálculo y Optimización (Preguntas 31 a 65)")
    print(f"  {YELLOW}{BOLD}[4]{RESET} Bloque C: Casos Regulatorios y Saneamiento (Preguntas 66 a 90)")
    print(f"  {BLUE}{BOLD}[5]{RESET} Modo Aleatorio Clustered (Mantiene cadenas vinculadas juntas)")
    print("  6. Volver")

    sub = input(f"\n{BOLD}Seleccione modalidad [1-6] (default: 1): {RESET}").strip()

    if sub == "2":
        questions_to_run = mod_questions[0:30]
        title = f"{MODULE_NAMES[mod_num]} - Bloque A"
    elif sub == "3":
        questions_to_run = mod_questions[30:65]
        title = f"{MODULE_NAMES[mod_num]} - Bloque B"
    elif sub == "4":
        questions_to_run = mod_questions[65:90]
        title = f"{MODULE_NAMES[mod_num]} - Bloque C"
    elif sub == "5":
        try:
            n = int(input("¿Cuántas preguntas desea practicar? (1-90): ").strip())
            n = max(1, min(len(mod_questions), n))
        except ValueError:
            n = 20
        questions_to_run = sample_clustered(mod_questions, n, all_db=db)
        title = f"{MODULE_NAMES[mod_num]} - Aleatorio ({len(questions_to_run)} preg)"
    elif sub == "6":
        return
    else:
        # Default: Secuencial completo o rango
        print(f"\n¿Desea estudiar desde la pregunta 1 hasta la 90 o un rango específico?")
        print("  1. Todo el módulo completo (Preguntas 1 a 90)")
        print("  2. Especificar rango personalizado (ej. de la 30 a la 60)")
        rng = input("Opción [1-2] (default: 1): ").strip()
        if rng == "2":
            try:
                ini = int(input("Pregunta inicial (1-90): ").strip())
                fin = int(input("Pregunta final (1-90): ").strip())
                ini = max(1, min(90, ini))
                fin = max(ini, min(90, fin))
                questions_to_run = mod_questions[ini-1:fin]
                title = f"{MODULE_NAMES[mod_num]} (Preguntas {ini} a {fin})"
            except ValueError:
                questions_to_run = mod_questions
                title = f"{MODULE_NAMES[mod_num]} (Completo 1-90)"
        else:
            questions_to_run = mod_questions
            title = f"{MODULE_NAMES[mod_num]} (Completo 1-90)"

    questions_to_run = ensure_prerequisites(questions_to_run, db)
    if sub == "5":
        title = f"{MODULE_NAMES[mod_num]} - Aleatorio ({len(questions_to_run)} preg)"
    run_quiz(questions_to_run, title=title, tutor_mode=True)

def mode_cuaderno_errores(db):
    errors = hydrate_questions(load_errors(), db)
    if not errors:
        print_banner()
        print(f"{GREEN}{BOLD}¡Felicidades! Tu Cuaderno de Estudio está al día (0 preguntas pendientes).{RESET}")
        print(f"{DIM}Cuando falles o saltes [S] preguntas en los simulacros, se registrarán aquí automáticamente.{RESET}\n")
        input(f"{DIM}Presione ENTER para volver...{RESET}")
        return

    falladas = [e for e in errors if e.get("error_type") == "fallada"]
    saltadas = [e for e in errors if e.get("error_type") == "saltada"]

    print_banner()
    print(f"{BOLD}{CYAN}📓 CUADERNO DE ESTUDIO Y REPASO ACTIVO:{RESET}\n")
    print(f"  • Total preguntas pendientes: {BOLD}{len(errors)}{RESET}")
    print(f"    - Preguntas falladas:      {RED}{BOLD}{len(falladas)}{RESET}")
    print(f"    - Preguntas saltadas [S]:  {YELLOW}{BOLD}{len(saltadas)}{RESET}\n")
    print("  1. Repasar TODAS las pendientes (Falladas + Saltadas)")
    print(f"  2. Repasar únicamente las FALLADAS ({len(falladas)})")
    print(f"  3. Repasar únicamente las SALTADAS ({len(saltadas)})")
    print("  4. Muestra rápida aleatoria (15 preguntas)")
    print("  5. Vaciar / limpiar el cuaderno de estudio")
    print("  6. Volver")

    choice = input(f"\n{BOLD}Seleccione una opción [1-6]: {RESET}").strip()

    if choice == "1":
        sampled = list(errors)
        title = "Repaso Completo de Errores y Saltadas"
    elif choice == "2":
        if not falladas:
            print(f"{GREEN}No tienes preguntas falladas registradas.{RESET}")
            time.sleep(1)
            return
        sampled = list(falladas)
        title = "Repaso de Preguntas Falladas"
    elif choice == "3":
        if not saltadas:
            print(f"{GREEN}No tienes preguntas saltadas registradas.{RESET}")
            time.sleep(1)
            return
        sampled = list(saltadas)
        title = "Repaso de Preguntas Saltadas"
    elif choice == "4":
        sampled = sample_clustered(errors, min(15, len(errors)), all_db=db)
        title = f"Muestra Rápida ({len(sampled)} preg)"
    elif choice == "5":
        confirm = input(f"{RED}¿Seguro que desea vaciar todo el cuaderno de repaso? (s/N): {RESET}").strip().lower()
        if confirm == "s":
            save_errors([])
            print(f"{GREEN}Cuaderno de estudio vaciado correctamente.{RESET}")
            time.sleep(1)
        return
    else:
        return

    sampled = ensure_prerequisites(sampled, db)
    if choice == "4":
        title = f"Muestra Rápida ({len(sampled)} preg)"

    # Ejecutar preguntas de repaso con opción de desmarcar
    total = len(sampled)
    results = []
    total_time = 0
    resolved_ids = []

    print_banner()
    print(f"{BOLD}{MAGENTA}MODALIDAD: {title}{RESET}")
    print(f"Preguntas por resolver: {BOLD}{total}{RESET}\n")
    input(f"{GREEN}{BOLD}Presione ENTER para comenzar el repaso...{RESET}")

    for idx, q in enumerate(sampled, 1):
        clear_screen()
        res, t = ask_question(q, idx, total, tutor_mode=True)
        if res == "QUIT" or res is None:
            break
        results.append(res)
        total_time += t
        if res["is_correct"]:
            resolved_ids.append(q["id"])

    # Remover preguntas dominadas del cuaderno
    if resolved_ids:
        updated_errors = [e for e in errors if e["id"] not in resolved_ids]
        save_errors(updated_errors)
        print(f"\n{GREEN}{BOLD}🎉 ¡Gran progreso! Acertaste {len(resolved_ids)} preguntas y han sido removidas de tus pendientes.{RESET}")
        time.sleep(2)

    if results:
        show_summary(results, total_time, title)

def mode_estadisticas(db):
    print_banner()
    history = load_stats()
    errors = load_errors()

    falladas = sum(1 for e in errors if e.get("error_type") == "fallada")
    saltadas = sum(1 for e in errors if e.get("error_type") == "saltada")

    print(f"{BOLD}{CYAN}📊 RADIOGRAFÍA Y ESTADÍSTICAS DE PREPARACIÓN:{RESET}\n")
    print(f"  • Banco total disponible:       {BOLD}900 preguntas{RESET} (10 módulos oficiales)")
    print(f"  • Pendientes en Cuaderno:       {BOLD}{len(errors)}{RESET} ({RED}{falladas} falladas{RESET}, {YELLOW}{saltadas} saltadas{RESET})")
    print(f"  • Sesiones registradas:         {BOLD}{len(history)}{RESET}\n")

    if history:
        print(f"{BOLD}Historial de sesiones recientes:{RESET}")
        print(f"{DIM}{'-'*75}{RESET}")
        print(f" {'Fecha':<19} {'Modalidad':<28} {'Score':<13} {'Tiempo':<9}")
        print(f"{DIM}{'-'*75}{RESET}")
        for h in history[-8:]:
            color = GREEN if h["pct"] >= 70 else (YELLOW if h["pct"] >= 50 else RED)
            skp = h.get("skipped", 0)
            score_str = f"{h['correct']}/{h['total']} ({h['pct']}%)"
            min_str = f"{h['time_seconds']/60:.1f} min"
            print(f" {h['timestamp']:<19} {h['title'][:26]:<28} {color}{score_str:<13}{RESET} {min_str:<9}")
        print(f"{DIM}{'-'*75}{RESET}")
    else:
        print(f"{DIM}Aún no has completado sesiones. ¡Inicia tu primer simulacro para medir tu avance!{RESET}")

    print()
    input(f"{DIM}Presione ENTER para volver al menú principal...{RESET}")

def main():
    db = load_database()

    while True:
        print_banner()
        errors = load_errors()
        err_badge = f"{YELLOW}({len(errors)} pendientes){RESET}" if errors else f"{GREEN}(0 pendientes){RESET}"

        print(f"{BOLD}SELECCIONE UNA MODALIDAD DE ENTRENAMIENTO:{RESET}\n")
        print(f"  {BOLD}{GREEN}[1]{RESET} ⚡ {BOLD}Simulacro General Tipo Examen SUNASS{RESET} {DIM}(30, 50 o 90 preg. con cadenas en orden){RESET}")
        print(f"  {BOLD}{BLUE}[2]{RESET} 🎯 {BOLD}Estudio por Módulo Específico{RESET} {DIM}(Secuencial Bloques A, B, C o Rango){RESET}")
        print(f"  {BOLD}{YELLOW}[3]{RESET} 📓 {BOLD}Cuaderno de Errores y Saltadas{RESET} {err_badge}")
        print(f"  {BOLD}{CYAN}[4]{RESET} 📊 {BOLD}Estadísticas y Radiografía de Nivel{RESET} {DIM}(Seguimiento histórico){RESET}")
        print(f"  {BOLD}{RED}[5]{RESET} 🚪 {BOLD}Salir{RESET}")

        choice = input(f"\n{BOLD}Ingrese su opción [1-5]: {RESET}").strip()

        if choice == "1":
            mode_simulacro_general(db)
        elif choice == "2":
            mode_por_modulo(db)
        elif choice == "3":
            mode_cuaderno_errores(db)
        elif choice == "4":
            mode_estadisticas(db)
        elif choice == "5":
            print(f"\n{GREEN}¡Muchos éxitos en el examen de SUNASS! Con disciplina la vacante es tuya.{RESET}\n")
            break

if __name__ == "__main__":
    main()
