# desafio-byebnk

# Base Permission
A permissão primária para todos os endpoint é que o usuário esteja autenticado no sistema.

## APIs Endpoints

| URI | Inputs | Outputs |
| --- | --- | --- |
| `GET api/carteira`| | Saldo e informações relevantes da carteira |
| `GET api/ativos` | | Todos os ativos do user |
| `POST api/ativos` | Nome, Modalidade | |
| `GET api/aplicacoes` | | Todas as aplicacoes do user |
| `POST api/aplicacoes` | Ativo, Quantidade, Preco Unitário | |
| `GET api/resgates` | | Todos os resgates do user |
| `POST api/resgates` | Ativo, Quantidade, Preco Unitário | |

## Como acessar a página de administração?
Para acessar a página de administração como superusuário, basta utilizar o username `root` e senha `root`.