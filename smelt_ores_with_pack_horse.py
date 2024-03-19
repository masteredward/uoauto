from lib.items import search_item_on_container, split_item_stack_on_container, move_items_to_container, move_items_to_container_no_merge_respect_weight

pack_horse_serial = 0x0021E650
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

split_item_stack_on_container('ore', pack_horse_backpack, 2)

forges = find_forge()

if len(forges) > 0:
    Player.HeadMessage(65,'Found forge!')
    move_items_to_container_no_merge_respect_weight('ore', pack_horse_backpack, Player.Backpack.Serial)
    ores = search_item_on_container('ore', Player.Backpack.Serial)
    Player.HeadMessage(90,'Starting smelting process...') 
    while len(ores) > 0:
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
        ores = list(set(ores) - set(removed_ores))
        if len(ores) > 0:
            move_items_to_container_no_merge_respect_weight('ore', pack_horse_backpack, Player.Backpack.Serial)
            ores = search_item_on_container('ore', Player.Backpack.Serial)
else:
    Player.HeadMessage(1100,'No nearby forge found!')

move_items_to_container('ingot', Player.Backpack.Serial, pack_horse_backpack)
move_items_to_container('ore', Player.Backpack.Serial, pack_horse_backpack)

Player.HeadMessage(90,'Script finished.')