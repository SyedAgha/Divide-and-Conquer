import networkx as nx
import numpy as np

class Leader_Identification(object):
	
	def __init__(self, leader_epsilon):
		self.overlap=leader_epsilon
		
	def __inclusion(self, c1, c2, epsilon):
		"""
		:param c1: node neighbors
        :param c2: node neighbors
		"""
		
		intersection = set(c2) & set(c1)
		smaller_set = min(len(c1), len(c2))
		return len(intersection)/float(smaller_set)
	

	def __search_leader(self, G, leaders, is_leader, epsilon):
		"""
		:param G: G: the networkx graph on which perform DCS
        :param leadrs:list of leaders
        :param is_leader: check if this node satisfies our condition
        :param dlt_nodes: nodes that failed to satisfy our condition in previous iteration
        :param epsilon: the tolerance required in order to merge communities
		"""
		
		com_val=[]
		find_edge=[]
		
		node_nbrs=G.neighbors(is_leader)
		
		if(len(node_nbrs)>2):
			
			for _, leader in enumerate(leaders):
				
				lead_nbrs=G.neighbors(leader)
				find_edge=np.append(find_edge, G.has_edge(is_leader,leader))
				com_val=np.append(com_val,self.__inclusion(node_nbrs, lead_nbrs, epsilon))
		
		#return len(com_val), sum(com_val<=epsilon), sum(find_edge==1)
		return len(com_val), len(np.where(com_val<=epsilon)[0]), len(np.where(find_edge>0)[0])

	
	def leader_finding(self, G):
		"""
		:param G: G: the networkx graph on which perform DCS
		"""
		
		nod=[nx.degree(G, i)+ sum(nx.degree(G, G.neighbors(i)).values()) for i in G.nodes()]
		sort_with_extended_degree=sorted(np.column_stack((nod,G.nodes())), key=lambda x: x[0], reverse=True)
		leaders=[sort_with_extended_degree[i][1] for i in range(2)]
                   	
		for j,k in enumerate(sort_with_extended_degree[2:-1]):
			
			leader_condition=self.__search_leader(G, leaders, k[1], self.overlap)
			
			#condition to avoid redundant leaders
			if(leader_condition[1]>0 and ((leader_condition[0]-leader_condition[1])<=2) and leader_condition[2]<=1):
				leaders.append(k[1])
		
		return leaders
