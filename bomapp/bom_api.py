
class Part:
    """
    Class to describe a part.
    """
    def __init__(self, part_number, quantity=1):
        self.quantity = quantity
        self.part_number = part_number
        self.sub_parts = []


def create_bom(bom_requests):
    """
    Create dictionary of parts to represent BoM.
    :param bom_str: BoM json
    :return:
    """
    bom = {}
    root = None
    # loop through nodes
    bom_json = bom_requests.get_bom()
    if bom_json:
        for node in bom_json['data']:
            part_id, quantity, parent_part_id = node['part_id'], node['quantity'], node['parent_part_id']
            part_number = bom_requests.get_part(part_id)
            if not part_number:
                return {}, None
            # check part is in dictionary
            if part_id in bom:
                bom[part_id].quantity = quantity
                # create parent if necessary
                if parent_part_id not in bom:
                    parent_part_number = bom_requests.get_part(parent_part_id)
                    bom[parent_part_id] = Part(parent_part_number)
                bom[parent_part_id].sub_parts.append(part_id)
            else:
                # add new part
                bom[part_id] = Part(part_number, quantity)
                # check parent in the dictionary
                if parent_part_id in bom:
                    # add sub-part
                    bom[parent_part_id].sub_parts.append(part_id)
                else:
                    if parent_part_id:
                        # create parent and add sub-part
                        parent_part_number = bom_requests.get_part(parent_part_id)
                        bom[parent_part_id] = Part(parent_part_number)
                        bom[parent_part_id].sub_parts.append(part_id)
                    else:
                        # store the root
                        root = part_id
    return bom, root


def dfs(bom, quantities, part_id, quantity):
    """
    Perform a depth first traversal of BoM dictionary and calculate the quantity of each part.
    :param bom: BoM dictionary
    :param quantities: dictionary of parts and quantities
    :param part_id: current part id
    :param quantity: current quantity
    :return:
    """
    new_quantity = bom[part_id].quantity * quantity
    part_number = bom[part_id].part_number
    quantities[part_number] += new_quantity
    for sub_part_id in bom[part_id].sub_parts:
        dfs(bom, quantities, sub_part_id, new_quantity)
