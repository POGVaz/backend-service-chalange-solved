# backend-service-chalange-solved
Solução para o desafio: https://github.com/getninjas/backend-service-challenge da GetNinjas.

# Ferramentas utilizadas
Django foi escolhido para tratar das requisições web devido à minha experiência com o framework e com Python.
Com isso, a escolha de usar Celery como worker para tarefas em segundo plano veio facilmente, já que é usado normalmente em conjunto com Django.
Da mesma forma, o broker default do Celery é o Rabbitmq e como nenhuma configuração adicional é necessária para usá-los juntos este também foi escolhido.
Postgres foi escolhido como banco de dados também por sua comodidade em configuração com Django.

# Estrutura
A solução apresentada se divide em 4 containers, criados pelo docker:

  -Web_server: Onde a aplicação em Django roda e recebe as requisições com as informações do pedido.
  
  -Broker: Onde o Rabbitmq recebe as tarefas em segundo plano e distribui para as filas do Celery.
  
  -Worker: Onde o Celery recebe as tarefas do Rabbitmq e executa a busca por latitude e longitude assincronamente em segundo plano.
  
  -Database: Onde o Postgres roda o banco de dados com as informações da aplicação.


# Testes e solução
Foram projetados dois testes que garantem a funcionalidade da aplicação:
Um para testar a recepção dos posts com os dados do pedido, que garante que os objetos sejam criados no banco de dados, e outro para testar a execução da tarefa em segundo plano, que garante o correto funcionamento doacesso à API do Google Maps.

# Conclusão
Finalmente, o projeto desenvolvido atende a todas as requisições apresentadas, apesar da funcionalidade limitada.

A maior dificuldade deste projeto foi trabalhar com Docker e aplicações rodando em diversos containers, já que é uma ferramente inédita para mim. Ocorre o mesmo com Celery: entender o funcionamento (chamadas e execuções) das tarefas em segundo plano se provou dificultoso.

Para o futuro, uma melhor escolha de usuários e senhas para os serviços utilizados (como o banco de dados) seria bem vinda, assim como o uso de uma chave própria para o acesso da API do Google Maps. Também seria mais interessante uma aplicação mais robusta, que aceite melhor outros dados enviados pelo pedido e trate dos erros envolvidos nos processos.
