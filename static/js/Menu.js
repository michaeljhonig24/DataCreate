const selectbtns = document.querySelectorAll('.options .selectbtn')
    selectbtns.forEach(btn => {
        btn.addEventListener('mouseover', () => {
            btn.style.transform = 'scale(1.2)';
            btn.classList.add('blurborder')
        })
        btn.addEventListener('mouseout', () => {
            btn.style.transform = 'scale(1)';
            btn.classList.remove('blurborder');
        })
    });


document.addEventListener('DOMContentLoaded', () => {
  textanimation();
});

function textanimation(){
    const menutext = document.querySelectorAll('h2');
    menutext.forEach((menu) => {
        const text = menu.innerHTML.trim();
        const words = text.split(" ");
        menu.innerHTML = '';
        words.forEach((word, index) =>{
            const span = document.createElement('span');
            span.innerHTML = word + '&nbsp';
            span.classList.add('char')
            span.style.animationDelay = `${index * 0.15}s`;
            menu.appendChild(span);
        });
    });
    const menulist = document.querySelectorAll('li');
    menulist.forEach((menu, index) => {
        const text = menu.innerHTML.trim();
        const words = text.split(" ")
        menu.innerHTML = '';
        words.forEach((word, wordindex) => {
            const span = document.createElement('span');
            span.innerHTML = word + '&nbsp;';
            span.classList.add('char');
            span.style.animationDelay = `${(index * 1.2) + wordindex * 0.15}s`;
            menu.appendChild(span);
        })
    })
    }
