class is_afm:

	def is_afm(self,afm):
			try:
				if len(afm)==9:#9 digits
					afm = int(afm)#go to exception if afm !=int() or go to the next line!
					return None,True
				else:
					return "A.F.M must has 9 digit!",False
			except ValueError:
				return "You must enter a integer number as AFM!\n",False#never used basically!
				
