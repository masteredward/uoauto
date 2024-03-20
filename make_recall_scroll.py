import random

from lib.items import (
    search_item_on_container,
    sum_items_charges_on_container,
    move_items_to_container
)

from lib.variables import (
    inscription_scroll_batch,
    house_containers,
    gumps
)

scroll_batch = inscription_scroll_batch['recall']

containers = house_containers

Player.HeadMessage(90, 'Starting Recall Script Creation Script')
while True:
    pen_total_charges = sum_items_charges_on_container("scribe's pen", Player.Backpack.Serial)
    Player.HeadMessage(90, f'Total pen charges: {pen_total_charges}!')

    if pen_total_charges >= scroll_batch:
        move_items_to_container('blank scroll', scroll_batch, containers['inscription_tools'], Player.Backpack.Serial)
        move_items_to_container('black pearl', scroll_batch, containers['magery_reagents'], Player.Backpack.Serial)
        move_items_to_container('blood moss', scroll_batch, containers['magery_reagents'], Player.Backpack.Serial)
        move_items_to_container('mandrake root', scroll_batch, containers['magery_reagents'], Player.Backpack.Serial)

        for _ in range(scroll_batch):
            random_pen = random.choice(search_item_on_container("scribe's pen", Player.Backpack.Serial))
            Items.UseItem(random_pen)
            Gumps.WaitForGump(gumps['inscription'], 5000)
            Gumps.SendAction(gumps['inscription'], 21)
            Gumps.WaitForGump(gumps['inscription'], 5000)
            Gumps.SendAction(gumps['inscription'], 302)
            Gumps.WaitForGump(gumps['inscription'], 5000)
            Gumps.SendAction(gumps['inscription'], 0)
            Misc.Pause(1000)

        move_items_to_container('recall', -1, Player.Backpack.Serial, containers['inscription_tools'])

        Player.UseSkill('meditation')
        while Player.Mana < 100:
            Misc.Pause(5000)
    else:
        Player.HeadMessage(1100 ,f'Script requires at least {scroll_batch} pen charges! Aborting.')
        break