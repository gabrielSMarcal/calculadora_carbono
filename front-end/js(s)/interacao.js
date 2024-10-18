// Função para adicionar a classe de visibilidade à animação
document.addEventListener("DOMContentLoaded", () => {
    const fadeIns = document.querySelectorAll('.fade-in');

    fadeIns.forEach((fadeIn) => {
        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        });

        observer.observe(fadeIn);
    });

    // Efeito de rolagem suave ao clicar nos links do navbar
    const links = document.querySelectorAll('.navbar ul li a');

    links.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            targetSection.scrollIntoView({ behavior: 'smooth' });
        });
    });
});

