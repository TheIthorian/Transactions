import { Space, Tag } from 'antd';

export function makeTransactionDateRenderer() {
    return text => {
        if (text) {
            const date = new Date(text);
            return date?.toLocaleString('en-GB', {
                year: 'numeric',
                month: 'numeric',
                day: 'numeric',
            });
        }
    };
}

export function makeDescriptionRenderer() {
    return (_, record) => {
        const { description } = record;
        const MAX_LENGTH = 50;
        if (description.length > MAX_LENGTH) {
            return description.substring(0, MAX_LENGTH) + '...';
        }

        return description;
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
