import xlrd
import xlwt
from xlutils.copy import copy

book = xlrd.open_workbook("periodic_table.xls")
sheet = book.sheet_by_index(0)
wb = copy(book)
wsheet = wb.get_sheet(0)


class Node(): 
	def __init__(self, tpl, val, parent = None):
	  	self.values = [[tpl, val]]
	  	self.children = []  
	  	self.parent = parent

	# def __str__(self):
 # 		return "(%s, %d)" % (self.tpl, self.val)

	def insert(self, newnode):
	  	if len(self.values) == 3:
	  		#print("There are 3 elements in node")
	  		clonednode = self
	  		outlier = Node(self.values[1][0], self.values[1][1])
	  		self = outlier 
	  		#print("created an outlier")
	  		#print(outlier.values)
	  		leftchild = Node(clonednode.values[0][0], clonednode.values[0][1])
	  		#print("created a leftchild")
	  		#print(leftchild.values)
	  		rightchild = Node(clonednode.values[2][0], clonednode.values[2][1])
	  		#print("created a rightchild")
	  		#print(rightchild.values)
	  		outlier.children.append(leftchild)
	  		outlier.children.append(rightchild) 
	  		#print("children of outlier")
	  		#print(outlier.children)
	  		leftchild.parent = outlier
	  		rightchild.parent = outlier


	  		if not clonednode.leaf():
	  			#print("I am not a leaf")
		  		leftchild.children.append(clonednode.children[0])
		  		clonednode.children[0].parent = leftchild
		  		leftchild.children.append(clonednode.children[1])
		  		clonednode.children[1].parent = leftchild
		  		#print("rearenged self's children to leftchild")
		  		#print(leftchild.children)
		  		rightchild.children.append(clonednode.children[2])
		  		clonednode.children[2].parent = rightchild
		  		rightchild.children.append(clonednode.children[3])
		  		clonednode.children[3].parent = rightchild
		  		#print("rearenged self's children to rightchild")
		  		#print(rightchild.children)

		  	else:
		  		pass

		  	if clonednode.parent:
		  		#print("There is a parent node upwards")
		  		if newnode.values[0][0][1] == outlier.values[-1][0][1] and newnode.values[0][0][0] == outlier.values[-1][0][0]:
		  			#print("newnode and outlier have the same values")
		  			#print(newnode.values[0][0])
		  			#print(newnode.values[-1][0])
		  			outlier.values[0].extend(newnode.values[0][1:])
		  			clonednode.parent.put(outlier, clonednode) 
		  			return self
		  		else:
		  			#print("putting outlier to parents")
		  			#for child in clonednode.parent.children:
		  				#print(child.values)
		  			clonednode.parent.put(outlier, clonednode)
		  			#for child in clonednode.parent.children:
		  				#print(child.values)
		  	else:
		  		pass#print("don't have parents")
		  		



		  	if newnode.values[-1][0][0] < outlier.values[0][0][0]:
		  		leftchild.insert(newnode)
		  		#print("newnode is inserted to left child")
		  		#print("leftchild's values are"),
		  		#print(leftchild.values)
		  		
		  		#print("outlier:"),
		  		
		  		#print(self.children[0].values)
		  		return self

		  	elif newnode.values[0][0][0] > outlier.values[-1][0][0]:
		  		#print("newnode is inserted to right child")
		  		rightchild.insert(newnode)
		  		return self

		  	else:
		  		#print("They have equal first values")
		  		if newnode.values[-1][0][1] < outlier.values[0][0][1]:
		  			leftchild.insert(newnode)
		  			#print("newnode is inserted to left child be scnd val")
		  			return self
		  		elif newnode.values[0][0][1] > outlier.values[-1][0][1]:
		  			rightchild.insert(newnode)
		  			#print("newnode is inserted to right child be scnd val")
		  			return self

		else:
			#print("There are less than 3 elements in the Node")
			if self.leaf():  
				#print("This node is a leaf. Can insert.") 
				for t in self.values:
					if newnode.values[0][0] in t:
						t.extend(newnode.values[0][1:])
						return self
				self.values.append(newnode.values[0])
				self.values.sort(key=lambda x:(x[0][0],x[0][1]))
				#print("Values in the leaf after insertion:"), 
				#print(self.values)
				return self

			else:
				#print("current node is not a leaf, should insert to his children")
				if newnode.values[0][0][0] > self.values[-1][0][0]:
					self.children[-1].insert(newnode)
					#print("Insertion was made to rightmost child")
					return self
				elif newnode.values[0][0][0] < self.values[0][0][0]:
					#print("Insertion was made to leftmost child")
					self.children[0].insert(newnode)
					return self
				elif newnode.values[0][0][0] > self.values[0][0][0] and newnode.values[0][0][0] < self.values[-1][0][0]:
					#print("Insertion was made to middle child")
					self.children[1].insert(newnode) 
					return self

				if len(self.values) != 1: #definitely equal case
					#print("They are equal by first key and there are two values in node")
					if newnode.values[0][0][1] > self.values[-1][0][1]:
						#print("Insertion was made to rightmost child")
						self.children[-1].insert(newnode)
						return self
					elif newnode.values[0][0][1] < self.values[0][0][1]:
						#print("Insertion was made to leftmost child")
						self.children[0].insert(newnode)
						return self
					elif newnode.values[0][0][1] > self.values[0][0][1] and newnode.values[0][0][1] < self.values[-1][0][1]:
						#print("Insertion was made to middle child")
						self.children[1].insert(newnode) 
						return self
					#equal to first equal to second
					elif newnode.values[0][0][1] == self.values[0][0][1]:
						#print("input value is equal to first node's value")
						self.values[0].extend(newnode.values[0][1:])
						return self
					else:
						#print("input value is equal to second node's value")
						self.values[-1].extend(newnode.values[0][1:])
						return self

				else: #definitely equal case
					#print("They are equal by first key and there is one value in node")
					if newnode.values[0][0][1] > self.values[0][0][1]:
						#print("Insertion was made to rightmost child")
						self.children[-1].insert(newnode)
						return self
					elif newnode.values[-1][0][1] < self.values[0][0][1]:
						#print("Insertion was made to leftmost child")
						self.children[0].insert(newnode)
						return self
					else:
						#print("They are completely equal")
						self.values[0].extend(newnode.values[0][1:])
						return self





	def put(self, mynode, redun):
		mynode.parent = self
		self.children.extend(mynode.children)
		if redun in self.children:
			self.children.remove(redun) 
		self.children.sort(key=lambda x: (x.values[0][0][0], x.values[0][0][1])) 
		self.values.append(mynode.values[0])
		self.values.sort(key=lambda x:(x[0][0],x[0][1]))
		for child in self.children:
			child.parent = self

  	def leaf(self):
  		if not self.children:
  			return True

  	def find(self, tpl):  #tpl (key, key)
  		for nd in self.values:
  			if tpl in nd:
  				return nd[1:]

  		if self.leaf():
  			return False

  		if tpl[0] > self.values[-1][0][0]:
  			return self.children[-1].find(tpl)

  		for i in range(len(self.values)):
  			if tpl[0] < self.values[i][0][0]:
  				return self.children[i].find(tpl)

  		#cases when they are equal by first value
  		if tpl[1] > self.values[-1][0][1]:
  			return self.children[-1].find(tpl)

  		for nd in range(len(self.values)):
  			if tpl[1] < self.values[i][0][1]:
  				return self.children[i].find(tpl)

  	def findnext(self):
  		while self.children: 
  			return self.children[0].findnext()
  		return self

  	def findprev(self):
  		while self.children: 
  			return self.children[-1].findnext()
  		return self

  	def kick(self, val):
  		# print("deleting"),
		tpl = (sheet.cell_value(val,1), sheet.cell_value(val,10))
  		# print(tpl)
  		el = self.findk(tpl)  #is a node containing tpl to be deleted
  		# print("node containing to be deleted val"),
  		# print(el.values)
  		elpos = None
  		for i in range(len(el.values)):
  			if tpl in el.values[i]:  
  				elpos = i
  		
  		# print("it's located on this index in the values list"),
  		# print(elpos)
  		if el.leaf() and len(el.values)>1:  
  			# print("case when node is leaf and has at least 2 elements")
  			for i in range(len(el.values)):
  				if i!=len(el.values):
  					if tpl in el.values[i]:  
  						if len(el.values[i]) > 2:
  							el.values.remove(val)
  						else:
  							del el.values[i]

  		if not el.leaf():
  			# print("case when node isn't leaf")
  			if len(el.children[elpos+1].values)>1:  
  				# print("right child has more than 1 element")
  				# print(el.children[elpos+1].values)
  				# print("his successor is:"),
  				nxt = el.children[elpos+1].findnext() #is node with values
  				# print(nxt.values[0])
  				el.values[elpos] = nxt.values[0] #is first Node from children
  				# print("changing value in the node to it's successor's. Now value in our node is:"),
  				# print(el.values[elpos])
  				# print("Now we should delete successor")
  				el.children[elpos+1].kick(nxt.values[0][1])
  				# print("List of values of node which contained successor:"),
  				# print(nxt.values)



  			elif len(el.children[elpos].values)>1:   
  				# print("left child has more than 1 element")
  				# print("his predecessor is:"),
  				prv = el.children[elpos].findprev() #is node with values
  				# print(prv.values[-1])
  				# print("changing value in the node to it's predecessor's. Now value in our node is:"),
  				el.values[elpos] = prv.values[-1] #is first Node from children
  				# print(el.values[elpos])
  				# print("Now we should delete predecessor")
  				el.children[elpos].kick(prv.values[-1][1])
  				# print("List of values of node which contained predecessor:"),
  				# print(prv.values)

  			else: #checked
  				# print("both children have only one key, merging children with parent. (parent is taken from parents node). And start deleting val")
  				# print("Our node before deleting val:"),
  				# print(el.values)
  				# print("his left child:"),
  				# print(el.children[elpos].values)
  				el.children[elpos].values.append(el.values[elpos])
  				el.children[elpos].values.extend(el.children[elpos+1].values)
  				el.children[elpos].children.extend(el.children[elpos+1].children)
  				del el.values[elpos]  
  				del el.children[elpos+1]
  				# print("Our node after deleting val:"),
  				# print(el.values)
  				# print("his left child after merging with el and his right child:"),
  				# print(el.children[elpos].values)
  				if len(el.values) == 0:
  					self = el.children[elpos]
  				return self.kick(val)
  		return self

  	def check(self, posofch):
  		# print("starting restructuring tree while searching for el")
  		if len(self.children[posofch].values) == 1:
  			# print("child where we want to go has only one value")
  			# print("posofch"),
  			# print(posofch)
  			# print("len:"),
  			# print(len(self.children))
  			# print(self.children[posofch-1].values)
  			if posofch == -1:
  				posofch = len(self.children)-1
  			if posofch+1 < len(self.children):
  				if len(self.children[posofch+1].values)>=2:  
  					# print("we can steal from right sibling")
  					self.children[posofch].values.append(self.values[posofch])
  					self.values[posofch] = self.children[posofch+1].values[0]
  					del self.children[posofch+1].values[0] #del from sibl
  					if self.children[posofch+1].children:
  						self.children[posofch].children.append(self.children[posofch+1].children[0]) #taking children of appended sibl
  						del self.children[posofch+1].children[0] #del newly appended child from sibl children list

  			if posofch-1 >= 0: 
  				
	  			if len(self.children[posofch-1].values)>=2: 
	  				# print("we can steal from left sibling")
  					self.children[posofch].values.insert(0, self.values[posofch-1])
  					self.values[posofch-1] = self.children[posofch-1].values[-1]
  					del self.children[posofch-1].values[-1]
  					# print("new posofch val:"),
  					# print(posofch)
  					# print("len(self.children):"), 
  					# print(len(self.children))
  					# print(len(self.children[posofch-1].children)) 
  					if self.children[posofch-1].children:
						self.children[posofch].children.insert(0, self.children[posofch-1].children[-1])
						del self.children[posofch-1].children[-1]

			else:
				if posofch+1 < len(self.children) and posofch-1 >= 0:
					if len(self.children[posofch-1].values) == 1 and len(self.children[posofch+1].values) == 1:
						# print("merging two lonely children and parent")
						self.children[posofch].values.append(self.values[posofch])
						self.children[posofch].values.append(self.children[posofch+1].values[0])
						del self.values[posofch]
						self.children[posofch].children.extend(self.children[posofch+1].children)
						del self.children[posofch+1]
		return self





  	def findk(self, tpl):  #tpl (key, key)
  		# print("going for an element")
  		for nd in self.values:
  			if tpl in nd:
  				# print("found element")
  				return self

  		if self.leaf():
  			# print("didn't find el")
  			return False
  		# print(self.values)
  		if tpl[0] > self.values[-1][0][0]:
  			# print("going to the right side")
  			self = self.check(-1)
  			return self.children[-1].findk(tpl)

  		for i in range(len(self.values)):
  			if tpl[0] < self.values[i][0][0]:
  				# print("going to side:"),
  				# print(i)
  				self = self.check(i)
  				return self.children[i].findk(tpl)

  		#cases when they are equal by first value
  		# print("case when equal by first key")
  		if tpl[1] > self.values[-1][0][1]:
  			# print("going to the right side")
  			self = self.check(-1)
  			return self.children[-1].findk(tpl)

  		for nd in range(len(self.values)):
  			if tpl[1] < self.values[i][0][1]:
  				# print("going to side:"),
  				# print(i)
  				self = self.check(i)
  				return self.children[i].findk(tpl)

  				 

