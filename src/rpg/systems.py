from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from random import randint
from typing import Dict, List

from .models import Boss, BuffType, Character, Food, Item, Material, Quest, Rarity, Upgrade, WorldState


@dataclass
class CombatSystem:
    def attack_boss(self, hero: Character, boss: Boss) -> Dict[str, int]:
        damage = hero.effective_damage + randint(0, 6)
        boss.hp -= damage
        result = {"hero_damage": damage, "boss_remaining_hp": max(0, boss.hp)}
        if boss.hp > 0:
            hero.hp -= boss.damage
            result["boss_damage"] = boss.damage
            result["hero_remaining_hp"] = max(0, hero.hp)
        else:
            boss.defeated = True
            result["boss_damage"] = 0
            result["hero_remaining_hp"] = hero.hp
        return result


@dataclass
class InventorySystem:
    materials: List[Material] = field(default_factory=list)

    def add_item(self, hero: Character, item: Item) -> None:
        hero.inventory.append(item)

    def add_material(self, material: Material) -> None:
        self.materials.append(material)

    def consume_materials(self, required: Dict[str, int]) -> bool:
        bag = Counter(m.name for m in self.materials)
        if any(bag[name] < qty for name, qty in required.items()):
            return False
        remaining = required.copy()
        new_materials: list[Material] = []
        for material in self.materials:
            need = remaining.get(material.name, 0)
            if need > 0:
                remaining[material.name] -= 1
            else:
                new_materials.append(material)
        self.materials = new_materials
        return True


@dataclass
class CraftingSystem:
    def forge_weapon(self, hero: Character, inventory: InventorySystem, weapon_name: str) -> Item:
        recipe = {"Minério Arcano": 2, "Essência Ancestral": 1}
        if not inventory.consume_materials(recipe):
            raise ValueError("Materiais insuficientes para forjar arma rara.")
        item = Item(
            name=weapon_name,
            rarity=Rarity.EPICO,
            attack=14,
            visual_token="arma_epica_roxa",
        )
        hero.inventory.append(item)
        return item

    def enhance_weapon(self, item: Item, material: Material) -> Item:
        if material.rarity in (Rarity.LENDARIO, Rarity.MONSTRUOSO):
            item.attack += 5
            item.visual_token = f"{item.visual_token}_brilho"
        else:
            item.attack += 2
        return item


@dataclass
class CookingSystem:
    def cook_food(self, ingredient_name: str) -> Food:
        recipes = {
            "Carne Selvagem": Food("Ensopado de Caça", BuffType.VIDA, 20, 3),
            "Pimenta Rubra": Food("Guisado Flamejante", BuffType.DANO, 6, 4),
            "Raiz Lunar": Food("Caldo Revigorante", BuffType.STAMINA, 15, 5),
        }
        return recipes.get(ingredient_name, Food("Ração Simples", BuffType.VIDA, 5, 1))

    def apply_food_buff(self, hero: Character, food: Food) -> None:
        hero.active_buffs[food.buff_type] = hero.active_buffs.get(food.buff_type, 0) + food.value


@dataclass
class UpgradeSystem:
    applied_upgrades: Dict[str, List[Upgrade]] = field(default_factory=dict)

    def apply_upgrade(self, item: Item, upgrade: Upgrade) -> None:
        item.attack += upgrade.bonus_attack
        item.defense += upgrade.bonus_defense
        self.applied_upgrades.setdefault(upgrade.name, []).append(upgrade)

    def synergy_bonus(self, item: Item, upgrade_name: str) -> int:
        count = len(self.applied_upgrades.get(upgrade_name, []))
        if count >= 3:
            item.attack += 3
            item.defense += 2
            return 5
        if count == 2:
            item.attack += 1
            return 1
        return 0


@dataclass
class QuestSystem:
    def complete_quest(self, hero: Character, quest: Quest) -> None:
        if quest.completed:
            return
        quest.completed = True
        hero.inventory.extend(quest.rewards)


@dataclass
class WorldSystem:
    def create_world(self) -> WorldState:
        quests = [
            Quest(
                "Sombras de Eldoria",
                "Investigue ruínas e descubra o culto antigo.",
                [Item("Manto dos Vigias", Rarity.RARO, defense=5, visual_token="manto_azul")],
            ),
            Quest(
                "A Forja Perdida",
                "Recupere o coração da forja primordial.",
                [Item("Manopla Magna", Rarity.EPICO, attack=4, defense=3, visual_token="manopla_dourada")],
            ),
        ]
        bosses = [
            Boss("Górgona de Vidro", hp=160, damage=14, reward_materials=[Material("Essência Ancestral", Rarity.LENDARIO)]),
            Boss("Titã Monstruoso", hp=280, damage=21, reward_materials=[Material("Núcleo Monstruoso", Rarity.MONSTRUOSO)]),
        ]
        return WorldState(
            regions=["Vales de Brasa", "Floresta Espectral", "Costa Quebrada", "Fortaleza de Ônix"],
            quests=quests,
            bosses=bosses,
            narrative_hours=26,
            current_region="Vales de Brasa",
        )
