import { API_URL, API_KEY } from 'config';
import { handleResponse } from 'util/rest';
import { makeStore } from 'util/store';
import { MODES } from './constants';

export async function getBreakdown(filter, mode) {
    const url =
        mode == MODES.Monthly ? '/getAverageTransactionBreakdown' : '/getTransactionBreakdown';
    const response = await fetch(API_URL + url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Api-Key': API_KEY,
            password: makeStore('user').get('password'),
        },
        body: JSON.stringify({ ...filter }),
    });

    const data = await handleResponse(response);

    return {
        type: 'doughnut',
        data,
        options: {
            plugins: {
                tooltip: {
                    callbacks: {
                        label: ({ dataset, dataIndex }) => {
                            return (
                                dataset.labels[dataIndex] +
                                ': £' +
                                dataset.data[dataIndex]?.toLocaleString()
                            );
                        },
                    },
                },
                legend: {},
            },
            responsive: true,
            maintainAspectRatio: false,
            cutout: 30,
        },
    };
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
