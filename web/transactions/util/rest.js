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

function convertFromApi(transaction) {
    return {
        ...transaction,
        description: transaction.original_description ?? transaction.current_description,
        amount: transaction.amount / 100,
        tags: [transaction.tag.l1, transaction.tag.l2, transaction.tag.l3],
    };
}

export { handleHTTPError, handleResponse, convertFromApi };
