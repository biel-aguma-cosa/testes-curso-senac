function open_tab(event,tab) {
    let i, tab_content, tab_buttons
    tab_content = document.getElementsByClassName('content');
    tab_buttons = document.getElementsByClassName('tab_b');
    let target = document.getElementById(tab);
    let button = event.currentTarget
    
    for (i=0; (i < tab_content.length) && (i < tab_content.length); i++) {
        tab_content[i].style.display = 'none';
        tab_buttons[i].className = tab_buttons[i].className.replace(' active','')
    };
    target.style.display = 'block'
    button.className += ' active'
}

function temperature(type,index) {
    const dummy = ['K','F','C']
    switch (index) {
        case 0:
            globalThis.temp_vals.C = Number(globalThis.targets[type].C.value)
            globalThis.temp_vals.K = globalThis.temp_vals.C + 273.15  
            globalThis.temp_vals.F = globalThis.temp_vals.C * 9/5 + 32
            break
        case 1:
            globalThis.temp_vals.K = Number(globalThis.targets[type].K.value)
            globalThis.temp_vals.C = globalThis.temp_vals.K - 273.15    
            globalThis.temp_vals.F = (globalThis.temp_vals.C * 1.8) + 32
            break
        case 2:
            globalThis.temp_vals.F = Number(globalThis.targets[type].F.value)
            globalThis.temp_vals.C = (globalThis.temp_vals.F - 32)*5/9
            globalThis.temp_vals.K = globalThis.temp_vals.C + 273.15  
            break
    }
    for (let i of dummy) {
        globalThis.targets.num[i].value    = parseFloat(globalThis.temp_vals[i]).toFixed(2)
        globalThis.targets.slider[i].value = parseFloat(globalThis.temp_vals[i]).toFixed(2)
    }
}
function message(data,type,sender) {
    let _div = document.createElement('div')
    let div = document.createElement('div')
    let text = document.createElement('p')
    let user = document.createElement('p')

    _div.style.backgroundColor = 'rgba(102, 127, 207, 0.48)'
    div.className = 'bubble'+type
    user.className = 'user'+type

    user.innerText = sender
    text.innerText = data

    div.appendChild(text)
    _div.appendChild(user)
    
    globalThis.sock.text_field.appendChild(_div)
    globalThis.sock.text_field.appendChild(div)
}
function speak() {
    let entry = globalThis.sock.entry_field.value

    if (
        globalThis.user.name &&
        globalThis.user.password &&
        globalThis.socket.readyState == WebSocket.OPEN
    ) {
        globalThis.socket.send(JSON.stringify(
            {
                'type' : 'message',
                'message' : entry,
                'user' : globalThis.user
            }
        ))
    }
    globalThis.sock.entry_field.value = ''
}

function message_handler(data) {
        switch (data.type) {
            case 'message':
                if (data.sender == globalThis.user.name) {
                    message(
                        data.message,
                        '',
                        data.sender
                    )
                }else{
                    message(
                        data.message,
                        ' server',
                        data.sender
                    )
                }
                break
            case 'login':
                globalThis.user.name     = data.user.name
                globalThis.user.password = data.user.password
                for (let msg of data.data) {
                    if (msg.sender == globalThis.user.name) {
                        message(
                            msg.message,
                            '',
                            msg.sender
                        )}else{
                        message(
                            msg.message,
                            ' server',
                            msg.sender
                        )}}
                break
            case 'error':
                message('ERRO!',' server','server')
                break
            case 'patient_show':
                patient_view(data.patient)
                break
            case 'patient_list':
                patient_list(data)
                break
            default:
                break
        }
}

function login() {
    globalThis.socket = new WebSocket("ws://10.144.36.88:52007")
    globalThis.socket.onopen = function () {
        globalThis.socket.send(JSON.stringify(
            {
                'type' : 'login',
                'user' : globalThis.user
            }
        ))
    }
    globalThis.socket.onmessage = function (event) {
        console.log('message received!')
        const reader = new FileReader()

        reader.onload = function () {
            message_handler(JSON.parse(reader.result))
        }
        reader.readAsText(event.data)
        
    }
}

