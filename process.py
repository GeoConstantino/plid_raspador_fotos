import base64

from zeep import Client

from decouple import config

# configurações de acesso
CNPJ = config('CNPJ')
CHAVE = config('CHAVE')
PERFIL = config('PERFIL')
CPF = config('CPF')

# local para fotos
PATH = "fotos"


def manda_consulta(rg, conn):
    #conn = Client(URL_CONSULTA_RG)
    conn.service.consultarRG(CNPJ,CHAVE,PERFIL,rg, rg.zfill(10),CPF)


def pega_resultado(rg, ress):
    res = ress.service.BuscarProcessados(CNPJ,CHAVE,PERFIL,rg)
    res = res[0]
    return (res.fotoCivil)

def conectar_busca():
    return (Client("http://10.200.96.170:8080/servico.asmx?wsdl"))

def conectar_resultado():
    return (Client("http://10.200.96.170:8181/servico.asmx?wsdl"))


def salva_foto(foto, rg):
    try:
        with open('{path}/{rg}.jpg'.format(rg=rg, path=PATH), 'wb') as fobj:
            fobj.write(base64.b64decode(str.encode(foto)))
        print("foto salva: {}".format)
    except:
        print("erro ao salvar o arquivo do rg: {}".format(rg)) 

if __name__=="__main__":

    #procesa csv
    # 

    conn = conectar_busca()

    ress = conectar_resultado()

    lista_rg = ['211367230','98255060']

    for rg in lista_rg:
        manda_consulta(rg, conn)

    for rg in lista_rg:
        foto = pega_resultado(rg, ress)
        if foto is not None:
            salva_foto(foto.string[0], rg)
        else:
            print("{} foto não localizada.".format(rg))
