# evool

## Problema
Coefficients:

    COEFICIENT_SWITCH_CROMOZOM_LA_MATE = .5              # % schimba cromozom  
    COEFICIENT_MUTATIE_CROMOZOM_INDIVIDUAL = .5          # % gena ramane neafectata,   mic--> mutatii intensive 
    COEFICIENT_DELTA_MUTATIE_CROMOZOM_INDIVIDUAL = .05   # deplasarea mutatiei
    COEFICIENT_INDIVIZI_MATE = .5                        # % un individ se imperecheaza

Mapped Space: ???

Solve:
    n_rounds=3, n_indivizi=20, n_generatii=2, mortalitate=.9, live_better=True, specie='wolverine' ):

Specia:   a problem can handle multiple species


## Individ
### Def
Contains the genes of an individ over the problem space. See problem.
    genes are coordinates of the characteristics map/ Space
    character are values of individ's characteristics

get_character()


### Methods 
    __init__(problem)
Throws an exception if problem is not passed

# Sample 
    Problem's space
    S = {
        'x': [x for x in np.arange(-10, 10, 0.0001)],
        'y': [x for x in np.arange(-10, 10, 0.0001)],      
    } 
    Maximize for i=individ
    def my_fitness( i ):
        return -i['x']**2 + 1 -i['y']**2
 