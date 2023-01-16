import { API_URL } from 'config';
import { handleResponse, defaultRequest } from 'util/rest';

export async function getBudget(budgetId) {
    const response = await fetch(API_URL + '/getBudget', defaultRequest({ budget_id: budgetId }));

    const data = await handleResponse(response);
    return {
        ...data,
        key: data.id,
    };
}

export async function getBudgetItems(budgetId) {
    const response = await fetch(
        API_URL + '/getBudgetItems',
        defaultRequest({ budget_id: budgetId })
    );

    const data = await handleResponse(response);
    return data.map(item => ({
        ...item,
        key: item.id,
    }));
}

export async function addBudgetItem(budgetId, newItem) {
    const response = await fetch(
        API_URL + '/addBudgetItem',
        defaultRequest({ budget_id: budgetId, l1: newItem.l1, amount: newItem.amount })
    );

    await handleResponse(response);
}
