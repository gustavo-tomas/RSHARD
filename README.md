# RSHARD
RSA? Nunca nem vi. Aqui é RSHARD.

Trabalho 2 de Segurança Computacional - UnB - 2022/1.

Gustavo Tomás de Paula - 190014148

Mateus de Paula Rodrigues - 190015793


## Funcionamento
Para rodar o programa, execute:  
```
python3 src/main.py
```

A entrada é composta por qualquer quantidade de caracteres hexadecimais (0123456789abcdef):  
```
cafebabe
```

A saída mostra o processo de cifragem da mensagem usando AES, com codificação BASE64 (padrão MIME) e cifragem RSA do hash e da chave AES (a chave é codificada com OAEP). Veja o arquivo de [exemplo](/example.txt) para entender melhor.
```
MESSAGE ENCRYPTED WITH AES:
NTNiMDFkNDE4ZjJmMmY5ODk1ZTNkYzg0ZGU3ZGZjZjQ=
```
