import pytest

from pokerbot.games.variant import VariantGame, VariantConfig, SneakPeekHoldem


def test_variant_config_defaults():
    cfg = VariantConfig()
    assert cfg.name == "custom"
    assert cfg.num_players == 2
    assert cfg.antes == 0.0
    assert cfg.wild_cards == []
    assert cfg.auction is False


def test_variant_game_root():
    g = VariantGame(VariantConfig(name="Test", antes=1.0, wild_cards=["Joker"], auction=True))
    assert g.name == "Test"
    assert g.num_players == 2
    s = g.root()
    assert s.is_terminal() is False
    assert s.config.antes == 1.0
    assert "Joker" in s.config.wild_cards
    d = g.describe()
    assert d["auction"] is True
    assert d["antes"] == 1.0


def test_sneak_peek_holdem_stub():
    g = SneakPeekHoldem()
    assert g.name == "Sneak Peek Hold'em"
    assert g.config.peek_allowed is True
    assert g.config.hole_cards == 2
    assert g.config.community_cards == 5
    s = g.root()
    assert s.info_set_key(0).startswith("Sneak Peek Hold'em")


def test_custom_rules_via_config():
    cfg = VariantConfig(name="AuctionWild", antes=0.5, wild_cards=["2s"], auction=True, num_players=3)
    g = VariantGame(cfg)
    assert g.num_players == 3
    assert g.config.auction is True
    assert g.config.antes == 0.5
