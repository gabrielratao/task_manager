//ARMEZAR AS FUNÇÃO DO FRONT

//acesso aos endpoints
function get_teste(){
    fetch('http://localhost:3000/teste')
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Erro:', error));
}


function get_tasks(){
    var tasks = []
    fetch('http://localhost:3000/tasks')
    .then(response => response.json())
    .then(task => {
        tasks.push(task)
        console.log(task)
        }
        )
    .catch(error => console.error('Erro:', error));
    console.log('tasks:', tasks)
    add_task(tasks)
}



//MANIPULAÇÃO ELEMENTOS HTML
var section_tasks = document.getElementById('read_tasks');

function add_task(tasks){
    var task_div = document.createElement('div')
    var tasks_div_str = ''
    tasks.forEach(function(task) {
        var task_str = task.join(', ')
        tasks_div_str += task_str + '<br>'
    })

    
    task_div.innerHTML = tasks_div_str
    section_tasks.appendChild(task_div)
}


