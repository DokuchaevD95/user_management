const logoutBtn = document.querySelector('#logout')
logoutBtn.addEventListener('click', logout)


async function post(url, data) {
    let response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    if (response.status >= 200 && response.status < 400) {
        return response
    }

    alert(await response.text());
    throw new Error('Fetch err');
}


async function get(url) {
    let response = await fetch(url);

    if (response.status >= 200 && response.status < 400) {
        return response
    }

    alert(await response.text());
    throw new Error('Fetch err');
}


async function logout() {
    let response = await get('/logout');
    document.location.replace('/auth')
}