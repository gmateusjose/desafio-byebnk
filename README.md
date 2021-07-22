# desafio-byebnk

# Base Permission
A permissão primária para todos os endpoint é que o usuário esteja autenticado no sistema.

## APIs Endpoints

| URI | Inputs | Outputs |
| --- | --- | --- |
| `GET api/ativos` | | Todos os ativos do user |
| `POST api/ativos` | Nome, Modalidade | |
| `GET api/operacoes` | | Todas as aplicacoes/resgates do user |
| `POST api/operacoes` | Ativo, Operação, Quantidade, Preco Unitário | |
| `GET api/carteira`| | Saldo e informações relevantes da carteira |

## Como acessar a página de administração?
Para acessar a página de administração como superusuário, basta utilizar o username `root` e senha `root`.