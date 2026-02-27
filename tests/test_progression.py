from rpg.engine import GameEngine


def test_game_flow_has_expected_systems():
    engine = GameEngine()
    intro = engine.start_game("Arqueiro", "Lira")
    assert "26 horas" in intro

    log = engine.do_core_progression()
    assert "Quest concluída" in log
    assert "Buff culinário aplicado" in log
    assert "Arma forjada/equipada" in log


def test_each_class_has_6_skills():
    classes = ["Arqueiro", "Paladino", "Tanque", "Assassino"]
    for cls in classes:
        engine = GameEngine()
        engine.start_game(cls, "Hero")
        assert len(engine.hero.skill_tree.skills) == 6