class Btree():
	def __init__(self):
		self.root = None

	def push(self, val): 
		tpl = (sheet.cell_value(val,1), sheet.cell_value(val,10))#name  mass sheet.cell_value(i,j)
		#print("inserting"),
		#print(tpl[0])
		if self.root is None:
			self.root = Node(tpl, val)
		else:
			self.root = self.root.insert(Node(tpl, val)) #tpl are obtained from table (key, key) val
		while self.root.parent:
			self.root = self.root.parent

	def search(self, tpl):
		return self.root.find(tpl)

	def delete(self, val):
		self.root.kick(val)
		if self.root.values == []:
			self.root = self.root.children[0]

	def printtree(self):
		print ('<<<----tree---->>>')
		print ('----root----')
		print (self.root.values)
		print ('----children----')
		for child in self.root.children:
			print child.values,
			print "      ",

	#change in the table, change in the tree
	def update(self, val, newtpl):
		self.delete(val)
		wsheet.write(val, 1, newtpl[0])
		wsheet.write(val, 10, newtpl[1])
		wb.save("periodic_table.xls")
		self.push(val)



# def main():
# 	tree = Btree()
# 	while True:
# 		oprt = raw_input("Please, say which operation do you want to do?-->  ")
		
# 		if oprt == "i":
# 			val = raw_input("Please, input value-->  ")
# 			tree.push(int(val))
# 			tree.printtree()
# 		elif oprt == "d":
# 			val = raw_input("Please, input value-->  ")
# 			tree.delete(int(val))
# 			tree.printtree()




# if __name__ == '__main__':
# 	main()
# tree = Btree()
# for i in range(1,100):
# 	tree.push(i)
# print(tree.search(("Boron", 10.81)))
# for i in range(1, 55):
# 	tree.delete(i)

# #1.008
# #tree.update(1, ("Hydro", 1.008))
# print("\n")
# tree.printtree()




















  




