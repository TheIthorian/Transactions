import { API_URL } from 'config';
import { handleResponse, defaultRequest } from 'util/rest';

export async function getTimeline(filter, group_by_tags = true) {
    const url = '/getTransactionTimeline';
    console.log({ filter });
    const response = await fetch(API_URL + url, defaultRequest({ filter, group_by_tags }));

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

export async function getAllL2Tags() {
    const url = '/getAllTags';
    const response = await fetch(API_URL + url, defaultRequest());

    let data;
    try {
        data = await handleResponse(response);
    } catch {
        data = [];
    }

    return Array.from(new Set(data.map(t => t.l2)));
}

export async function getAllL3Tags() {
    const url = '/getAllTags';
    const response = await fetch(API_URL + url, defaultRequest());

    let data;
    try {
        data = await handleResponse(response);
    } catch {
        data = [];
    }

    return Array.from(new Set(data.map(t => t.l3)));
}
