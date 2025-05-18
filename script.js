let tarefas = JSON.parse(localStorage.getItem("tarefas")) || [];
let editandoId = null;

function salvarNoStorage() {
  localStorage.setItem("tarefas", JSON.stringify(tarefas));
}

function renderizarTarefas() {
  const lista = $("#listaTarefas");
  lista.empty();

  tarefas.forEach((tarefa, index) => {
    const concluidaClass = tarefa.concluida ? 'concluida' : '';
    const item = $(`
      <li class="list-group-item ${concluidaClass}">
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <input type="checkbox" class="form-check-input me-2 check-concluir" data-id="${index}" ${tarefa.concluida ? 'checked' : ''}>
            <a href="detalhes.html?id=${index}" class="text-decoration-none fw-bold">${tarefa.titulo}</a><br>
            <small>${tarefa.descricao}</small><br>
            <small>Entrega: ${tarefa.dataEntrega}</small>
          </div>
          <div>
            <button class="btn btn-editar btn-sm btn-warning" data-id="${index}">Editar</button>
            <button class="btn btn-excluir btn-sm btn-danger" data-id="${index}">Excluir</button>
          </div>
        </div>
      </li>
    `);
    lista.append(item);
  });
}

function limparFormulario() {
  $("#titulo").val("");
  $("#descricao").val("");
  $("#dataEntrega").val("");
  editandoId = null;
}

$("#formTarefa").on("submit", function (e) {
  e.preventDefault();
  const novaTarefa = {
    titulo: $("#titulo").val(),
    descricao: $("#descricao").val(),
    dataEntrega: $("#dataEntrega").val(),
    concluida: false,
    comentarios: []
  };

  if (editandoId === null) {
    tarefas.push(novaTarefa);
  } else {
    tarefas[editandoId] = { ...novaTarefa, comentarios: tarefas[editandoId].comentarios };
  }

  salvarNoStorage();
  renderizarTarefas();
  limparFormulario();
});

$("#formTarefa").on("reset", limparFormulario);

$("#listaTarefas").on("click", ".btn-editar", function () {
  const id = $(this).data("id");
  const tarefa = tarefas[id];
  $("#titulo").val(tarefa.titulo);
  $("#descricao").val(tarefa.descricao);
  $("#dataEntrega").val(tarefa.dataEntrega);
  editandoId = id;
});

$("#listaTarefas").on("click", ".btn-excluir", function () {
  const id = $(this).data("id");
  if (confirm("Deseja excluir esta tarefa?")) {
    tarefas.splice(id, 1);
    salvarNoStorage();
    renderizarTarefas();
  }
});

$("#listaTarefas").on("change", ".check-concluir", function () {
  const id = $(this).data("id");
  tarefas[id].concluida = this.checked;
  salvarNoStorage();
  renderizarTarefas();
});

renderizarTarefas();
