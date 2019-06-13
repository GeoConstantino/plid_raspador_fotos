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
PATH = "out"


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

def conectar_busca():
    return (Client("http://10.200.96.170:8080/servico.asmx?wsdl"))

def conectar_resultado():
    return (Client("http://10.200.96.170:8181/servico.asmx?wsdl"))


def salva_foto(foto, rg):
    with open('{path}/{rg}.jpg'.format(rg=rg, path=PATH), 'wb') as fobj:
        fobj.write(base64.b64decode(str.encode(foto)))
    
   #print('foto salva:' + rg)

    

def lista_rgs(file):
    df = pd.read_csv(file, encoding='latin1')
    df = df.loc[:,['VTMA_RG','SNCA_VTMA_DK']]
    df = df.values.tolist()

    return df

if __name__=="__main__":

    conn = conectar_busca()
    ress = conectar_resultado()

    for root,dirs,files in os.walk("in"):
        for file in files:
            if file.endswith(".csv"):
                file_rgs = lista_rgs(file)
                
                for rg, ident in file_rgs:
                    manda_consulta(rg, conn)

                for rg, ident in file_rgs:
                    try:
                        foto = pega_resultado(rg, ress)
                    except TypeError as error:
                        print("Não encontrado {errorg}, {tipoerro}".format(errorg=rg, tipoerro=error))
                    if foto is not None:
                        salva_foto(foto, ident)
                    else:
                        print("{} foto não localizada.".format(rg))