function getMain () {
    return fetch('response_1623132079225.json')
}

getMain().then(response => {
    return response.json();
})