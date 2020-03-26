import os
import json
import numpy as np
import time
from pprint import pformat
import pandas as pd
import glob
import re
import os

# from evol.solutia import Solutia
# Problema:
#    initializeaza spatiul 
#                  coeficientii 
#                  functia fitness de maximizat 
#                  salveaza orice obiect in path_to_evol     

class Problema:
  COEFICIENT_SWITCH_CROMOZOM_LA_MATE = .5              # % schimba cromozom  
  COEFICIENT_MUTATIE_CROMOZOM_INDIVIDUAL = .5          # % gena ramane neafectata,   mic--> mutatii intensive 
  COEFICIENT_DELTA_MUTATIE_CROMOZOM_INDIVIDUAL = .05   # deplasarea mutatiei
  COEFICIENT_INDIVIZI_MATE = .5                        # % un individ se imperecheaza

  # OUTSIDE
  def demap(self, map):
      ret = []
      for c in map.keys():
          if map[c]:
              ret.append(c)
      ret = sorted(ret)
      return ret


  def __init__(self, fitness, path_to_evol, space, space_static={}, is_bitmap_space=False):
    self.raw_fitness = fitness
   
    self.path_to_evol = path_to_evol
    self.SPACE = space
    self.SPACE_STATIC = space_static
    self.is_bitmap_space = is_bitmap_space


  def default_encoding_for_json(self,obj):
      if type(obj).__module__ == np.__name__:
          if isinstance(obj, np.ndarray):
              return obj.tolist()
          else:
              return obj.item()
      raise TypeError('Unknown type:', type(obj))


  def fitness( self, i ):   
  '''  wrapping fitness
        save Individ
        and calculate fitness at calc. time
  '''

      start = time.time()
      ret = self.raw_fitness(i['caracter'])
      end = time.time()
      durata = end - start    

      obj = { 
              "specie":       i['specie'],
              "name":         i['name'],
              "score":        ret,
              "durata_exec":  durata,
            }
      obj[ i['specie'] ]             =  json.dumps( i['caracter'] , default=self.default_encoding_for_json)  
      
      if self.is_bitmap_space:
        obj[ i['specie'] + '_demapped' ] =  json.dumps( self.demap( i['caracter'] ), default=self.default_encoding_for_json)

      self.save(  json.dumps(obj, default=self.default_encoding_for_json) , sufix=str(obj['score'])[:6], specia = i['specie'] )
      return ret

  # OUTSIDE
  def get_timestamp(self):
    from datetime import datetime
    now = datetime.now()
    timestamp =  int( datetime.timestamp(now) ) 
    timestamp = str( datetime.fromtimestamp(timestamp)) .replace(":", "").replace("-", "").replace(" ", "_") 
    return timestamp


  def save(self, d, sufix='', specia='' ):
    x = d
  
    specie_folder_name = ''
    runda_subfolder_name = None
    if 'runda_' in specia:
      runda_pos = specia.find('runda_')
      runda_subfolder_name = specia[runda_pos:] 
      specie_folder_name = specia[:runda_pos-1] 

      specie_folder = os.path.join( self.path_to_evol , specie_folder_name )
      if not os.path.exists(specie_folder):
        os.mkdir(specie_folder) 
      
      runda_subfolder = os.path.join( specie_folder, runda_subfolder_name ) 
      if not os.path.exists(runda_subfolder) :
        os.mkdir(runda_subfolder)
      
      folder = runda_subfolder

    else:
      specie_folder_name = specia

      folder = os.path.join(  self.path_to_evol , specie_folder_name )
      if not os.path.exists(folder):
        os.mkdir(folder) 

    s = '_'+sufix
    # name = x.get('name', self.get_timestamp())
    name = self.get_timestamp()
    fname = os.path.join( folder ,  "evo_"+s+ '_' +name+ ".json" )
    
    f = open( fname ,"a+")
    f.write( x )
    f.close()


  def get_evol_summary( self,   specie = '', top=10, with_save=True ):  
    files1 = [ f for f in glob.glob(self.path_to_evol + '/'+specie+"*/*.json", recursive=True) ]
    files2 = [ f for f in glob.glob(self.path_to_evol + '/'+specie+"*/*/*.json", recursive=True) ]  
    files  = list( set(files1).union(set(files2))) 

    scores = []
    for f in files:
        with open(f,'r') as json_file:     
          text_data = json_file.read()     
          
          if text_data[0] == "[":
            text_data  
            
          text_data = '[' + re.sub(r'\}\s*\{', '},{', text_data) + ']'
          data_array = json.loads(text_data)
          
          for data in data_array:
            s = data['specie']
            v = data[s]
            # print(s, '\n', v)
            data['individ'] = v
            del data[s]
        
            data['file']= os.path.basename(f)      
            scores.append( data )

    ret = pd.DataFrame(scores)    
    ret = ret.sort_values(by=['score'], ascending=False)
    c_ret = ['score', 'name', 'individ', 'file', 'durata_exec']

    ret = ret[c_ret].head(top)
    if with_save:
      ret.to_csv( os.path.join(self.path_to_evol, specie+'_summary.csv' ) )

    return ret[c_ret]


  def solve(self, n_rounds=3, n_indivizi=20, n_generatii=2, mortalitate=.9, live_better=True, specie='wolverine' ):
    type_of_life = 'better' if live_better else 'worse'
    from evol.populatie import Populatie
    for i in range(n_rounds):
        p = Populatie(N=n_indivizi, pb=self, specie= specie+'_runda_'+str(i) )
        p.live_N_generations(G=n_generatii, mortality=mortalitate, type_of_life=type_of_life)
