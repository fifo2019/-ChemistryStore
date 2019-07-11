document.getElementById('product').addEventListener('click',(event)=>{
        if(event.target.tagName === 'BUTTON') {
            if(event.target.className === 'quantity-arrow-minus') {
                if(event.target.nextElementSibling.value != 0) event.target.nextElementSibling.value -=1;
            }
            if(event.target.className === 'quantity-arrow-plus') {
                event.target.previousElementSibling.value = +event.target.previousElementSibling.value+1;
            }
        }
    });