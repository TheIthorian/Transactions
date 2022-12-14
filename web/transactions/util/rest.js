import { makeCustomError } from './error';

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

export { handleHTTPError, handleResponse };
