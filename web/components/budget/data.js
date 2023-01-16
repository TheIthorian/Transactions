import { API_URL, API_KEY } from 'config';
import { handleResponse } from 'util/rest';
import { makeStore } from 'util/store';

export async function getBudget(budgetId) {
    const response = await fetch(API_URL + '/getBudget', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Api-Key': API_KEY,
            session_id: makeStore('user').get('session_id'),
        },
        body: JSON.stringify({ budget_id: budgetId }), // This fails when null. Check error handling in Response.py
    });

    console.log(response);

    const data = await handleResponse(response);
    return convertBudgetFromApi(data);
}

function convertBudgetFromApi(budget) {
    return {
        ...budget,
        key: budget.id,
    };
}

export async function getBudgetItems(budgetId) {
    const response = await fetch(API_URL + '/getBudgetItems', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Api-Key': API_KEY,
            session_id: makeStore('user').get('session_id'),
        },
        body: JSON.stringify({ budget_id: 1 }),
    });

    const data = await handleResponse(response);
    return data.map(convertBudgetItemFromApi);
}

function convertBudgetItemFromApi(budgetItem) {
    return {
        ...budgetItem,
        key: budgetItem.id,
    };
}
