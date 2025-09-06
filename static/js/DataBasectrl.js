const selectbtns = document.querySelectorAll('.options .selectbtn, .Choices button, .Welcome button, button')
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
    }

const welcomeclosebtn = document.querySelector('.Welcome button');
const welcomescrn = document.querySelector('.Welcome');
welcomeclosebtn.addEventListener('click', () => {
        welcomescrn.style.animation = 'fade 1s ease-out forwards';
        setTimeout(() => {
            welcomescrn.style.display = 'none';
        }, 1000);
})

const settingsbtn = document.querySelector('.Settings button');
const settingsscrn = document.querySelector('.Settings');
const customizescrn = document.querySelector('.customize');
const rulesscrn = document.querySelectorAll('.rules');
const Settingsbtnscrn = document.querySelectorAll('.SettingsBtn')
settingsbtn.addEventListener('click', () =>  {
    if (settingsbtn.innerHTML === '∧') {
        rulesscrn.forEach((rule) => {
            rule.style.animation = 'fade .2s linear forwards';
        });
        settingsbtn.style.animation = 'btnfadeout .2s linear forwards';
        setTimeout(() => {
            settingsscrn.style.animation = 'menuup .95s linear forwards';
            settingsbtn.style.animation = 'buttonshiftup 1s linear forwards'
        }, 200);
        setTimeout(() =>{
            customizescrn.style.animation ='fadein .2s linear forwards';
            settingsbtn.innerHTML = 'V';
            customizescrn.style.display = 'flex';
            settingsbtn.style.animation = 'fadein .2s linear forwards';
        }, 1200);
    }
    else {
        customizescrn.style.animation = 'fade .2s linear forwards';
        settingsbtn.style.animation = 'fade .2s linear forwards';
        setTimeout(() => {
            customizescrn.style.display = 'none';
            settingsscrn.style.animation = 'menudown .95s  linear forwards';
            settingsbtn.style.animation = 'buttonshiftdown 1s linear forwards';
        }, 200);
        setTimeout(() => {
            rulesscrn.forEach((rule, index) => {
                rule.style.animation ='fadein .2s linear forwards';
                rule.style.animationDelay = `${index * .15}s`
            })
            settingsbtn.innerHTML = '∧';
            settingsbtn.style.animation = 'btnfadein .2s linear forwards';
        }, 1200);
    }
})

function clearCustom(btn){
    customizescrn.style.animation = 'fade .2s linear forwards';
    settingsbtn.style.animation = 'fade .2s linear forwards';
    settingsscrn.style.animation = 'fade .2s linear forwards';
    setTimeout(() => {
        btn.style.display = 'flex';
        btn.style.alignItems = 'center';
        customizescrn.style.display = 'none';
        settingsbtn.style.display = 'none';
        btn.style.animation = 'fadein .2s ease-in forwards';
        }, 100);
}
const backbtn = document.querySelector('.back');
function backappear(){
    backbtn.style.display = 'block';
    backbtn.style.animation = 'fadein .2s ease-in forwards';
}
function customizeback(btn){
    btn.style.animation = 'fade .2s ease-out forwards';
    backbtn.style.animation = 'fade .2s ease-out forwards'
    setTimeout(() => {
        btn.style.display = 'none';
        settingsbtn.style.display = 'flex';
        customizescrn.style.display = 'flex';
        settingsbtn.style.translate = '90px 20px';
        settingsbtn.style.justifyContent = 'center'
        customizescrn.style.animation = 'fadein .2s linear forwards';
        settingsbtn.style.animation = 'fadein .2s linear forwards';
        settingsscrn.style.animation = 'fadein .2s linear forwards';
        backbtn.style.display = 'none';
    }, 200);
}

