import { Button, Card, Divider, Input } from 'antd';
import { useEffect, useState } from 'react';

import { Error } from 'components/error';
import { Budget } from 'components/budget';

import { addBudget, getBudgets } from './data';

export default function Budgets() {
    const [budgets, setBudgets] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        getBudgets().then(setBudgets).catch(setError);
    }, []);

    function handleAddBudget(name, limit) {
        addBudget(name, limit);
    }

    if (error) {
        return <Error error={error} />;
    }

    return (
        <Card style={{ marginTop: 10 }} bodyStyle={{ padding: 15 }}>
            {budgets.map(budget => (
                <Budget
                    budgetId={budget.id}
                    name={budget.name}
                    totalLimit={budget.totalLimit}
                    key={budget.id}
                />
            ))}
            <Divider style={{ marginTop: 8, marginBottom: 8 }} />
            {!budgets.length ? <AddBudget onSubmit={handleAddBudget} /> : null}
        </Card>
    );
}

function AddBudget({ onSubmit }) {
    const [name, setName] = useState(null);
    const [limit, setLimit] = useState(null);

    function handleChangeName(e) {
        setName(e.target.value);
    }

    function handleChangeLimit(e) {
        setLimit(e.target.value);
    }

    return (
        <>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
                <h1>Add new Budget: </h1>
                <label>Name: </label>
                <Input onChange={handleChangeName} type='text' />
                <label>Limit: </label>
                <Input onChange={handleChangeLimit} type='number' />
                <Button onClick={() => onSubmit(name, limit)}>Add</Button>
            </div>
        </>
    );
}
