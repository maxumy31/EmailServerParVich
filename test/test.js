const URL = "http://127.0.0.1:12345"


function processEchoRequest()
{
    //Эхо запрос
    const getArgs = $(".echo_message").val()
    
    if(getArgs === undefined || getArgs === "")
    {
        processGetRequest("/echo","GET",{})
    }
    else
    {
        processGetRequest("/echo","GET",{"echo" : getArgs})
    }
}

function processPostRequest(endpoint,requestMethod,postArgs)
{
    const finalEndpoint = URL + endpoint
    alert(requestMethod + " запрос на " + finalEndpoint)
    fetch(finalEndpoint,
        {
        method: requestMethod,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',  // Простые заголовки
        },
        body: postArgs,  // Отправляем данные в формате URL-кодирования
        })
        .then((response) => response.text())
        .then((data) => alert('Ответ от сервера: ' + data))
        .catch((error) => alert('Ошибка: '+ error));
}

function processGetRequest(endpoint,requestMethod,getArgs)
{
    const finalEndpoint = URL + endpoint + dictToGetRequest(getArgs)
    alert(requestMethod + " запрос на " + finalEndpoint)
    fetch(finalEndpoint,
        {
        method: requestMethod,
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
