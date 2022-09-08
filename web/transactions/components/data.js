import { API_URL } from 'config';
import { handleResponse } from 'util/rest';

export async function getBreakdown(filter) {
    const response = await fetch(API_URL + '/getTransactions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ...filter }),
    });

    const data = await handleResponse(response);

    // return data.map(convertFromApi);

    return {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [
            {
                label: 'Amount per Tag',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                ],
                borderWidth: 1,
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
