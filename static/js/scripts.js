const botaoTema = document.getElementById('tema-btn');


if (localStorage.getItem('tema') === 'escuro') {
    document.body.classList.add('dark-mode');

}

botaoTema.addEventListener('click', () => {
    
    document.body.classList.toggle('dark-mode');

    if (document.body.classList.contains('dark-mode')) {
        localStorage.setItem('tema', 'escuro');
        botaoTema.textContent = "🌞"
    } else {
        localStorage.setItem('tema', 'claro');
        botaoTema.textContent = "🌙"
    }

});

