import { API_URL, API_KEY } from 'config';
import { handleResponse } from 'util/rest';
import { makeStore } from 'util/store';

export async function getTimeline(filter, group_by_tags = true) {
    const url = '/getTransactionTimeline';
    const response = await fetch(API_URL + url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Api-Key': API_KEY,
            session_id: makeStore('user').get('session_id'),
        },
        body: JSON.stringify({ filter, group_by_tags }),
    });

    const data = await handleResponse(response);

    return {
        type: 'bar',
        data,
        options: {
            plugins: {
                tooltip: {
                    callbacks: {
                        label: ({ dataset, dataIndex }) => {
                            return (
                                dataset.label +
                                ': ' +
                                new Date(data.labels[dataIndex]).toLocaleDateString('en-UK', {
                                    year: 'numeric',
                                    month: 'long',
                                }) +
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
        },
    };
}
