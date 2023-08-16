# Um bot do discord para auxiliar classificação manual de dados para algoritmos de ML.

Primeiro, navegue até o diretório em que deseja baixar o repositório e insira o seguinte comando:

```
$ git clone https://github.com/kyujulian/LabelingBot
```

Em seguida, é recomendado criar um ambiente virtual e instalar as dependências usando a o seguinte recorte:
```
cd LabelingBot &&
python3 -m venv discord-bot 
```

Em linux:

```
source discord-bot/bin/activate &&
python3 -m pip install -r requirements.txt
```

# Configurando

Com as dependências instaladas,  resta configurar as interfaces com o Discord e Google Sheets.

## Google Sheets API

As instruções nativas podem ser encontradas em: https://developers.google.com/workspace/guides/configure-oauth-consent


## Passo 1

Com uma conta no Google, crie um projeto Google Cloud [neste link](https://developers.google.com/workspace/guides/create-project) .

## Passo 2

Com o projeto no google clouds criado, o próximo passo é configurar a autenticação (OAuth), que deve ser feito de acordo com estas [instruções](https://developers.google.com/workspace/guides/configure-oauth-consent?hl=pt-br).

Em seguida, crie as [credenciais do cliente ID do OAuth.](https://developers.google.com/workspace/guides/create-credentials?hl=pt-br)

Click em 'Fazer Download do json'


## Passo 3
![[https://github.com/kyujulian/LabelingBot/blob/master/readme/download_client.png]]

![[https://github.com/kyujulian/LabelingBot/blob/master/readme/rename.png]]

Agora, você deve renomear o arquivo para 'credentials.json' e movê-lo para o diretório principal em que você clonou o repositório. ( ...LabelingBot)


Com essa parte fora do caminho. Resta criar o bot no discord.

## Discord Bot


# Uso
_TODO_
 - ~Comando para escolher outra(s) planilha~
 - ~Timeout no comando de votar~
 - ~Abstrair dados para permitir "votação offline"~
 - ~Refinar a interface do bot~
 - Jogar tudo num container em Docker
