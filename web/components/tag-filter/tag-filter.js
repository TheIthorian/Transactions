import { Select } from 'antd';

export function TagFilter({ allTags, defaultValue, onChange }) {
    return (
        <Select
            mode='multiple'
            allowClear
            style={{
                minWidth: '200px',
                maxWidth: '300px',
                marginRight: '5px',
            }}
            placeholder='Filter by Tag'
            onChange={onChange}
            defaultValue={defaultValue}
        >
            {allTags.map(tag => (
                <Select.Option key={tag}>{tag}</Select.Option>
            ))}
        </Select>
    );
}
