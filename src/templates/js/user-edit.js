const editBtn = document.querySelector('#edit');
editBtn.addEventListener('click', updateUser)

async function updateUser() {
    let idElement = document.querySelector('#id');
    let loginElement = document.querySelector('#login');
    let passwordElement = document.querySelector('#password');
    let lastNameElement = document.querySelector('#last_name');
    let firstNameElement = document.querySelector('#first_name');
    let isAdminElement = document.querySelector('#is_admin');

    await post('/users/edit/' + idElement.value, {
        id: idElement.value,
        login: loginElement.value,
        password: passwordElement.value,
        last_name: lastNameElement.value,
        first_name: firstNameElement.value,
        is_admin: isAdminElement.checked
    });

    document.location.replace('/users/list');
}