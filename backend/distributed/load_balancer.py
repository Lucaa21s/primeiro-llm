from distributed.node_manager import get_available_nodes



def select_node():

    nodes = get_available_nodes()

    return nodes[0]
