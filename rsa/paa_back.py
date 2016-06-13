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
            # print i, Z[i]

        i = i + 1

    Z.__delitem__(0)  # deletei o zero da inicializacao

    numero_amostrasZ = len(Z)

    print"numero de linhas de Z vale: " + str(numero_amostrasZ)
    return Z
    print "*********** fim de lerbase() ********************************"

# *************************** fim das funcoes auxiliares ***********************



#******** principal **********************************

#ingredientes do RSA (de cript e seg de rede , 4. edicao, pag. 207)

#p,q numeros primos                     privados, escolhidos
#n=pq                                   publico, calculado
#e, com mdc(fi(n),e)=1 , com 1<e<fi(n)  publico, escolhido   fi e a funcao totiente
#d congruente e^-1*mod(fi(n))            privado, calculado
# chave privada={d,n}
#chave publica={e,n}


#criando p e q
print"************************************************"
#https://pt.wikipedia.org/wiki/RSA
print"Escolhendo aleatoriamente p...(n.maxbits=1024) "

p = prime.getprime(512)  # com n bits<256, deu erro na decodificacao da linha - caracteres estranhos
print"O valor de p eh :", p
print"Escolhendo aleatoriamente q...(n.maxbits=1024)"
q = prime.getprime(512)
print"O valor de q eh:", q
n = p * q
print"n=p*q=", n
toti = (p - 1) * (q - 1)
print"funcao totiente(n) vale:", toti
print"Escolhendo e , com e valendo 1<e<toti(n).."

achou = "nao"

for i in range(1, 3000):
    e = randnum.read_random_odd_int(512)
    #print"e vale:",e
    if e < toti:
        if prime.are_relatively_prime(e, toti) and e > 1:
            #print"e vale:",e
            achou = "sim"
            break

if achou == "nao":
    print"nao achou e"
    exit(0)

print"e vale:", e
print"************************************************"
print "Chave publica vale: {e,n}={", e, ",", n, "}"
print"************************************************"

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

print"************************************************"
print "Chave privada vale: {p,q,d}={", p, ",", q, ",", d, "}"
print"************************************************"


#variaveis locais
arquivo = []
codificado = []
arquivo_dec = []
teste = []
linha_int = []
c = []
g = []
decod = []

print"Carregando o arquivo..."

arquivo = lerBase()
linhas = len(arquivo)
#print"Numero de linhas do arquivo eh :",linhas

print"************************************************"
print"Iniciando a codificacao por linha..."

for linha in range(0, linhas):
    linha_int.append(int(arquivo[linha + 1].encode("hex"),
                         16))  #http://www.commandlinefu.com/commands/view/9884/convert-ascii-string-to-hex
    print"linha", linha + 1, arquivo[linha + 1], linha_int[linha]

"""
forca_bruta.append(int(arquivo[1].encode("hex"),16))
print"linha",1,forca_bruta[0]
exit(0)
"""

print"Encryptando..."

for linha in range(0, linhas):
    # a funcao pow(x,y,z)  eh nativa do python e com 3 argumentos vale (x**y) % z ou seja, x^y modz
    c.append(pow(linha_int[linha], e, n))
    print"C=M^e mod(n) vale:", linha + 1, c[linha]

print"Decryptando..."

for linha in range(0, linhas):
    g.append(pow(c[linha], d, n))
    print"M=C^d mod(n) vale:", linha, g[linha]

print "Revertendo o int para string..."

for linha in range(0, linhas):
    decod.append(transform.int2bytes(g[linha]))
    print"linha", linha, decod[linha]

print"Codificacao concluida"
print"************************************************"

print"Algoritmo de forca bruta..."
# Conhecida a mensagem M e a chave publica e, achar a chave privada d



#***** main *************************
#1-Gerar p




exit(0)

