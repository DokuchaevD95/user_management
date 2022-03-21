const signInBtn = document.querySelector('#sign-in');
signInBtn.addEventListener('click', checkAuth)


async function checkAuth() {
    let login = document.querySelector('#login');
    let password = document.querySelector('#password');

    let response = await post('/auth', {
        login: login.value,
        password: password.value
    });

    let userData = await response.json();
    document.location.replace('/auth/ok?jwt=' + userData.token)
}