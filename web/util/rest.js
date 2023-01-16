import { makeCustomError } from './error';
import { makeStore } from 'util/store';
import { API_KEY } from 'config';

async function handleHTTPError(response) {
    const responseData = await response.json();
    let error;
    if (response.status === 400) {
        error = makeCustomError({
            title: 'Bad request',
            message: responseData._schema,
            detail: '',
        });
    } else if (response.status < 500) {
        error = makeCustomError({
            title: responseData.error?.name,
            message: responseData.error?.message,
            detail: responseData,
        });
    } else {
        error = makeCustomError({
            title: 'Error',
            message: 'Unknown server error',
            detail: responseData,
        });
    }

    console.log(error);
    return error;
}

async function handleResponse(response) {
    if (response.ok) {
        return await response.json();
    }
    throw await handleHTTPError(response);
}

function defaultRequest(body = null) {
    return {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Api-Key': API_KEY,
            session_id: makeStore('user').get('session_id'),
        },
        body: body && JSON.stringify(body),
    };
}

export { handleHTTPError, handleResponse, defaultRequest };
