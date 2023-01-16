import { Button, Select } from 'antd';
import { useEffect, useRef, useState } from 'react';

import { API_URL } from 'config';
import { defaultRequest, handleResponse } from 'util/rest';

export function TagSelection({ budgetId, onChange, onAdd }) {
    const [availableTags, setAvailableTags] = useState([]);
    const [selected, setSelected] = useState(null);

    useEffect(() => {
        getAvailableTags(budgetId).then(setAvailableTags).catch(console.warn);
    }, []);

    function clearSelected() {
        setSelected(null);
    }

    function handleAdd() {
        onAdd(selected);
        setAvailableTags(availableTags => availableTags.filter(t => t.name !== selected));
        clearSelected();
    }

    function handleChange(value) {
        onChange?.();
        setSelected(value);
    }

    return (
        <>
            <Button style={{ marginTop: 10, marginRight: 10 }} onClick={handleAdd}>
                Add
            </Button>
            <Select value={selected} style={{ width: 200 }} onChange={handleChange}>
                {availableTags.map(tag => (
                    <Select.Option key={tag.name} value={tag.name}>
                        {tag.name}
                    </Select.Option>
                ))}
            </Select>
        </>
    );
}

async function getAvailableTags(budgetId) {
    const response = await fetch(
        API_URL + '/getAvailableTags',
        defaultRequest({ budget_id: budgetId })
    );

    const data = await handleResponse(response);
    return data;
}