const alertscrn = document.querySelector('.alert');
const alerttext = document.querySelector('.alert h2');
const addButton = document.querySelector('.Add');
const addsettingsbtn = document.querySelector('.addsettings');
addButton.addEventListener('click', () =>{
    clearCustom(addsettingsbtn);
    backappear();
    backbtn.addEventListener('click', () => {
        customizeback(addsettingsbtn);
    })
    const namebox = document.querySelector('#name');
    namebox.value = '';
    setTimeout(()=> {
        namebox.focus();
    }, 300)
    
    const submitbtn = addsettingsbtn.querySelector('.submit');
    submitbtn.addEventListener('click', async (e) => {
    e.preventDefault();
        const name = namebox.value;
        const datatypebox = document.querySelector('.select');
        const datatype = datatypebox.value;
        if (!name || /\d/.test(name)){
            alertscrn.style.animation = 'fadein .2s linear forwards';
            alerttext.innerHTML = 'Please enter a name that is not blank or contains numbers';
            namebox.value = '';
            namebox.focus();
            setTimeout(() => {
            alertscrn.style.animation = 'fade .2s linear forwards';
            }, 1600);
            return;
        }
    try{
        const response = await fetch("/add_column", { 
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({column: name, type: datatype})
    })
    const data = await response.json();
    
     if (data.status === "success") {
    console.log('Column added successfully!');
    await dataload();
  } else {
    console.error("backend error:", data.message);
  }
  
    }
  catch (error) {
  console.error("Network error:", error);
    }
    
    addsettingsbtn.style.animation = 'fade .2s ease-out forwards';
    backbtn.style.animation = 'fade .2s ease-out forwards';
    setTimeout(() => {
        alerttext.innerHTML = `Column ${name} added to the database`;
        alertscrn.style.animation = 'fadein 1s linear forwards'
        addsettingsbtn.style.display = 'none';
        backbtn.style.display= 'none';
        settingsbtn.style.display = 'flex';
        customizescrn.style.display = 'flex';
        settingsbtn.style.translate = '90px 20px';
        settingsbtn.style.justifyContent = 'center'
        customizescrn.style.animation = 'fadein .2s linear forwards';
        settingsbtn.style.animation = 'fadein .2s linear forwards';
        settingsscrn.style.animation = 'fadein .2s linear forwards';
    }, 200);
    setTimeout(() => {
        alertscrn.style.animation = 'fade .2s linear forwards';
    }, 2000);
    }, {once: true});
  });

const insertButton = document.querySelector('.Insert');
const insertsettings = document.querySelector('.insertsettings');
const insertLabel = insertsettings.querySelector('label.insertbox');
const insertInput = insertsettings.querySelector('#insertbox');
const insertSubmit = insertsettings.querySelector('button.submit');

let columns = [];
let rowData = {};
let currentIndex = 0;

insertButton.addEventListener('click', async () => {
    const res = await fetch('/get_columns');
    columns = await res.json();
    rowData = {};
    currentIndex = 0;
    if(columns.length <= 1){
      alertscrn.style.animation = 'fadein .2s linear forwards';
        alerttext.innerHTML = 'Please add Columns to your database before Inserting values';
        setTimeout(() => {
            alertscrn.style.animation = 'fade .2s linear forwards';
        }, 1500); 
    }
    else{
      clearCustom(insertsettings);
     backappear();
     backbtn.addEventListener('click', () => {
     customizeback(insertsettings);
    });
    if (columns[currentIndex] === 'id'){
        currentIndex++;
    }
    insertLabel.textContent = `Enter value for ${columns[currentIndex]}`;
    setTimeout(() => {
    insertInput.value = '';
    insertInput.focus();
    insertsettings.style.display = 'flex';
    insertsettings.style.opacity = '1';
    }, 400);
   
    } 
    
});

