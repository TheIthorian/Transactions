import { API_URL, API_KEY } from 'config';
import { handleResponse } from 'util/rest';
import { makeStore } from 'util/store';

export async function getBudgets() {
    const response = await fetch(API_URL + '/getBudgets', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Api-Key': API_KEY,
            session_id: makeStore('user').get('session_id'),
        },
    });

    const data = await handleResponse(response);
    return data.map(convertBudgetFromApi);
}

function convertBudgetFromApi(budget) {
    return {
        ...budget,
        totalLimit: budget.total_limit,
        key: budget.id,
    };
}
