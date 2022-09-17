import { API_URL } from 'config';
import { handleResponse } from 'util/rest';

export async function getBreakdown(filter) {
    const response = await fetch(API_URL + '/getTransactionBreakdown', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
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
                            return dataset.labels[dataIndex] + ': ' + dataset.data[dataIndex];
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

export async function getAllTags() {
    const response = await fetch(API_URL + '/getAllTags', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    const data = await handleResponse(response);
    return Array.from(new Set(data.map(t => t.l1)));
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
