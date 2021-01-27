def remove_duplicates_preserving_order(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def to_simple_obj_list(ll):
    return list(map(lambda x: x.to_obj(), ll))


def to_detail_obj_list(ll):
    return list(map(lambda x: x.to_detail(), ll))