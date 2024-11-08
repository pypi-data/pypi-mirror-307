def test(*args):
    for index, arg in enumerate(args):
        if not isinstance(arg, int):
            print(f"L'arg position {index} avec la valeur '{arg}' n'est pas un entier, voici le type : {type(arg)}" )
            return
    print('Tout les args sont des entier')