from rpg.engine import GameEngine


def run_demo() -> None:
    print("=== Chaos of the World - RPG 2D (Protótipo Modular) ===")
    print("Classes: Arqueiro | Paladino | Tanque | Assassino")
    chosen = input("Escolha sua classe: ").strip() or "Arqueiro"
    name = input("Nome do herói: ").strip() or "Aerin"

    engine = GameEngine()
    print(engine.start_game(chosen, name))
    print(engine.do_core_progression())


if __name__ == "__main__":
    run_demo()
