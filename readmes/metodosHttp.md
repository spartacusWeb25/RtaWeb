Métodos HTTP:


Para criação de um novo registro:
POST /api/tabelasalafami/


Todas as vezes que formos editar algum objeto de um form por completo devemos usar o método PUT.
PUT /api/tabelasalafami/

Todas as vezes que formos excluir algum objeto de um form por completo devemos usar o método DELETE.
DELETE /api/tabelasalafami/

todas as vezes que foremos editar parcialmente devemos usar o método PATCH.
PATCH /api/tabelasalafami/


a rede funciona com return e response.

o cliente faz a requisição e o servidor responde com a resposta.

sendo assim temos:
POST, PUT, DELETE, PATCH

então eu sendo o cliente faço o POST para criar um novo registro.
bato no post com um objeto json com os dados do registro.
then((response) => {
    // Tratar a resposta do servidor
    console.log(response);
    // Pode fazer algo com a resposta, como atualizar a página
});
