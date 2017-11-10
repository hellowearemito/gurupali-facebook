# import copy


def track_groups(communities_list):

    initial_groups, cnt = init_groups(communities_list[0])
    groups_tracking = [initial_groups]
    old_groups_dict = initial_groups

    for i in range(1, len(communities_list)):
        new_groups, cnt = get_next_generation_groups(old_groups_dict, communities_list[i], cnt)
        print(new_groups.keys())
        groups_tracking.append(new_groups)
        old_groups_dict = new_groups

    return groups_tracking


def init_groups(first_month_communities):
    first_groups = dict()
    cnt = 0
    for first_month_community in first_month_communities:
        cnt += 1
        first_groups[cnt] = first_month_community

    return first_groups, cnt


def get_next_generation_groups(old_groups_dict, new_groups_list, cnt):
    new_groups_dict = dict()
    new_groups_list_rest = new_groups_list

    if not new_groups_list:
        return new_groups_dict, cnt

    for old_group_id, old_group_members in old_groups_dict.items():
        common_element_number = get_common_members(old_group_members, new_groups_list)
        max_index = common_element_number.index(max(common_element_number))
        new_groups_dict[old_group_id] = new_groups_list[max_index]

        print(new_groups_list)
        print(new_groups_list[max_index])
        print(new_groups_list_rest)
        new_groups_list_rest.remove(new_groups_list[max_index])
        if not new_groups_list_rest: break

    if new_groups_list_rest:
        for act_group in new_groups_list_rest:
            cnt += 1
            new_groups_dict[cnt] = act_group

    return new_groups_dict, cnt


def get_common_members(old_group, new_groups):
    res = []
    for i in range(len(new_groups)):
        res.append(len(list(set(old_group).intersection(new_groups[i]))))

    return res


# TODO: k-click algorithm can put one node to multiple community, we should decide which is more valid
# later def trim_groups()


# def track_groups(communities_list):
#
#     old_dict = dict()
#     group_dict_list = []
#     cnt = 0
#     for i in communities_list[0]:
#         cnt += 1
#         old_dict[cnt] = i
#
#     group_dict_list.append(old_dict)
#
#     for i in range(1, len(communities_list)):
#         act_communities = communities_list[i]
#
#         for old_dict_group_id, old_dict_value in old_dict.items():
#
#             new_dict = dict()
#
#             for act_community in act_communities:
#                 best_match_group_id = 0
#                 max_common_element = 0
#                 common_element = len(list(set(act_community).intersection(old_dict_value)))
#                 if common_element>max_common_element:
#                     max_common_element = common_element
#                     best_match_group_id = old_dict_group_id
#                     best_match_group = act_community
#
#                 if best_match_group_id != 0:
#                     new_dict[best_match_group_id] = best_match_group
#
#
#
#     return groups_tracking



x = [[["a","b","c", "j","k"], ["d", "e"]], [["a","b","c"]], [], [ ["d", "e"], ["a","b","c"]]]
print(track_groups(x))
