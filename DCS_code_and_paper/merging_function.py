
class Merging(object):
	
	def __init__(self):
		"""
        Constructor
        """

	def __generalized_inclusion(self, c1, c2, epsilon):
		"""
		:param c1: community
        :param c2: community
		"""
		
		intersection = set(c2) & set(c1)
		smaller_set = min(len(c1), len(c2))
		
		if len(intersection) == 0:
			return None
		
		if not smaller_set == 0:
			res = float(len(intersection)) / float(smaller_set)
		
		if res >= epsilon:
			union = set(c2) | set(c1)
			return union
			
	def merge_communities(self, communities, actual_community, epsilon):
		
		"""
		:param communities: dictionary of communities
        :param actual_community: a community
        :param epsilon: the tolerance required in order to merge communities 
		"""
		
		if tuple(actual_community) in communities:
			return communities
		
		else:
			
			inserted = False
			
			for test_community in communities.items():
				
				union=self.__generalized_inclusion(actual_community, test_community[0], epsilon)
				
				if union is not None:
					communities.pop(test_community[0])
					communities[tuple(sorted(union))] = 0
					inserted = True
					break
			
			if not inserted:
				communities[tuple(sorted(actual_community))] = 0
		
		return communities
