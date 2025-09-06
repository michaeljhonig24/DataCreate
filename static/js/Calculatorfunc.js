const buttons = document.querySelectorAll('.btn');
const display = document.getElementById('numvalue');
const legaloperands = ['+',' -','x','/'];
const legalkeys = ['0','1','2','3','4','5','6','7','8','9','.','+','-','_','/','x','*','c','C','Backspace', 'Enter'];
let firstnum;
let secnum;
let operator;
const addbutton = document.querySelector('.addbtn');
const subbutton = document.querySelector('.subbtn');
const mulbutton = document.querySelector('.mulbtn');
const divbutton = document.querySelector('.divbtn');
const decbutton = document.querySelector('.decbtn');
const negbutton = document.querySelector('.negbtn');
const delbutton = document.querySelector('.delbtn');
const clrbutton = document.querySelector('.clrbtn');
const eqbutton = document.querySelector('.eqbtn');
const scrollBtn = document.querySelector('.slider');

addbutton.addEventListener('click', Add)
subbutton.addEventListener('click', Subtract);
mulbutton.addEventListener('click', Multiply);
divbutton.addEventListener('click', Divide);
decbutton.addEventListener('click', Decimal)
negbutton.addEventListener('click', Negative)
delbutton.addEventListener('click', Delete);
clrbutton.addEventListener('click', Clear)
eqbutton.addEventListener('click', calculatorResult)

const keyToButton = {
    '+': addbutton,
    '-': subbutton,
    '*': mulbutton,
    'x': mulbutton,
    '/': divbutton,
    'Enter': eqbutton,
    'Backspace': delbutton,
    'c': clrbutton,
    'C':clrbutton,
    '.': decbutton,
    '_': negbutton,
};



function handleInput(key){
    if(display.value === '0'){
        display.value = key;
    } else {
        display.value += key;
    }
}
buttons.forEach(button => {
    buttons.forEach(btn => {
    const label = btn.innerText;
    keyToButton[btn.innerText] = btn;
    });
    
    button.addEventListener('click', () => {
        const val = button.innerHTML;
        if (display.value === '0'){
            display.value = val;
        }
        else{ 
            display.value += val;
        }
    })
    button.addEventListener('mousedown', () => {
        ButtonAction(button);
    })
    button.addEventListener('mouseup', () => {
        ButtonReset(button);
    })
})


document.addEventListener('keydown', (event) => {
    let key = event.key;
    if (!legalkeys.includes(key)){
        return;
    }
    if (key === 'Enter'){
        event.preventDefault();
        calculatorResult();
    } else if(key === "Backspace"){
        Delete();
    } else if(key.toLowerCase() === 'c'){
       Clear();
    } else if(key === '+'){
        Add();
    } else if(key === '-'){
        Subtract();
    } else if(key === '_'){
        Negative();
    } else if(key === '*' || key === 'x'){
        Multiply();
    } else if(key === '/'){
        Divide();
    }
     else {
        handleInput(key);
    }
    const button = keyToButton[key];
    if (button){
        ButtonAction(button);
    }
    document.addEventListener('keyup', (event) => {
        const button = keyToButton[event.key];
        if (button){
            ButtonReset(button);
        }
    })
})



for (const btn of Object.values(keyToButton)) {
    if (btn) {
        btn.addEventListener('mousedown', () => ButtonAction(btn));
        btn.addEventListener('mouseup', () => ButtonReset(btn));
    }
}

function Add(){
    const val = addbutton.innerHTML;
    if (display.value.slice(-1) === '.'){
        display.value += '0';
    }
    if (!legaloperands.some(op => display.value.includes(op))){
        firstnum = Number(display.value);
        operator = val;
        display.value = 0
    }
}

function Subtract(){
    const val = subbutton.innerHTML;
    if (display.value.slice(-1) === '.'){
        display.value += '0';
    }
    if (!legaloperands.some(op => display.value.includes(op))){
        firstnum = Number(display.value);
        operator = val;
        display.value = 0
    }
}

