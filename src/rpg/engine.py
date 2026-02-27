from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .classes import build_class
from .models import Character, Material, Rarity, Upgrade
from .systems import CombatSystem, CookingSystem, CraftingSystem, InventorySystem, QuestSystem, UpgradeSystem, WorldSystem


@dataclass
class GameEngine:
    hero: Optional[Character] = None
    combat: CombatSystem = field(default_factory=CombatSystem)
    inventory: InventorySystem = field(default_factory=InventorySystem)
    crafting: CraftingSystem = field(default_factory=CraftingSystem)
    cooking: CookingSystem = field(default_factory=CookingSystem)
    upgrades: UpgradeSystem = field(default_factory=UpgradeSystem)
    quests: QuestSystem = field(default_factory=QuestSystem)
    world_system: WorldSystem = field(default_factory=WorldSystem)

    def start_game(self, class_name: str, hero_name: str) -> str:
        self.hero = build_class(class_name, hero_name)
        world = self.world_system.create_world()
        self.world = world

        self.inventory.add_material(Material("Minério Arcano", Rarity.RARO))
        self.inventory.add_material(Material("Minério Arcano", Rarity.RARO))
        self.inventory.add_material(Material("Essência Ancestral", Rarity.LENDARIO))

        return (
            f"{hero_name}, o(a) {self.hero.cls_name}, inicia em {world.current_region}. "
            f"Campanha principal estimada: {world.narrative_hours} horas."
        )

    def do_core_progression(self) -> str:
        if not self.hero:
            raise RuntimeError("Inicie o jogo primeiro.")

        hero = self.hero
        quest = self.world.quests[0]
        self.quests.complete_quest(hero, quest)

        food = self.cooking.cook_food("Pimenta Rubra")
        self.cooking.apply_food_buff(hero, food)

        forged = self.crafting.forge_weapon(hero, self.inventory, "Arco da Aurora" if hero.cls_name == "Arqueiro" else "Lâmina Astral")
        hero.equip("arma", forged)

        upgrade = Upgrade("Runa de Ruptura", bonus_attack=2)
        self.upgrades.apply_upgrade(forged, upgrade)
        # Simula aplicação da mesma melhoria em múltiplos itens para bônus de sinergia.
        self.upgrades.applied_upgrades.setdefault(upgrade.name, []).extend([upgrade, upgrade])
        synergy = self.upgrades.synergy_bonus(forged, upgrade.name)

        boss = self.world.bosses[0]
        combat_log = self.combat.attack_boss(hero, boss)

        unlocked = hero.skill_tree.unlock(hero.skill_tree.skills[1].name)

        return (
            f"Quest concluída: {quest.title}. "
            f"Buff culinário aplicado: {food.name}. "
            f"Arma forjada/equipada: {forged.name} ({forged.rarity.value}), sinergia +{synergy}. "
            f"Combate contra {boss.name}: dano causado {combat_log['hero_damage']}, HP boss {combat_log['boss_remaining_hp']}. "
            f"Nova habilidade desbloqueada: {unlocked}."
        )
