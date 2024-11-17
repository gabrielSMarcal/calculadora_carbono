// Função para salvar os dados no localStorage
function salvarDados() {
  localStorage.setItem('tipo-carro', document.getElementById('tipo-carro').value);
  localStorage.setItem('km-carro', document.getElementById('km-carro').value);
  localStorage.setItem('km-onibus', document.getElementById('km-onibus').value);
  localStorage.setItem('tipo-gas', document.getElementById('tipo-gas').value);
  localStorage.setItem('qtd-botijao', document.getElementById('qtd-botijao').value);
  localStorage.setItem('qtd-encanado', document.getElementById('qtd-encanado').value);
  localStorage.setItem('tipo-energia', document.getElementById('tipo-energia').value);
  localStorage.setItem('kwh-consumidos-input', document.getElementById('kwh-consumidos-input').value);
  localStorage.setItem('valor-conta-input', document.getElementById('valor-conta-input').value);
};

// Função para restaurar os dados do localStorage
function restaurarDados() {
  document.getElementById('tipo-carro').value = localStorage.getItem('tipo-carro') || "";
  document.getElementById('km-carro').value = localStorage.getItem('km-carro') || "";
  document.getElementById('km-onibus').value = localStorage.getItem('km-onibus') || "";
  document.getElementById('tipo-gas').value = localStorage.getItem('tipo-gas') || "";
  document.getElementById('qtd-botijao').value = localStorage.getItem('qtd-botijao') || "";
  document.getElementById('qtd-encanado').value = localStorage.getItem('qtd-encanado') || "";
  document.getElementById('tipo-energia').value = localStorage.getItem('tipo-energia') || "";
  document.getElementById('kwh-consumidos-input').value = localStorage.getItem('kwh-consumidos-input') || "";
  document.getElementById('valor-conta-input').value = localStorage.getItem('valor-conta-input') || "";
};

// Chamar a função para restaurar os dados ao carregar a página
window.onload = function() {
  restaurarDados();
  mostrarOpcaoEnergia();
  mostrarOpcaoGas();
};

/* FUNÇÕES PARA VERIFICAR OS DADOS INSERIDOS PELO USUÁRIO */

// Função para verificar se os campos de Carro estão preenchidos
function verificarCarro() {
  const tipoCarro = document.getElementById('tipo-carro').value;
  const kmCarro = document.getElementById('km-carro').value;

  if (tipoCarro === "") {
    alert("Selecione um tipo de veículo 🚗");
    return false;
  }
  if (kmCarro === "") {
    alert("Insira a quilometragem percorrida 🚗");
    return false;
  }
  return true;
};

// Função para verificar se o campo de Ônibus está preenchido
function verificarOnibus() {
  const kmOnibus = document.getElementById('km-onibus').value;
  if (kmOnibus === "") {
    alert("Insira a quilometragem percorrida no ônibus 🚌");
    return false;
  }
  return true;
};

// Função para verificar se os campos de Gás estão preenchidos
function verificarGas() {
  const tipoGas = document.getElementById('tipo-gas').value;
  const qtdBotijao = document.getElementById('qtd-botijao').value;
  const qtdEncanado = document.getElementById('qtd-encanado').value;
  if (tipoGas === "") {
    alert("Selecione um modo de cálculo para gás 🏮");
    return false;
  }
  if (tipoGas === "Botijão (13kg)" && qtdBotijao === "") {
    alert("Insira a quantidade de botijões 🏮");
    return false;
  }
  if (tipoGas === "Gás Encanado (m³/mês)" && qtdEncanado === "") {
    alert("Insira o consumo de gás encanado 🏮");
    return false;
  }
  return true;
};

// Função para verificar se os campos de Energia estão preenchidos
function verificarEnergia() {
  const tipoEnergia = document.getElementById('tipo-energia').value;
  const kwhConsumidos = document.getElementById('kwh-consumidos-input').value;
  const valorConta = document.getElementById('valor-conta-input').value;
  if (tipoEnergia === "") {
    alert("Selecione um modo de cálculo para energia ⚡");
    return false;
  } if (tipoEnergia === "kWh" && kwhConsumidos === "") {
    alert("Insira o consumo em kWh ⚡");
    return false;
  } if (tipoEnergia === "Conta de Luz" && valorConta === "") {
    alert("Insira o valor da conta de luz ⚡");
    return false;
  }
  return true;
};

// Função para limpar os dados do localStorage e os inputs
function limparDados() {
  localStorage.clear();
  document.getElementById('tipo-carro').value = "";
  document.getElementById('km-carro').value = "";
  document.getElementById('km-onibus').value = "";
  document.getElementById('tipo-gas').value = "";
  document.getElementById('qtd-botijao').value = "";
  document.getElementById('qtd-encanado').value = "";
  document.getElementById('tipo-energia').value = "";
  document.getElementById('kwh-consumidos-input').value = "";
  document.getElementById('valor-conta-input').value = "";

  // Limpar resultados
  document.getElementById('resultado-carro-mensal').innerHTML = "";
  document.getElementById('resultado-carro-anual').innerHTML = "";
  document.getElementById('resultado-onibus-mensal').innerHTML = "";
  document.getElementById('resultado-onibus-anual').innerHTML = "";
  document.getElementById('resultado-gas-mensal').innerHTML = "";
  document.getElementById('resultado-gas-anual').innerHTML = "";
  document.getElementById('resultado-energia-mensal').innerHTML = "";
  document.getElementById('resultado-energia-anual').innerHTML = "";
};

// Função para limpar os dados de Carro
function limparCarro() {
  localStorage.removeItem('tipo-carro');
  localStorage.removeItem('km-carro');
  window.location.href = '/limpar_carro/';
};

// Função para limpar os dados de Ônibus
function limparOnibus() {
  localStorage.removeItem('km-onibus');
  window.location.href = '/limpar_onibus/';
};

// Função para limpar os dados de Energia
function limparEnergia() {
  localStorage.removeItem('tipo-energia');
  localStorage.removeItem('kwh-consumidos-input');
  localStorage.removeItem('valor-conta-input');
  window.location.href = '/limpar_energia/';
};

// Função para limpar os dados de Gás
function limparGas() {
  localStorage.removeItem('tipo-gas');
  localStorage.removeItem('qtd-botijao');
  localStorage.removeItem('qtd-encanado');
  window.location.href = '/limpar_gas/';
};

// Retorno do input de acordo com a opção selecionada
function mostrarOpcaoEnergia() {
  const tipoEnergia = document.getElementById('tipo-energia').value;
  const inputValorConta = document.getElementById('input-valor-conta');
  const inputKwh = document.getElementById('input-kwh');
  
  if (tipoEnergia === "kWh") {
    inputValorConta.style.display = "none";
    inputKwh.style.display = "block";

  } else {
    inputValorConta.style.display = "block";
    inputKwh.style.display = "none";
  }
};

function mostrarOpcaoGas() {
  const tipoGas = document.getElementById("tipo-gas").value;

  if (tipoGas === "Botijão (13kg)") {
    document.getElementById("input-botijao").style.display = "block";
    document.getElementById("input-encanado").style.display = "none";
  
  } else if (tipoGas === "Gás Encanado (m³/mês)") {
    document.getElementById("input-botijao").style.display = "none";
    document.getElementById("input-encanado").style.display = "block";
  }
};




