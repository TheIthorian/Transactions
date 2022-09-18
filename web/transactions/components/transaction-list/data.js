import { API_URL, API_KEY } from 'config';
import { handleResponse } from 'util/rest';

export async function getAllTransactions({ account, dateFrom, dateTo, minValue, maxValue, tags }) {
    const response = await fetch(API_URL + '/getTransactions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Api-Key': API_KEY,
        },
        body: JSON.stringify({
            account,
            date_from: dateFrom,
            date_to: dateTo,
            min_value: minValue,
            max_vaule: maxValue,
        }),
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
