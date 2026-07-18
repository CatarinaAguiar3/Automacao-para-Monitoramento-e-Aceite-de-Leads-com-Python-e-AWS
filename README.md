# Automação para Monitoramento e Aceite de Leads com Python e AWS

<img src="Imagens\Banner - Automação Leads v2.0b.png">

# Resumo 
Em um sistema comercial, novos leads precisam ser aceitos em até 10 minutos pelo vendedor. Desenvolvi uma automação para monitorar a plataforma, assumir os leads automaticamente e notificar o vendedor por e-mail. O projeto é executado em nuvem, tem deploy automatizado e reduziu a perda de leads de 70% para 0%.
A solução foi construída com Python, Selenium, é executada continuamente em uma instância AWS EC2, com deploy automatizado via GitHub Actions e notificações por e-mail. Durante sua utilização, a perda de leads caiu de 70% para 0%.

# ⭐ Destaques do projeto
- É um projeto real que atualmente é utilizado pelo vendedor.
- Envio automático de notificações por e-mail após cada lead identificado e aceito.
- Deploy automatizado utilizando GitHub Actions.
- Execução contínua em uma instância AWS EC2 com Linux.

# Tecnologias Utilizadas
Python • Selenium • AWS EC2 • Linux • GitHub Actions • Git • SSH • SCP • Cron • SMTP • HTML • CSS • XPath • Variáveis de Ambiente • GitHub Secrets

# Problema de Negócio
**Este é um projeto real**, por questões de confidencialidade a empresa não será mencionada. O sistema da empresa permite que usuários interessados nos produtos se cadastrem para saber mais informações. Então, entre as 9h e 21h, os dados de contato são distribuídos pelo sistema entre os vendedores que só tem até 10 minutos para assumir o lead. Caso não o façam, o lead é encaminhado para outro vendedor.

De acordo com a empresa, esse tipo de leads é o que tem maior chance de conversão. E a remuneração dos vendedores desta empresa é 100 % comissionada, então captar este tipo de leads é uma grande vantagem.
Antes da automação, era necessário que um colaborador permanecesse atualizando manualmente a página durante 12 horas (9h – 21h). 
Esse processo apresentava diversos problemas:
- **Janela de tempo crítica:** cada lead possuía apenas 10 minutos para ser assumido. Caso o vendedor não identificasse a oportunidade a tempo, o contato era redistribuído.
- **Monitoramento contínuo:** a necessidade de acompanhar a plataforma por 12 horas diárias tornava o processo desgastante e pouco eficiente.
- **Perda de oportunidades:** pausas para outras atividades, atendimentos ou indisponibilidade momentânea poderiam resultar na perda de leads de alto potencial.
- **Baixa escalabilidade:** o processo dependia exclusivamente de acompanhamento humano, limitando a capacidade de resposta.


# Objetivo do Projeto
O objetivo do projeto foi eliminar o processo manual de aceite de leads desenvolvendo uma automação que monitorasse periodicamente a plataforma e realizasse automaticamente o aceite dos leads assim que fossem identificados.
Desafio
Embora o objetivo parecesse simples, a implementação apresentou alguns desafios. 

## Elementos Dinâmicos
O maior desafio técnico do projeto foi a natureza dinâmica do botão "Assumir" lead. Ele surgia na interface sem aviso prévio e desaparecia em até 10 minutos, o que dificultava a inspeção do elemento.

<img src="Imagens\Tela com e sem o botão Assumir.png">

Como solução, durante o desenvolvimento da automação, foi necessário desenvolver um mecanismo capaz de comparar a estrutura da página entre execuções para detectar alterações na interface.
Então, foi criado o arquivo complementar, detector_elementos.py. 
1.	**Mapeamento Inicial:** O script faz uma varredura na página e salva informações sobre os elementos encontrados no arquivo de histórico elementos_historico.txt.
2.	**Detecção de Alterações:** Nas próximas execuções, ele captura novamente todos os elementos e compara com o arquivo de histórico. Caso sejam detectadas diferenças em relação ao histórico, o script identifica os novos elementos e atualiza o arquivo de histórico.
3.	**Registro:** Os principais eventos da automação são registrados em logs (log.txt).

