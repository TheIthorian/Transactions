import { API_URL } from 'config';
import { handleResponse, defaultRequest } from 'util/rest';

export async function getBudgets() {
    const response = await fetch(API_URL + '/getBudgets', {
        ...defaultRequest(),
        method: 'GET',
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

export async function addBudget(name, limit) {
    console.log({ name, limit });
    const response = await fetch(
        API_URL + '/addBudget',
        defaultRequest({ name, total_limit: limit })
    );

    await handleResponse(response);
}
