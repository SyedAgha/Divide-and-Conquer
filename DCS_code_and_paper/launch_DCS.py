import networkx as nx
import community as dcs
import local_centrality as bg
import leader_selection as ls
from time import gmtime, strftime
from optparse import OptionParser

def main(file):

	print strftime("%Y-%m-%d %H:%M:%S", gmtime())

	##############create a graph from txt file#############
	G=bg.make_graph(file)
	print nx.info(G)
	
	################local centrality to identify meaningful modules of the graph#############
	#we set 3000 as a module size as discusssed in our paper
	local_centrality=bg.Bridge(size=3000)
	bigmod, normmod=local_centrality.bridge_function(G)

	for _,j in enumerate(bigmod.values()):
		
		G1=G.subgraph(j)
		G2=local_centrality.create_ap_points(G1)
		_,norm_modules=local_centrality.bridge_function(G2)
		
		for i,k in enumerate(norm_modules.values(), start=len(normmod)):
			normmod[i]=k

	################leader identification and community spreading phase###############
	communities={}
	comm_counter=0
	
	for j,i in enumerate(normmod.values()):
		
		#for very small modules, we search for its neighbors and merge them in the communities
		if(len(i)<=9):
			
			sma=set(i)
			for k in i:
				sma.update(nx.neighbors(G, k))
			
			communities[comm_counter]=sma
			comm_counter+=1	
		
		else:
			
			#to avoid local heterogeneity we set epsilon (merging value) of 0.75 for big modules and 0.30 for small modules 
			if(10<=len(i)<=500):
				heterogeneity=0.30
			else:
				heterogeneity=0.75
						
			extract_G=G.subgraph(i)

			lead=ls.Leader_Identification(leader_epsilon=0.60)
			leaders=lead.leader_finding(extract_G)
			
			cd = dcs.Community()
			comm_list=cd.execute(extract_G, leaders, epsilon=heterogeneity, depth=2)
			
			for c in comm_list.keys():
				communities[comm_counter]=c
				comm_counter+=1
		
	#########results are stored in a file##################
	print strftime("%Y-%m-%d %H:%M:%S", gmtime())
	
	out_file_com = open("communities", "w")
	idc = 0
	
	for c in communities.values():
		out_file_com.write("%s\n" % (' '.join([str(x) for x in sorted(c)])))
		idc += 1

	out_file_com.flush()
	out_file_com.close()

if __name__ == "__main__":

	usage = "usage: python %prog [options] filename"
	parser = OptionParser(usage)
	parser.add_option("-f", "--file", dest="file")
	(options, args) = parser.parse_args()
	network_file = options.file
	file = open(network_file, "r")
	main(file)


	