insertSubmit.addEventListener('click', async(e) => {
    e.preventDefault();
    if (columns.length === 0) {
        return;
    }

    const val = insertInput.value.trim();
    if (val === '') {
        alert('Please enter a value');
        return;
    }

    const datatype = await fetch('/checktype', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({column: columns[currentIndex]})
    });
    const type = await datatype.json();

    if (((type === "INT" || type === 'INTEGER') && /^-?\d+$/.test(val)) ||
    (type === "FLOAT" && /^-?\d+(\.\d+)?$/.test(val)) ||
    (type.startsWith("VARCHAR") && isNaN(Number(val))) ||
    (type === "BOOLEAN" && /^(true|false|1|0)$/i.test(val))) {
         rowData[columns[currentIndex]] = val;
        currentIndex++;
        if (currentIndex < columns.length) {
        insertInput.value = '';
        insertLabel.textContent = `Enter value for ${columns[currentIndex]}`;
        insertInput.focus();
    } else {
        try{
            const response = await fetch('/insert_data', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(rowData)
      });
      const data = await response.json();
      if (data.status === 'success') {
        console.log('Row inserted successfully!');
        dataload();
        } else {
          console.error('Insert error:', data.message);
        }
        }
        catch (error) {
        console.error("Network error:", error);
     }
      insertsettings.style.display = 'none';
      insertsettings.style.opacity = '0';
      alerttext.innerHTML = 'Values Inserted into the database';
      alertscrn.style.animation ='fadein .4s linear forwards';
      rowData = {};
      currentIndex = 0;
      insertInput.value = '';
      insertsettings.style.animation = 'fade .2s ease-out forwards';
      backbtn.style.animation = 'fade .2s ease-out forwards';
    setTimeout(() => {
        insertsettings.style.display = 'none';
        backbtn.style.display = 'none';
        settingsbtn.style.display = 'flex';
        customizescrn.style.display = 'flex';
        settingsbtn.style.translate = '90px 20px';
        settingsbtn.style.justifyContent = 'center'
        customizescrn.style.animation = 'fadein .2s linear forwards';
        settingsbtn.style.animation = 'fadein .2s linear forwards';
        settingsscrn.style.animation = 'fadein .2s linear forwards';
    }, 200);
    setTimeout(() => {
        alertscrn.style.animation = 'fade .2s linear forwards';
        alerttable.innerHTML = '';
        alertlist.innerHTML = '';
    }, 2000)
    }
    } else {
        alertscrn.style.animation = 'fadein .2s linear forwards';
        alerttext.innerHTML = `Please insert a valid value type for ${columns[currentIndex]}`
        setTimeout(() => {
            alertscrn.style.animation = 'fade .2s linear forwards';
            alerttext.innerHTML = '';
        }, 1000);
    }
});

