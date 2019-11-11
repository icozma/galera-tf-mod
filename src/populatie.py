from evol.individ import Individ
from evol.problema import Problema

from random import random,randrange

"""
type = random    
       uniform  - not yet  as grid search method
"""
class Populatie:
  def __init__(self, N=0, type = 'random',  insi=None, pb=None, specie='params'):
    self.pb = pb
    self.specie = specie

    if type == 'random':
      self.insi = []
      self.add_insi(N)      
    else:
      self.insi = [None]*N      
    
    if insi is not None:
      self.insi = insi
     
    
  def eval(self):
    ret = sum( [v.fitness_val for v in self] )/len(self) if len(self)>0 else -1
    return ret
  
  def add_insi(self, N=1):  
    for i in range(N):
      self.insi.append( Individ(pb=self.pb, specie=self.specie) ) 

    
    
  def __setitem__( self, idx, data ):   
    if idx >= len(self.insi ):
      self.insi.append( data )
    else:      
      self.insi[idx] = data
    
    
  def __getitem__( self, key):  
    if isinstance( key, slice ):
        #Get the start, stop, and step from the slice
        return Populatie( insi = [self.insi[k] for k in range(*key.indices(len(self)))] ) 
    elif isinstance( key, int ):
      if key < 0 : #Handle negative indices
        key += len( self.insi )
      if key < 0 or key >= len( self ) :
        raise IndexError( "The index (%d) is out of range."%key )
      return self.insi[key] 
    else:
        raise TypeError ( "Invalid argument type." ) 


  def sort(self, reverse=True):
    self.insi.sort( key=lambda x: x.fitness_val, reverse=reverse )


  def __iter__(self):
    for i in self.insi:
      yield i 
  
  
  def __str__(self):
    return ",\n".join( str(x) for x in self.insi )

  
  def __len__(self):
    return len( self.insi )
  

  """
  type_of_life:  better, random, worse
  """
  def live(self, mortality=.5, type_of_life='better'):
      # combinari si mutatii

      if type_of_life == 'worse':
        self.sort(reverse=False)
      else:  #  type_of_life == 'better':    
        self.sort(reverse=True)

      p = self.insi
      n = len(self)

      for i in range(n):
        f  = self[ randrange( n ) ]   
        mp = random()<Problema.COEFICIENT_INDIVIZI_MATE        
        if mp:
          c = self[i].mate(f)
          self[ len(self)] =  c 
     
      next_gen_size = (int)( len(p) * (1-mortality) )
      del self.insi[next_gen_size:]


  def live_N_generations(self, G=1, mortality=.5, type_of_life='better'):
    for g in range(G):
      ap = len(self.insi)
      av = self.eval()
      print( "Generatia {g}: [{ap}, {av}] ".format( g=g, ap=ap, av=av ) )
      if ap>1:
        self.live( mortality=mortality, type_of_life=type_of_life )
      else:
        break

    ap = len(self.insi)
    av = self.eval()
    print( "Generatia finala: [{ap}, {av}] ".format( ap=ap, av=av ) )

