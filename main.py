from os.path import exists
from modulo import buscar_serie, cargar_binario, cargar_generos, cargar_series, determinar_cantidad_genero, guardar_bin, guardar_cvs, mostrar_carga, mostrar_resultados_generos, obtener_coincidentes_tiempo, registro_generos, validar_tiempo


def menu()->int:
    '''
    Interfaz Grafica Consola con retorno de opcion elejida.
    '''
    print(f'''
    {'='*60}
            MENU
    {'='*60}
        0) - Salir.
        1) - Cargar Generos.
        2) - Cargar Series.
        3) - Mostrar Series Segun Duracion.
        4) - Determinar la cantidad de Series x Genero.
        5) - Generar Binario de los resultados x Genero.
        6) - Mostrar Binario de resultados.
        7) - Buscar Serie x Nombre.
    {'='*60}
    ''')
    opc = ''
    flag = False

    while not opc.isdigit() or (int(opc) < 0 or int(opc) > 7):

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
    conteo_generos = []
    while True:
        opc = menu()

        if opc == 1:
            generos = cargar_generos(generos)
            
            if len(generos) != 0:
                conteo_generos = [0] * len(generos)

                print('\nGeneros Cargados Correctamente')
            
            else:

                print('No se pudieron cargar los Generos.')

        elif opc == 2:
            series, c = cargar_series(series, generos)

            if c != 0:
                print('\nSeries Cargados Correctamente')
                print(f"Se cargaron {len(series)} series, y {c-len(series)} fueron descartadas...")

            else:
                print("Cargue los 'Generos' antes de volver a intentar.\n")

            del c

        elif opc == 3:
            if len(series) != 0:
                desde = validar_tiempo("Indique el Inicio")
                hasta = validar_tiempo("Indique el Final")

                coincidentes, duracion = obtener_coincidentes_tiempo(desde, hasta, series)

                for i in range(len(coincidentes)):
                    print("\n", coincidentes[i].__str__())
                
                print(f"\nLa duracion promedio de las series coincidentes es {round(duracion/len(coincidentes), 2)} minutos.")


                eleccion = input("\nDesea Guardar los resultados Obtenidos? [S|N]  ")

                if eleccion in "sSyY":
                    guardar_cvs(coincidentes)

                    print("\nDatos Guardados Correctamente...")
                
                else:
                    print("\nDatos Mostrados Correctamente...")

            else:
                print("Cargue las 'Series' antes de volver a intentar.\n")
            
            del desde, hasta, coincidentes, duracion, eleccion

        elif opc == 4:
            if len(series) != 0 and len(generos) != 0:

                conteo_generos = determinar_cantidad_genero(conteo_generos, series)
                
                mostrar_resultados_generos(conteo_generos, generos)

                print("\nResultados Mostrados Correctamente...")

            else:
                print("\nAntes debe cargar los Generos y las Series...")

        elif opc == 5:
            if len(generos) != 0 and len(conteo_generos) != 0:
                registro = registro_generos(generos, conteo_generos)

                guardar_bin(registro)

                print("\nResultados Guardados Correctamente...")

            else:
                print("\nAntes debe cargar los Generos y Resultados...")

            del registro

        elif opc == 6:
            LOCATE = '.\\results.bin'

            if exists(LOCATE):
                file = open(LOCATE, 'rb')

                carga = cargar_binario(file)
                file.close()

                mostrar_carga(carga)

                print("\nResultados Mostrados Correctamente...")

            else:
                print('\nNo Existen Resultados Guardados...')

            del file, carga

        elif opc == 7:
            if len(series) != 0:
                titulo = input('\nIngrese el titulo de la serie a buscar: ')
            
                series = buscar_serie(titulo, series)

            else:
                print('\nAntes de buscar una serie debe Cargarlas...')

            del titulo

        else:
            exit('Done!')


if __name__ == '__main__':
    app()
