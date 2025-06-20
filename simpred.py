import sys
import math

#Calculo do indice de acesso no BPB
def extrair_indice_bpb(endereco, tamanho_bpb):
    bits_index = int(math.log2(tamanho_bpb))
    return (endereco >> 2) & (tamanho_bpb - 1)

#Automato de 4 estados: Para simular a segunda predicao a ser tomada
def preditor_2bits_estado_atual(estado, ocorreu):
    if ocorreu == 'T':
        return min(estado + 1, 3)
    else:
        return max(estado - 1, 0)

def preditor_2bits_predicao(estado):
    return 'T' if estado >= 2 else 'N'

def main():
    if len(sys.argv) != 3:
        print("Uso: python simpred.py <arquivoTrace> <nLinhasBPB>")
        sys.exit(1)

    nome_arquivo = sys.argv[1]
    n_linhas_bpb = int(sys.argv[2])

    # Buffers de predição
    bpb_1bit = ['N'] * n_linhas_bpb
    bpb_2bits = [0] * n_linhas_bpb  

    # Contadores
    total = 0
    acertos_nt = acertos_t = acertos_dir = acertos_1bit = acertos_2bits = 0

    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            total += 1
            endereco_str, alvo_str, ocorreu = linha.strip().split()
            endereco = int(endereco_str)
            alvo = int(alvo_str)

            # Predição Not-Taken
            if ocorreu == 'N':
                acertos_nt += 1

            # Predição Taken
            if ocorreu == 'T':
                acertos_t += 1

            # Predição Direção
            direcao = 'T' if alvo < endereco else 'N'
            if direcao == ocorreu:
                acertos_dir += 1

            # Predição 1-bit
            indice = extrair_indice_bpb(endereco, n_linhas_bpb)
            pred_1bit = bpb_1bit[indice]
            if pred_1bit == ocorreu:
                acertos_1bit += 1
            bpb_1bit[indice] = ocorreu  # atualiza predição

            # Predição 2-bits
            estado = bpb_2bits[indice]
            pred_2bit = preditor_2bits_predicao(estado)
            if pred_2bit == ocorreu:
                acertos_2bits += 1
            bpb_2bits[indice] = preditor_2bits_estado_atual(estado, ocorreu)

    def taxa(acertos):
        return round(acertos / total * 100, 2) #Arredondamento previsto no trabalho

    print(f"nBranchesExecutados = {total}")
    print(f"Taxa de acertos Not-Taken      = {taxa(acertos_nt)}%")
    print(f"Taxa de acertos Taken          = {taxa(acertos_t)}%")
    print(f"Taxa de acertos Direção        = {taxa(acertos_dir)}%")
    print(f"Taxa de acertos 1-bit dinâmica = {taxa(acertos_1bit)}%")
    print(f"Taxa de acertos 2-bits dinâm.  = {taxa(acertos_2bits)}%")


main() #Chamando main ao final
