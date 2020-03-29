from random import random , randrange, choice
from src.problema import Problema
from src.utils import get_timestamp

from pprint import pformat
import json
import os

class Individ: 

  def __init__(self, pb, *args, **kwargs):  
      """ Creates individ from:
            g = list of genes over pb.Space indexes
            d = dictionary of characteristics over pb.Space
            f = json file with dictionary, see d
            random individ over pb.Space
      
      Arguments:
          pb {Problem} -- [description]
      
      Raises:
          Exception: [description]
      """    
      self.verbose = kwargs.get('verbose',False)
      self.name = get_timestamp()
      self.specie = kwargs.get('specie','')
      self.gene = None
      self.pb = pb
      if not isinstance(self.pb, Problema):
        raise Exception("Inidivid fara probleme!") 

      g = kwargs.get('g',None)
      d = kwargs.get('d',None)
      f = kwargs.get('f',None)

      if g:   self.gene = g         # build from genes list
      elif d: self.gene = self.__genes_from_dict( d=d )  if d else None
      elif f: self.gene = self.__genes_from_json( f=f ) if f else None
      else:   self.gene = self.__individ_random()      

      # needed not to recalculate fitness on each mutation
      with_calc_fitness = kwargs.get('with_calc_fitness',True)
      self.fitness_val = -1
      if with_calc_fitness:
          # c = self.get_caracter()
          # self.fitness_val = self.pb.fitness(c)
          self.fitness_val = self.pb.fitness( self )


  def __genes_from_json(self,  f=''):
      """Create individ from json file
      
      Keyword Arguments:
          f {str} -- json file path  (default: {''})
      """        
      g = None
      if os.path.exists(f): 
        with open(self.file) as json_file:
          data = json.load( json_file )
          if self.specie in data:
            g = self.__genes_from_dict( data[self.specie] )
          else: 
            raise ValueError('Individ deserialization failed! \n\tSpecia {specie} nu este gasita in {fis}'.format( specie= self.specie, fis=self.file ))
      return g


  def __individ_random(self):      
    """ return genes of a random individ
    """        
    if self.verbose:       
      import sys
      fn = sys._getframe().f_code.co_name
      print( fn )
      
    g = {}
    for k in self.pb.SPACE.keys():
      g[ k ] =  randrange( len( self.pb.SPACE[k]) ) 
    return g


  def __genes_from_dict(self, d={}, name=''):
    """ return genes of an individ over the pb.Space
    
    Returns:
        Dict -- dict of ganes
    """    
    if self.verbose:       
      import sys
      fn = sys._getframe().f_code.co_name
      print( fn )

    g = {}
    for c in d.keys():   # construieste genele pe spatiu   
      for i in range( len(self.pb.SPACE[c]) ) :
        if d[c] <= self.pb.SPACE[c][i]  :
          g[c] = i
          break       

    return g


  def like( self, b ):  
    """return how alike are two individs, 
         LIKLEHOOD:   distance between indexes
    
    Arguments:
        b {Individ} -- the individ to compare
    """      
    ret = 0 
    for k in self.pb.SPACE.keys():
      l = len( self.pb.SPACE[k] )
      ret += abs( self.gene[k] - b.gene[k] )
    ret = ret / len(self.pb.SPACE.keys())
    return ret
      
      
  def mutate( self , with_calc_fitness=True):
    """ chose a gene gt
        find the chromozome to mutate in gene, as delta from curent poz, see COEFICIENT_DELTA_MUTATIE_CROMOZOM_INDIVIDUAL
        fix the gene with delta if it has the chance, per COEFICIENT_MUTATIE_CROMOZOM_INDIVIDUAL
        make a new individ 
        recalculate the fitness if with_calc_fitness

    Keyword Arguments:
        with_calc_fitness {bool} -- [description] (default: {True})
    
    Returns:
        Individ -- the new individ with mutation
    """    
    gt = list( self.gene.keys() )
    gena_fix = choice( gt )

    # deprecated: { +1 -1 }  poate ar trebui facuta o alegere ... -1 0 +1 ...   
    # 
    # new: amplitudiinea mutatiei se alege in spatiul problemei > al genei 
    #    ca si coef. i.e. 5% impact 
    delta = Problema.COEFICIENT_DELTA_MUTATIE_CROMOZOM_INDIVIDUAL
    poz_pe_gena = (int)( len( self.pb.SPACE[gena_fix] ) * delta ) 
    val_mutatie = poz_pe_gena if random() <= self.pb.COEFICIENT_MUTATIE_CROMOZOM_INDIVIDUAL else -poz_pe_gena

    val_fix = self.gene[gena_fix] + val_mutatie
    val_fix = val_fix if val_fix >= 0 and val_fix < len( self.pb.SPACE[gena_fix] ) else self.gene[gena_fix]

    from copy import deepcopy 
    m = deepcopy(self.gene)
    m[gena_fix] = val_fix
    
    name = "*{}".format(self.name)

    i = self.__class__(pb=self.pb, g=m, name=name, specie=self.specie, with_calc_fitness=with_calc_fitness)
    return i

      
  def mate( self, f):
    """ Cross combine two individs
    
    Arguments:
        f {Individ} -- female individ
    
    Returns:
        Individ -- child individ
    """   
    if f.gene == self.gene:  # clona ==> producem o serie de mutatii pe self
      nmut = 20
    else:
      nmut = 1

    for i in range( nmut ):
      self = self.mutate( with_calc_fitness=False )  
    
    c = {}
    for k in self.gene.keys():
      m_gene_preserved = random()<=Problema.COEFICIENT_SWITCH_CROMOZOM_LA_MATE 
      c[k] = self.gene[k] if m_gene_preserved else f.gene[k] 
    
    name = "({}+{})".format(self.name, f.name)
    i = self.__class__( pb=self.pb, g=c, name=name, specie=self.specie, with_calc_fitness=True )   
    return i


  def get_caracter( self ):
    """ Gets the character of Individual
    
    Returns:
        Dict -- of characteristics over pb.Space
    """
    c = {}   
    if self.gene :
      for k in self.gene.keys():
        c[k] = self.pb.SPACE[k][ self.gene[k]]
    return c
    

  def to_dict( self ):
    """ Converts to dict
    
    Returns:
        Dict -- Individual specs as Dict
    """    
    return {   
                'specie': self.specie,
                'name': self.name,
                'score':  self.fitness_val, 
                'caracter': self.get_caracter(),
                'gene': self.gene,
            }  


  def __str__( self ):
    """ Converts to string
    
    Returns:
        str -- 
    """   
    return pformat( self.to_dict(), indent=4)

