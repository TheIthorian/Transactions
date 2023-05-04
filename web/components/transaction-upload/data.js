import { API_URL } from 'config';
import { handleResponse, defaultRequest } from 'util/rest';

export async function addUpload(file) {
    const options = defaultRequest();
    options.headers['file'] = file;
    const response = await fetch(API_URL + '/addUpload', options);

    const data = await handleResponse(response);
    return {
        ...data,
        key: data.id,
    };
}
