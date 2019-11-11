from random import random , randrange, choice
from evol.problema import Problema

from pprint import pformat
import json

class Individ:
        
  # def __init__(self, g=None, pb=None, file=None, name='', specie='params', with_calc_fitness=True, caracter=None):  # fitenss, gene, problema
  def __init__(self, *args, **kwargs):  # fitenss, gene, problema
    #args -- tuple of anonymous arguments
    #kwargs -- dictionary of named arguments
        # self.num_holes = kwargs.get('num_holes',random_holes())

    self.name   = kwargs.get('name','')
    self.specie = kwargs.get('specie','')

    self.pb = kwargs.get('pb',None) 
    if isinstance(self.pb, Problema):
        self.f = self.pb.fitness
    else:
      raise Exception("Inidivid fara probleme!")    

    self.file = kwargs.get('file',None) 
    self.specie = kwargs.get('specie','wolverine') 

    g = None
    if self.file is not None: 
      with open(self.file) as json_file:
        data = json.load( json_file )
        if self.specie in data:
          g = self.__from_caracter( data[self.specie] )
        else: 
          raise ValueError('Individ deserialization failed! \n\tSpecia {specie} nu este gasita in {fis}'.format( specie= self.specie, fis=self.file ))
            
    if g is None:
      self.gene = self.get_individ_random()   
    else: 
      self.gene = g

    caracter = kwargs.get('caracter', None) 
    if caracter:
      self.__from_caracter( caracter )

    with_calc_fitness = kwargs.get('with_calc_fitness', True) 
    if with_calc_fitness:
      self.fitness_val = self.fitness()
    else:
      self.fitness_val = -1


  def __from_caracter(self, car={}, name=''):
    g = {}
    for c in car.keys():   # construieste genele pe spatiu   
      is_sorted = self.pb.SPACE[c] == sorted( self.pb.SPACE[c])
      if not is_sorted:
        print( 'Atentie dimensiune nesortata, poate vrei sa o sortezi in spatiu mai intai! see', c)
      g[c] = 2
      if is_sorted:
        for i in range( len(self.pb.SPACE[c]) ) :
          g[c] = i
          if car[c] <= self.pb.SPACE[c][i]  :
            break       
      else:
        for i in range( len(self.pb.SPACE[c]) ) :
          g[c] = i
          if car[c] == self.pb.SPACE[c][i]  :
            break    

    self.gene = g
    self.name = name
    return g


  def asemanare( self, b ):    
    ret = 0 
    
    for k in self.pb.SPACE.keys():
      l = len( self.pb.SPACE[k] )
      ret += abs( self.gene[k] - b.gene[k] ) / l
    
    ret = ret / len(self.pb.SPACE.keys())
    
    return ret
    
          
  def get_individ_random(self):
    self.name = self.pb.get_timestamp()
    g = {}
    for k in self.pb.SPACE.keys():
      g[ k ] =  randrange( len( self.pb.SPACE[k]) ) 
    return g
  
    
  def fitness( self ):
    c = self.get_caracter()
    self.caracter = c['caracter']
    self.fitness_val = self.f( c )
    return self.fitness_val
      
      
  def mutatie( self , with_calc_fitness=True):
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
    if f.gene == self.gene:  # clona ==> producem o serie de mutatii pe self
      nmut = 20
    else:
      nmut = 1

    for i in range( nmut ):
      self = self.mutatie( with_calc_fitness=False )  
    
    c = {}
    for k in self.gene.keys():
      m_gene_preserved = random()<=Problema.COEFICIENT_SWITCH_CROMOZOM_LA_MATE 
      c[k] = self.gene[k] if m_gene_preserved else f.gene[k] 
    
    name = "({}+{})".format(self.name, f.name)
    i = self.__class__( pb=self.pb, g=c, name=name, specie=self.specie, with_calc_fitness=True )   
    return i


  def get_caracter( self ):
    caracter_temp = {}   
    for k in self.gene.keys():
      caracter_temp[k] = self.pb.SPACE[k][ self.gene[k]]

    ret = {
        'name': self.name,  
        'specie': self.specie,
        'caracter': caracter_temp
    }

    return ret 
      
 
  def __str__( self ):
    return pformat( 
              str( 
                {   'specie': self.specie,
                    'name': self.name,
                    'fitness':  self.fitness_val, 
                    'caracter': self.caracter,
                    'gene': self.gene,
                })   , indent=4)

