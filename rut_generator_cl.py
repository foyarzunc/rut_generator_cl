import argparse
import random
import re
import subprocess

def install(package):
    subprocess.check_call(['python', "-m", "pip", "install", package])

try:
    from prettytable import PrettyTable
except ImportError:
    print("Instalando prettytable...")
    install("prettytable")
    from prettytable import PrettyTable



parser = argparse.ArgumentParser(description="Generador de RUTs Chile", add_help=False)
parser.add_argument("-f", '--file', type=str, action='store', help="Archivo de destino donde serán almacenados los ruts")
parser.add_argument("-s", '--separator', action="store_true", help="Genera ruts con separador y digito verificador ej: 12.345.678-9")
parser.add_argument("-d", "--dash", action="store_true", help="Genera ruts con separador ej: 12345678-9")
parser.add_argument("-c", "--count", type=int, default=10, action="store", help="Indica la cantidad de ruts a generar")
parser.add_argument("-h", "--help", action="store_true", help="Muestra la tabla de opciones de ayuda")
args = parser.parse_args()


x = PrettyTable()
x.field_names = ["Argumento","Descripción","Ejemplo"]
x.add_row(["-f", "--file","Archivo de destino donde serán almacenados los ruts"])
x.add_row(["-s", "--separator","Genera ruts con separador y digito verificador ej: 12.345.678-9"])
x.add_row(["-d", "--dash", "Genera ruts con separador ej: 12345678-9"])
x.add_row(["-c", "--count","Indica la cantidad de ruts a generar"])
x.add_row(["-h", "--help", "Muestra esta tabla de ayuda"])



def calculate_dv(rut):
    rut = str(rut)
    rut_invertido = rut[::-1]
    factores = [2, 3, 4, 5, 6, 7]
    suma = 0
    for i, digito in enumerate(rut_invertido):
        suma += int(digito) * factores[i % len(factores)]
    
    resto = suma % 11
    digito_verificador = 11 - resto
    
    if digito_verificador == 11:
        return '0'
    elif digito_verificador == 10:
        return 'K'
    else:
        return str(digito_verificador)

def normalice_with_dot(list_rut):
    find_dash = re.compile("-")
    list_return = []
    for row in list_rut:
        if (find_dash.search(row)):
            rut, dv = row.split("-")
        else:
            rut = row[:len(row)-1]            
            dv = row[-1]
        rut = int(re.sub(r"\D", "", rut))
        p_rut = f"{rut:,}".replace(",", ".")
        final_rut = f"{p_rut}-{dv.upper()}"
        list_return.append(final_rut)
    return list_return

def normalice_without_dot(list_rut):
    find_dash = re.compile("-")
    list_return = []
    for rut in list_rut:
        if find_dash.search(rut):
            # El RUT ya tiene guión, lo dejamos como está
            list_return.append(rut)
        else:
            # El RUT no tiene guión, lo separamos y añadimos
            base_rut = rut[:-1]  # Todo excepto el último carácter
            dv = rut[-1]  # Último carácter
            list_return.append(f"{base_rut}-{dv}")
    return list_return

def make_rut(list_rut):
    return [f"{rut}{calculate_dv(rut)}" for rut in list_rut]

def rut_generator_cl():
    if args.help:
        print(x)
    else:
        unique_rut = []
        if args.count:
            while args.count > len(unique_rut):
                num_rut = random.randint(7000000, 25999999)
                if num_rut not in unique_rut:
                    unique_rut.append(num_rut)
        unique_rut = make_rut(unique_rut)
        if args.separator:
            unique_rut = normalice_with_dot(unique_rut)
        elif args.dash:
            unique_rut = normalice_without_dot(unique_rut)
        
        if (args.file):
            with open(args.file, mode="w") as fop:
                fop.write("\n".join(unique_rut))
        else:
            print("\n".join(unique_rut))


    #print(unique_rut)

if __name__ == "__main__":
    rut_generator_cl()