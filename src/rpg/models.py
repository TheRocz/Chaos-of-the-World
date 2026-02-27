from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class Rarity(str, Enum):
    COMUM = "comum"
    INCOMUM = "incomum"
    RARO = "raro"
    EPICO = "epico"
    LENDARIO = "lendario"
    MONSTRUOSO = "monstruoso"


class BuffType(str, Enum):
    DANO = "dano"
    VIDA = "vida"
    STAMINA = "stamina"


@dataclass
class Skill:
    name: str
    description: str
    power: int
    stamina_cost: int
    unlocked: bool = False


@dataclass
class SkillTree:
    cls_name: str
    skills: List[Skill]

    def unlock(self, skill_name: str) -> bool:
        for skill in self.skills:
            if skill.name.lower() == skill_name.lower() and not skill.unlocked:
                skill.unlocked = True
                return True
        return False

    def unlocked_skills(self) -> List[Skill]:
        return [s for s in self.skills if s.unlocked]


@dataclass
class Item:
    name: str
    rarity: Rarity
    attack: int = 0
    defense: int = 0
    stamina: int = 0
    visual_token: str = "base"


@dataclass
class Upgrade:
    name: str
    bonus_attack: int = 0
    bonus_defense: int = 0


@dataclass
class Food:
    name: str
    buff_type: BuffType
    value: int
    duration_turns: int


@dataclass
class Material:
    name: str
    rarity: Rarity


@dataclass
class Quest:
    title: str
    description: str
    rewards: List[Item]
    completed: bool = False


@dataclass
class Boss:
    name: str
    hp: int
    damage: int
    reward_materials: List[Material]
    defeated: bool = False


@dataclass
class Character:
    name: str
    cls_name: str
    hp: int
    damage: int
    stamina: int
    skill_tree: SkillTree
    inventory: List[Item] = field(default_factory=list)
    equipped: Dict[str, Item] = field(default_factory=dict)
    active_buffs: Dict[BuffType, int] = field(default_factory=dict)

    def equip(self, slot: str, item: Item) -> None:
        self.equipped[slot] = item
        if item not in self.inventory:
            self.inventory.append(item)

    @property
    def effective_damage(self) -> int:
        bonus = sum(i.attack for i in self.equipped.values())
        bonus += self.active_buffs.get(BuffType.DANO, 0)
        return self.damage + bonus

    @property
    def effective_hp(self) -> int:
        bonus = sum(i.defense for i in self.equipped.values())
        bonus += self.active_buffs.get(BuffType.VIDA, 0)
        return self.hp + bonus


@dataclass
class WorldState:
    regions: List[str]
    quests: List[Quest]
    bosses: List[Boss]
    narrative_hours: int = 24
    current_region: Optional[str] = None
