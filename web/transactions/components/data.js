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
    console.log(data);

    return data;
    // return data.map(convertFromApi);

    const colors = [
        'rgba(255, 99, 132, 0.2)',
        'rgba(255, 99, 132, 0.2)',
        'rgba(255, 99, 132, 0.2)',
        'rgba(255, 99, 132, 0.2)',
        'rgba(255, 99, 132, 0.2)',
        'rgba(255, 99, 132, 0.2)',
        '#ffffff',
        'rgba(54, 162, 235, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        '#ffffff',
    ];

    return {
        labels: [
            'Red:1',
            'Red:2.1',
            'Red:2.2',
            'Red:3.1',
            'Red:3.2',
            'Red:3.3',
            'Red:none',
            'Blue:1',
            'Blue:2.1',
            'Blue:2.2',
            'Blue:2.3',
            'Blue:3.1',
            'Blue:none',
        ],
        datasets: [
            {
                label: 'Amount per Tag level 1',
                data: [120, 0, 0, 0, 0, 0, 0, 30, 0, 0, 0, 0, 0],
                backgroundColor: colors,
            },
            {
                label: 'Amount per Tag level 2',
                data: [0, 70, 40, 0, 0, 0, 10, 0, 15, 5, 10, 0, 0],
                backgroundColor: colors,
            },
            {
                label: 'Amount per Tag level 3',
                data: [0, 0, 0, 10, 20, 0, 90, 0, 0, 0, 0, 10, 0, 20],
                backgroundColor: colors,
            },
        ],
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
