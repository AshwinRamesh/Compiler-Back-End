
class Optimiser():

    @staticmethod
    def dfs(cfg):
        """AWW YEAH IT'S DFS TIME THANKS INFO1905 THANKS COMP2907 THANKS COMP3456 THANKS MATH2969 THANKS COMP3608"""
        reachable_nodes = []
        nodes = [cfg.get_start()]
        while nodes:
            for node in nodes:
                reachable_nodes.append(node)
                nodes.remove(node)
                nodes += node.get_out_nodes()
        return reachable_nodes

    @classmethod
    def remove_unreachable_nodes(self, cfg):
        reachable_nodes = self.dfs(cfg)
        cfg.set_nodes(filter(lambda node : node in reachable_nodes, cfg.get_nodes()))
