from pathlib import Path

base_levels_folder = Path('../levels/0')
level0: dict[str, Path] = {
    'player': base_levels_folder / 'level_0_player.csv',
    'coins': base_levels_folder / 'level_0_coins.csv',
    'enemies': base_levels_folder / 'level_0_enemies.csv',
    'grass': base_levels_folder / 'level_0_grass.csv',
    'crates': base_levels_folder / 'level_0_crates.csv',
    'palms_bg': base_levels_folder / 'level_0_palms_bg.csv',
    'palms_fg': base_levels_folder / 'level_0_palms_fg.csv',
    'terrain_bg': base_levels_folder / 'level_0_terrain_bg.csv',
    'constraints': base_levels_folder / 'level_0_constraints.csv',
    'terrain_fg': base_levels_folder / 'level_0_terrain_fg.csv'
} # yapf: disable