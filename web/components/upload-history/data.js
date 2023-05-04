import { API_URL } from 'config';
import { defaultRequest, handleResponse } from 'util/rest';

export async function getUploads() {
    const response = await fetch(API_URL + '/getUploads', defaultRequest({}));

    const data = await handleResponse(response);
    return data.map(item => ({ key: item.id, ...item }));
}
