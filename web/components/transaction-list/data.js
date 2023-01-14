import { API_URL, API_KEY } from 'config';
import { handleResponse } from 'util/rest';
import { makeStore } from 'util/store';

export async function getAllTransactions(filter) {
    const response = await fetch(API_URL + '/getTransactions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Api-Key': API_KEY,
            session_id: makeStore('user').get('session_id'),
        },
        body: JSON.stringify({ ...filter }),
    });

    const data = await handleResponse(response);
    return data.map(convertFromApi);
}

function convertFromApi(transaction) {
    return {
        ...transaction,
        description: transaction.original_description ?? transaction.current_description,
        amount: transaction.amount / 100,
        tags: [transaction.tag.l1, transaction.tag.l2, transaction.tag.l3],
        tagColor: transaction.tag.color,
        key: transaction.id,
    };
}
