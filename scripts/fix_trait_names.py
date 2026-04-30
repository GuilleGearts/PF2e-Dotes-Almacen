"""
Aplica correcciones manuales a traits_data.json usando los términos
canónicos de Devir (edición española oficial de Pathfinder 2e).
"""
import json, os

CORRECTIONS = {
    # === ANCESTRÍAS ===
    "android":      "Androide",
    "anadi":        "Anadi",
    "automaton":    "Autómata",
    "azarketi":     "Azarketi",
    "catfolk":      "Gente Gato",
    "dwarf":        "Enano",
    "elf":          "Elfo",         # Devir: Elfo, NO "Duende"
    "fetchling":    "Fetchling",
    "fleshwarp":    "Distorsionado",
    "gnome":        "Gnomo",
    "goblin":       "Goblin",       # Devir mantiene "Goblin"
    "halfling":     "Mediano",
    "hobgoblin":    "Hobgoblin",    # Devir mantiene "Hobgoblin"
    "human":        "Humano",
    "kitsune":      "Kitsune",
    "kobold":       "Kobold",       # Devir mantiene "Kobold"
    "leshy":        "Leshy",
    "lizardfolk":   "Lagartija",
    "orc":          "Orco",
    "ratfolk":      "Ratoide",
    "shoony":       "Shoony",
    "strix":        "Strix",
    "tengu":        "Tengu",
    "sprite":       "Sprite",
    "grippli":      "Grippli",
    "poppet":       "Muñeco",
    "goloma":       "Goloma",
    "shisk":        "Shisk",
    "nautilus":     "Náutilo",
    "skeleton":     "Esqueleto",
    "conrasu":      "Conrasu",

    # === CLASES ===
    "alchemist":    "Alquimista",
    "barbarian":    "Bárbaro",
    "bard":         "Bardo",
    "champion":     "Campeón",
    "cleric":       "Clérigo",
    "druid":        "Druida",
    "fighter":      "Guerrero",
    "investigator": "Investigador",
    "magus":        "Magus",
    "monk":         "Monje",
    "oracle":       "Oráculo",
    "psychic":      "Psíquico",
    "ranger":       "Explorador",   # Devir: Explorador
    "rogue":        "Pícaro",
    "sorcerer":     "Hechicero",
    "summoner":     "Invocador",
    "swashbuckler": "Espadachín",
    "thaumaturge":  "Taumaturgo",
    "witch":        "Bruja",
    "wizard":       "Mago",
    "inventor":     "Inventor",
    "gunslinger":   "Pistolero",
    "animist":      "Animista",

    # === TRADICIONES MÁGICAS ===
    "arcane":       "Arcano",
    "divine":       "Divino",
    "occult":       "Oculto",
    "primal":       "Primigenio",   # Devir: Primigenio

    # === TIPOS DE ACCIÓN / MECÁNICAS ===
    "attack":       "Ataque",
    "aura":         "Aura",
    "cantrip":      "Truco",        # Devir: Truco, NO "Broma"
    "concentrate":  "Concentración",
    "contingency":  "Contingencia",
    "curse":        "Maldición",
    "detection":    "Detección",
    "disease":      "Enfermedad",
    "emotion":      "Emoción",
    "fear":         "Miedo",
    "flourish":     "Exhibición",   # Devir: Exhibición
    "fortune":      "Fortuna",
    "general":      "General",
    "healing":      "Curación",     # Devir: Curación, NO "Cicatrización"
    "hex":          "Maleficio",
    "illusion":     "Ilusión",      # NO "Espejismo"
    "impulse":      "Impulso",
    "incorporeal":  "Incorpóreo",
    "light":        "Luz",
    "magical":      "Mágico",
    "manipulate":   "Manipulación",
    "mental":       "Mental",
    "mindless":     "Sin mente",    # Devir: Sin mente, NO "Imbécil"
    "misfortune":   "Infortunio",   # Devir: Infortunio
    "morph":        "Transformación",
    "move":         "Movimiento",
    "nonlethal":    "No letal",
    "oath":         "Juramento",
    "polymorph":    "Polimorfo",    # Devir: Polimorfo
    "press":        "Encadenado",   # Devir: Encadenado
    "skill":        "Habilidad",
    "sleep":        "Sueño",        # NO "Dormir"
    "sonic":        "Sónico",
    "spellshot":    "Conjuro",
    "spirit":       "Espíritu",
    "stance":       "Postura",
    "summoned":     "Convocado",
    "teleportation":"Teletransportación",
    "trap":         "Trampa",
    "visual":       "Visual",
    "auditory":     "Auditivo",

    # === TIPOS DE DAÑO / ELEMENTOS ===
    "acid":         "Ácido",
    "air":          "Aire",
    "cold":         "Frío",
    "darkness":     "Oscuridad",
    "death":        "Muerte",
    "earth":        "Tierra",
    "electricity":  "Electricidad",
    "fire":         "Fuego",
    "force":        "Fuerza",
    "negative":     "Negativo",
    "plant":        "Planta",
    "poison":       "Veneno",
    "positive":     "Positivo",
    "water":        "Agua",

    # === CRIATURAS ===
    "aberration":   "Aberración",
    "animal":       "Animal",
    "beast":        "Bestia",
    "celestial":    "Celestial",
    "construct":    "Constructo",
    "dragon":       "Dragón",
    "elemental":    "Elemental",
    "fiend":        "Demonio",      # Devir: Demonio
    "fey":          "Feérico",      # Devir: Feérico
    "fungus":       "Hongo",
    "giant":        "Gigante",
    "humanoid":     "Humanoide",
    "monitor":      "Monitor",
    "ooze":         "Cieno",
    "spirit":       "Espíritu",
    "undead":       "No muerto",    # Devir: No muerto (con espacio)

    # === VARIOS ===
    "aeon":         "Eón",
    "agathion":     "Agación",
    "alchemical":   "Alquímico",
    "amp":          "Amplificación",# Devir: Amplificación
    "amphibious":   "Anfibio",
    "analog":       "Analógico",
    "angel":        "Ángel",
    "archetype":    "Arquetipo",
    "apex":         "Ápex",
    "aasimar":      "Aasimar",
    "tiefling":     "Tiefling",
    "blessing":     "Bendición",
    "champion":     "Campeón",
    "clumsy":       "Torpe",
    "cold":         "Frío",
    "complex":      "Complejo",
    "consumable":   "Consumible",
    "cursebound":   "Ligado a maldición",
    "deadly":       "Letal",
    "dual":         "Dual",
    "dwarven":      "Enano",
    "elven":        "Élfico",
    "enchantment":  "Encantamiento",
    "evocation":    "Evocación",
    "extradimensional": "Extradimensional",
    "finesse":      "Destreza",
    "flexible":     "Flexible",
    "focused":      "Concentrado",
    "free":         "Libre",
    "good":         "Bueno",
    "evil":         "Malvado",
    "lawful":       "Legal",
    "chaotic":      "Caótico",
    "gnomish":      "Gnómico",
    "halfling":     "Mediano",
    "holy":         "Sagrado",
    "unholy":       "Profano",
    "horrifying":   "Aterrador",
    "incapacitation": "Incapacitación",
    "injury":       "Herida",
    "investigator": "Investigador",
    "linguistic":   "Lingüístico",
    "minion":       "Esbirro",
    "mutagen":      "Mutágeno",
    "necromancy":   "Nigromancia",
    "open":         "Abierto",
    "orcish":       "Orca",
    "paralyzed":    "Paralizado",
    "persistent":   "Persistente",
    "reload":       "Recarga",
    "resonant":     "Resonante",
    "revelation":   "Revelación",
    "scrying":      "Escrutinio",
    "secret":       "Secreto",
    "shadow":       "Sombra",
    "spellheart":   "Corazón de conjuro",
    "splash":       "Salpicadura",
    "summon":       "Convocar",
    "tattoo":       "Tatuaje",
    "talisman":     "Talismán",
    "teleportation": "Teletransportación",
    "thrown":       "Arrojadizo",
    "true":         "Verdadero",
    "uncommon":     "Poco común",
    "rare":         "Raro",
    "unique":       "Único",
    "common":       "Común",
    "versatile":    "Versátil",
    "virulent":     "Virulento",
    "vitality":     "Vitalidad",
    "void":         "Vacío",
    "voluminous":   "Voluminoso",
    "wand":         "Varita",
    "zombie":       "Zombi",
}

def main():
    path = os.path.join("..", "web", "traits_data.json")
    with open(path, 'r', encoding='utf-8') as f:
        traits = json.load(f)

    corrected = 0
    for trait_id, corrections_name in CORRECTIONS.items():
        if trait_id in traits:
            traits[trait_id]["es"]["name"] = corrections_name
            corrected += 1
        else:
            print(f"  [SKIP] '{trait_id}' not found in traits_data.json")

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(traits, f, ensure_ascii=False, indent=2)

    print(f"Correcciones aplicadas: {corrected}/{len(CORRECTIONS)}")

if __name__ == "__main__":
    main()
