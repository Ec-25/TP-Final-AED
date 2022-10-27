
from modulo import cargar_generos, cargar_series


def menu()->int:
    '''
    Interfaz Grafica Consola con retorno de opcion elejida.
    '''
    print(f'''
    {'='*40}
            MENU
    {'='*40}
        0) - Salir.
        1) - Cargar Generos.
        2) - Cargar Series.
    {'='*40}
    ''')
    opc = ''
    flag = False
    while not opc.isdigit() or (int(opc) < 0 or int(opc) > 2):

        if flag:
            print('Opcion Invalida...')
        else:
            flag = True

        opc = input('Ingrese opcion: ')

    return int(opc)


def  app():
    '''
    Ejecucion de App Principal.
    '''
    generos = []
    series = []
    while True:
        opc = menu()

        if opc == 1:
            generos = cargar_generos(generos)
            print('\nGeneros Cargados Correctamente')

        elif opc == 2:
            series, c = cargar_series(series, generos)
            if c != 0:
                print('\nSeries Cargados Correctamente')
                print(f"Se cargaron {len(series)} series, y {c-len(series)} fueron descartadas...")

            else:
                print("Cargue los 'Generos' antes de volver a intentar.\n")

        else:
            exit('Done!')


if __name__ == '__main__':
    app()