from __future__ import annotations

from .models import Character, Skill, SkillTree


def _make_skill_tree(cls_name: str, templates: list[tuple[str, str, int, int]]) -> SkillTree:
    skills = [
        Skill(name=name, description=desc, power=power, stamina_cost=cost)
        for name, desc, power, cost in templates
    ]
    skills[0].unlocked = True
    return SkillTree(cls_name=cls_name, skills=skills)


def build_class(class_name: str, hero_name: str) -> Character:
    base = class_name.lower()

    if base == "arqueiro":
        tree = _make_skill_tree(
            "Arqueiro",
            [
                ("Flecha Precisa", "Disparo focado com dano alto.", 12, 5),
                ("Rajada", "Ataca em cone, ótimo para grupos.", 10, 7),
                ("Passo Sombrio", "Reposiciona e aumenta crítico.", 8, 6),
                ("Armadilha de Espinhos", "Controle de área.", 9, 8),
                ("Foco do Caçador", "Bônus progressivo de dano.", 11, 6),
                ("Chuva de Flechas", "Ultimate de área massiva.", 20, 15),
            ],
        )
        return Character(hero_name, "Arqueiro", hp=100, damage=16, stamina=100, skill_tree=tree)

    if base == "paladino":
        tree = _make_skill_tree(
            "Paladino",
            [
                ("Golpe Consagrado", "Ataque corpo a corpo com luz.", 11, 4),
                ("Escudo Divino", "Reduz dano recebido.", 7, 6),
                ("Cura Sagrada", "Regenera vida própria.", 8, 9),
                ("Martelo da Justiça", "Atordoa inimigos.", 12, 8),
                ("Aura da Esperança", "Buff em área.", 10, 8),
                ("Julgamento Celeste", "Explosão de luz devastadora.", 22, 16),
            ],
        )
        return Character(hero_name, "Paladino", hp=130, damage=12, stamina=90, skill_tree=tree)

    if base == "tanque":
        tree = _make_skill_tree(
            "Tanque",
            [
                ("Provocação", "Força foco dos inimigos.", 6, 4),
                ("Muralha", "Grande aumento defensivo.", 5, 8),
                ("Impacto Sísmico", "Dano e controle próximo.", 10, 9),
                ("Carga Pesada", "Avanço com stun.", 11, 8),
                ("Regeneração de Ferro", "Recupera vida por tempo.", 7, 7),
                ("Guardião Inabalável", "Ultimate de mitigação total.", 16, 14),
            ],
        )
        return Character(hero_name, "Tanque", hp=170, damage=9, stamina=110, skill_tree=tree)

    if base == "assassino":
        tree = _make_skill_tree(
            "Assassino",
            [
                ("Golpe nas Sombras", "Ataque crítico veloz.", 13, 5),
                ("Veneno Rápido", "Dano contínuo.", 9, 6),
                ("Evasão Fantasma", "Evita próximo ataque.", 6, 5),
                ("Lâmina Dupla", "Combo de dois hits.", 12, 8),
                ("Passo Mortal", "Mobilidade extrema.", 10, 7),
                ("Execução Silenciosa", "Finalização de elite.", 24, 16),
            ],
        )
        return Character(hero_name, "Assassino", hp=95, damage=18, stamina=105, skill_tree=tree)

    raise ValueError("Classe inválida. Use Arqueiro, Paladino, Tanque ou Assassino.")
