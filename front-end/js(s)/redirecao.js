document.querySelectorAll('.funcionam').forEach((botao) => {
  botao.addEventListener('click', () => {
    window.location.href = 'calculo_carbono.html'; // Redireciona para a página de cálculo
  });
});