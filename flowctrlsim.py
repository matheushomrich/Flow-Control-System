#T1 da disciplina de Introdução à Redes de Computadores
#Feito pela dupla Matheus Homrich e Thiago Mello

import sys

# Stop-and-Wait ARQ
def saw():

    print()


# Go-Back N
def gbn(seqbits):
    
    print()


# Selective Repeat ARQ
def sr(seqbits):
    
    print()


# Init
# Inicializado com os parâmetros algo, seqbits, num_frames, lost_pkts
# algo -> usa if para escolher qual dos 3 métodos usar
# seqbits -> calcula (2**seqbits)-1 para usar quando apropriado
# num_frames -> qtd de frames a transferir
# lost_pkts -> lista de frames perdidos, separados por vírgulas, 
#caso não tenha nenhum, usar valor 0

algo = sys.argv[1]
seqbits = sys.argv[2]
num_frames = sys.argv[3]
lost_pkts = sys.argv[4]

if (algo == "saw"): saw()
elif (algo == "gbn"): gbn(seqbits)
elif (algo == "sr"): sr(seqbits)

# Saída deve ser no formato
# Envio do frame <N> com seq <seqno>: A ->> B : (<N>) Frame <seqno>
# Ack do frame <seqno>: B -->> A : Ack <seqno+1>
# Falha no envio do frame <N> com seq <seqno>: A -x B : (<N>) Frame <seqno>
# Falha no envio do ack para frame <seqno>: B --x A : Ack <seqno+1>
# Retransmissão do frame <N> com seq <seqno>: A ->> B : (<N>) Frame <seqno> (RET)
# Nak do frame <seqno>: B -->> A : (<N>) NAK <seqno>
# Timeout para receber ack do frame <N>: Note over A : TIMEOUT (<N>)
