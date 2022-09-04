import { delay } from 'util/delay';

export async function getAllTransactions() {
    await delay(1000);
    return [
        {
            id: 1,
            key: 1,
            account: 'Some account',
            date: new Date(),
            description: 'Some description',
            amount: 100,
            tag: null,
        },
        {
            id: 2,
            key: 2,
            account: 'Some account 2',
            date: new Date(),
            description: 'Some description 2',
            amount: 102,
            tag: null,
        },
    ];
}
