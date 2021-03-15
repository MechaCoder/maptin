
export function getUserId(){
    /* this will return a user key or redirect to `/` 
    if the key is found to invalid the the key should be removed and the user redirected to `/`
    */

    const key = 'usr_token';

     var usr_token = localStorage.getItem(key)
     if(usr_token == null){
        alert('the user key has not been found')
        window.location.href = '/';
        return;
     }

     if(usr_token.length != 256){
          console.log(usr_token.length);
          alert('the user key is not the correct length')
          window.localStorage.removeItem(key)
          window.location.href = '/';
          return;
     }

     return usr_token;
}

export function userIdExists(){
     const key = 'usr_token';
     var k = window.localStorage.getItem(key)
     if(k == null){
          return false;
     }

     if(k.toString().length === 256){
          return true;
     }

     return false;

}

export function getMapHexFromURL(){
     var l = window.location.href;
     l = l.split('/');
     return l[l.length - 1]
}

export function testPassword(password){
     var pass=  /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?!.*\s).{8,15}$/;
     if(password.match(pass)){
          return true
     }
     return false
}

export function validateEmail(email) {
     const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
     return re.test(String(email).toLowerCase());
 }
