import { API_URL } from 'config';
import { handleResponse, convertFromApi } from 'util/rest';

export async function getAllTransactions({ account, dateFrom, dateTo, minValue, maxValue, tags }) {
    const response = await fetch(API_URL + '/getTransactions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
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
