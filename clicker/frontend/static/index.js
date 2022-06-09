 function setColor(green, orange, element){
	let style=getComputedStyle(element);
	if (style.backgroundColor==green){
		element.style.backgroundColor=orange;
	}
	else if (style.backgroundColor==orange)
	{
		element.style.backgroundColor=green;
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
        weight.innerHTML=`${data.core.weight} кг`
        let green="rgb(0, 128, 0)"
        let orange="rgb(255, 140, 0)"
        let style=getComputedStyle(weight);
        console.log(data.core);
        if ((data.core.is_weight_prev_for_next_level && style.backgroundColor==green) || (!data.core.is_weight_prev_for_next_level && style.backgroundColor==orange))
        {
            setColor(green, orange, weight)
        }
    }).catch(error => console.log(error))
}
