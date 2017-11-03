

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


def blah5(): 
    """bleh"""
    print(d)

def _inverse_permutation(p):
    """inverse permutation"""
    n = p.size
    s = np.zeros(n, dtype=np.int32)
    i = np.arange(n, dtype=np.int32)
    np.put(s, p, i)  # s[p] = i
    return s


blah((1,2))
blah()


