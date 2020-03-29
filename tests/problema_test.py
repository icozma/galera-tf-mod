import unittest
from src.problema import Problema
from src.individ import Individ

from random import random
import numpy as np

# Spatiul problemei 
S = {
    'x': [x for x in np.arange(-10, 10, 0.0001)],
    'y': [x for x in np.arange(-10, 10, 0.0001)],    
    'a': ['a', 'b']  
} 
# Functia de maximizat per i=individ
def my_fitness( i ):
    return -i['x']**2 - i['y']**2 + 1


class Problema_tests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Space = S
        self.f = my_fitness
        

    def test_make_problema(self):
        import os
        path_to_evol='./tests_result'
        if not os.path.exists(path_to_evol):
            os.mkdir(path_to_evol)

        pb = Problema(fitness=self.f, space=self.Space)
        d = { 'x':2 , 'y':2  }
        i = Individ( pb=pb, d=d)
        print( "Individul ", i )
        pb.save( i)

        self.assertNotEqual(1, 0, "Shall be >0, macar o mutatie ")
     
     
    def test_make_problema_save_np_array(self):
        my_f = lambda i: i['x']**2 + 1 - i['y']**3
        import numpy as np
        pb = Problema(fitness=my_f,  space=self.Space)
        d = {'x':2, 'y':3, 'a': 'a'  }
        i = Individ(pb=pb, d=d)
        print(i)
        self.assertNotEqual(1, 0, "Shall be >0, macar o mutatie ")


    def test_problema_get_summary(self):
        my_f = lambda i: -i['x']**2 + 1 - i['y']**2
        pb = Problema(fitness=my_f,  space=self.Space)
       
        from src.populatie import Populatie
        p = Populatie(N=100, pb=pb, specie='teste')
        p.live_N_generations(G=10, mortality=.80, type_of_life='better')

        self.assertNotEqual(1, 0, "Shall just run!")


if __name__ == '__main__':
    unittest.main()

