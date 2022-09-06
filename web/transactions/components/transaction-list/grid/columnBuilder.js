import { LABELS } from 'components/i18n';
import { makeTransactionDateRenderer, makeTagRenderer } from './renderers';

export function buildColumns(store) {
    return [
        {
            title: LABELS.id,
            dataIndex: 'id',
            key: 'id',
        },
        {
            title: LABELS.accountName,
            dataIndex: 'account',
            key: 'account',
        },
        {
            title: LABELS.transactionDate,
            dataIndex: 'date',
            key: 'date',
            render: makeTransactionDateRenderer(),
        },
        {
            title: LABELS.transactionDescription,
            dataIndex: 'description',
            key: 'description',
        },
        {
            title: LABELS.transactionAmount,
            dataIndex: 'amount',
            key: 'amount',
        },
        {
            title: LABELS.transactionTag,
            dataIndex: 'tags',
            key: 'tags',
            // defaultFilteredValue: store.get('filters')?.tags,
            render: makeTagRenderer(),
        },
    ];
}
