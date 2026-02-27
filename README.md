# Chaos of the World — Protótipo de RPG 2D Modular

Este projeto entrega uma base jogável (CLI) com arquitetura modular para um RPG 2D de mundo aberto, preparada para evolução para engine gráfica (Godot, Unity ou Pygame).

## Recursos implementados

- **4 classes jogáveis**: Arqueiro, Paladino, Tanque e Assassino.
- **Árvore de 6 habilidades por classe**, com desbloqueio progressivo.
- **Mundo aberto com regiões**, quests e bosses.
- **Narrativa principal definida para ~26h**, dentro do alvo de 20–30h.
- **Equipamentos com raridades**: comum, incomum, raro, épico, lendário e monstruoso.
- **Equipamentos com visual token**, permitindo alteração visual do personagem por item equipado.
- **Sistema de forja** para criar/fortalecer armas usando materiais raros.
- **Sistema de culinária** com alimentos que aplicam buffs (dano, vida, stamina).
- **Sistema de melhorias (upgrades)** com bônus de sinergia ao aplicar em múltiplos itens.
- **Sistemas modulares separados**: combate, inventário, mundo, quests, forja, culinária e upgrades.

## Estrutura

- `src/rpg/models.py` → entidades e tipos do jogo.
- `src/rpg/classes.py` → definição de classes e árvores de habilidade.
- `src/rpg/systems.py` → sistemas centrais de gameplay.
- `src/rpg/engine.py` → orquestração do loop principal/progressão.
- `main.py` → demo interativa simples.

## Executar

```bash
python -m pip install -e .
python main.py
```

## Próximos passos (recomendado)

1. Integrar renderização 2D (spritesheets e animações).
2. Persistência de save game (JSON/SQLite).
3. IA de inimigos e pathfinding.
4. Quest graph com escolhas e consequências.
5. Multiplayer cooperativo opcional.
