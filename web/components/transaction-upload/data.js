import { API_URL, API_KEY } from 'config';
import { handleResponse } from 'util/rest';
import { makeStore } from 'util/store';

export async function addUpload(formData) {
    const response = await fetch(API_URL + '/addUpload', {
        method: 'POST',
        headers: {
            'Api-Key': API_KEY,
            session_id: makeStore('user').get('session_id'),
        },
        body: formData,
    });

    const data = await handleResponse(response);
    return data.map(upload => ({ key: upload.id, ...upload }));
}
