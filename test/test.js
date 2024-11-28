const URL = "http://127.0.0.1:12345"


function processEchoRequest()
{
    //Эхо запрос
    const endpoint = "/echo"
    const getArgs = $(".echo_message").val()
    
    if(getArgs === undefined || getArgs === "")
    {
        processGetRequest(endpoint,{})
    }
    else
    {
        processGetRequest(endpoint,{"echo" : getArgs})
    }
}

function processEmailRegistration()
{
    const endpoint = "/email"
    const getArgs = $(".register_email").val()

    if(getArgs === undefined || getArgs === "")
        {
            processGetRequest(endpoint,{})
        }
        else
        {
            processGetRequest(endpoint,{"email" : getArgs})
        }
}

function processMailSend()
{
    const endpoint = "/email_send"
    const author = $(".mail_author").val()
    const target = $(".mail_target").val()
    const content = $(".mail_content").val()
    const theme = $(".mail_theme").val()

    processGetRequest(endpoint,{"author" : author,"target":target,"content":content,"theme":theme})

}

function processMailRecieve()
{
    const endpoint = "/email_recieve"

    const reciever = $(".mail_reciever").val()

    processGetRequest(endpoint,{"reciever":reciever})
}

function processEmailExists()
{
    const endpoint = "/email_exists"
    const getArgs = $(".check_email_exists").val()

    if(getArgs === undefined || getArgs === "")
        {
            processGetRequest(endpoint,{})
        }
        else
        {
            processGetRequest(endpoint,{"email" : getArgs})
        }
}

function processPostRequest(endpoint,postArgs)
{
    const finalEndpoint = URL + endpoint
    alert("POST" + " запрос на " + finalEndpoint)
    fetch(finalEndpoint,
        {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',  // Простые заголовки
        },
        body: postArgs,  // Отправляем json
        })
        .then((response) => response.text())
        .then((data) => alert('Ответ от сервера: ' + data))
        .catch((error) => alert('Ошибка: '+ error));
}

function processGetRequest(endpoint,getArgs)
{
    const finalEndpoint = URL + endpoint + dictToGetRequest(getArgs)
    alert("GET" + " запрос на " + finalEndpoint)
    fetch(finalEndpoint,
        {
        method: "GET",
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',  
        }, 
        })
        .then((response) => response.text())
        .then((data) => alert('Ответ от сервера: ' + data))
        .catch((error) => alert('Ошибка: '+ error));
}

function dictToGetRequest(dict)
{
    if(Object.keys(dict).length === 0) {return ""}
    const test = Object.entries(dict).
    map(([k,v],i) =>
        k + "=" + v
    ).
    reduce((v1,v2) =>
        v1 + "&" + v2
    )
    return "?" + test
}
