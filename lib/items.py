'''
Search for a given item name on a specified container serial.
Returns a list with the Item object
'''
def search_item_on_container(item_name, container_serial):
    item_filter = Items.Filter()
    item_filter.Movable = 1
    item_filter.OnGround = 0
    item_filter.Name = item_name
    filtered_items = Items.ApplyFilter(item_filter)
    items_on_container = []
    for filtered_item in filtered_items:
        if filtered_item.Container == container_serial:
            items_on_container.append(filtered_item)
    return items_on_container

'''
Sum all givem item name charges in the backpack. Useful for crafting/gathering scripts.
Returns an integer with the total number of charges amoung all found items
'''
def sum_items_charges_on_container(item_name, container_serial):
    items_on_container = search_item_on_container(item_name, container_serial)
    total_charges = 0
    for item in items_on_container:
        total_charges += int(item.Properties[1].Args)
    return total_charges

'''
Move items from on container to another. Can be used for merging stacks if the source and destination containers are the same.
Returns nothing
'''
def move_items_to_container(item_name, amount, source_container_serial, destination_container_serial):
    items_on_container = search_item_on_container(item_name, source_container_serial)
    for item in items_on_container:
        Player.HeadMessage(90, f'Moving {item_name} to container.')
        Items.Move(item, destination_container_serial, amount)
        Misc.Pause(1000)

def move_items_to_container_no_merge_respect_weight(item_name, source_container_serial, destination_container_serial):
    items_on_container = search_item_on_container(item_name, source_container_serial)
    for item in items_on_container:
        Player.HeadMessage(90, f'Moving {item_name} to container.')
        player_remaining_weight = Player.MaxWeight - Player.Weight
        Player.HeadMessage(90, f'Player weight remaining {player_remaining_weight}.')
        if player_remaining_weight > item.Weight:
            Items.Move(item, destination_container_serial, -1, 0, 0)
            Misc.Pause(1000)
        else:
            break

'''
Split the items stacks on a specified.container
Useful for decrease the item smelting loss
Returns nothing
'''
def split_item_stack_on_container(item_name, container_serial, split_size):
    items_already_split = []
    Player.HeadMessage(90, f'Begin to split {item_name} into stacks of {split_size}')
    while True:
        items_on_container = search_item_on_container(item_name, container_serial)
        for item in items_on_container:
            item_amount = item.Amount
            if item_amount > (split_size + 1):
                Items.Move(item, container_serial, split_size, 0, 0)
                Misc.Pause(1000)
            else:
                items_already_split.append(item)
        if len(list(set(items_on_container) - set(items_already_split))) == 0:
            Player.HeadMessage(90, f'Number of small {item_name} stacks: {len(items_on_container)}')
            break