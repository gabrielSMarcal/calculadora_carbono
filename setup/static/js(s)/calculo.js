//Calculo do carro
function calcularCarro() {
    const tipoCarro = document.getElementById('tipo-carro').value;
    const kmPercorridos = document.getElementById('km-carro').value;
    let emissaoTotal, emissaoMensal, emissaoAnual;

    // Cálculo para álcool ou gasolina
    if (tipoCarro === "alcool") {
        emissaoTotal = kmPercorridos * 0.8; // Exemplo de cálculo para álcool
    } else {
        emissaoTotal = kmPercorridos * 2.3; // Exemplo de cálculo para gasolina
    }

    // Cálculo mensal e anual
    emissaoMensal = emissaoTotal / 12;
    emissaoAnual = emissaoTotal;

    // Exibir resultados
    document.getElementById('resultado-carro-mensal').textContent = `Emissão mensal: ${emissaoMensal.toFixed(2)} kg CO₂`;
    document.getElementById('resultado-carro-anual').textContent = `Emissão anual: ${emissaoAnual.toFixed(2)} kg CO₂`;
}

// Função para limpar os dados
function limparCarro() {
    document.getElementById('tipo-carro').value = "alcool"; // Volta para a opção padrão
    document.getElementById('km-carro').value = "";
    document.getElementById('resultado-carro-mensal').textContent = "";
    document.getElementById('resultado-carro-anual').textContent = "";
}

//Calculo do ônibus 
function calcularTransportePublico() {
  const kmPercorridos = document.getElementById('km-onibus').value;
  const fatorEmissaoOnibus = 0.1; // Exemplo: Ônibus emite 0.1 kg CO₂ por km
  let emissaoTotal, emissaoMensal, emissaoAnual;
  
  // Cálculo de emissão total para ônibus
  emissaoTotal = kmPercorridos * fatorEmissaoOnibus;
  
  // Cálculos mensais e anuais
  emissaoMensal = emissaoTotal * 20;  // Exemplo: considerando 20 dias de uso por mês
  emissaoAnual = emissaoMensal * 12;

  // Exibir resultados
  document.getElementById('resultado-onibus-mensal').textContent = `Emissão mensal: ${emissaoMensal.toFixed(2)} kg CO₂`;
  document.getElementById('resultado-onibus-anual').textContent = `Emissão anual: ${emissaoAnual.toFixed(2)} kg CO₂`;
}

// Função para limpar os dados
function limparTransporte() {
  document.getElementById('km-onibus').value = "";
  document.getElementById('resultado-onibus-mensal').textContent = "";
  document.getElementById('resultado-onibus-anual').textContent = "";
}

//mostrar dentro um texto de acordo com a opção escolhida
function exibirInputEnergia() {
  const tipoEnergia = document.getElementById('tipo-energia').value;
  const inputValorConta = document.getElementById('input-valor-conta');
  const inputKwh = document.getElementById('input-kwh');
  
  // Alterna entre os inputs com base na seleção
  if (tipoEnergia === "valor-conta") {
    inputValorConta.style.display = "block";
    inputKwh.style.display = "none";
  } else {
    inputValorConta.style.display = "none";
    inputKwh.style.display = "block";
  }
}

//Calculo de energia
function calcularEnergia() {
  const tipoEnergia = document.getElementById('tipo-energia').value;
  let emissaoTotal, emissaoMensal, emissaoAnual;
  
  // Cálculo baseado no valor da conta
  if (tipoEnergia === "valor-conta") {
    const valorConta = document.getElementById('valor-conta-input').value;
    emissaoTotal = valorConta * 0.075; // Exemplo de cálculo para valor da conta
  } else {
    // Cálculo baseado no consumo em kWh
    const kwhConsumidos = document.getElementById('kwh-consumidos-input').value;
    emissaoTotal = kwhConsumidos * 0.84; // Exemplo de cálculo para consumo em kWh
  }
  
  // Cálculos mensais e anuais
  emissaoMensal = emissaoTotal;
  emissaoAnual = emissaoTotal * 12;

  // Exibir resultados
  document.getElementById('resultado-energia-mensal').textContent = `Emissão mensal: ${emissaoMensal.toFixed(2)} kg CO₂`;
  document.getElementById('resultado-energia-anual').textContent = `Emissão anual: ${emissaoAnual.toFixed(2)} kg CO₂`;
}

// Função para limpar os dados
function limparEnergia() {
  document.getElementById('valor-conta-input').value = "";
  document.getElementById('kwh-consumidos-input').value = "";
  document.getElementById('resultado-energia-mensal').textContent = "";
  document.getElementById('resultado-energia-anual').textContent = "";
}

//Calculo de gás
function calcularGas() {
const tipoGas = document.getElementById("tipo-gas").value;
let emissaoMensal = 0;
let emissaoAnual = 0;

// escolha do tipo de gás
if (tipoGas === "botijao") {
  const qtdBotijao = parseFloat(document.getElementById("qtd-botijao").value);
  if (!isNaN(qtdBotijao)) {
    // Exemplo de cálculo de emissão para botijão de gás
    emissaoMensal = qtdBotijao * 2.98; // Aproximadamente 2.98 kg de CO2 por botijão de 13kg
  }
} else if (tipoGas === "encanado") {
  const qtdEncanado = parseFloat(document.getElementById("qtd-encanado").value);
  if (!isNaN(qtdEncanado)) {
    // Exemplo de cálculo de emissão para gás encanado
    emissaoMensal = qtdEncanado * 2.02; // Aproximadamente 2.02 kg de CO2 por m³ de gás natural
  }
}

// Calcula a emissão anual
emissaoAnual = emissaoMensal * 12;

// Exibe os resultados
document.getElementById("resultado-gas").textContent = `Emissão Mensal: ${emissaoMensal.toFixed(2)} kg CO₂`;
document.getElementById("resultado-gas-anual").textContent = `Emissão Anual: ${emissaoAnual.toFixed(2)} kg CO₂`;
}

function mostrarOpcaoGas() {
const tipoGas = document.getElementById("tipo-gas").value;

if (tipoGas === "botijao") {
  document.getElementById("input-botijao").style.display = "block";
  document.getElementById("input-encanado").style.display = "none";
} else if (tipoGas === "encanado") {
  document.getElementById("input-botijao").style.display = "none";
  document.getElementById("input-encanado").style.display = "block";
}
}

function limparGas() {
// Limpa os inputs e resultados
document.getElementById("qtd-botijao").value = '';
document.getElementById("qtd-encanado").value = '';
document.getElementById("resultado-gas").textContent = '';
document.getElementById("resultado-gas-mensal").textContent = '';
document.getElementById("resultado-gas-anual").textContent = '';
}



