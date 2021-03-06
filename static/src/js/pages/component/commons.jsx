
export function getUserId(){
    /* this will return a user key or redirect to `/` 
    if the key is found to invalid the the key should be removed and the user redirected to `/`
    */ 

    const key = 'usr_token';

    var usr_token = localStorage.getItem(key)
    if(usr_token == null){
        window.location.href = '/';
        return;
   }

   if(usr_token.length != 128){
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

     if(k.toString().length === 128){
          return true;
     }

     return false;

}

export function getMapHexFromURL(){
     var l = window.location.href;
     l = l.split('/');
     return l[l.length - 1]
}