const editButtons = document.querySelectorAll('#edit');
const delButtons = document.querySelectorAll('#delete');

function handeDeleteClosure(url) {
    return async () => {
        await get(url);
        document.location.replace('/users/list');
    };
}

function toEditPage(url) {
  return () => document.location.replace(url);
}

editButtons.forEach((element, key, list) => {
    let url = '/users/edit/' + element.dataset.user_id;
    element.addEventListener('click', toEditPage(url));
});

delButtons.forEach((element, key, list) => {
    let url = '/users/delete/' + element.dataset.user_id;
    element.addEventListener('click', handeDeleteClosure(url))
})