function Multiply(){
    const val = mulbutton.innerHTML;
    if (display.value.slice(-1) === '.'){
        display.value += '0';
    }
    if (!legaloperands.some(op => display.value.includes(op))){
        firstnum = Number(display.value);
        operator = val;
        display.value = 0
    }
}

function Divide(){
    const val = divbutton.innerHTML;
    if (display.value.slice(-1) === '.'){
        display.value += '0';
    }
    if (!legaloperands.some(op => display.value.includes(op))){
        firstnum = Number(display.value);
        operator = val;
        display.value = 0
    }
}

function Decimal(){
    if (display.value === ''){
        display.value = 0;
    } 
    else if (display.value.includes('.')){
        display.value += '';
    }else {
        display.value += '.';
    }
}

function Negative(){
    let neg = '-' + display.value
    if (display.value.slice(-1) === '.'){
        display.value += '0';
    }
    if (display.value.includes('-') || display.value === '0'){
        display.value += '';
    } else{
        display.value = neg;
    }
}

function Delete(){
    display.value = display.value.slice(0, -1);
    if(display.value.slice(-1) === '' || display.value.slice(-1) === '-'){
        display.value = 0;
    }
}

function Clear(){
     display.value = 0;
}

function calculatorResult() {
    let result;
    secnum = Number(display.value);
    const expr = `${firstnum}${operator}${secnum}`;

    if (Number.isFinite(firstnum) && Number.isFinite(secnum) && !(firstnum === 0 && secnum === 0)) {
        switch (operator) {
            case '+':
                result = firstnum + secnum;
                break;
            case '-':
                result = firstnum - secnum;
                break;
            case 'x':
                result = firstnum * secnum;
                break;
            case '/':
                result = firstnum / secnum;
                break;
        }

        display.value = result;

        fetch('/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                expression: expr,
                result: result
            })
        })
        .then(res => res.json())
        .then(data => {
            console.log(data);
            loadHistory();
        })
        .catch(err => console.error(err));

        firstnum = 0;
        secnum = 0;
    }
}


function loadHistory() {
    fetch('/history')
    .then(res => res.json())
    .then(data => {
        const table = document.querySelector('.calcTable');
        while (table.rows.length > 1) {
            table.deleteRow(1);
        }
    

        data.slice(0, 7).forEach(entry => {
            const newRow = document.createElement('tr');

            const exprCell = document.createElement('td');
            exprCell.textContent = entry.expression;

            const resultCell = document.createElement('td');
            resultCell.textContent = entry.result;
            
            newRow.appendChild(exprCell);
            newRow.appendChild(resultCell);
            table.appendChild(newRow);
        });
        rowanimationin();
    })
    .catch(err => console.error('Failed to load history:', err));
}

function rowanimationin(){
    const rows = document.querySelectorAll('.calcTable td');
        rows.forEach((row, index) => {
            row.style.opacity = 0;
            row.style.animation = 'rowfadein 0.6s ease-in forwards';
            row.style.animationDelay = `${index * 0.1}s`
        })
}
function rowanimationout() {
  const rows = document.querySelectorAll('.calcTable td');
  for (let i = rows.length - 1; i >= 0; i--) {
    rows[i].style.animation = 'none';
    rows[i].offsetHeight; 
    rows[i].style.animation = 'rowfadeout 0.6s ease-out';
    rows[i].style.animationDelay = `${(rows.length - 1 - i) * 0.1}s`;
    rows[i].style.animationFillMode = 'backwards';

  }
   const totalTime = ((rows.length - 1) * 0.1 + 0.6) * 1000;
   return totalTime;
}

function sliderAction(btnval) {
    btnval.classList.add('blurborder')

}
function sliderReset(btnval) {
    btnval.classList.remove('blurborder')
}

function ButtonAction(btnval) {
    btnval.style.backgroundColor = "gray";
    btnval.style.transform = 'scale(0.85)';
    btnval.classList.add('blurborder')
}
function ButtonReset(btnval) {
    btnval.style.backgroundColor = "white";
    btnval.style.transform = 'scale(1)';
    btnval.classList.remove('blurborder')
}

