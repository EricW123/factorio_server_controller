function bindInputSubmit(input, submit) {
    input.onkeydown = (ev) => {
        if (ev.key === 'Enter') {
            submit.click(); // Trigger submit click on Enter
        } else if (ev.key === 'Escape') {
            input.blur(); // Remove focus from input to trigger blur event
        }
    };

    input.onblur = (ev) => {
        if (ev.relatedTarget && ev.relatedTarget === submit)
            submit.click(); // If focus moved to submit, trigger its click
        input.value = ''; // Clear input on blur
    };
}


function fetchPlayers() {
    fetch('/list-players')
        .then(res => res.text())
        .then(text => {
            document.getElementById('playerText').textContent = text;
        })
        .catch(console.error);
}

function startServer() {
    fetch('/start-server')
        .then(res => res.text())
        // .then(console.log)
        .catch(console.error);
}

function stopServer() {
    fetch('/stop-server')
        .then(res => res.text())
        // .then(console.log)
        .catch(console.error);
}

function updateServer() {
    fetch('/update-server')
        .then(res => res.text())
        // .then(console.log)
        .catch(console.error);
}

fetchPlayers();
setInterval(fetchPlayers, 5000);


function updateLogs() {
    fetch('/get-logs')
        .then(res => res.json())
        .then(lines => {
            let logBox = document.querySelector('#logBox');
            logBox.innerHTML = lines.map(
                line => `<div>${line}</div>`
            ).join('');
            logBox.scrollTop = logBox.scrollHeight;
        })
        .catch(console.error);
}

updateLogs();
setInterval(updateLogs, 1000);


// function listMod() {
//     fetch('/list-mods')
//         .then(res => res.json())
//         .then(mods => {
//             let modBox = document.querySelector('#modBox');
//             modBox.innerHTML = ''; // Clear existing mods
//             Object.entries(mods).forEach(([mod_id, mod_name]) => {
//                 let li = document.createElement('div');
//                 li.className = 'modLi';

//                 let txt = document.createElement('span');
//                 txt.textContent = `${mod_id.padStart(7)} (${mod_name})`;
//                 li.appendChild(txt);

//                 let removeButton = document.createElement('button');
//                 removeButton.className = 'removeButton';
//                 removeButton.textContent = '❌';
//                 removeButton.onclick = removeMod.bind(null, mod_id);
//                 li.appendChild(removeButton);

//                 modBox.appendChild(li);
//             });
//             let li = document.createElement('div');
//             li.id = 'addContainer';
//             li.className = 'modLi';
//             li.textContent = '+'
//             li.onclick = addMod;
//             modBox.appendChild(li);

//             modBox.scrollTop = modBox.scrollHeight;
//         })
//         .catch(console.error);
// }


// function addMod() {
//     let addCont = document.getElementById('addContainer');

//     function addModToList() {
//         let input = addCont.querySelector('input');
//         let modId = input.value.trim();
//         if (!modId) return listMod();

//         fetch(`/check-mod/${modId}`)
//             .then(res => res.json())
//             .then(data => {
//                 if (!data.valid) throw new Error('Invalid mod ID');
//                 return fetch('/add-mod', {
//                     method: 'POST',
//                     headers: { 'Content-Type': 'application/json' },
//                     body: JSON.stringify({ "mod_id": modId, "mod_name": data.mod_name })
//                 });
//             })
//             .then(res => res.text())
//             // .then(console.log)
//             .catch(console.error)
//             .finally(listMod);
//     }

//     let input = document.createElement('input');
//     input.type = 'text';
//     input.placeholder = 'Mod ID';

//     addCont.textContent = '';
//     addCont.onclick = undefined;
//     addCont.appendChild(input);
//     input.focus();

//     let confirmButton = document.createElement('button');
//     confirmButton.textContent = '✔';
//     confirmButton.onclick = () => {
//         addModToList();
//     };
//     addCont.appendChild(confirmButton);

//     bindInputSubmit(input, confirmButton);
// }


// function removeMod(modId) {
//     fetch('/remove-mod', {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ "mod_id": modId })
//     })
//         .then(res => res.text())
//         // .then(console.log)
//         .catch(console.error)
//         .finally(listMod);
// }


// listMod();


document.addEventListener('DOMContentLoaded', () => {
    let rconInput = document.getElementById('rconCommand');
    let rconSubmit = document.getElementById('submitRcon');
    bindInputSubmit(rconInput, rconSubmit);
});


function sendRconCommand() {
    let command = document.getElementById('rconCommand').value.trim();
    if (!command) return;

    fetch('/send-rcon-command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "command": command })
    })
        .then(res => res.json())
        .then(data => {
            document.getElementById('rconResponse').textContent = `rconResponse: ${data.response || 'No response'}`;
        })
        .catch(console.error);
    document.getElementById('rconCommand').blur(); // Remove focus from input to
}
