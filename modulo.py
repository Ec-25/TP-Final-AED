from os.path import getsize
from pickle import dump, load

class Series:
    def __init__(self, poster:str, title:str, runtime:str, certificate:str, episodes:int, genre:int, rating:float, overwiew:str, votes:int) -> None:
        self.poster_link = poster
        self.series_title = title
        self.runtime_series = runtime
        self.certificate = certificate
        self.runtime_episodes = episodes
        self.genre = genre
        self.rating = rating
        self.overwiew = overwiew
        self.no_vote = votes


    def __str__(self) -> str:
        return f' Serie: {self.series_title} ; Runtime: {self.runtime_series} ; Cerificacion: {self.certificate} ; Tiempo Prom de Episodios: {self.runtime_episodes} min ; Genero: {self.genre} ; Rating: {self.rating} ; Resumen: {self.overwiew} ; Votos: {self.no_vote} '


    def save(self) -> str:
        return f'{self.series_title}|{self.runtime_series}|{self.certificate}|{self.runtime_episodes}|{self.genre}|{self.rating}|{self.overwiew}|{self.no_vote}'    


class Generos:
    def __init__(self, index:int, nombre:str, cantidad:int) -> None:
        self.indice = index
        self.nombre = nombre
        self.cantidad = cantidad


    def __str__(self) -> str:
        return f"\n[Indice de Codigo:]  {self.indice}   [Genero:]   {self.nombre}   [Cantidad Listado:] {self.cantidad}"


def cargar_generos(vector: list)->list:
    LOCATE = '.\\generos.txt'

    file = open(LOCATE, 'rt')
    SIZE = getsize(LOCATE)
    
    # tell() position actual|| seek() move pointer
    while file.tell() < SIZE:
        obj = file.readline()
        vector.append(obj[:-1])

    file.close()
    return vector


def cargar_series(vector: list, codigos: list)->list:
    LOCATE = '.\\series_aed.csv'

    file = open(LOCATE, 'rt')
    SIZE = getsize(LOCATE)
    
    if not codigos == []:
        flag = False
        cont = 0
        # tell() position actual|| seek() move pointer
        while file.tell() < SIZE:
            cont += 1
            line = file.readline()
            
            if flag:
                obj = process_line(line[:-1])

                flag_cumple, obj = cumple_duracion(obj)
                
                if not flag_cumple:
                    continue

                obj = formatear_genero(obj, codigos)

                pos = buscar_posicion(obj.no_vote, vector)

                vector.insert(pos, obj)

            else:
                flag = True


        file.close()
        return vector, cont
    
    else:
        file.close()
        print('\nNo Han sido cargados los Codigos...')
        return [], 0


def process_line(line: str)->Series:
    sec = line.split('|')

    flt = sec[6].replace(',', '.')
    #epi = sec[4].replace("min", "")

    obj = Series(
        sec[0],
        sec[1],
        sec[2],
        sec[3],
        sec[4], # int(epi),
        sec[5],
        float(flt),
        sec[7],
        int(sec[12])
    )
    return obj


def buscar_posicion(votos: int, registro: list)-> int:
    izq = 0
    der = len(registro) - 1

    while izq <= der:
        cen = (izq + der) // 2

        if registro[cen].no_vote == votos:
            return cen + 1

        elif registro[cen].no_vote > votos:
            izq = cen + 1

        else:
            der = cen - 1

    return izq


def cumple_duracion(registro: Series)->Series:

    if registro.runtime_episodes == "":
        t = False

    else:
        t = True
        dur:str = registro.runtime_episodes
        dur = dur.replace("min", "")
        registro.runtime_episodes = int(dur)

    return t, registro
    

def formatear_genero(objeto: Series, generos: list)->Series:
    genre = objeto.genre
    index = generos.index(genre)
    objeto.genre = index

    return objeto


def validar_tiempo(msg: str)->int:
    """
    El mensaje indica lo que el usuario debe cargar.
    """
    x = ''
    flag = False
    while True:
        if flag:
            print('Carga Invalida, Ingrese un nro. valido...')

        else:
            flag = True

        x = input(f"\n{msg}: ")

        if x.isdigit() and int(x) >= 0:
            return int(x)

        else:
            pass


def obtener_coincidentes_tiempo(desde: int, hasta: int, lista: list):
    coincidentes = []
    duracion = 0
    for i in range(len(lista)):
        elemento: Series = lista[i]

        if desde < elemento.runtime_episodes < hasta:
            coincidentes.append(elemento)
            duracion += elemento.runtime_episodes

    return coincidentes, duracion


def guardar_cvs(lista: list)->None:
    LOCATE = '.\\series_saved.csv'
    file = open(LOCATE, 'wt')

    line = 'Poster_Link|Series_Title|Runtime_of_Series|Certificate|Runtime_of_Episodes|Genre|IMDB_Rating|Overview|No_of_Votes\n'

    file.write(line)

    for i in range(len(lista)):
        objeto: Series = lista[i]
            
        line = objeto.save()
        msg = line + '\n'

        file.write(msg)

    file.close()
    return


def determinar_cantidad_genero(bault: list, series: list)->list:
    for i in range(len(series)):
        objeto: Series = series[i]
        genero = objeto.genre

        bault[genero] += 1

    return bault


def mostrar_resultados_generos(contador: list, generos: list)->None:
    for i in range(len(contador)):
        genero = generos[i]
        resultado = contador[i]
        if resultado > 1:
            print(f"\nHay '{resultado}' series de Genero '{genero}'")

        else:
            print(f"\nHay '{resultado}' serie de Genero '{genero}'")

    return


def registro_generos(generos: list, resutados: list)->list:
    registro = []
    
    for i in range(len(generos)):
        genero = generos[i]
        resutado = resutados[i]
        indx = i

        objeto = Generos(indx, genero, resutado)

        registro.append(objeto)

    return registro


def guardar_bin(registro: list)->None:
    LOCATE = '.\\results.bin'
    file = open(LOCATE, 'wb')

    dump(registro, file)

    file.close()
    return


def cargar_binario(file)->list:
    lib = load(file)

    lib = tuple(lib)

    return lib


def mostrar_carga(carga: list)->None:
    for i in range(len(carga)):

        objeto: Generos = carga[i]

        print(objeto.__str__())

    return


def buscar_serie(a_buscar: str, lista: list)->list:
    flag = False

    for i in range(len(lista)):
        objeto: Series = lista[i]

        if objeto.series_title == a_buscar:

            objeto.no_vote += 1
            
            flag = True
            break

    if flag:
        print("\nSe ha encontrado una coincidencia y se ha visitado...\n")
        print(objeto.__str__())

    else:
        print(f"\nNo se ha encontrado ninguna coincidencia con {a_buscar}")

    return lista


