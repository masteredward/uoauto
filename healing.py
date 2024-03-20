import random

from lib.items import (
    search_item_on_container
)

from lib.mobiles import (
    search_mobiles_by_name
)

from lib.variables import (
    healing_allies,
    healing_pauses
)

allies = healing_allies
pauses = healing_pauses

def heal_allies():
    for ally in allies:
        search = search_mobiles_by_name(ally, 2)
        if len(search) > 0:
            mobile = search[0]
            if mobile.Hits < mobile.HitsMax:
                Player.HeadMessage(65, f'Ally need healing: {mobile.Name}')
                bandages = random.choice(search_item_on_container('clean bandage', Player.Backpack.Serial))
                if bandages:
                    Player.HeadMessage(65, f'Using bandage on {mobile.Name}!')
                    Items.UseItem(bandages)
                    Target.WaitForTarget(10000, False)
                    Target.TargetExecute(mobile)
                    Player.HeadMessage(90, f'Bandages Remaining: {bandages.Amount}')
                    Misc.Pause(pauses['afterBandage'])
                else:
                    Player.HeadMessage(1100, 'No bandages found!')
def heal_self():
    if Player.Hits < Player.HitsMax:
        bandages = random.choice(search_item_on_container('clean bandage', Player.Backpack.Serial))
        if bandages:
            Player.HeadMessage(65, 'Using bandage on yourself!')
            Items.UseItem(bandages)
            Target.WaitForTarget(10000, False)
            Target.Self()
            Player.HeadMessage(90, f'Bandages Remaining: {bandages.Amount}')
            Misc.Pause(pauses['afterBandage'])
        else:
            Player.HeadMessage(1100, 'No bandages found!')

Player.HeadMessage(65, 'Starting Healing Bot')
while not Player.IsGhost:
    heal_self()
    heal_allies()
    Misc.Pause(pauses['loop'])