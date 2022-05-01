#T1 da disciplina de Introdução à Redes de Computadores
#Feito pela dupla Matheus Homrich e Thiago Mello

from enum import Flag
import sys


# Stop-and-Wait ARQ
def saw(num_frames, lost_pkts):
    # Emissor envia 1 frame, receptor tenta receber, se não houver erros, receptor envia ack
    #se houver erros => Timeout e emissor tenta novamente

    # define a quantidade de mensagens que devem aparecer na tela
    # numero de frames + quantidade de erros * 2
    if lost_pkts[0] == "0":
       transmission = ["x"] * (((num_frames) * 2) + 1)
    else:
        transmission = ["x"] * (((num_frames + len(lost_pkts)) * 2) + 1)
    x = 1
    errs = 1
    #percorre o array transmission e muda os valores de strings
    while x != len(transmission):
        #como x começa em 1, quando x for impar é transmissão de a para b
        if (x%2!=0): #A -->> B
            #se a posição atual estiver na lista de erros marca como "error"
            if str(errs) in lost_pkts:
                transmission[x] = "error"
            #senão verifica se a posição anterior é um timeout ou erro, para ser "retry"
            #caso não tenha problemas, marca como "ok"
            else:
                if(x != 0):
                    if transmission[x-1] == "timeout" or transmission[x-1] == "error":
                        transmission[x] = "retry"
                    else:
                        transmission[x] = "ok"
                else:
                        transmission[x] = "ok"
            errs +=1
        #com x par é mensagem de b para a   
        else: #B -->> A
            #se a posição atual estiver na lista de erros marca como "error"
            if str(errs) in lost_pkts:
                transmission[x] = "error"
                errs +=1
            #se a posição anterior for erro marca a atual com "timeout"
            elif transmission[x-1] == "error":
                transmission[x] = "timeout"
            #senão marca com "ok"
            else:
                transmission[x] = "ok"
                errs +=1
        x+=1
    #chama func auxiliar para imprimir mensagem na tela
    printAuxSaw(transmission)


def printAuxSaw(transmission):
    x = 1
    frame = False
    n = 1
    #percorre todo o array
    while x != len(transmission):
        if(x%2!=0): #A -->> B
            #mensagem caso "ok"
            if transmission[x]=="ok": 
                if frame: print("A ->> B : ("+str(n)+") Frame 1")
                else: print("A ->> B : ("+str(n)+") Frame 0")
            #mensagem caso "error"
            elif transmission[x] == "error":
                if frame: print("A -x B : ("+str(n)+") Frame 1")
                else: print("A -x B : ("+str(n)+") Frame 0")
            #mensagem caso "retry"
            elif transmission[x] == "retry":
                if frame: print("A ->> B : ("+str(n)+") Frame 1 (RET)")
                else: print("A ->> B : ("+str(n)+") Frame 0 (RET)")
                
        else:   #B -->> A
            #mensagem caso ok
            if transmission[x]=="ok":
                if not frame:
                    print("B -->> A : Ack 1")
                else:
                    print("B -->> A : Ack 0")
                frame = not frame
                n+=1
            #mensagem caso "timeout"
            elif transmission[x]=="timeout":
                print("Note over A : TIMEOUT ("+str(n)+")")
            #mensagem caso "error"
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
    window = (2 ** seqbits) - 1
    transmission = ["x"] * ((num_frames) * 3)
    #winPos = 0
    x = 1
    n = 1
    frame = 0
    ackN = 1
    errorFlag = False
    #errors = ["x"] * 
    if lost_pkts[0] == "0":
        while x < num_frames:
            winPos = 0
            while winPos < window:
                if n > num_frames:
                    window = winPos
                    break
                print("A ->> B : ("+str(n)+") Frame "+str(frame))
                winPos += 1
                x += 1
                n += 1
                frame += 1
                if frame > window: frame = 0
            winPos = 0
            while winPos < window:
                print("B -->> A : Ack "+str(ackN))
                winPos += 1
                #x += 1
                ackN += 1
                if ackN > window: ackN = 0


    else:
        count = 1
        windRecept = 0
        while x < num_frames:
            winPos = 0

            while winPos < window:
                if transmission[x] == "x":
                    if str(x) in lost_pkts:
                        transmission[x] = "error"
                        
                    else:
                        transmission[x] = "ok"
                        if windRecept == frame:
                            transmission[x+3] = "ack "+str(n)
                        winPos += 1
                        n += 1
                        frame += 1
                        if frame > window: frame = 0
                        if windRecept > window: windRecept = 0
                
                x += 1
    print(transmission)


            # winPos = 0

            # while winPos < window:
            #     if n > num_frames:
            #         window = winPos
            #         break
            #     if (str(count) in lost_pkts):
            #         print("A -x B : ("+str(n)+") Frame "+str(frame))
            #         #..................

            #         winPos += 1
            #         x += 1
            #         n += 1
            #         frame += 1
            #         if frame > window: frame = 0
            #     else:
            #         print("A ->> B : ("+str(n)+") Frame "+str(frame))
            #         winPos += 1
            #         x += 1
            #         n += 1
            #         frame += 1
            #         if frame > window: frame = 0
            #     count += 1
            # winPos = 0
            # while winPos < window:
            #     print("B -->> A : Ack "+str(ackN))
            #     winPos += 1
            #     #x += 1
            #     ackN += 1
            #     if ackN > window: ackN = 0
            #     count += 1




        
            




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