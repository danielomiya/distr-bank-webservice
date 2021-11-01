# services/data

Serviço responsável pelo armazenamento dos dados de contas.

## Sistema de _lock_

> Deve ser implementado um modelo baseado no conceito de leitores e escritores, onde a exclusão mútua é imposta para o caso de escritores mas não para leitores

Considerando o trecho acima e as limitações do protocolo HTTP, o bloqueio de uma conta gera um _hash_, que deve ser passado de volta ao serviço no momento que for atualizá-la. Dessa forma, garantimos que apenas o cliente que fez o bloqueio irá realizar a atualização desse dado. Por fim, sabendo que um cliente pode sofrer de erros diversos e nunca desbloquear uma conta, também é possível 'forçar' um desbloqueio.

## Endpoints

| Method | Path                 | Description                       |
| ------ | -------------------- | --------------------------------- |
| GET    | /accounts/:id        | Busca informações da conta        |
| POST   | /accounts/:id        | Atualiza o saldo da conta         |
| POST   | /accounts/:id/lock   | Bloqueia a conta para atualização |
| POST   | /accounts/:id/unlock | Desbloqueia a conta               |

## Exemplos

### Buscando informações de uma conta

#### Request

    curl -X GET http://localhost:5000/accounts/1 -H 'Accept: application/json'

#### Response

    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 59
    Server: Werkzeug/2.0.2 Python/3.8.2
    Date: Sun, 17 Oct 2021 05:03:03 GMT

    {
      "balance": 1000.0,
      "id": 1,
      "is_locked": false
    }

### Bloqueando uma conta para atualização

#### Request

    curl -X POST http://localhost:5000/accounts/1/lock -H 'Accept: application/json'

#### Response

    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 87
    Server: Werkzeug/2.0.2 Python/3.8.2
    Date: Sun, 17 Oct 2021 05:06:40 GMT

    {
      "id": 1,
      "is_locked": true,
      "lock": "5e5a41fe-17bc-4c23-a253-0058f860af8a"
    }

### Atualizando dados de uma conta

#### Request

    curl -X PUT http://localhost:5000/accounts/1 -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"lock":"5e5a41fe-17bc-4c23-a253-0058f860af8a", "balance":41995.44}'

#### Response

    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 60
    Server: Werkzeug/2.0.2 Python/3.8.2
    Date: Sun, 17 Oct 2021 05:16:33 GMT

    {
      "balance": 41995.44,
      "id": 1,
      "is_locked": true
    }

### Desbloqueando uma conta

#### Request

    curl -X POST http://localhost:5000/accounts/1/unlock -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"lock":"cbc355ae-e62c-4875-bb43-fd06dfa5c244"}'

#### Response

    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 37
    Server: Werkzeug/2.0.2 Python/3.8.2
    Date: Sun, 17 Oct 2021 05:19:35 GMT

    {
      "id": 1,
      "is_locked": false
    }

### Forçando o desbloqueio uma conta

#### Request

    curl -X POST http://localhost:5000/accounts/1/unlock -H 'Accept: application/json' -H 'Content-Type: application/json' -d '{"force":true}'

#### Response

    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 37
    Server: Werkzeug/2.0.2 Python/3.8.2
    Date: Sun, 17 Oct 2021 05:20:17 GMT

    {
      "id": 1,
      "is_locked": false
    }
