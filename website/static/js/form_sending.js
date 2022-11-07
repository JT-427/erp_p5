function requset_and_toast_alert(url, method, form_data, message, reload=true){
  fetch(url, {
    method: method.toUpperCase(),
    body: JSON.stringify(form_data),
    headers: new Headers({
        'Content-Type': 'application/json'
    })
  }).then(function(response){
    return response.status;
  }).then(function(status){
    const result = status === 200 || status === 201 || status === 204 ? 'success':'fail';
    message += result === 'success' ? '成功':'失敗，請洽開發人員';
    toast_alert(result, message, reload);
  })
}

function toast_alert(result, message, reload=true){
  const toastLiveExample = document.getElementById('liveToast')
  if(result === 'success'){
    toastLiveExample.classList.add('bg-success');
  }else{
    toastLiveExample.classList.add('bg-danger');
  }
  toastLiveExample.getElementsByClassName('toast-body')[0].innerHTML = message;
  
  const toast = new bootstrap.Toast(toastLiveExample)
  toast.show();
  window.setTimeout(
    (() => reload?location.reload():toast.hide()), 1500
  );
};