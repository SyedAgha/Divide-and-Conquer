"""
Created on 14/nov/2015

@author: "Syed Agha Muhammad"
@contact: aghahashmi@gmail.com
"""
import networkx as nx
from merging_function import Merging

class Community(Merging):

    def __init__(self):
        """
        Constructor
        """
        
        Merging.__init__(self)
        self.all_communities = {}
        
    def execute(self, G, leader_nodes, epsilon, depth):
        """
        Execute CD algorithm
        :param G: the networkx graph on which perform detection
        :param epsilon: the tolerance required in order to merge communities (default 0.5)
        :param depth: the level of depth for neighborhood extraction (1 or 2)
        """
        
        self.G = G
        self.epsilon = epsilon
        self.depth=depth
        self._communities(leader_nodes,G, nx.density(G), self.depth)

        return  self.all_communities
        
    def _communities(self, leaders, G, graph_density, depth):
        """

        :param leader: leading nodes
        :param G: graph
        :param graph_density: density of the whole graph
        :param depth: neighboorhood order
        """
        
        for _, i in enumerate(leaders):
			
			order_neigborhod=1
			new=[]
			community_list=[]
			dlt_nodes=[]
			ego_nodes=set()
			
			while(order_neigborhod<=depth):
							
				ego_nodes=self.__without_ego(self.G, ego_nodes, order_neigborhod, dlt_nodes, i)
				extract_subgraph = G.subgraph(ego_nodes)
				edges_in_subgraph=extract_subgraph.size()
				nodes_to_be_checked_for_community=list(set(ego_nodes).difference(set([i]), set(new)))
				new.extend(nodes_to_be_checked_for_community)
				outside_cc_edges=sum(nx.degree(G, ego_nodes).values())-2*edges_in_subgraph
				with_node_conductance=(outside_cc_edges/((2.0*(edges_in_subgraph))+outside_cc_edges))
			
				for _, nods in enumerate(nodes_to_be_checked_for_community):
					
					in_comm=extract_subgraph.degree(nods)
					out_comm=G.degree(nods)-in_comm
					outside_edges_of_a_node=edges_in_subgraph-in_comm
					without_node_cf=((outside_cc_edges-out_comm)/(0.001+(2.0*outside_edges_of_a_node)+(outside_cc_edges-out_comm)))
					conductance_score_node=without_node_cf-with_node_conductance
					subgraph_density_without_node=self.__generalized(outside_edges_of_a_node, len(extract_subgraph)-1)
					density_score_node=nx.density(extract_subgraph)-subgraph_density_without_node+graph_density
					
					"""condition for a node to be included in a community"""
					if(conductance_score_node>=0 and density_score_node>=0):
						community_list.append(nods)
					else:
						dlt_nodes.append(nods)
				
				order_neigborhod+=1
			
			community_list.append(i)
			
			if(len(community_list)<=6):
				community_list.extend(extract_subgraph.nodes())
			
			self.all_communities = Merging.merge_communities(self, self.all_communities, list(set(community_list)), self.epsilon) 
	return 

    def __generalized(self, d1, d2):
        """
        :param d1: edges
        :param d2: nodes
        """
        
        if(d2==1):
			return 0
        
        return ((2.0*d1)/((d2)*(d2-1))) 

    def __without_ego(self, G, list_nodes, root, dlt_nodes, leader):
        """
        :param G: graph
        :list_nodes: nodes included in the previous iteration
        :root: depth level
        :dlt_nodes: nodes that failed to satisfy our condition in previous iteration
        :leader: root node
        """
        
        if root==1:
			nodes = set([leader])
			nodes.update(G.neighbors(leader))
			return nodes
        else:
			remove_unimportant_nodes= list(set(list_nodes).difference(set(dlt_nodes)))
			nodes = set()
			nodes.update(remove_unimportant_nodes)
			for n in remove_unimportant_nodes:
				nodes.update(nx.neighbors(G, n))
			return set(nodes).difference(set(dlt_nodes))
