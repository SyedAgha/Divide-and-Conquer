import networkx as nx
import numpy as np
from merging_function import Merging


class Bridge(Merging):
	
	def __init__(self, size=None):
		"""
        Constructor
        """
		
		Merging.__init__(self)
		self.size=size		
	
	def __assign_to_biggest_module(self, comm, community_list):
		
		comm.pop(np.argmax(community_list))
		community_list.remove(max(community_list))
		return list(reduce(lambda x,y: x+y,comm))
	
	def __delete_edges(self, graph, nolist, node):
		
		select_edges=set.intersection(set(nolist), set(nx.neighbors(graph, node)))
		select_edges_to_remove=[(j,node) for j in select_edges 
								if(nx.degree(graph, node)>1 and nx.degree(graph, j)>1)]
		graph.remove_edges_from(select_edges_to_remove)	
		return graph

	
	def create_ap_points(self, G):
		"""
		this method creates weak articulation points 
		:param G: the networkx graph on which perform detection
		"""
		
		for j in G:
			
			egonet = G.subgraph(nx.all_neighbors(G,j))
			local=nx.connected_components(egonet)
			extract_components=list(local)
			
			#to avoid whiskers, we verify this condition and it produced good results for >5
			if(len(egonet.nodes())>5):
				
				all_communities = {}
				
				for k in extract_components:
					for l in k:
						#small value of epsilon or merging parameter to identiy divserse second-order neighborhood in the graph
						all_communities = Merging.merge_communities(self, all_communities, nx.neighbors(G, l), 0.30)
				
				communities_counter=[len(x) for x in all_communities.keys()]
				
				if(sum(np.bincount(communities_counter)[3:])>1):
					
					#this process is similar for this function and bridge_function
					tobedel=self.__assign_to_biggest_module(all_communities.keys(), communities_counter)
					self.__delete_edges(G, tobedel, j)
		
		return G

	def bridge_function(self, G):
		"""
		bridge function to identify weak nodes of the graph
		:param G: the networkx graph on which perform detection
		"""
		
		components=nx.connected_component_subgraphs(G)
		big_mod={}
		normal_mod={}
		bigmodcounter=normmodcounter=0
		
		for _, i in enumerate(components):
			
			for _,j in enumerate(i):
				
				egonet = i.subgraph(nx.all_neighbors(i,j))
				local=nx.connected_components(egonet)
				conn_comp=list(local)

				if len(conn_comp)>1:
					
					all_communities = {}
					
					for k in conn_comp:
						
						egos_local_communities=set(k)
						for l in k:
							egos_local_communities.update(nx.neighbors(i, l))
						
						egos_local_communities.remove(j)
						
						#merge two list if they have even a single member in common
						all_communities = Merging.merge_communities(self, all_communities, list(egos_local_communities), 0)
					
					communities_counter=[len(x) for x in all_communities.keys()]
									
					if(sum(np.bincount(communities_counter)[3:])>1):
						
						#if big modules identified then remove the edges and assign the node to the largest component connected to it
						tobedel=self.__assign_to_biggest_module(all_communities.keys(), communities_counter)
						self.__delete_edges(i, tobedel, j)
			
			assign_modules=list(nx.connected_components(i))
			
			#check modules size and assign them
			for i, mod in enumerate(assign_modules):
				
				if(len(mod)>self.size):
					big_mod[bigmodcounter]=mod
					bigmodcounter+=1
				
				else:
					normal_mod[normmodcounter]=mod
					normmodcounter+=1
		
		return big_mod, normal_mod

def make_graph(data):
	G=nx.Graph()
	for row in data:
		part = row.strip().split()
		G.add_edge(int(part[0]), int(part[1]))
	return G
