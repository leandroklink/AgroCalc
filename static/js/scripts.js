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


//configuração de barra lateral para dispositivos móveis
const menuBtn = document.getElementById('menu-btn');
const sidebar = document.querySelector('.sidebar');

menuBtn.addEventListener('click', () => {
    sidebar.classList.toggle('ativo');
});

//script para grafico
const canvas = document.getElementById('graficoTalhoes');

if (canvas) {

    new Chart(canvas, {
        type: 'bar',
        data: {
            labels: nomes,
            datasets: [{
                label: 'Produção (sacas)',
                data: producoes
            }]
        },
        options: {
            responsive: true
        }
    });
}
