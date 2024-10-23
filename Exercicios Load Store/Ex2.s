# Implemente um programa em Assembly MIPS que seja equivalente ao seguinte código em C:
#
# for(i = 0; i < 10; i++) {
#             v[i] = v[i] + 15;
#             printf("Vetor [%d] = %d", i, v[i]);
# }
# O programa deve:
# Inicializar um vetor v de inteiros com 10 elementos.
# Iterar sobre o vetor utilizando um laço (for), somando 15 a cada elemento do vetor.
# Exibir, após cada iteração, o valor atualizado de cada elemento no formato:
# Vetor [índice] = valor.

.data
    v: .word 10 20 30 40 50 60 70 80 90 100         # cria um vetor
.text 
    main: 
        addi $s1, $s1, 0    # s1 = 0 / i=0
        addi $s2, $s2, 10   # i < 10
    

    for:
        
