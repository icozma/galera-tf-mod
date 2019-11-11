import unittest
from src.problema import Problema

class Problema_tests(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from random import random
        import numpy as np
        # Spatiul problemei 
        self.Space = {
            'x': [x for x in np.arange(-10, 10, 0.0001)],
            'y': [x for x in np.arange(-10, 10, 0.0001)],      
        } 
        # Functia de maximizat per i=individ
        def my_fitness( i ):
            return -i['x']**2 + 1 -i['y']**2
        self.f = my_fitness
        

    def test_make_problema(self):
        pb = Problema(fitness=self.f, path_to_evol='./temp', space=self.Space)
        pb.save( {'a':1} )
        self.assertNotEqual(1, 0, "Shall be >0, macar o mutatie ")
     

    def test_make_problema_save(self):
        my_f = lambda i: i['x']**2 + 1 - i['y']**3
        pb = Problema(fitness=my_f, path_to_evol='./temp', space=self.Space)
        pb.fitness( {'x':2, 'y':3} )
        self.assertNotEqual(1, 0, "Shall be >0, macar o mutatie ")


    def test_make_problema_save_np_array(self):
        my_f = lambda i: i['x']**2 + 1 - i['y']**3
        import numpy as np
        
        pb = Problema(fitness=my_f,  path_to_evol='./temp', space=self.Space)
        pb.fitness( {'x':2, 'y':3, 'a': np.array(['a', 'b']).tolist()   } )
        self.assertNotEqual(1, 0, "Shall be >0, macar o mutatie ")


    def test_problema_get_summary(self):
        my_f = lambda i: -i['x']**2 + 1 - i['y']**2
        pb = Problema(fitness=my_f, path_to_evol='./temp', space=self.Space)
        # import src.individ as Individ
        # i = Individ( caracter={'x':2, 'y':3   } , pb=pb)
        # pb.fitness( i )
       
        from src.populatie import Populatie
        p = Populatie(N=100, pb=pb, specie='teste')
        p.live_N_generations(G=10, mortality=.80, type_of_life='better')
        
        df = pb.get_evol_summary(specie='teste', save_to='summary')
        print(df)

        has_score = 'score' in list( df.columns ) 
        self.assertIn('score', list(df.columns), "Shall have score column")


if __name__ == '__main__':
    unittest.main()

