# Usage

No momento, dentro do `main.py` temos duas arrays que devem ser preenchidas:

```python
API_KEYS = [] 
CHANNEL_IDS = []
```

Precisamos de uma lista de API Keys devido a cotas de requisições da API do Youtube, e a lista de IDs dos canais para puxar as métricas.

Após preencher essas arrays, basta rodar o comando: 

```bash
python main.py
```

# Estrutura do banco de dados

Pensei em estrutuar o banco usando o conceito de hot e cold data, onde os dados que são mais acessados ficam em uma tabela e os dados que são menos acessados ficam em outra tabela.

**Hot Data**: Os dados que seriam são mais acessados são os dados de métricas de vídeos e canais, então esses dados ficariam em uma tabela separada.

**Cold Data**: Os dados que são menos acessados são os dados de vídeos e canais, então esses dados ficariam em uma tabela separada.

Entao na tabela de vídeos e canais teriam apenas os dados que são menos acessados, e na tabela de métricas teriam os dados que são mais acessados. Isso facilitará a otimização de consultas e a escalabilidade do banco, pois quando essas tabelas hots crescerem muito, podemos separar elas em outra tabela e torna-las cold.

## Tables

### Table `channels` (Cold Data)

| Coluna | Tipo | Descrição |
| --- | --- | --- |
| `id` | `INTEGER (PK)` | index |
| `channelId` | `TEXT` | ID do canal |
| `channelName` | `TEXT` | Nome do canal |
| `channelLabel` | `TEXT` | Esquerda / Direita |
| `createdAt` | `DATE` | Data de criação |
| `updatedAt` | `DATE` | Data de atualização |

### Table `videos` (Cold Data)

| Coluna | Tipo | Descrição |
| --- | --- | --- |
| `id` | `INTEGER (PK)` | index |
| `videoId` | `TEXT` | ID do vídeo |
| `videoTitle` | `TEXT` | Título do vídeo |
| `publishedAt` | `DATE` | Data de publicação |
| `channelId` | `ID (FK)` | ID do canal |

### Table `videoMetrics` (Hot Data)

| Coluna | Tipo | Descrição |
| --- | --- | --- |
| `id` | `INTEGER (PK)` | index |
| `videoId` | `ID (FK)` | ID do vídeo |
| `channelId` | `ID (FK)` | ID do canal |
| `videoViews` | `INTEGER` | Número de visualizações |
| `videoLikes` | `INTEGER` | Número de likes |
| `videoComments` | `INTEGER` | Número de dislikes |
| `createdAt` | `DATE` | Data de criação |

### Table `channelMetrics` (Hot Data)

| Coluna | Tipo | Descrição |
| --- | --- | --- |
| `metricsId` | `INTEGER (PK)` | index |
| `channelId` | `ID (FK)` | ID do canal |
| `subscribers` | `INTEGER` | Número de inscritos |
| `views` | `INTEGER` | Número de visualizações |
| `comments` | `INTEGER` | Número de comentarios |
| `likes` | `INTEGER` | Número de likes |
| `metricsDate` | `DATE` | Data da métrica |