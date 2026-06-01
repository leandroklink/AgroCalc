//capturando botao do html
const botaoTema = document.getElementById('tema-btn');


if (localStorage.getItem('tema') === 'escuro') {
    document.body.classList.add('dark-mode');

}
//adiconando evento para o clique do botao
botaoTema.addEventListener('click', () => {
    
    document.body.classList.toggle('dark-mode');
    //verificando if do botao para saber se o mesmo está ou não com modo escuro ativado
    if (document.body.classList.contains('dark-mode')) {
        //setando botao para o modo escuro 
        localStorage.setItem('tema', 'escuro');
        //alterando conteudo do botao para um sol
        botaoTema.textContent = "🌞"
    } else {
        //setando tema para claro
        localStorage.setItem('tema', 'claro');
        //alterando conteudo do botao para uma lua
        botaoTema.textContent = "🌙"
    }

});

