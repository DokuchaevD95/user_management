signInBtn = document.querySelector('#sign-in');
signInBtn.addEventListener('click', checkAuth)


async function checkAuth() {
    let login = document.querySelector('#login');
    let password = document.querySelector('#password');

    if (!login.value || !password.value) {
        alert('Enter login and passwd');
    }

    let response = await post('/auth', {
        login: login.value,
        password: password.value
    });

    let userData = await response.json();
    let token = userData.token;
    console.log(userData);
    document.location.replace('/auth/ok?jwt=' + token)
}