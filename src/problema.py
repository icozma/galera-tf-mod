import os
import json
import numpy as np
import time
from pprint import pformat
import pandas as pd
import glob
import re
import os

from src.utils import dict2list, get_timestamp, default_encoding_for_json

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


  def __init__(self, fitness, space, is_bitmap_space=False, save_to=None):
    self.raw_fitness = fitness          # mandatory 
    self.SPACE = self.ordered_space(space)   # mandatory 
    # self.path_to_evol = path_to_evol          # optional 
    self.is_bitmap_space = is_bitmap_space      # ????
    self.save_to = save_to


  def ordered_space(self, S):
    """ Sort the space
    """
    T = {}
    for c in S.keys():   
      dim = sorted( S[c] )
      is_sorted = S[c] == dim
      if not is_sorted :
        T[c] = dim
      else:
        T[c] = S[c]
    return T


  def fitness( self, i ):   
      """ wrapping fitness:
            calculate fitness
            execution time
            save Individ         !!! circular dependency  individ <> problem
      """
      t_start = time.time()
      score = self.raw_fitness(i.get_caracter())
      t_end = time.time()
      exec_period = (t_end-t_start)*1000.0    

      obj = i.to_dict()
      obj[ obj['specie'] ]      =  i.get_caracter()
      obj[ 'durata_exec' ]      =  exec_period
      obj[ 'score' ]            =  score
      
      # if self.is_bitmap_space:
      #   # obj[ i['specie'] + '_demapped' ] =  json.dumps( dict2list( caracter ), default=default_encoding_for_json)
      #   obj[ i['specie'] + '_demapped' ] =  json.dumps(caracter , default=default_encoding_for_json)
      if self.save_to:    
        self.save(  obj=json.dumps(obj,default=default_encoding_for_json) , 
                    path = self.save_to,
                    sufix=str(obj['score'])[:6], 
                    specia = obj['specie'] )
      return score


  # OUTSIDE ? in solver
  def solve(self, n_rounds=3, n_indivizi=20, n_generatii=2, mortalitate=.9, live_better=True, specie='wolverine' ):
    """ 
    """
    type_of_life = 'better' if live_better else 'worse'
    from src.populatie import Populatie
    for i in range(n_rounds):
        p = Populatie(N=n_indivizi, pb=self, specie= specie+'_runda_'+str(i) )
        p.live_N_generations(G=n_generatii, mortality=mortalitate, type_of_life=type_of_life)


  def save(self, obj, path='.', sufix='', specia='' ):  
    """ Saves as specia > runda > individ_name_score_timestamp
    """
    def make_folder_if_need( f ):
        if not os.path.exists(f):
          os.mkdir(f) 
        return f

    specie_dir = ''
    round_dir = None
    if 'runda_' in specia:
      runda_pos = specia.find('runda_')
      round_dir = specia[runda_pos:] 
      specie_dir = specia[:runda_pos-1] 

      specie_folder = os.path.join( path , specie_dir )
      specie_folder = make_folder_if_need(specie_folder)
      
      runda_subfolder = os.path.join( specie_folder, round_dir )       
      folder = make_folder_if_need( runda_subfolder ) 

    else:
      specie_dir = specia
      folder = os.path.join( path , specie_dir )
      folder = make_folder_if_need(folder)

    fname = specia + '__' + sufix + '__'+get_timestamp() + ".json" 
    fname = os.path.join( folder ,  fname )
    
    f = open( fname ,"a+")
    f.write( str(obj) )
    f.close()


  # def get_evol_summary( self,   specie = '', top=10, with_save=True ): 
  #   """ reads some individs and produces a summary
  #   """ 
  #   files1 = [ f for f in glob.glob(self.path_to_evol + '/'+specie+"*/*.json", recursive=True) ]
  #   files2 = [ f for f in glob.glob(self.path_to_evol + '/'+specie+"*/*/*.json", recursive=True) ]  
  #   files  = list( set(files1).union(set(files2))) 

  #   scores = []
  #   for f in files:
  #       with open(f,'r') as json_file:     
  #         text_data = json_file.read()     
          
  #         if text_data[0] == "[":
  #           text_data  
            
  #         text_data = '[' + re.sub(r'\}\s*\{', '},{', text_data) + ']'
  #         data_array = json.loads(text_data)
          
  #         for data in data_array:
  #           s = data['specie']
  #           v = data[s]
  #           # print(s, '\n', v)
  #           data['individ'] = v
  #           del data[s]
        
  #           data['file']= os.path.basename(f)      
  #           scores.append( data )

  #   ret = pd.DataFrame(scores)    
  #   ret = ret.sort_values(by=['score'], ascending=False)
  #   c_ret = ['score', 'name', 'individ', 'file', 'durata_exec']

  #   ret = ret[c_ret].head(top)
  #   if with_save:
  #     ret.to_csv( os.path.join(self.path_to_evol, specie+'_summary.csv' ) )

  #   return ret[c_ret]