## Execução contínua 
A automação precisava funcionar 12 horas por dia sem depender do computador do desenvolvedor. Isso exigiu a utilização de infraestrutura em nuvem.

## Aviso via e-mail sobre o aceite do lead
Também era necessário informar para o vendedor o aceite do lead. Como o objetivo era apenas notificar o vendedor após o aceite do lead, optou-se pelo envio de e-mail por ser uma solução simples e de baixo custo operacional. Para isso, foi necessário configurar o SSMTP e instalar o pacote MailUtils na instância Linux para permitir o envio automático de e-mails.


# Arquitetura Geral
O código é desenvolvido localmente e após concluir uma alteração, é realizado um push para o repositório no GitHub. Como o projeto envolve dados sensíveis, como login e senha, foram utilizados arquivos .env e GitHub Secrets para armazenar credenciais de forma segura.

<img src="Imagens\Fluxograma - Arquitetura Geral v1b.png" width="40%">
<br>

Sempre que uma alteração é enviada ao repositório, um workflow do GitHub Actions é executado automaticamente, realizando o deploy da aplicação para a instância EC2.
A EC2 foi utilizada para permitir que a automação permanecesse em execução independentemente do computador da desenvolvedora.

O workflow cópia automaticamente a nova versão da aplicação para a instância Linux hospedada na AWS EC2 utilizando conexão SSH para transferir os arquivos e executar comandos remotamente.

Após o deploy, a própria infraestrutura da AWS fica responsável pela execução da automação. Um agendador (cron) inicia o script automaticamente às 9h e encerra a execução às 21h, garantindo que a automação permaneça ativa apenas durante o período em que novos leads podem ser recebidos.

Durante a execução, o arquivo principal script.py executa a automação feita em Python e Selenium. Entre suas responsabilidades estão: 
- iniciar o navegador; 
- realizar login; 
- atualizar a página; 
- clicar no botão "Assumir"; 
- fechar o modal de confirmação após assumir o lead; 
- repetir continuamente esse processo.
  
Ao encontrar e clicar no botão “Assumir”, o script utiliza o SSMTP e o pacote MailUtils para enviar automaticamente uma notificação por e-mail ao vendedor.

Assim, além de automatizar o aceite de novos leads essa solução também envia uma mensagem avisando o vendedor.

# Arquitetura do código principal
A automação inicia, acessa o sistema, realiza o login utilizando credenciais armazenadas nas variáveis de ambiente. Após o login, inicia-se um processo contínuo de monitoramento da página principal.

Os novos leads são adicionados dinamicamente à interface, sem recarregamento completo da página. Para verificar se há novos leads, a automação clica no botão `↻` (atualizar) que atualiza a tabela com os nomes dos leads.

Quando um novo lead é disponibilizado, o botão "Assumir" passa a estar disponível na interface. A automação identifica esse botão e realiza o clique automaticamente.

Após o aceite, um modal é exibido com as informações do cliente. O script fecha esse modal automaticamente para retomar o monitoramento. Em seguida, o processo continua até que outro lead surja na tela.

<img src="Imagens\Fluxograma - Arquitetura do código principal v1b.png" width="50%">

# Demonstração da Aplicação
Para preservar a confidencialidade da empresa, foi desenvolvida uma aplicação demonstrativa em Flask que reproduz o fluxo da plataforma utilizada no projeto, incluindo a tela de login, a página principal e o modal de aceite de leads. O vídeo a seguir apresenta o funcionamento da interface e a execução da automação nesse ambiente de demonstração.



https://github.com/user-attachments/assets/6698d5c5-6c06-42e5-8ea7-70ed4b3f0758



# Resultado
**Resultado obtido:** durante a utilização da automação, a perda de leads foi reduzida de **70% para 0%**, eliminando a necessidade de monitoramento manual da plataforma entre 9h e 21h.
