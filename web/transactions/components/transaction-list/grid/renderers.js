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

export function makeTagRenderer(allTaskTypes) {
    return (_, record) => {
        const tagById = getAllTagsById(allTaskTypes);
        return (
            <Space size={4} wrap>
                {record.taskTypes?.map(tagId => {
                    const tag = tagById[tagId];
                    return (
                        <Tag margin={0} color={tag?.color} key={tag.value}>
                            {tag?.label}
                        </Tag>
                    );
                })}
            </Space>
        );
    };
}

function getAllTagsById(allTaskTypes) {
    const byId = allTaskTypes.reduce(function (map, obj) {
        map[obj.value] = { ...obj };
        return map;
    }, {});
    return byId;
}