function login_submission_handler(event) {
    event.preventDefault();
    const data = new FormData(event.target)
    globalThis.user = {
        'name' : data.get('username'),
        'password': data.get('password')
    }

    login()
}

function patient_view(patient) {
    const form = document.getElementById('medic_form')
    form.name.value      = patient.name
    form.birthdate.value = patient.birthdate
    form.sex.value       = patient.sex
    form.diagnosis.value = patient.diagnosis
    form.state.value     = patient.state
    form.treatment.value = patient.treatment
    form.release.value   = patient.release
}

function patient_click(event) {
    let i
    let selected_patient = event.currentTarget
    let patients = document.getElementsByClassName('patient')
    for (i=0; (i < patients.length); i++) {
        patients[i].className = patients[i].className.replace(' active','')
    }
    selected_patient.className += ' active'
    if (
        globalThis.user.name &&
        globalThis.user.password &&
        globalThis.socket.readyState == WebSocket.OPEN
    ) {
        globalThis.socket.send(JSON.stringify(
            {
                'type' : 'get_patient',
                'patient' : selected_patient.innerText,
                'user' : globalThis.user
            }
        ))
    }
}

function patient_save() {
    const form = document.getElementById('medic_form')
    const patient_data = {
        'name'     : form.name.value,
        'birthdate': form.birthdate.value,
        'sex'      : form.sex.value,
        'diagnosis': form.diagnosis.value,
        'state'    : form.state.value,
        'treatment': form.treatment.value,
        'release'  : form.release.value
    }
    if (
        globalThis.user.name &&
        globalThis.user.password &&
        globalThis.socket.readyState == WebSocket.OPEN
    ) {
        globalThis.socket.send(JSON.stringify(
            {
                'type' : 'save_patient',
                'patient' : form.name.value,
                'data' : patient_data,
                'user' : globalThis.user
            }
        ))
    }
}

function patient_list(data) {
    const patient_list = document.getElementById('patient_list')
    const patients = document.getElementsByClassName('patient')

    for (let patient of patients) {
        patient_list.removeChild(patient)
    }
    console.log(data)
    console.log(data.list)
    for (let patient of data.list) {
        let new_patient = document.createElement('h3')

        new_patient.className = 'patient'
        new_patient.onclick = patient_click
        new_patient.innerText = patient

        patient_list.appendChild(new_patient)
    }
}
function patient_new() {
    const form = document.getElementById('medic_form')
    form.name.value      = ""
    form.birthdate.value = ""
    form.sex.value       = ""
    form.diagnosis.value = ""
    form.state.value     = ""
    form.treatment.value = ""
    form.release.value   = ""
}

function main() {
    globalThis.reader = new FileReader()

    globalThis.targets = {
        "slider" : {
            "K" : document.getElementById('K_slider'),
            "F" : document.getElementById('F_slider'),
            "C" : document.getElementById('C_slider')},
        "num" : {
            'K': document.getElementById('K_num'),
            'F': document.getElementById('F_num'),
            'C': document.getElementById('C_num')},
        "index" : {
            'C': 0,
            'K': 1,
            'F': 2}}
    globalThis.sock = {'text_field' : document.getElementById('sock_field'),    'entry_field': document.getElementById('sock_text')}

    globalThis.temp_vals = {"K" : 0,        "F" : 0,        "C" : 0    }
    globalThis.dummy = ['C','K','F'];
    globalThis.user = {'name' : null,'password' : null}

    globalThis.socket_tab = document.getElementById('socket_tab')
    globalThis.forms = document.getElementsByClassName('login_form');

    document.getElementById('default').click()

    for (let form of globalThis.forms) {
        form.addEventListener('submit',login_submission_handler)
    }

    document.addEventListener('keydown', function (event) {
        if (event.key == 'Enter') {
            if (socket_tab.className.includes('active')) {speak()}
        }
    })
}