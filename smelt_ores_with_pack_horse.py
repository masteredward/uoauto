from lib.items import (
    search_item_on_container,
    move_items_to_container
)
from lib.variables import (
    pack_horse_serial,
    ores_to_skip_merge,
    ore_colors
)

pack_horse_backpack = Mobiles.FindBySerial(pack_horse_serial).Backpack.Serial

def check_result():
    journal = Journal.GetTextByType('System')
    journal.Reverse()
    for entry in journal:
        if entry == 'You burn away the impurities but are left with less useable metal.':
            return True
        elif entry == 'You smelt the ore removing the impurities and put the metal in your backpack.':
            return True
        elif entry == 'There is not enough metal-bearing ore in this pile to make an ingot.':
            return False
        elif entry == 'You have no idea how to smelt this strange ore!':
            return False

def find_forge():
    forge_filter = Items.Filter()
    forge_filter.Movable = 0
    forge_filter.OnGround = 1
    forge_filter.RangeMax = 2
    forge_filter.Name = 'forge'
    return Items.ApplyFilter(forge_filter)

def create_skip_merge_list():
    skip_merge_list = []
    for ore_color in ores_to_skip_merge:
        skip_merge_list.append(ore_colors[ore_color])
    return skip_merge_list

def move_ores_from_pack_horse():
    skip_merge_list = create_skip_merge_list()
    while Player.Weight < Player.MaxWeight:
        items_on_container = search_item_on_container('ore', pack_horse_backpack)
        if len(items_on_container) == 0:
            break
        for item in items_on_container:
            Player.HeadMessage(90, 'Fetching ore')
            if item.Hue in skip_merge_list:
                Player.HeadMessage(90, 'Ore in skip merge list')
                Items.Move(item, Player.Backpack.Serial, 2, 0, 0)
            else:
                Player.HeadMessage(90, 'Merging ore')
                Items.Move(item, Player.Backpack.Serial, 2)
            player_remaining_weight = Player.MaxWeight - Player.Weight
            Player.HeadMessage(90, f'Player weight remaining {player_remaining_weight}.')
            Misc.Pause(1000)

forges = find_forge()

if len(forges) > 0:
    Player.HeadMessage(65,'Found forge!')
    move_ores_from_pack_horse()
    ores = search_item_on_container('ore', Player.Backpack.Serial)
    Player.HeadMessage(90,'Starting smelting process...') 
    while True:
        removed_ores = []
        for ore in ores:
            if ore.Weight > 2:
                Items.UseItem(ore)
                Target.WaitForTarget(10000, False)
                Target.TargetExecute(forges[0])
                Misc.Pause(2000)
                if not check_result():
                    Player.HeadMessage(90,'Ore not smeltable.') 
                    removed_ores.append(ore)
            else:
                removed_ores.append(ore)
        move_items_to_container('ingot', -1, Player.Backpack.Serial, pack_horse_backpack)
        ores = list(set(ores) - set(removed_ores))
        if len(search_item_on_container('ore', pack_horse_backpack)) > 0:
            move_ores_from_pack_horse()
            ores = search_item_on_container('ore', Player.Backpack.Serial)
        elif len(ores) == 0:
            break
        else:
            ores = search_item_on_container('ore', Player.Backpack.Serial)
else:
    Player.HeadMessage(1100,'No nearby forge found!')

move_items_to_container('ingot', -1, Player.Backpack.Serial, pack_horse_backpack)
move_items_to_container('ore', -1, Player.Backpack.Serial, pack_horse_backpack)

Player.HeadMessage(90,'Script finished.')