const updateButton = document.querySelector('.Update');
const updatelabel = document.querySelector('.updatebox');
const updateselect = document.querySelector('#updatebox');
const updatesettings = document.querySelector('.updatesettings');
const updatesubmitcol = updatesettings.querySelector('button.submit');
const updatevaluebox = document.querySelector('#updatevalue');
const updatevaluelabel = document.querySelector('.updatevalue');
let colval = null;
updateButton.addEventListener('click', async() => {
    const res = await fetch('/get_columns');
    const columns = await res.json();
    const colcheck = columns[0]
    const resrow = await fetch('/get_rows', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({column: colcheck})
            });
    const rowcheck = await resrow.json()
    if(columns.length !== 1 && rowcheck.length){
    clearCustom(updatesettings);
    updatevaluebox.value = ' ';
    backappear();
    backbtn.addEventListener('click', () => {
        customizeback(updatesettings);
        setTimeout(() => {
        updatelabel.textContent ='Select a Column';
        colval = null;
        updateselect.innerHTML = '';
        updatevaluebox.value = '';
        updatevaluelabel.style.display = 'none';
        updatevaluebox.style.display = 'none';
        }, 400);  
    }, {once: true});
    updateselect.innerHTML = '';
    columns.forEach(col => {
        if (col !== 'id'){
        const option = document.createElement('option');
        option.value = col;
        option.textContent = col;
        updateselect.appendChild(option);
        }
    });
    colval = null;
    } else{
        alertscrn.style.animation = 'fadein .2s linear forwards';
        alerttext.innerHTML = 'Please add Columns and data to your database before Updating values';
        setTimeout(() => {
            alertscrn.style.animation = 'fade .2s linear forwards';
        }, 1500);
    }
});
 updatesubmitcol.addEventListener('click', async(e) => {
    e.preventDefault();
         if (updatevaluebox.value !== '' && updatevaluebox.value !== null){
            if(!colval){
            updatevaluebox.value = '';
            colval = updateselect.value; 
            const res = await fetch('/get_rows', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({column: colval})
            });
            const rows = await res.json();
            updateselect.innerHTML = '';
            rows.forEach(row => {
                const option = document.createElement('option');
                if (row === null || row === undefined){
                    option.value = 'null'
                    option.textContent = 'null';
                }else{
                    option.value = row;
                    option.textContent = row;
                }
                updateselect.appendChild(option);    
                
            })
            updatelabel.textContent = `Select a Row in ${colval}`;
            updatevaluelabel.style.display = 'flex';
            updatevaluebox.style.display = 'flex';
            updatevaluebox.style.animation = 'fadein .2s ease-in forwards';
            updatevaluelabel.style.animation = 'fadein .2s ease-in forwards';
        } else {
            const datatype = await fetch('/checktype', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({column: colval})
            });
            const type = await datatype.json();
            const selectedRow = updateselect.value;
            const newvalue = updatevaluebox.value;
            if (((type === "INT" || type === 'INTEGER') && /^-?\d+$/.test(newvalue)) ||
            (type === "FLOAT" && /^-?\d+(\.\d+)?$/.test(newvalue)) ||
            (type.startsWith("VARCHAR") && isNaN(Number(newvalue))) ||
            (type === "BOOLEAN" && /^(true|false|1|0)$/i.test(newvalue))) {
                try {
                const response = await fetch('/update_row', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({column: colval, row: selectedRow, value: newvalue})
                })
            const data = response.json();
            if (data.status === "success") {
            console.log('Column Updated successfully!');
            } else {
            console.error("backend error:", data.message);
            }
            
            }
            catch (error) {
            console.error("Network error:", error);
            } 
            await dataload();
            alertscrn.style.animation = 'fadein 1s linear forwards';
            alerttext.innerHTML = `Column ${colval} Updated in the database`;
            colval = null;
            updatesettings.style.animation = 'fade .2s ease-out forwards';        
            backbtn.style.animation = 'fade .2s ease-out forwards';
            setTimeout(() => {
            updatesettings.style.display = 'none';
            alertscrn.style.animation = 'fadein 1s linear forwards';
            backbtn.style.display = 'none';
            settingsbtn.style.display = 'flex';
            customizescrn.style.display = 'flex';
            settingsbtn.style.translate = '90px 20px';
            settingsbtn.style.justifyContent = 'center'
            customizescrn.style.animation = 'fadein .2s linear forwards';
            settingsbtn.style.animation = 'fadein .2s linear forwards';
            settingsscrn.style.animation = 'fadein .2s linear forwards';
            updateselect.innerHTML = '';
            updatelabel.textContent = 'Select a Column';
            updatevaluebox.value = '';
            updatevaluelabel.style.display = 'none';
            updatevaluebox.style.display = 'none';
        }, 200);
            setTimeout(()=>{
                alertscrn.style.animation = 'fade .2s linear forwards';
            }, 2000);
            } else{
            alertscrn.style.animation = 'fadein .2s linear forwards';
            alerttext.innerHTML = `Please insert a valid value type for ${colval}`
            setTimeout(() => {
            alertscrn.style.animation = 'fade .2s linear forwards';
            alerttext.innerHTML = '';
        }, 1000);
            }
         }
        } else {
            alertscrn.style.animation = 'fadein .2s linear forwards';
            alerttext.innerHTML = 'Please assign the column an updated value';
             setTimeout(() => {
            alertscrn.style.animation = 'fade .2s linear forwards';
            }, 1500);
        }
    });

