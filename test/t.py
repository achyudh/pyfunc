

def blah(p=(None,None)): 
   """ silly method
    

       .. versionadded:: 0.17

       Parameters
       ----------
       p : tuple, optional
   """
   print(p)


def blah2(c=None, d='str'): 
   """ silly method 2
    

       .. versionadded:: 0.17

       Parameters
       ----------
       c : tuple, optional
       d: string
   """
   print(d)

def blah3(): 
   """ silly method 2
    

       .. versionadded:: 0.17

       Returns
       ----------
       ding: int

   """
   ding =0
   return ding

def blah4(): 
   """ silly method 2
    

       .. versionadded:: 0.17

       Parameters
       ----------

   """
   print(d)

blah((1,2))
blah()


