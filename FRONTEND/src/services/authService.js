const API_URL = "http://localhost:5000";

export async function loginUser(credentials){
    const response = await fetch(
        `${API_URL}/login`,
        {
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify(credentials)
        }
    );
    const data = await response.json();
    if(!response.ok){
        throw new Error(data.error);
    }
    return data;
}


export async function registerUser(userData){
    const response = await fetch(
        `${API_URL}/api/auth/register`,
        {
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body: JSON.stringify({userData})
        }
    );

    const data = await response.json();
    if(!response.ok){
        throw new Error(data.error);
    }
    return data;
}

