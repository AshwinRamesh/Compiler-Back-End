
class Optimiser():

    @staticmethod
    def dfs(cfg):
        #TODO: Is our graph ever going to be cyclic? If it is dfs will go forever, and we need to mark nodes as visited etc.
        reachable_nodes = []
        nodes = [cfg.get_start()]
        while nodes:
            for node in nodes:
                nodes.remove(node)
                nodes += node.get_out_nodes()
                reachable_nodes.append(node)
        return reachable_nodes

    @classmethod
    def remove_unreachable_nodes(self, cfg):
        reachable_nodes = self.dfs(cfg)
        #filter out and nodes that aren't reachable, and set the cfg's nodes to the new filtered list
        cfg.set_nodes(filter(lambda node : node in reachable_nodes, cfg.get_nodes()))
