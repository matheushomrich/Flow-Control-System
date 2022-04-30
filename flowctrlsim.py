#T1 da disciplina de Introdução à Redes de Computadores
#Feito pela dupla Matheus Homrich e Thiago Mello

import sys
from tkinter import Frame

# Stop-and-Wait ARQ
def saw(num_frames, lost_pkts):
    # Emissor envia 1 frame, receptor tenta receber, se não houver erros, receptor envia ack
    #se houver erros => Timeout e emissor tenta novamente
    frame = False
    c = 0
    if int(lost_pkts[0]) == 0:
        for i in range(1, num_frames+1):
            if frame:
                print("A ->> B : ("+str(i)+") Frame 1")
                print("B -->> A : Ack 0")
            else:
                print("A ->> B : ("+str(i)+") Frame 0")
                print("B -->> A : Ack 1")
            frame = not frame
    elif (len(lost_pkts)==1):
        i = 1
        while i <= num_frames:
            if frame:
                print("A ->> B : ("+str(i)+") Frame 1") # falta arrumar o print "A -x B" caso a transmissão tenha erro
                if(len(lost_pkts) > c):
                    if(i == int(lost_pkts[c])):
                        print("Note over A : TIMEOUT ("+str(i)+")")
                        i-=1
                        c+=1
                        frame = not frame
                    else:
                        print("B -->> A : Ack 0")
                else:
                    print("B -->> A : Ack 0")
            else:
                print("A ->> B : ("+str(i)+") Frame 0")
                if(len(lost_pkts) > c):
                    if(i == int(lost_pkts[c])):
                        print("Note over A : TIMEOUT ("+str(i)+")")
                        i=i-1
                        c+=1
                        frame = not frame
                    else:
                        print("B -->> A : Ack 1")
                else:
                    print("B -->> A : Ack 1")
            frame = not frame
            i+=1
    else:
        transmission = ["x"] * (((num_frames + len(lost_pkts)) * 2) + 1)
        x = 1
        errs = 1
        while x != len(transmission):
            if (x%2!=0): #A -->> B
                if str(errs) in lost_pkts:
                    transmission[x] = "error"
                else:
                    if(x != 0):
                        if transmission[x-1] == "timeout" or transmission[x-1] == "error":
                            transmission[x] = "retry"
                        else:
                            transmission[x] = "ok"
                    else:
                            transmission[x] = "ok"
                errs +=1
                    
            else: #B -->> A
                
                if str(errs) in lost_pkts:
                    transmission[x] = "error"
                    errs +=1
                elif transmission[x-1] == "error":
                    transmission[x] = "timeout"
                else:
                    transmission[x] = "ok"
                    errs +=1
            x+=1
        printAuxSaw(transmission)


def printAuxSaw(transmission):
    x = 1
    frame = False
    n = 1
    #print(transmission)
    while x != len(transmission):
        if(x%2!=0): #A -->> B
            #print(transmission[x])
            if transmission[x]=="ok": 
                if frame: print("A ->> B : ("+str(n)+") Frame 1")
                else: print("A ->> B : ("+str(n)+") Frame 0")
                #frame = not frame
            elif transmission[x] == "error":
                if frame: print("A -x B : ("+str(n)+") Frame 1")
                else: print("A -x B : ("+str(n)+") Frame 0")
            elif transmission[x] == "retry":
                if frame: print("A ->> B : ("+str(n)+") Frame 1 (RET)")
                else: print("A ->> B : ("+str(n)+") Frame 0 (RET)")
                #frame = not frame
                #n+=1

        else:   #B -->> A
            #print(transmission[x])
            if transmission[x]=="ok":
                if not frame:
                    print("B -->> A : Ack 1")
                else:
                    print("B -->> A : Ack 0")
                frame = not frame
                n+=1
            elif transmission[x]=="timeout":
                print("Note over A : TIMEOUT ("+str(n)+")")
            elif transmission[x]=="error":
                if not frame:
                    print("B --x A : Ack 1")
                    print("Note over A : TIMEOUT ("+str(n)+")")
                else:
                    print("B --x A : Ack 0")
                    print("Note over A : TIMEOUT ("+str(n)+")")
    
        x+=1

    

# Go-Back N
def gbn(seqbits, num_frames, lost_pkts):
    
    print()


# Selective Repeat ARQ
def sr(seqbits, num_frames, lost_pkts):
    ""
    print()


# Init
# Inicializado com os parâmetros algo, seqbits, num_frames, lost_pkts
# algo -> usa if para escolher qual dos 3 métodos usar
# seqbits -> calcula (2**seqbits)-1 para usar quando apropriado
# num_frames -> qtd de frames a transferir
# lost_pkts -> lista de frames perdidos, separados por vírgulas, 
#caso não tenha nenhum, usar valor 0

algo = sys.argv[1]
seqbits = int(sys.argv[2])
num_frames = int(sys.argv[3])
lost_pkts = sys.argv[4]

lost_pkts = lost_pkts.split(",")
if (algo == "saw"): saw(num_frames, lost_pkts)
elif (algo == "gbn"): gbn(seqbits, num_frames, lost_pkts)
elif (algo == "sr"): sr(seqbits, num_frames, lost_pkts)

# Saída deve ser no formato
# Envio do frame <N> com seq <seqno>: A ->> B : (<N>) Frame <seqno>
# Ack do frame <seqno>: B -->> A : Ack <seqno+1>
# Falha no envio do frame <N> com seq <seqno>: A -x B : (<N>) Frame <seqno>
# Falha no envio do ack para frame <seqno>: B --x A : Ack <seqno+1>
# Retransmissão do frame <N> com seq <seqno>: A ->> B : (<N>) Frame <seqno> (RET)
# Nak do frame <seqno>: B -->> A : (<N>) NAK <seqno>
# Timeout para receber ack do frame <N>: Note over A : TIMEOUT (<N>)