const [title, list] = document.querySelectorAll('.info h2, .info ul');
const closebtn = document.querySelector('.info button');
closebtn.addEventListener('mouseover', () =>{
    closebtn.style.transform = 'scale(1.2)';
    closebtn.classList.add('blurborder');
});
closebtn.addEventListener('mouseout', () =>{
    closebtn.style.transform = 'scale(1)';
    closebtn.classList.remove('blurborder');
})
closebtn.addEventListener('click', () => {
    const infoscrn = document.querySelector('.info');
    infoscrn.style.animation = 'infoclose 1s ease-out forwards';
    setTimeout(() => {
        openbtn.style.display = 'block';
    }, 1000)
    title.style.opacity = '0';
    list.style.opacity = '0';
    closebtn.style.display = 'none';
})

const openbtn = document.querySelector('.info .open');
openbtn.addEventListener('mouseover', () =>{
    openbtn.style.transform = 'scale(1.1)';
    openbtn.classList.add('blurborder');
});
openbtn.addEventListener('mouseout', () =>{
    openbtn.style.transform = 'scale(1)';
    openbtn.classList.remove('blurborder');
})
openbtn.addEventListener('click', () => {
    const infoscrn = document.querySelector('.info');
    infoscrn.style.animation = 'infoopen 1s ease-in forwards';
    openbtn.style.display = 'none';
    setTimeout(() => {
    title.style.opacity = '1';
    list.style.opacity = '1';
    closebtn.style.display = 'block';
    }, 1000)
})

const slidebtn = document.querySelector('.slider');
slidebtn.addEventListener('mouseover', () => {
    sliderAction(slidebtn);
})

slidebtn.addEventListener('mouseout', () => {
     sliderReset(slidebtn);
})

const deldb = document.querySelector('.deldata');
deldb.addEventListener('mousedown', () =>  {
    ButtonAction(deldb);
})

deldb.addEventListener('mouseup', () => {
    ButtonReset(deldb);
})

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

function scrollToTop() {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
}
deldatabtn = document.querySelector('.deldata');

deldatabtn.addEventListener('mouseover', () => {
    deldatabtn.style.transform = 'scale(1.2)';
    deldatabtn.classList.add('blurborder');
})
deldatabtn.addEventListener('mouseout', () => {
    deldatabtn.style.transform = 'scale(1)';
    deldatabtn.classList.remove('blurborder');
})

deldatabtn.addEventListener('click', () => {
    const animationtime = rowanimationout();
    setTimeout(() =>{fetch('/clear', {method: 'POST'})
    .then(res => res.json())
    .then(data => {
        console.log(data);
        loadHistory()
    })
    .catch(err =>  console.error('Failed to clear historyL', err));
    }, animationtime)
})

function textanimation() {
  const container = document.querySelector('.info h2');
  const text = container.innerText.trim();
  const words = text.split(" ");
  container.innerHTML = '';
  const halfway = Math.floor(words.length / 2);
  words.forEach((word, index) => {
    const span = document.createElement('span');
    span.innerHTML = word + '&nbsp;';
    span.classList.add('char');
    span.style.animationDelay = `${index * 0.15}s`;
    container.appendChild(span);
    if (index === halfway) {
      container.appendChild(document.createElement('br'));
    }
  });

   const listItems = document.querySelectorAll('.info li');
   listItems.forEach((li, liIndex) => {
    const liText = li.innerText.trim();
    const liWords = liText.split(" ");
    li.innerHTML = '';

    liWords.forEach((word, wordIndex) => {
      const span = document.createElement('span');
      span.innerHTML = word + '&nbsp;';
      span.classList.add('char');
      span.style.animationDelay = `${(liIndex * 1.2) + wordIndex * 0.15}s`;
      li.appendChild(span);
      if ((wordIndex + 1) % 10 === 0) {
        li.appendChild(document.createElement('br'));
      }
    });
  });
}


document.addEventListener('DOMContentLoaded', () => {
  loadHistory();
  textanimation();
  if (scrollBtn) {
    scrollBtn.addEventListener('click', scrollToTop);
    window.addEventListener('scroll', () => {
      if (window.scrollY > 180) {
        scrollBtn.style.display = 'block';
      } else {
        scrollBtn.style.display = 'none';
      }
    });
  }
});