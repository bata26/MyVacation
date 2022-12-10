export function getAuthorizationHeader(userID , role){
    return{
        "userID" : userID,
        "role" : role
    };
}