const removeButton = document.querySelector('.Remove');
const removelabel = document.querySelector('.removebox');
const removeselect = document.querySelector('#removebox');
const removesettings = document.querySelector('.removesettings');
const removesubmit = removesettings.querySelector('button.submit');
removeButton.addEventListener('click', async() => {
    const res = await fetch('/get_columns');
    const columns = await res.json();
    if (columns.length !== 1){
        columns.forEach(col => {
        if(col !== 'id'){
        const option = document.createElement('option');
        option.value = col;
        option.textContent = col;
        removeselect.appendChild(option);
        }
    });
    clearCustom(removesettings);
    backappear();
    backbtn.addEventListener('click', () => {
        customizeback(removesettings);
        removeselect.innerHTML ='';
    })
    removesubmit.addEventListener('click', async(e)=> {
        e.preventDefault();
        const columnName = removeselect.value;
        if (!columnName){
        return;
        } 
        try{
            const response = await fetch("/remove_column", { 
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({column: columnName})
        }); 
        const data = await response.json();
        if (data.status === "success") {
            console.log('Column removed successfully!');
            await dataload();
        } else {
            console.error("backend error:", data.message);
        }
        }
        catch (error){
            console.error("Network error:", error);
        }

    alertscrn.style.animation = 'fadein 1s ease-in forwards';
    alerttext.innerHTML = `Column ${columnName} Removed from the Database`;
    removesettings.style.animation = 'fade .2s ease-out forwards';
    backbtn.style.animation = 'fade .2s ease-out forwards';
    setTimeout(() => {
        removesettings.style.display = 'none';
        backbtn.style.display = 'none';
        settingsbtn.style.display = 'flex';
        customizescrn.style.display = 'flex';
        settingsbtn.style.translate = '90px 20px';
        settingsbtn.style.justifyContent = 'center'
        customizescrn.style.animation = 'fadein .2s linear forwards';
        settingsbtn.style.animation = 'fadein .2s linear forwards';
        settingsscrn.style.animation = 'fadein .2s linear forwards';
        removeselect.innerHTML ='';
    }, 200);
    setTimeout(() => {
        alertscrn.style.animation = 'fade .2s linear forwards';
    }, 1600);
    });    
    } else{
        alertscrn.style.animation = 'fadein .2s linear forwards';
        alerttext.innerHTML = 'Please add Columns to your database before Removing values';
        setTimeout(() => {
            alertscrn.style.animation = 'fade .2s linear forwards';
        }, 1500);
    }
});

const clearbtn = document.querySelector('.clear');
clearbtn.addEventListener('click', async(e)=>{
    e.preventDefault();
    try{
        const res = await fetch('/cleardb', {method: 'POST'})
        const data = await res.json();
        console.log(data);
        alertscrn.style.animation = 'fadein .4s linear forwards';
        alerttext.innerHTML = `Column data cleared from the database`;
        await dataload();
        setTimeout(() => {
            alertscrn.style.animation = 'fade .2s linear forwards';
            alerttext.innerHTML = '';
        }, 2000)
    
    }
    catch (err) {
        console.error('Failed to clear database', err);
    }
    });

async function dataload(){
    const tablehead = document.querySelector('.databasebox');
    tablehead.innerHTML = '';
    const trname = document.createElement('tr');
    const trhead = document.createElement('th');
    trhead.classList.add('Name')
    trhead.colSpan = 100;
    trhead.textContent = 'Table';
    trname.appendChild(trhead);
    tablehead.appendChild(trname);

    const res = await fetch('/get_columns');
    const columns = (await res.json()).slice(0, 5);

    const trcol = document.createElement('tr');
    trcol.classList.add('ColumnNames');
    tablehead.appendChild(trcol);
    const columnNames = document.querySelector('.ColumnNames');
    columnNames.innerHTML = '';
    columns.forEach(col => {
            const newhead = document.createElement('th');
            newhead.textContent = col;
            columnNames.appendChild(newhead)
    });
    const resrow = await fetch('/get_row');
    const rows = (await resrow.json()).slice(0, 9);

    
    rows.forEach(row => {
    const tr = document.createElement('tr');
    tr.classList.add('rowdata');

    row.slice(0, columns.length).forEach(val => {
        const td = document.createElement('td');
        td.textContent = val === null || val === undefined || val === '' ? 'null' : val;
        tr.appendChild(td);
    });

    tablehead.appendChild(tr);
});
}
document.addEventListener('DOMContentLoaded', () => {
  textanimation();
  dataload();
});
