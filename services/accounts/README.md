# services/accounts

Serviço principal responsável pelas movimentações realizadas nas contas.

## Endpoints

| Method | Path                                                 | Description                             |
| ------ | ---------------------------------------------------- | --------------------------------------- |
| POST   | /deposito/:account/:amount                           | Aumenta o saldo da conta e retorna nada |
| POST   | /saque/:account/:amount                              | Diminui o saldo da conta e retorna nada |
| POST   | /saldo/:account                                      | Retorna o saldo da conta                |
| POST   | /transferencia/:account-origin/:account-dest/:amount | Transferência de uma conta para a conta |
