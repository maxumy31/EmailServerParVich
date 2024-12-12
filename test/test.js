const URL = "http://127.0.0.1:12345"



function processEchoRequest()
{
    //Эхо запрос

    const IsMulti = $(".echo_multirequest_enabled").prop("checked");
    const MultiCount = Number($(".echo_multirequest_count").val());

    const requests_count = IsMulti ? MultiCount : 1

    const endpoint = "/echo"
    const getArgs = $(".echo_message").val()
    
    if(getArgs === undefined || getArgs === "")
    {
        processGetRequest(endpoint,{},requests_count)
    }
    else
    {
        processGetRequest(endpoint,{"echo" : getArgs},requests_count)
    }
}

function processEmailRegistration()
{
    const endpoint = "/email"
    const email = $(".register_email_login").val()
    const pass = $(".register_email_password").val()

    {
        processPostRequest(endpoint,JSON.stringify({"email" : email,"password":pass}))
    }
}

function processMailSend()
{
    const endpoint = "/email_send"
    const author = $(".mail_author").val()
    const password = $(".mail_author_password").val()
    const target = $(".mail_target").val()
    const content = $(".mail_content").val()
    const theme = $(".mail_theme").val()

    processPostRequest(endpoint,JSON.stringify({"author" : author,"target":target,"content":content,"theme":theme,"password":password}))

}

function processMailRecieve()
{
    const endpoint = "/email_recieve"

    const reciever = $(".mail_reciever").val()
    const password = $(".mail_reciever_password").val()


    processPostRequest(endpoint,JSON.stringify({"reciever":reciever,"password":password}))
}

function processEmailExists()
{
    const endpoint = "/email_exists"
    const getArgs = $(".check_email_exists").val()

    
    //if(getArgs === undefined || getArgs === "")

    processGetRequest(endpoint,{"email" : getArgs})
}

function processPostRequest(endpoint,postArgs)
{
    const finalEndpoint = URL + endpoint
    alert("POST" + " запрос на " + finalEndpoint)
    fetch(finalEndpoint,
        {
        method: "POST",
        headers: {
            'Content-Type': 'application/json', 
        },
        body: postArgs,  
        })
        .then((response) => response.text())
        .then((data) => {alert('Ответ от сервера: ' + data); console.log(JSON.parse(data));return})
        .catch((error) => console.log('Ошибка: '+ error));
}

function processGetRequest(endpoint,getArgs,times = 1)
{
    const finalEndpoint = URL + endpoint + dictToGetRequest(getArgs);


    for(let i = 0; i < times;i++)
    {
        console.log("Request sent")
        fetch(finalEndpoint,
        {
        method: "GET",
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',  
        }, 
        })
        .then((response) => response.text())
        .then((data) =>{ console.log('Ответ от сервера: ' + data)
                console.log(JSON.parse(data))})
        .catch((error) => console.log('Ошибка: '+ error))
    };
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
    return "?" + test + `&cacheBuster=${Date.now()}_${Math.random()}`
}
