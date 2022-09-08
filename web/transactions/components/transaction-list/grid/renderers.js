import { Space, Tag } from 'antd';

export function makeTransactionDateRenderer() {
    return text => {
        if (text) {
            const date = new Date(text);
            return date?.toLocaleString(
                'en-GB',
                { timeZone: 'UTC' },
                { year: 'numeric', month: 'numeric', day: 'numeric' }
            );
        }
    };
}

export function makeAmountRenderer() {
    return (_, record) => {
        const { amount } = record;
        return amount < 0 ? `-£${-record.amount.toFixed(2)}` : `£${record.amount.toFixed(2)}`;
    };
}

export function makeTagRenderer(allTags = []) {
    return (_, record) => {
        return (
            <Space size={4} wrap>
                {record.tags?.map(tagName => {
                    return (
                        tagName && (
                            <Tag margin={0} key={tagName} color={record.tagColor}>
                                {tagName}
                            </Tag>
                        )
                    );
                })}
            </Space>
        );
    };
}
