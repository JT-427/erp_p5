let modal = document.getElementById('modifyModal');
let modalBody = modal.querySelector('.modal-body');
// show create matarial buying record modal
let create_btn = document.getElementById('create_btn');
create_btn.addEventListener('click', () => {
    const modifyModal = new bootstrap.Modal('#modifyModal', {
        keyboard: false
    });

    modalBody.removeAttribute('sn');
    let inputs = modal.querySelectorAll('input');
    for(pos=0; pos<inputs.length; pos++){
        inputs[pos].value = '';
    };
    modal.querySelector('.modal-footer').querySelector('[name="delete"]').style.display = 'none';
    modifyModal.show(modal);
});


function matarial_variation_commit(url, msg){
    // commit
    let modifyButtons = document.getElementsByClassName('modifyButton');
    const matarial_id = document.getElementById('matarial').getAttribute('matarial_id');
    for(i=0; i<modifyButtons.length; i++){
        let btn = modifyButtons[i];
        btn.addEventListener('click', () => {
            let data = Object();
            if(btn.name === 'save'){
                const inputs_ = modalBody.querySelectorAll('input, select');
                for(j=0; j<inputs_.length; j++){
                    let input_item = inputs_[j];
                    data[`${input_item.id}`] = input_item.value
                };
                if(modalBody.getAttribute('sn')){
                    data['sn'] = modalBody.getAttribute('sn');
                }
                requset_and_toast_alert(url+matarial_id, 'put', data, '新增/修改');
            }else if(btn.name === 'delete'){
                if(modalBody.getAttribute('sn')){
                    data['sn'] = modalBody.getAttribute('sn');
                    requset_and_toast_alert(url+matarial_id, 'delete', data, '刪除');
                }
            }
        });
    };
}