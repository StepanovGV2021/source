//План работы

/// Для выполнения задания будет использоваться российский аналог https://api.timepad.ru

//1. Первый запрос (готово)
//2. 'Authorization': 'Bearer получить и отправить в запросе (это было больно, но готово)
//3. Гет запрос по тестовым параметрам без формы (готово)
//4. Распарсить полученные данные (готово)
//5. Собрать нужные данные в отдельный массив (готово)
//6. Прикрутить первые формы с помощью bootstrap (готово)
//7. Начать писать клиент на VUE (готово)
//8. Прикрутить лоадер чтобы показывало загрузку при открытии сервера (готово)
//9. Оживить формы даты (готово)
//10. Отключать кнопку отправить если форма пустая (готово)
//11. Закодировать город, чтобы нормально собрать ссылку для запроса (готово)
//12. Прикрутить рабочую ссылку к карточке (готово)
//13. Разобраться почему карты не прогружались и склейвались (готово)
// P.S Некоторые карты без изображений, потому что API timepad не присылает их изображение с сервера
// P.S2 Повторяющиеся карточки получаются естественно от того что мероприятия проходят не один раз и в разное время.
const express = require('express')
const path = require('path')
const app = express()
const request = require('request')
var fs = require('fs')

const host = 'localhost'
const port = 3000

const DATES = [{}]
const CARDS = []

function genurl(city, date) { //готово
    //const true_url_example = 'https://api.timepad.ru/v1/events?limit=10&skip=0&cities=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0&fields=location&sort=+id&starts_at_min=10.04.2021&starts_at_max=10.04.2021'
    const protocol = 'https://'
    const host = 'api.timepad.ru'
    const path = '/v1/events'

    let start = date.date_input_start.toString().split('T')[0] //отрезаем секунды от времени
    let end = date.date_input_end.toString().split('T')[0]

    const param = {
        limit: 100,
        skip: 0,
        cities: encodeURI(city).toString(),
        fields: 'location',
        sort: '+id',
        starts_at_min: start, //отрежем часы время 2021-04-06T14:52,
        starts_at_max: end
    }
    return protocol + host + path + '?limit='+ param.limit+'&skip=' + param.skip + '&cities=' + param.cities + '&fields=' + param.fields + '&sort=' + param.sort + '&starts_at_min=' + param.starts_at_min + '&starts_at_max=' + param.starts_at_max
}
// Как же я запарился с засовыванием токена.

var temp = []
var timepadEvent = []

app.use(express.json())

//POST

app.post("/api/conect",  function(req, res) {

    console.log(req.body)

    let options = {
        'method': 'GET', // подымаем Гет запрос для получения данных
        'url':genurl(req.body.city,req.body),
        'headers': {
            'Authorization': 'Bearer cd5b2090b462c011b87c23a372670b262fe1478a'
        }
    }
    console.log(genurl(req.body.city,req.body),)
    request(options, function (error, response) // Делаем запрос к API timepad
    {
        if (error)
            return res.status(500).send({ message: error })
        else
        {
            //const jsonBody = JSON.parse(body)
            temp = JSON.parse(response.body)["values"]
            temp.forEach(function(event1, i, temp)
            {
                if (event1.poster_image)
                {
                    event1.name = event1.name.replace(/&/g,'')
                    event1.name = event1.name.replace(/quot;/g,'')
                    event1.name = event1.name.replace(/quot/g,'')
                    event1.name = event1.name.replace(/amp;/g,'')
                    event1.name = event1.name.replace(/amp/g,'')
                    timepadEvent[i] = {

                        'image_link': event1.poster_image.default_url,
                        'url': event1.url,
                        'name': event1.name

                    }
                }
                else
                {
                    //чистим заголовки
                    event1.name = event1.name.replace(/&/g,'')
                    event1.name = event1.name.replace(/quot;/g,'')
                    event1.name = event1.name.replace(/quot/g,'')
                    event1.name = event1.name.replace(/amp;/g,'')
                    event1.name = event1.name.replace(/amp/g,'')
                    timepadEvent[i] = {

                        'image_link': "",
                        'url': event1.url,
                        'name': event1.name
                    }

                }
            })
            console.log("Получили данные") //собррали
        }
    })
    return res.status(201).json(timepadEvent)

})

//GET

app.get('/api/conect', (req, res)=>{
    setTimeout(()=> {
        res.status(200).json(DATES)
    }, 1000)
})


app.use(express.static(path.resolve(__dirname, "client")))

app.get('/', (req, res) =>
{
    var options = {
        'method': 'GET', // Гет запрос к API timepad чтобы проверить что он доступен
        'url': "https://api.timepad.ru"
    }
    request(options,(err, response, body) =>
        {
            if (err)
                return res.status(500).send({ message: err })
            else
                return res.sendFile(path.resolve(__dirname, "client", 'index_p.html'))
        }
    )
})

app.listen(port, host, () =>
    console.log(`Сервер http://${host}:${port}`)
)