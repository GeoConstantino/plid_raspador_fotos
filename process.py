import argparse
import base64
import os

import pandas as pd

from zeep import Client
from decouple import config

import ipdb

# configurações de acesso
CNPJ = config('CNPJ')
CHAVE = config('CHAVE')
PERFIL = config('PERFIL')
CPF = config('CPF')

# local para fotos
PATH = "retratos"


### adicinar feature de passar apenas um rg
### 

def conectar_busca():
    return (Client("http://10.200.96.170:8080/servico.asmx?wsdl"))


def conectar_resultado():
    return (Client("http://10.200.96.170:8181/servico.asmx?wsdl"))


def manda_consulta(rg, conn):
    print('sending {}'.format(rg))
    conn.service.consultarRG(CNPJ,CHAVE,PERFIL,rg, rg.zfill(10),CPF)


def pega_resultado(rg, ress):
    res = ress.service.BuscarProcessados(CNPJ,CHAVE,PERFIL,rg)
    try:
        res1 = res[0].fotoCivil
        res2 = res1.string[0]
    except:
        return None
    return (res2)


def salva_foto(foto, rg):
    check_out_exist(PATH)
    with open('{path}/{rg}.jpg'.format(rg=rg, path=PATH), 'wb') as fobj:
        fobj.write(base64.b64decode(str.encode(foto)))
    
 
def lista_rgs(file):
    df = pd.read_csv(file, encoding='latin1')
    df = df.loc[:,['VTMA_RG','SNCA_VTMA_DK']]
    df = df.values.tolist()

    return df


def check_out_exist(path):
    if not os.path.isdir(path):
        os.makedirs(PATH)
        

if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--rg',
        help='Para pesquisar por foto de apenas um RG.'
    )
    parser.add_argument(
        '--name',
        help='Nome do arquivo ".jpg" a ser salvo.'
    )

    args = parser.parse_args()
    arg_rg = args.rg
    arg_name = args.name

    conn = conectar_busca()
    ress = conectar_resultado()

    if arg_rg is None:
        for root,dirs,files in os.walk("in"):
            for file in files:
                
                if file.endswith(".csv"):
                    file_rgs = lista_rgs(file)
                    
                    for rg, ident in file_rgs:
                        manda_consulta(rg, conn)

                    for rg, ident in file_rgs:
                        
                        foto = pega_resultado(rg, ress)
                        
                        if foto is not None:
                            salva_foto(foto, ident)
                        else:
                            print("{} foto não localizada.".format(rg))
    
    else:
        manda_consulta(arg_rg,conn)
        foto = pega_resultado(arg_rg, ress)
        if foto is not None:
            salva_foto(foto, arg_name)
        else:
            print('Foto não localizada.')
