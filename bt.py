from bt_nodes import *
from behaviors import *

class BT:
    def __init__(self, ghost):
        self.ghost = ghost

    def update(self, dt):
        pass
    
    def start_behavior(self):

        root = Selector(name='High Level Ordering of Strategies')

        #Action()
        #the structure isn't created yet but it would go here

        root.child_nodes = [Scattering, Chasing, Freight]

        logging.info('\n' + root.tree_to_string())
        return root