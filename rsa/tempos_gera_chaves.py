__author__ = 'Salvador'

import time

import prime
import common
import randnum


# ******* gera chaves publica e privada ******************
def gera_chaves(pbits, qbits, ebits):
    # criando p e q
    #print"************************************************"
    #https://pt.wikipedia.org/wiki/RSA
    #print"Escolhendo aleatoriamente p com n.maxbits=",pbits

    p = prime.getprime(pbits)  # com n bits<256, deu erro na decodificacao da linha - caracteres estranhos
    #print"O valor de p eh :",p
    #print"Escolhendo aleatoriamente q com n.maxbits=",qbits
    q = prime.getprime(qbits)
    #print"O valor de q eh:",q
    n = p * q
    #print"n=p*q=",n
    toti = (p - 1) * (q - 1)
    #print"funcao totiente(n) vale:",toti
    #print"Escolhendo e , com e valendo 1<e<toti(n).."

    achou = "nao"

    for i in range(1, 3000):  # tenta criar e no maximo 3000 vezes antes de sair com erro
        #print"ebits vale:",ebits
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

    #print"e vale:",e
    #print"************************************************************************************"
    #print "Chave publica vale: {e,n}={",e,",",n,"}"
    #print"************************************************************************************"

    #print "Calculando d..."
    #d congruente 1 mod(toti(n)) ou seja, d eh o inverso multiplicativo de e em mod(toti(n))

    #algoritmo de euclides estendido: extended_gcd(a, b):
    #retorna uma tupla (r, i, j) de modo que r = gcd(a, b) = ia + jb ou d=ax+by, para a tupla (d,x,y) cormen 680
    # r = gcd(a,b) i = inverso multiplicativo de a mod b
    #      ou      j = inverso multiplicativo of b mod a
    # Neg return values for i or j are made positive mod b or a respectively
    # Iterative Version is faster and uses much less stack space

    tuplad = common.extended_gcd(e, toti)
    #print"tupla d vale:",tuplad
    d = tuplad[1]
    #print "d vale:", d

    #print"************************************************************************************"
    #print "Chave privada vale: {d,n}={",d,",",n,"}"
    #print"************************************************************************************"

    return (p, q, d, e, n)


print"Teste de tempos de geracao de chaves em funcao do num. de bits "

pbits = 5096
qbits = 5096
ebits = 5096
timer1 = time.clock()
# print "inicio",timer1
gera_chaves(pbits, qbits, ebits)
timer2 = time.clock()
#print"fim",timer2
print "duracao:=", (timer2 - timer1) * 1000, "ms"

