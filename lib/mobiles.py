'''
Search for a given mobile name withing range
Returns a list with the Mobile object
'''
def search_mobiles_by_name(name, range):
    mobiles_filter = Mobiles.Filter()
    mobiles_filter.RangeMax = range
    mobiles_filter.Name = name
    filtered_mobiles = Mobiles.ApplyFilter(mobiles_filter)
    mobiles_found = []
    for filtered_mobile in filtered_mobiles:
        mobiles_found.append(filtered_mobile)
    return mobiles_found

