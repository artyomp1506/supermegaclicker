 function setImage(image_number){
     let image = document.getElementById('main_cake');
	 image.src= `http://img.pspa.su/cake${image_number}.jpg`
 }
 function setColor(green, orange, element){
	let style=getComputedStyle(element);
	if (style.backgroundColor==green){
		element.style.backgroundColor=orange;
	}
	else if (style.backgroundColor==orange)
	{
		element.style.backgroundColor = green;
	}
}
function call_click() {
    fetch('/backend/call_click', {
        method: 'GET'
    }).then(response => {
        if (response.ok) {
            return response.json()
        }
        return Promise.reject(response)
    }).then(data => {
        let weight = document.getElementById('current_weight');
        weight.innerHTML = `${data.core.weight} кг`
		let level = document.getElementById('current_level');
        level.innerHTML = `${data.core.level}`
		let size = document.getElementById('current_size');
        size.innerHTML = `${data.core.current_size}`
        let green="rgb(0, 128, 0)"
        let orange="rgb(255, 140, 0)"
        let style=getComputedStyle(weight);
        console.log(data.core);
        if (data.core.is_levelup && data.core.level<=10)
        {
            setImage(data.core.image_number)
        }
        if ((data.core.is_weight_prev_for_next_level && style.backgroundColor==green) || (!data.core.is_weight_prev_for_next_level && style.backgroundColor==orange))
        {
            setColor(green, orange, weight)
        }
    }).catch(error => console.log(error))
}
/**
    Функция для получения кукесов.
    Она нужна для того, чтобы получить токен пользователя, который хранится в cookie.
    Токен пользователя, в свою очередь, нужен для того, чтобы система распознала, что запросы защищены.
    Без него POST и PUT запросы выполняться не будут, потому что так захотел Django.
*/
function getCookie(name) { 
    let cookieValue = null; 
    if (document.cookie && document.cookie !== '') { 
        const cookies = document.cookie.split(';'); 
        for (let i = 0; i < cookies.length; i++) { 
            const cookie = cookies[i].trim(); 
            if (cookie.substring(0, name.length + 1) === (name + '=')) { 
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1)); 
                break; 
            } 
        } 
    } 
    return cookieValue; 
}

/** Функция покупки буста */
function buy_boost(boost_id) { 
    const csrftoken = getCookie('csrftoken') // Забираем токен из кукесов

    fetch(`/backend/boost/${boost_id}/`, { 
        method: 'PUT', // Теперь метод POST, потому что мы изменяем данные в базе
        headers: { // Headers - мета-данные запроса
            "X-CSRFToken": csrftoken, // Токен для защиты от CSRF-атак, без него не будет работать
            'Content-Type': 'application/json' 
        }
    }).then(response => { 
        if (response.ok) return response.json() 
        else return Promise.reject(response) 
    }).then(response => {
        if (response.error) return
        const old_boost_stats = response.old_boost_stats
        const new_boost_stats = response.new_boost_stats
       
        const coinsElement = document.getElementById('coins')
        coinsElement.innerText = Number(coinsElement.innerText) - old_boost_stats.price
        const powerElement = document.getElementById('click_power')
        powerElement.innerText = Number(powerElement.innerText) + old_boost_stats.power

        update_boost(new_boost_stats) // Обновляем буст на фронтике
    }).catch(err => console.log(err)) 
}

/** Функция для обновления буста на фронтике */
function update_boost(boost) { 
    const boost_node = document.getElementById(`boost_${boost.id}`) 
    boost_node.querySelector('#boost_level').innerText = boost.level 
    boost_node.querySelector('#boost_power').innerText = boost.power 
    boost_node.querySelector('#boost_price').innerText = boost.price
}


