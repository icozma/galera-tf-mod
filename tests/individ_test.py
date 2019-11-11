import unittest

class Individ_tests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        from src.problema import Problema
        from random import random
        import numpy as np

        # Spatiul problemei 
        Space = {
            'x': [x for x in np.arange(-10, 10, 0.0001)],
            'y': [x for x in np.arange(-10, 10, 0.0001)],      
        } 

        # Functia de maximizat per i=individ
        def my_fitness( i ):
            return -i['x']**2 + 1 -i['y']**2

        self.pb = Problema(fitness=my_fitness, path_to_evol='./', space=Space)

    def test_make_individ(self):
        from src.individ import Individ
        i = Individ(pb=self.pb)
        print(str(i))
        self.assertLess(i.fitness_val, 0, "Shall be equal")


    def test_mate_two(self):
        from src.individ import Individ
        m = Individ(pb=self.pb)
        print('\nmale: ',str(m))
        f = Individ(pb=self.pb)
        print('\nfemale: ', str(f))
        c = m.mate(f)
        print('\ncopil: ', c)
        self.assertNotEqual( c.fitness_val, m.fitness_val, "Shall Not be equal")


    def test_mutatie(self):
        eps = 0
        for dix in range(10):
            from src.individ import Individ
            i = Individ(pb=self.pb)
            print('\nindivid: ',str(i))
            j = i.mutatie()
            print(' mutant: ',str(j))
            eps += abs(i.fitness_val - j.fitness_val) 
        self.assertNotEqual(eps, 0, "Shall be >0, macar o mutatie ")


    def test_load_from_file(self):
        self.assertEqual(1, 0, "... ")


    def test_load_from_object(self):
        # Spatiul problemei 
        from src.individ import Individ
        i = Individ(pb=self.pb)
        print(str(i))

        self.assertEqual(1, 0, "... ")


    def test_asemnare(self):
        a = 0
        for dix in range(10):
            from src.individ import Individ
            i = Individ(pb=self.pb)
            print('\nindivid: ',str(i))
            j = i.mutatie()
            print(' mutant: ',str(j))
            print('asemanarea: ', str(i.asemanare(j)))
            a += i.asemanare(j)
           
        self.assertNotEqual(a, 0, "Shall be >0, macar o mutatie ")


    def test_from_carcter(self):
        import numpy as np
        import json
        from src.problema import Problema
        from src.individ import Individ
        
        Space={ 
                    'num_leaves':       [ x for x in np.arange(   30, 50,   1 ) ],
                    'min_child_weight': [ x for x in np.arange( .01, 1,   .01 ) ],
                    'feature_fraction': [ x for x in np.arange( .01, 1,   .01 ) ],
                    'bagging_fraction': [ x for x in np.arange( .01, 1,   .01 ) ],
                    'min_data_in_leaf': [ x for x in np.arange(  1, 100,   5  ) ],          
                    'max_depth':        [ x for x in np.arange(  6, 16,    1  ) ],
                    
                    'bagging_seed':     [ x for x in np.arange(  1, 100,    10  ) ],

                    'reg_alpha':  [ 1e-5, 1e-2, 0.1, 1, 100 ], # [ x for x in np.arange( .1, 100,    .1  ) ],
                    'reg_lambda': [ x for x in np.arange( .1, 1,    .05  ) ],
                    'subsample':  [ x for x in np.arange( .1, 1,    .05  ) ],

                    'random_state':   [50],
                    'boosting_type':  ['gbdt'],
                    'device':         ['gpu'],
                    # 'gpu_platform_id': [0],
                    # 'gpu_device_id':   [0],
                    
                    'objective':  ['binary'],
                    'metric':     ['auc'],       
                    'verbosity':  [-1],
                    'n_jobs':     [-1],
                    'silent':     [False],
                    'verbose':    [1],
                    # 'early_stopping_rounds': [100],
                
                'learning_rate': [0.3],
                'n_estimators':  [1000],
                }
        
        my_fitness = lambda i: 0
        Johns_pb = Problema(fitness=my_fitness, path_to_evol='./temp/', space=Space)
        John = Individ(pb=Johns_pb)
        s = "{\"num_leaves\": 47, \"min_child_weight\": 0.49, \"feature_fraction\": 0.62, \"bagging_fraction\": 0.86, \"min_data_in_leaf\": 61, \"max_depth\": 15, \"bagging_seed\": 11, \"reg_alpha\": 100, \"reg_lambda\": 0.45000000000000007, \"subsample\": 0.5500000000000002, \"random_state\": 50, \"boosting_type\": \"gbdt\", \"device\": \"gpu\", \"objective\": \"binary\", \"metric\": \"auc\", \"verbosity\": -1, \"n_jobs\": -1, \"silent\": false, \"verbose\": 1, \"learning_rate\": 0.3, \"n_estimators\": 1000}"
        caracterul_lui_Johny_as_a_boy = json.loads(s)
       
        John.from_caracter( caracterul_lui_Johny_as_a_boy )

        d = json.loads(s)
        d['name'] = 'test'
        jc =  John.get_caracter()['caracter']
        jc['name'] = 'test'
        # print(d)
        # print( jc== d )
        # print(jc)

        print("\n\nA: ", jc)
        print("\n\nB:" ,  d)
        


        self.assertEqual(d, jc, "Shall be >0, macar o mutatie ")


if __name__ == '__main__':
    unittest.main()

