__author__ = 'Salvador'

from arquivo import Arquivo
import prime
import common
import transform
import randnum


# *********************funcoes auxiliares ***************************************
def lerBase():
    Z = {0: ""}


    # lendo o arquivo e criando Z


    w = Arquivo("abalone_names.txt")
    le = w.open("abalone_names.txt")

    loop = "sim"
    i = 1

    print"Lendo o arquivo de dados txt e criando Z..."
    while 1:
        linha = w.readline()
        if linha == None:
            w.close()
            break
        else:
            Z[i] = linha
            print i, Z[i]

        i = i + 1

    Z.__delitem__(0)  # deletei o zero da inicializacao

    numero_amostrasZ = len(Z)

    print"numero de linhas de Z vale: " + str(numero_amostrasZ)
    return (Z, len(Z))
    # *************************************************************


import time
from math import sqrt


def verifica_fatores(n):
    # print "Inicio:",inicio
    d = 3
    x = int(sqrt(n))
    if n % 2 == 0:
        #print "E par"
        return False

    while d <= x:

        #print "divisor:",d
        if n % d == 0:
            final = time.ctime()
            print d, '*', n / d, '=', n
            return (d, n / d)
        else:
            d += 2

    return False


# **************  fim da funcao verifica_fatores ***************

#******* gera chaves publica e privada ******************
def gera_chaves(pbits, qbits, ebits):
    #criando p e q
    print"************************************************"
    #https://pt.wikipedia.org/wiki/RSA
    print"Escolhendo aleatoriamente p com n.maxbits=", pbits

    p = prime.getprime(pbits)  # com n bits<256, deu erro na decodificacao da linha - caracteres estranhos
    print"O valor de p eh :", p
    print"Escolhendo aleatoriamente q com n.maxbits=", qbits
    q = prime.getprime(qbits)
    print"O valor de q eh:", q
    n = p * q
    print"n=p*q=", n
    toti = (p - 1) * (q - 1)
    print"funcao totiente(n) vale:", toti
    print"Escolhendo e , com e valendo 1<e<toti(n).."

    achou = "nao"

    for i in range(1, 3000):  # tenta criar e no maximo 3000 vezes antes de sair com erro
        print"ebits vale:", ebits
        e = randnum.read_random_odd_int(ebits)
        #print"e vale:",e
        if e < toti:
            if prime.are_relatively_prime(e, toti) and e > 1:
                #print"e vale:",e
                achou = "sim"
                break

    if achou == "nao":
        print"nao achou e, por favor tente novamente"
        exit(0)

    print"e vale:", e
    print"************************************************************************************"
    print "Chave publica vale: {e,n}={", e, ",", n, "}"
    print"************************************************************************************"

    print "Calculando d..."
    #d congruente 1 mod(toti(n)) ou seja, d eh o inverso multiplicativo de e em mod(toti(n))

    #algoritmo de euclides estendido: extended_gcd(a, b):
    #retorna uma tupla (r, i, j) de modo que r = gcd(a, b) = ia + jb ou d=ax+by, para a tupla (d,x,y) cormen 680
    # r = gcd(a,b) i = inverso multiplicativo de a mod b
    #      ou      j = inverso multiplicativo of b mod a
    # Neg return values for i or j are made positive mod b or a respectively
    # Iterative Version is faster and uses much less stack space

    tuplad = common.extended_gcd(e, toti)
    print"tupla d vale:", tuplad
    d = tuplad[1]
    print "d vale:", d

    print"************************************************************************************"
    print "Chave privada vale: {d,n}={", d, ",", n, "}"
    print"************************************************************************************"

    return (p, q, d, e, n)


def codifica_linha(arquivo, linhas):
    linha_int = []

    print"************************************************"
    print"Iniciando a codificacao por linha..."
    print"linhas:", linhas

    for linha in range(0, linhas):
        linha_int.append(int(arquivo[linha + 1].encode("hex"),
                             16))  #http://www.commandlinefu.com/commands/view/9884/convert-ascii-string-to-hex
        print"linha", linha + 1, arquivo[linha + 1], linha_int[linha]

    return linha_int


def criptografa_linha(h, linhas, e, n):
    print"Encryptando..."
    c = []

    for linha in range(0, linhas):
        # a funcao pow(x,y,z)  eh nativa do python e com 3 argumentos vale (x**y) % z ou seja, x^y modz

        c.append(pow(h[linha], e, n))
        print"C=M^e mod(n) vale:", linha + 1, c[linha]

    return c


def decriptgrafa_linha(c, linhas, d, n):
    print"Decryptando..."
    g = []
    for linha in range(0, linhas):
        g.append(pow(c[linha], d, n))
        print"M=C^d mod(n) vale:", linha + 1, g[linha]

    return g


def decodifica_linha(g, linhas):
    decod = []
    print "Revertendo o int para string..."

    for linha in range(0, linhas):
        decod.append(transform.int2bytes(g[linha]))
        print"linha", linha + 1, decod[linha]

    print"Decodificacao concluida"
    print"************************************************"

    return decod


def continua():
    tecla = raw_input("Aperte qualquer tecla para continuar:")
    return


#*************************** fim das funcoes auxiliares ***********************



#******** principal **********************************

#ingredientes do RSA (de cript e seg de rede , 4. edicao, pag. 207)

#p,q numeros primos                     privados, escolhidos
#n=pq                                   publico, calculado
#e, com mdc(fi(n),e)=1 , com 1<e<fi(n)  publico, escolhido   fi e a funcao totiente
#d congruente e^-1*mod(fi(n))            privado, calculado
# chave privada={d,n}
#chave publica={e,n}


#criando p, q, n , e, d
# print"************************************************"
#https://pt.wikipedia.org/wiki/RSA


#variaveis locais

print"************************************************************************************"
print"Carregando o arquivo..."
arquivo = lerBase()
nlinhas = int(arquivo[1])
print"************************************************************************************"
#continua()

print"Gerando chaves publica e privada..."
bits = 32

chaves = gera_chaves(bits, bits, bits)  #(pbits,qbits,ebits)  e retorna (p,q,d,e,n)
p = chaves[0]
q = chaves[1]
d = chaves[2]
e = chaves[3]
n = chaves[4]
#print p,q,d,e,n

print"************************************************************************************"
#continua()
print"Codificando cada linha do arquivo em um numero inteiro ..."
arquivo_codificado = codifica_linha(arquivo[0], nlinhas)  # corresponde ao c
print"************************************************************************************"

print"Criptografando cada numero inteiro..."
arquivo_criptografado = criptografa_linha(arquivo_codificado, nlinhas, e, n)
print"************************************************************************************"
print"Decriptografando o arquivo..."
arquivo_decriptografado = decriptgrafa_linha(arquivo_criptografado, nlinhas, d, n)
print"************************************************************************************"
print "Decodificando de inteiro para ascii..."
arquivo_decodificado = decodifica_linha(arquivo_decriptografado, nlinhas)

print"Algoritmo de forca bruta..."
# Conhecida a mensagem M e a chave publica e, achar a chave privada d, sabendo que n=pq e (
#https://www.vivaolinux.com.br/artigo/Quebrando-a-criptografia-RSA?pagina=3
timer1 = time.clock()
forca_bruta = verifica_fatores(n)
timer2 = time.clock()
print "duracao da tentativa", (timer2 - timer1) * 1000, "ms"

exit(0)

